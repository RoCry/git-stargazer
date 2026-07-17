from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from typing import Any

JsonDict = dict[str, Any]
ReportRow = tuple[Mapping[str, Any], Sequence[Mapping[str, Any]], str | None]


def assemble_report(rows: Iterable[ReportRow]) -> JsonDict:
    materialized_rows = list(rows)
    repos: list[JsonDict] = []
    total_commits = 0
    active_repos = 0

    for repo, commits, summary in materialized_rows:
        commit_count = len(commits)
        total_commits += commit_count
        active_repos += int(commit_count > 0)
        item: JsonDict = {
            "name": repo["full_name"],
            "url": repo["html_url"],
            "commit_count": commit_count,
            "summary": summary,
            "description": repo.get("description"),
            "commits": [
                {
                    "sha": commit["sha"],
                    "message": commit["commit"]["message"],
                    "date": commit["commit"]["author"]["date"],
                }
                for commit in commits
            ],
        }
        if topics := repo.get("topics"):
            item["topics"] = topics
        repos.append(item)

    return {
        "total_repos_count": len(materialized_rows),
        "active_repos_count": active_repos,
        "total_commits_count": total_commits,
        "repos": repos,
    }


def merge_reports(left: Mapping[str, Any], right: Mapping[str, Any]) -> JsonDict:
    return {
        "total_repos_count": left["total_repos_count"] + right["total_repos_count"],
        "active_repos_count": left["active_repos_count"] + right["active_repos_count"],
        "total_commits_count": left["total_commits_count"] + right["total_commits_count"],
        "repos": [*left["repos"], *right["repos"]],
    }


def render_json_feed(report: Mapping[str, Any], *, published_at: datetime) -> JsonDict:
    feed: JsonDict = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "GitHub Starred Repositories Activity",
        "home_page_url": "https://github.com/RoCry/git-stargazer/releases/latest",
        "feed_url": "https://github.com/RoCry/git-stargazer/releases/download/latest/feed.json",
        "items": [],
    }

    for repo in report.get("repos", []):
        if repo.get("commit_count", 0) == 0:
            continue

        commit_url = f"{repo['url']}/commits"
        title = repo["name"]
        content_lines = [f"# {repo['name']}\n", f"{repo['commit_count']} commits\n"]
        content_html_lines: list[str] = []
        if summary := repo.get("summary"):
            title += f": {summary}"
            content_lines.append(f"### {summary}\n")
            content_html_lines.extend(['<div class="repo-summary">', f"<h3>{summary}</h3>", "</div>"])
        if description := repo.get("description"):
            content_lines.append(f"### {description}\n")
            content_html_lines.extend(
                [
                    '<div class="repo-description">',
                    f"<h4>{description}</h4>",
                    "</div>",
                ]
            )

        content_html_lines.append('<div class="commit-list">')
        for commit in repo.get("commits", []):
            if not commit.get("message"):
                continue
            commit_link = f"{repo['url']}/commit/{commit['sha']}"
            message = commit["message"].splitlines()[0].strip()
            content_lines.append(f"- {message}")
            content_html_lines.append(
                f'<div class="commit-item">• {message} '
                f'<a href="{commit_link}"><code>{commit["sha"][:7]}</code></a></div>'
            )
        content_html_lines.extend(
            [
                "</div>",
                '<div class="repo-footer">',
                f'<p><em><a href="{commit_url}">{repo["commit_count"]} commits</a></em></p>',
                "</div>",
            ]
        )
        feed["items"].append(
            {
                "id": repo["url"],
                "url": repo["url"],
                "title": title,
                "content_text": "\n".join(content_lines),
                "content_html": "\n".join(content_html_lines),
                "date_published": published_at.isoformat(),
                "tags": repo.get("topics", []),
            }
        )

    return feed


def render_markdown(report: Mapping[str, Any]) -> str:
    if not report["repos"]:
        return "# Recent Activity in Starred Repositories\nNo recent activity found in starred repositories."

    active_repos = [repo for repo in report["repos"] if repo["commit_count"] > 0]
    topic_frequency: dict[str, int] = {}
    for repo in active_repos:
        for topic in _topics(repo):
            topic_frequency[topic] = topic_frequency.get(topic, 0) + 1

    groups: dict[str, list[Mapping[str, Any]]] = {"Other": []}
    processed: set[str] = set()
    for index, repo in enumerate(active_repos):
        if repo["name"] in processed:
            continue
        shared_topics = set(_topics(repo))
        if not shared_topics:
            groups["Other"].append(repo)
            processed.add(repo["name"])
            continue

        similar = [repo]
        for other in active_repos[index + 1 :]:
            other_topics = set(_topics(other))
            if other["name"] not in processed and shared_topics & other_topics:
                similar.append(other)
                shared_topics &= other_topics
                processed.add(other["name"])

        group_name = (
            ", ".join(
                sorted(
                    shared_topics,
                    key=lambda topic: (-topic_frequency[topic], topic),
                )
            )
            if len(similar) > 1 and shared_topics
            else "Other"
        )
        groups.setdefault(group_name, []).extend(similar)
        processed.add(repo["name"])

    sections: list[str] = []
    for group_name in [*sorted(name for name in groups if name != "Other"), "Other"]:
        header = (
            "\n## Other"
            if group_name == "Other"
            else "\n## "
            + ", ".join(f"[{topic}](https://github.com/topics/{topic})" for topic in group_name.split(", "))
        )
        sections.append(header)
        for repo in sorted(
            groups[group_name],
            key=lambda item: (-item["commit_count"], item["name"].lower()),
        ):
            message = repo.get("summary")
            if not message and repo.get("commits"):
                message = repo["commits"][0].get("message")
            if message:
                sections.append(
                    f"- [{repo['name']}]({repo['url']}) [{repo['commit_count']}]({repo['url']}/commits): {message}"
                )

    return (
        "# Recent Activity in Starred Repositories\n"
        f"_{report['active_repos_count']} active repos with "
        f"{report['total_commits_count']} new commits_\n" + "\n".join(sections)
    )


def _topics(repo: Mapping[str, Any]) -> list[str]:
    return [topic for topic in repo.get("topics", []) if topic != "hacktoberfest"]
