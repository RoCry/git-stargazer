from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import httpx
from log import logger
from cache_manager import COMMITS_DEFAULT_SINCE_DAYS
import asyncio


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

    async def get_starred_repos(self, total_limit: int = 10, sort="updated") -> List[Dict]:
        """Fetch starred repositories for the authenticated user with pagination"""
        all_repos = []
        page = 1
        per_page = min(100, total_limit)  # GitHub's max per_page is 100

        while len(all_repos) < total_limit:
            response = await self.client.get(
                f"{self.base_url}/user/starred",
                params={"per_page": per_page, "page": page, "sort": sort},
            )
            response.raise_for_status()

            repos = response.json()
            if not repos:  # No more repos to fetch
                break

            all_repos.extend(repos)
            page += 1

            # Adjust per_page for the last request if needed
            remaining = total_limit - len(all_repos)
            if remaining < per_page:
                per_page = remaining

        return all_repos[:total_limit]

    def _is_commit_from_bot(self, commit: Dict) -> bool:
        author = commit.get("author")
        if not author:
            logger.info("No author found")
            return False

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
    ) -> Tuple[
        List[Dict], datetime | None
    ]:  # Modified return type to include timestamp
        last_modified = None

        t = (
            since_timestamp
            if since_timestamp
            else (datetime.now() - timedelta(days=COMMITS_DEFAULT_SINCE_DAYS))
        )
        http_modified_since = t.strftime("%a, %d %b %Y %H:%M:%S GMT")

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

        # If we're using a cached timestamp, remove the last known commit to avoid duplication
        if since_timestamp and commits:
            commits = [
                commit
                for commit in commits
                if commit["commit"]["committer"]["date"] != since_timestamp.isoformat()
            ]

        return commits, last_modified
