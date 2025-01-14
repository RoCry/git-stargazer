import asyncio
import json
import os
import glob
import time
from typing import List, Tuple, Dict
from github_client import GitHubClient, RateLimitException
from report_generator import ReportGenerator
from cache_manager import CacheManager
from log import logger
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# returns (github_token, repo_limit, is_in_github_actions)
def get_configuration() -> tuple[str, int, bool]:
    """Get configuration from environment variables"""
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    repo_limit = os.getenv("REPO_LIMIT", "").strip()
    repo_limit = int(repo_limit) if repo_limit else 100
    is_in_github_actions = os.getenv("GITHUB_ACTIONS")
    return github_token, repo_limit, bool(is_in_github_actions)


# returns (report_json_file_path, report_file_path)
def setup_report_files() -> tuple[str, str]:
    """Set up report file paths"""
    today_data_str = datetime.now().strftime("%Y-%m-%d")
    report_json_file = f"reports/recent_commits_{today_data_str}.json"
    report_file = f"reports/recent_commits_{today_data_str}.md"
    return report_json_file, report_file


# returns (report_json, repo_names)
def load_existing_report(report_json_file: str) -> tuple[dict | None, set]:
    if not os.path.exists(report_json_file):
        return None, set()

    with open(report_json_file, "r") as f:
        existing_report_json = json.load(f)
        existing_repo_names = set(
            [repo["name"] for repo in existing_report_json["repos"]]
        )
        logger.info(
            f"Found report file `{report_json_file}` from previous, will merge {existing_report_json['total_repos_count']} repos"
        )
        return existing_report_json, existing_repo_names


# returns (repo, commits)
async def fetch_repo_commits(
    github_client: GitHubClient,
    cache_manager: CacheManager,
    repo: dict,
    is_in_github_actions: bool,
) -> tuple[dict, list[dict]] | None:
    """Fetch recent commits for a single repository"""
    try:
        repo_name = repo["full_name"]
        since_timestamp = cache_manager.get_timestamp(repo_name)
        commits, last_modified = await github_client.get_recent_commits(
            repo_name,
            since_timestamp=since_timestamp,
            rise_exception_on_rate_limit=True,
        )

        # https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api?apiVersion=2022-11-28#pause-between-mutative-requests
        if is_in_github_actions:
            await asyncio.sleep(1)

        # Update cache with new timestamp
        if last_modified:
            cache_manager.set_timestamp(repo_name, last_modified)
        elif commits:
            latest_timestamp = commits[0]["commit"]["committer"]["date"]
            cache_manager.set_timestamp(repo_name, latest_timestamp)

        logger.info(f"Fetched {len(commits)} commits for {repo_name}")
        return repo, commits

    except RateLimitException as e:
        logger.error(f"Rate limit hit: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to fetch commits for {repo_name}: {str(e)}")
        return None


# returns [(repo, commits)]
async def fetch_all_repo_commits(
    github_client: GitHubClient,
    cache_manager: CacheManager,
    starred_repos: list[dict],
    is_in_github_actions: bool,
) -> list[tuple[dict, list[dict]]]:
    repos_with_commits: list[tuple[dict, list[dict]]] = []

    # because we are fetching the repos in order of updated time
    # if we have 10 consecutive empty commits, we can assume the rest are also empty
    # if so, stop fetching more commits to avoid rate limit
    # default 10, <= 0 means no limit
    empty_repo_limit = os.environ.get("EMPTY_REPO_CONSECUTIVE_LIMIT", "").strip()
    empty_repo_limit = int(empty_repo_limit) if (empty_repo_limit != "") else 10
    empty_commits_repo_count = 0

    logger.info(
        f"Fetching commits for {len(starred_repos)} repos, empty repo limit: {empty_repo_limit}"
    )

    for repo in starred_repos:
        result = await fetch_repo_commits(
            github_client, cache_manager, repo, is_in_github_actions
        )
        if not result:
            continue

        repos_with_commits.append(result)

        if result[1]:
            empty_commits_repo_count = 0
            continue
        # empty, increment count
        empty_commits_repo_count += 1

        if empty_repo_limit > 0 and empty_commits_repo_count >= empty_repo_limit:
            logger.info(
                f"Stopping fetching more commits as {empty_commits_repo_count} consecutive repos have no commits"
            )
            break

    return repos_with_commits


def save_reports(
    report_json: dict,
    report_json_file: str,
    report_file: str,
    is_in_github_actions: bool,
) -> None:
    os.makedirs("reports", exist_ok=True)
    with open(report_json_file, "w") as f:
        json.dump(report_json, f, ensure_ascii=False, indent=2)

    # Save Markdown report
    with open(report_file, "w") as f:
        f.write(ReportGenerator.json_report_to_markdown(report_json))

    # Set GitHub Actions output if running in CI
    if is_in_github_actions:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"report_file={report_file}\n")
            f.write(f"report_json_file={report_json_file}\n")


async def main():
    # Get configuration
    github_token, repo_limit, is_in_github_actions = get_configuration()

    # Initialize cache manager
    cache_manager = CacheManager()
    cache_manager.load()

    # Set up report files
    report_json_file, report_file = setup_report_files()

    # Load existing report if it exists
    existing_report_json, existing_repo_names = load_existing_report(report_json_file)

    async with GitHubClient(github_token) as github_client:
        # Fetch starred repositories
        starred_repos = await github_client.get_starred_repos(
            exclude_repo_names=existing_repo_names, total_limit=repo_limit
        )

        # Fetch recent commits for all repositories
        repos_with_commits = await fetch_all_repo_commits(
            github_client, cache_manager, starred_repos, is_in_github_actions
        )

    # Generate and save reports
    report_generator = ReportGenerator()
    report_json = await report_generator.generate_report_json(repos_with_commits)
    if existing_report_json:
        report_json = ReportGenerator.merge_reports(existing_report_json, report_json)

    save_reports(report_json, report_json_file, report_file, is_in_github_actions)

    # Clean up old reports and save cache
    _cleanup_reports_folder(
        exclude_files=[report_json_file, report_file],
        dry_run=not is_in_github_actions,
    )
    cache_manager.save()


def _cleanup_reports_folder(
    exclude_files: List[str],
    dry_run: bool = False,  # do not remove files in dry run
):
    """Clean up old report files, keeping recently updated ones and excluded files"""
    report_files = glob.glob("reports/*")
    current_time = time.time()

    for file_path in report_files:
        # Skip if file is in exclude list
        if file_path in exclude_files:
            continue

        # Skip if file was modified in last 12 hours
        if current_time - os.path.getmtime(file_path) < 12 * 3600:
            # the just updated file should be excluded
            logger.warning(f"Skipping {file_path} as it was modified recently")
            continue

        if dry_run:
            logger.info(f"Would remove old report file: {file_path}")
            continue

        try:
            os.remove(file_path)
            logger.info(f"Removed old report file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to remove {file_path}: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
