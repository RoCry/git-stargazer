from typing import List, Dict
from datetime import datetime, timedelta
import httpx
from log import logger

COMMITS_DEFAULT_SINCE_DAYS = 7


class GitHubClient:
    def __init__(self, token: str, timeout: int = 30):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.base_url = "https://api.github.com"
        self.client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def get_starred_repos(self, total_limit: int = 10) -> List[Dict]:
        """Fetch starred repositories for the authenticated user with pagination"""
        all_repos = []
        page = 1
        per_page = min(100, total_limit)  # GitHub's max per_page is 100

        while len(all_repos) < total_limit:
            response = await self.client.get(
                f"{self.base_url}/user/starred",
                headers=self.headers,
                params={"per_page": per_page, "page": page},
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
        since_timestamp: str | None = None,
    ) -> List[Dict]:
        """Fetch recent commits for a repository

        Args:
            repo_full_name: Full name of the repository (e.g., 'owner/repo')
            since_days: Number of days to look back for commits (ignored if since_timestamp is provided)
            exclude_bots: If True, filters out commits from bot users (default: True)
            since_timestamp: ISO format timestamp to fetch commits since (optional)
        """
        params = {}

        if since_timestamp:
            # For subsequent runs, get commits after the last known commit
            params["since"] = since_timestamp
        else:
            # For first run or when cache is expired, use the default time window
            params["since"] = (
                datetime.now() - timedelta(days=COMMITS_DEFAULT_SINCE_DAYS)
            ).isoformat()

        response = await self.client.get(
            f"{self.base_url}/repos/{repo_full_name}/commits",
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
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
                if commit["commit"]["committer"]["date"] != since_timestamp
            ]

        return commits
