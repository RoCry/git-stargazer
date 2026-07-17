from __future__ import annotations

from datetime import datetime, timezone

from report import assemble_report, merge_reports, render_json_feed, render_markdown


def repo(name: str, *, topics: list[str] | None = None) -> dict:
    return {
        "full_name": name,
        "html_url": f"https://github.com/{name}",
        "description": f"Description for {name}",
        "topics": topics or [],
    }


def commit(sha: str, message: str, committed_at: str) -> dict:
    return {
        "sha": sha,
        "commit": {
            "message": message,
            "author": {"date": committed_at},
            "committer": {"date": committed_at},
        },
    }


def test_assemble_report_counts_only_repos_with_commits_as_active() -> None:
    report = assemble_report(
        [
            (
                repo("org/active", topics=["python"]),
                [commit("abc1234", "Add feature", "2026-07-17T07:00:00Z")],
                "✨ Feature",
            ),
            (repo("org/quiet"), [], None),
        ]
    )

    assert report == {
        "total_repos_count": 2,
        "active_repos_count": 1,
        "total_commits_count": 1,
        "repos": [
            {
                "name": "org/active",
                "url": "https://github.com/org/active",
                "commit_count": 1,
                "summary": "✨ Feature",
                "description": "Description for org/active",
                "commits": [
                    {
                        "sha": "abc1234",
                        "message": "Add feature",
                        "date": "2026-07-17T07:00:00Z",
                    }
                ],
                "topics": ["python"],
            },
            {
                "name": "org/quiet",
                "url": "https://github.com/org/quiet",
                "commit_count": 0,
                "summary": None,
                "description": "Description for org/quiet",
                "commits": [],
            },
        ],
    }


def test_merge_reports_combines_same_day_counts_and_order() -> None:
    left = {
        "total_repos_count": 1,
        "active_repos_count": 1,
        "total_commits_count": 2,
        "repos": [{"name": "org/first"}],
    }
    right = {
        "total_repos_count": 2,
        "active_repos_count": 1,
        "total_commits_count": 1,
        "repos": [{"name": "org/second"}, {"name": "org/quiet"}],
    }

    assert merge_reports(left, right) == {
        "total_repos_count": 3,
        "active_repos_count": 2,
        "total_commits_count": 3,
        "repos": [
            {"name": "org/first"},
            {"name": "org/second"},
            {"name": "org/quiet"},
        ],
    }


def test_markdown_groups_shared_topics_then_other_in_stable_order() -> None:
    report = {
        "total_repos_count": 7,
        "active_repos_count": 6,
        "total_commits_count": 10,
        "repos": [
            _render_repo("org/python-a", 2, ["python", "hacktoberfest"]),
            _render_repo("org/python-b", 1, ["python", "cli"]),
            _render_repo("org/go-a", 2, ["go"]),
            _render_repo("org/go-b", 1, ["go", "cli"]),
            _render_repo("org/rust", 3, ["rust"]),
            _render_repo("org/hacktober", 1, ["hacktoberfest"]),
            _render_repo("org/plain", 0, []),
        ],
    }

    markdown = render_markdown(report)

    assert (
        markdown
        == """# Recent Activity in Starred Repositories
_6 active repos with 10 new commits_

## [go](https://github.com/topics/go)
- [org/go-a](https://github.com/org/go-a) [2](https://github.com/org/go-a/commits): Summary org/go-a
- [org/go-b](https://github.com/org/go-b) [1](https://github.com/org/go-b/commits): Summary org/go-b

## [python](https://github.com/topics/python)
- [org/python-a](https://github.com/org/python-a) [2](https://github.com/org/python-a/commits): Summary org/python-a
- [org/python-b](https://github.com/org/python-b) [1](https://github.com/org/python-b/commits): Summary org/python-b

## Other
- [org/rust](https://github.com/org/rust) [3](https://github.com/org/rust/commits): Summary org/rust
- [org/hacktober](https://github.com/org/hacktober) [1](https://github.com/org/hacktober/commits): Summary org/hacktober"""  # noqa: E501
    )
    assert "topics/hacktoberfest" not in markdown
    assert "org/plain" not in markdown


def test_json_feed_rendering_is_deterministic() -> None:
    report = {
        "total_repos_count": 1,
        "active_repos_count": 1,
        "total_commits_count": 1,
        "repos": [
            {
                "name": "org/project",
                "url": "https://github.com/org/project",
                "commit_count": 1,
                "summary": "✨ Feature",
                "description": "Useful project",
                "topics": ["python"],
                "commits": [
                    {
                        "sha": "abcdef012345",
                        "message": "Add feature\nMore detail",
                        "date": "2026-07-17T07:00:00Z",
                    }
                ],
            }
        ],
    }

    feed = render_json_feed(report, published_at=datetime(2026, 7, 17, 8, 0, tzinfo=timezone.utc))

    assert feed == {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "GitHub Starred Repositories Activity",
        "home_page_url": "https://github.com/RoCry/git-stargazer/releases/latest",
        "feed_url": "https://github.com/RoCry/git-stargazer/releases/download/latest/feed.json",
        "items": [
            {
                "id": "https://github.com/org/project",
                "url": "https://github.com/org/project",
                "title": "org/project: ✨ Feature",
                "content_text": "# org/project\n\n1 commits\n\n### ✨ Feature\n\n### Useful project\n\n- Add feature",
                "content_html": (
                    '<div class="repo-summary">\n<h3>✨ Feature</h3>\n</div>\n'
                    '<div class="repo-description">\n<h4>Useful project</h4>\n</div>\n'
                    '<div class="commit-list">\n<div class="commit-item">• Add feature '
                    '<a href="https://github.com/org/project/commit/abcdef012345">'
                    "<code>abcdef0</code></a></div>\n</div>\n"
                    '<div class="repo-footer">\n<p><em>'
                    '<a href="https://github.com/org/project/commits">1 commits</a>'
                    "</em></p>\n</div>"
                ),
                "date_published": "2026-07-17T08:00:00+00:00",
                "tags": ["python"],
            }
        ],
    }


def _render_repo(name: str, commit_count: int, topics: list[str]) -> dict:
    return {
        "name": name,
        "url": f"https://github.com/{name}",
        "commit_count": commit_count,
        "summary": f"Summary {name}",
        "description": None,
        "topics": topics,
        "commits": [
            {
                "sha": f"{name}-sha",
                "message": f"Commit {name}",
                "date": "2026-07-17T07:00:00Z",
            }
        ],
    }
