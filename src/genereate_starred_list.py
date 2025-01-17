# This script for personal temporary use.

import asyncio
import json
import os
from datetime import datetime, timezone, timedelta

from github_client import GitHubClient


async def save_all_starred_repos(client: GitHubClient):
    starred_repos = await client.get_starred_repos(
        exclude_repo_names=None,
        total_limit=50,
        sort="created",
        direction="asc",
    )
    with open("reports/all_starred_repos.json", "w") as f:
        json.dump(starred_repos, f, ensure_ascii=False, indent=2)

async def filter_repos(path: str):
    with open(path, "r") as f:
        repos = json.load(f)
    
    def __filter(repo: dict) -> bool:
        # stars >= 500
        if repo["stargazers_count"] < 5000:
            return False
        # not archived
        if repo["archived"]:
            return False
        # updated in the last year
        pushed_at = datetime.fromisoformat(repo["pushed_at"])
        if pushed_at.tzinfo is None:
            pushed_at = pushed_at.replace(tzinfo=timezone.utc)
        one_year_ago = datetime.now(timezone.utc) - timedelta(days=7)
        if pushed_at < one_year_ago:
            return False

        return True

    repos = [repo for repo in repos if __filter(repo)]
    print(f"Saving {len(repos)} repos")
    with open("reports/starred_repos_filtered.json", "w") as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
    # save to csv
    with open("reports/starred_repos_filtered.csv", "w") as f:
        f.write("name,stargazers_count,pushed_at,url,description\n")
        for repo in repos:
            simple_pushed_at = datetime.fromisoformat(repo["pushed_at"]).strftime("%Y-%m-%d")
            short_description = repo["description"][:100].replace(",", " ") if repo["description"] else ""
            f.write(f"{repo['full_name']},{repo['stargazers_count']},{simple_pushed_at},{repo['html_url']},{short_description}\n")

async def unstar_repos(client: GitHubClient):
    with open("reports/starred_repos_filtered.csv", "r") as f:
        repos = f.readlines()
    
    repos = repos[1:]
    for repo in repos:
        repo_name = repo.split(",")[0]
        print(f"DELETE {repo_name}")
        await client.unstar_repo(repo_name)
        await asyncio.sleep(1)

async def main():
    token = os.getenv("GITHUB_TOKEN")
    async with GitHubClient(token) as client:
        # await save_all_starred_repos(client)
        # await filter_repos("reports/_all_starred_repos.json")
        await unstar_repos(client)

if __name__ == "__main__":
    asyncio.run(main())
