from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import httpx
from log import logger
from cache_manager import COMMITS_DEFAULT_SINCE_DAYS
import asyncio


class RateLimitException(Exception):
    pass


class GitHubClient:
    def __init__(self, token: str, timeout: int = 30):
        self.token = token
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        self.base_url = "https://api.github.com"
        self.client = httpx.AsyncClient(timeout=timeout, http2=True, headers=headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def print_rate_limit(self):
        response = await self.client.get(f"{self.base_url}/rate_limit")
        logger.info(response.text)
    
    async def unstar_repo(self, repo_full_name: str):
        response = await self.client.delete(f"{self.base_url}/user/starred/{repo_full_name}")
        response.raise_for_status()

    async def get_repo(self, fullname: str) -> Dict:
        response = await self.client.get(f"{self.base_url}/repos/{fullname}")
        response.raise_for_status()
        return response.json()

    async def get_starred_repos(
        self,
        exclude_repo_names: Optional[set[str]],
        total_limit: int = 10,
        sort="updated",
        direction="desc",
    ) -> List[Dict]:
        """Fetch starred repositories for the authenticated user with pagination"""
        all_repos = []
        page = 1
        per_page = min(100, total_limit)  # GitHub's max per_page is 100

        while len(all_repos) < total_limit:
            logger.debug(
                f"Fetching /user/starred page={page}, per_page={per_page}, sort={sort}, direction={direction}"
            )
            response = await self.client.get(
                f"{self.base_url}/user/starred",
                params={
                    "per_page": per_page,
                    "page": page,
                    "sort": sort,
                    "direction": direction,
                },
            )
            response.raise_for_status()

            repos = response.json()
            if not repos:  # No more repos to fetch
                break

            if exclude_repo_names:
                repos = [
                    repo
                    for repo in repos
                    if repo["full_name"] not in exclude_repo_names
                ]

            all_repos.extend(repos)
            page += 1

            # Adjust per_page for the last request if needed
            remaining = total_limit - len(all_repos)
            if remaining < per_page:
                per_page = remaining

        logger.info(
            f"Fetched {len(all_repos)} starred repos, excluding {len(exclude_repo_names) if exclude_repo_names else 0}, total limit: {total_limit}"
        )
        return all_repos[:total_limit]

    def _is_commit_from_bot(self, commit: Dict) -> bool:
        author = commit.get("author")
        if not author:
            # logger.info("No author found")
            # assume it's a bot
            return True

        if author.get("type") == "Bot":
            return True

        if login := author.get("login"):
            if "[bot]" in login:
                return True

        return False

    async def get_recent_commits(
        self,
        repo_full_name: str,
        exclude_bots: bool = True,
        since_timestamp: datetime | None = None,
        rise_exception_on_rate_limit: bool = True,
    ) -> Tuple[
        List[Dict], datetime | None
    ]:  # Modified return type to include timestamp
        last_modified = None

        must_since_timestamp = (
            since_timestamp
            if since_timestamp
            else (datetime.now() - timedelta(days=COMMITS_DEFAULT_SINCE_DAYS))
        )
        http_modified_since = must_since_timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")

        # parameter interfere with 304 responses, so we use headers to get better performance
        # params["since"] = since_timestamp.isoformat()

        while True:
            try:
                response = await self.client.get(
                    f"{self.base_url}/repos/{repo_full_name}/commits",
                    headers={"if-modified-since": http_modified_since},
                )

                # Get Last-Modified from headers
                last_modified = response.headers.get("Last-Modified")
                if last_modified:
                    last_modified = datetime.strptime(
                        last_modified, "%a, %d %b %Y %H:%M:%S GMT"
                    )
                else:
                    logger.warning(
                        f"[{repo_full_name}] No Last-Modified header found: {response.headers}"
                    )

                # If content hasn't changed, return empty list
                if response.status_code == 304:
                    logger.info(
                        f"[{repo_full_name}] got 304 since {http_modified_since}"
                    )
                    return [], last_modified

                if (
                    response.status_code == 403
                    and "X-RateLimit-Remaining" in response.headers
                ):
                    # sleep and wait for rate limit doesn't work, raise an exception to stop and try re-run later
                    if rise_exception_on_rate_limit:
                        raise RateLimitException(f"Rate limit hit: {response.headers}")
                    # Handle rate limiting
                    reset_time = int(response.headers["X-RateLimit-Reset"])
                    wait_time = reset_time - datetime.now().timestamp()
                    if wait_time > 0:
                        logger.warning(
                            f"Rate limit hit. Waiting {wait_time:.0f} seconds..."
                        )
                        await asyncio.sleep(wait_time + 5)  # Add 5 second buffer
                        continue

                response.raise_for_status()
                break
            except httpx.HTTPError as e:
                if "rate limit" in str(e).lower():
                    # Fallback rate limit handling if headers aren't available
                    logger.warning("Rate limit hit. Waiting 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                raise

        commits = response.json()

        if exclude_bots:
            commits = [
                commit for commit in commits if not self._is_commit_from_bot(commit)
            ]

        # remove the commits before must_since_timestamp.
        # since we're using the headers to get the last modified date and github will return more commits
        must_since_ts = must_since_timestamp.timestamp()
        commits = [
            commit
            for commit in commits
            if datetime.fromisoformat(commit["commit"]["committer"]["date"]).timestamp() >= must_since_ts
        ]

        # If we're using a cached timestamp, remove the last known commit to avoid duplication
        # seems we don't need this, since we're using the headers to get the last modified date
        # if since_timestamp and commits:
        #     commits = [
        #         commit
        #         for commit in commits
        #         if commit["commit"]["committer"]["date"] != since_timestamp.isoformat()
        #     ]

        return commits, last_modified
