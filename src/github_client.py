from typing import List, Dict
import os
from datetime import datetime, timedelta
import httpx

class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"
    
    async def get_starred_repos(self, limit: int = 10) -> List[Dict]:
        """Fetch starred repositories for the authenticated user"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/user/starred",
                headers=self.headers,
                params={"per_page": limit}
            )
            response.raise_for_status()
            return response.json()
    
    async def get_recent_commits(self, repo_full_name: str, since_days: int = 7) -> List[Dict]:
        """Fetch recent commits for a repository"""
        since_date = (datetime.now() - timedelta(days=since_days)).isoformat()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo_full_name}/commits",
                headers=self.headers,
                params={"since": since_date}
            )
            response.raise_for_status()
            return response.json() 