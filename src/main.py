import asyncio
import os
from typing import List, Tuple, Dict
from github_client import GitHubClient
from report_generator import ReportGenerator
from cache_manager import CacheManager
from log import logger
from datetime import datetime


async def main():
    # Initialize clients
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    repo_limit = os.getenv("REPO_LIMIT")
    repo_limit = int(repo_limit) if repo_limit else 10

    # Initialize cache manager
    cache_manager = CacheManager()
    cache_manager.load()

    async with GitHubClient(github_token) as github_client:
        # Fetch starred repositories
        starred_repos = await github_client.get_starred_repos(total_limit=repo_limit)

        # Fetch recent commits for each repository
        repos_with_commits: List[Tuple[Dict, List[Dict]]] = []
        for repo in starred_repos:
            try:
                repo_name = repo["full_name"]
                since_timestamp = cache_manager.get_timestamp(repo_name)
                commits = await github_client.get_recent_commits(
                    repo_name, since_timestamp=since_timestamp
                )

                if commits:
                    # Update cache with the latest commit timestamp
                    latest_timestamp = commits[0]["commit"]["committer"]["date"]
                    cache_manager.set_timestamp(repo_name, latest_timestamp)

                logger.info(f"Fetched {len(commits)} commits for {repo_name}")
                repos_with_commits.append((repo, commits))
            except Exception as e:
                logger.error(f"Failed to fetch commits for {repo_name}: {str(e)}")
                continue

    # Generate report
    report_generator = ReportGenerator()
    report = await report_generator.generate_full_report(repos_with_commits)

    print("=" * 100)
    print(report)
    print("=" * 100)

    # Save report
    os.makedirs("reports", exist_ok=True)
    report_file = f"reports/recent_commits_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, "w") as f:
        f.write(report)

    # Set output for GitHub Actions
    if os.getenv("GITHUB_ACTIONS"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"report_file={report_file}\n")

    cache_manager.save()


if __name__ == "__main__":
    asyncio.run(main())
