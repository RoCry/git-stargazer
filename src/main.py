import asyncio
import os
from typing import List, Tuple, Dict
from github_client import GitHubClient
from report_generator import ReportGenerator

async def main():
    # Initialize clients
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    
    github_client = GitHubClient(github_token)
    report_generator = ReportGenerator()
    
    # Fetch starred repositories
    starred_repos = await github_client.get_starred_repos(limit=10)
    
    # Fetch recent commits for each repository
    repos_with_commits: List[Tuple[Dict, List[Dict]]] = []
    for repo in starred_repos:
        commits = await github_client.get_recent_commits(repo["full_name"])
        repos_with_commits.append((repo, commits))
    
    # Generate report
    report = await report_generator.generate_full_report(repos_with_commits)
    
    # Save report
    os.makedirs("reports", exist_ok=True)
    with open("reports/recent_activity.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    asyncio.run(main()) 