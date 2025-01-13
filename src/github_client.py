from typing import List, Dict
from datetime import datetime, timedelta
import httpx

class GitHubClient:
    def __init__(self, token: str, timeout: int = 30):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"
        self.client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def get_starred_repos(self, total_limit: int = 10) -> List[Dict]:
        # FIXME: pagination
        """Fetch starred repositories for the authenticated user"""
        response = await self.client.get(
            f"{self.base_url}/user/starred",
            headers=self.headers,
            params={"per_page": total_limit}
        )
        response.raise_for_status()
        return response.json()
    
    async def get_recent_commits(self, repo_full_name: str, since_days: int = 7) -> List[Dict]:
        """Fetch recent commits for a repository"""
        since_date = (datetime.now() - timedelta(days=since_days)).isoformat()
        
        response = await self.client.get(
            f"{self.base_url}/repos/{repo_full_name}/commits",
            headers=self.headers,
            params={"since": since_date}
        )
        response.raise_for_status()
        return response.json() 