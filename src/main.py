import asyncio
import os
from typing import List, Tuple, Dict
from github_client import GitHubClient
from report_generator import ReportGenerator
from log import logger

async def main():
    # Initialize clients
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    
    async with GitHubClient(github_token) as github_client:
        # Fetch starred repositories
        starred_repos = await github_client.get_starred_repos(total_limit=2)
        
        # Fetch recent commits for each repository
        repos_with_commits: List[Tuple[Dict, List[Dict]]] = []
        for repo in starred_repos:
            commits = await github_client.get_recent_commits(repo["full_name"])
            logger.info(f"Fetched {len(commits)} commits for {repo['full_name']}")
            repos_with_commits.append((repo, commits))
    
    # Generate report
    report_generator = ReportGenerator()
    report = await report_generator.generate_full_report(repos_with_commits)
    
    # Save report
    os.makedirs("reports", exist_ok=True)
    with open("reports/recent_activity.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    asyncio.run(main()) 