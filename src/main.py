import asyncio
import json
import os
from typing import List, Tuple, Dict
from github_client import GitHubClient
from report_generator import ReportGenerator
from cache_manager import CacheManager
from log import logger
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


async def main():
    # Initialize clients
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    repo_limit = os.getenv("REPO_LIMIT")
    repo_limit = int(repo_limit) if repo_limit else 10
    is_in_github_actions = os.getenv("GITHUB_ACTIONS")

    # Initialize cache manager
    cache_manager = CacheManager()
    cache_manager.load()

    today_data_str = datetime.now().strftime("%Y-%m-%d")
    report_json_file = f"reports/recent_commits_{today_data_str}.json"
    report_file = f"reports/recent_commits_{today_data_str}.md"

    if os.path.exists(report_json_file):
        logger.info(f"Report file {report_json_file} already exists")
        with open(report_json_file, "r") as f:
            existing_report_json = json.load(f)
            existing_repo_names = set(
                [repo["name"] for repo in existing_report_json["repos"]]
            )

    async with GitHubClient(github_token) as github_client:
        # await github_client.print_rate_limit()
        # Fetch starred repositories
        starred_repos = await github_client.get_starred_repos(
            exclude_repo_names=existing_repo_names, total_limit=repo_limit
        )

        # Fetch recent commits for each repository
        repos_with_commits: List[Tuple[Dict, List[Dict]]] = []
        for repo in starred_repos:
            try:
                repo_name = repo["full_name"]
                since_timestamp = cache_manager.get_timestamp(repo_name)
                commits, last_modified = await github_client.get_recent_commits(
                    repo_name, since_timestamp=since_timestamp
                )
                # https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api?apiVersion=2022-11-28#pause-between-mutative-requests
                if is_in_github_actions:
                    await asyncio.sleep(1)

                if last_modified:
                    # Update cache with Last-Modified from response headers
                    cache_manager.set_timestamp(repo_name, last_modified)
                elif commits:
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
    report_json = await report_generator.generate_report_json(repos_with_commits)
    if existing_report_json:
        report_json = merge_reports(existing_report_json, report_json)
    report = json_report_to_markdown(report_json)

    print("=" * 100)
    print(report)
    print("=" * 100)

    # Save report
    os.makedirs("reports", exist_ok=True)
    with open(report_json_file, "w") as f:
        json.dump(report_json, f, ensure_ascii=False, indent=2)
    with open(report_file, "w") as f:
        f.write(report)

    # Set output for GitHub Actions
    if is_in_github_actions:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"report_file={report_file}\n")
            f.write(f"report_json_file={report_json_file}\n")

    cache_manager.save()


def merge_reports(left: Dict, right: Dict) -> Dict:
    logger.info(
        f"Merging reports: {left['total_repos_count']} and {right['total_repos_count']}"
    )
    return {
        "total_repos_count": left["total_repos_count"] + right["total_repos_count"],
        "active_repos_count": left["active_repos_count"] + right["active_repos_count"],
        "total_commits_count": left["total_commits_count"]
        + right["total_commits_count"],
        "repos": left["repos"] + right["repos"],
    }


def json_report_to_markdown(json_report: Dict) -> str:
    """Generate markdown report from report data dictionary"""
    if not json_report["repos"]:
        return "# Recent Activity in Starred Repositories\nNo recent activity found in starred repositories."

    sections_md = []
    for repo in json_report["repos"]:
        if repo["commit_count"] == 0:
            continue
        if not repo["summary"]:
            continue
        section_md = f"- [{repo['name']}]({repo['url']}) {repo['commit_count']}: {repo['summary']}"
        sections_md.append(section_md)

    return (
        "# Recent Activity in Starred Repositories\n"
        f"_Tracking {json_report['active_repos_count']}/{json_report['total_repos_count']} "
        f"repos with {json_report['total_commits_count']} new commits_\n\n"
        + "\n".join(sections_md)
    )


if __name__ == "__main__":
    asyncio.run(main())
