from __future__ import annotations

import json
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

import httpx
import pytest
from commit_feed import CommitFeed
from config import Config
from github_client import GitHubClient
from pipeline import run_daily
from summarizer import CannedSummarizer, DisabledSummarizer

NOW = datetime(2026, 7, 17, 8, 0, tzinfo=timezone.utc)


def starred_repo(name: str, description: str) -> dict:
    return {
        "full_name": name,
        "html_url": f"https://github.com/{name}",
        "description": description,
        "topics": ["python"],
        "pushed_at": "2026-07-17T07:45:00Z",
    }


def commit(sha: str, message: str, committed_at: str) -> dict:
    return {
        "sha": sha,
        "author": {"login": "alice", "type": "User"},
        "commit": {
            "message": message,
            "author": {"date": committed_at},
            "committer": {"date": committed_at},
        },
    }


@pytest.mark.asyncio
async def test_full_daily_run_and_same_day_rerun_use_fake_adapters(
    tmp_path: Path,
) -> None:
    alpha = starred_repo("org/alpha", "Alpha project")
    beta = starred_repo("org/beta", "Beta project")
    request_counts: Counter[str] = Counter()

    def handler(request: httpx.Request) -> httpx.Response:
        request_counts[request.url.path] += 1
        match request.url.path:
            case "/user/starred":
                return httpx.Response(200, json=[alpha, beta])
            case "/repos/org/alpha/commits":
                return httpx.Response(
                    200,
                    headers={"Last-Modified": "Fri, 17 Jul 2026 07:30:00 GMT"},
                    json=[
                        commit("aaaaaaa111", "Add alpha", "2026-07-17T07:00:00Z"),
                        commit("bbbbbbb222", "Fix alpha", "2026-07-17T06:00:00Z"),
                    ],
                )
            case "/repos/org/beta/commits":
                return httpx.Response(
                    200,
                    json=[commit("ccccccc333", "Add beta", "2026-07-17T07:20:00Z")],
                )
            case _:
                raise AssertionError(f"Unexpected request: {request.url}")

    config = Config(
        github_token="token",
        report_date=date(2026, 7, 17),
        repo_limit=1,
        empty_streak_limit=10,
        summarizer_model=None,
        is_ci=False,
        github_output=None,
    )
    report_dir = tmp_path / "reports"
    watermark_file = tmp_path / "watermarks.json"
    summarizer = CannedSummarizer("✨ Alpha changes")

    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        feed = CommitFeed(transport, watermark_file=watermark_file, now=lambda: NOW)
        first = await run_daily(
            config,
            transport=transport,
            commit_feed=feed,
            summarizer=summarizer,
            report_dir=report_dir,
            published_at=NOW,
        )
        second = await run_daily(
            config,
            transport=transport,
            commit_feed=feed,
            summarizer=summarizer,
            report_dir=report_dir,
            published_at=NOW,
        )

    assert first.report["repos"] == [
        {
            "name": "org/alpha",
            "url": "https://github.com/org/alpha",
            "commit_count": 2,
            "summary": "✨ Alpha changes",
            "description": "Alpha project",
            "commits": [
                {
                    "sha": "aaaaaaa111",
                    "message": "Add alpha",
                    "date": "2026-07-17T07:00:00Z",
                },
                {
                    "sha": "bbbbbbb222",
                    "message": "Fix alpha",
                    "date": "2026-07-17T06:00:00Z",
                },
            ],
            "topics": ["python"],
        }
    ]
    assert second.report == {
        "total_repos_count": 2,
        "active_repos_count": 2,
        "total_commits_count": 3,
        "repos": [
            first.report["repos"][0],
            {
                "name": "org/beta",
                "url": "https://github.com/org/beta",
                "commit_count": 1,
                "summary": None,
                "description": "Beta project",
                "commits": [
                    {
                        "sha": "ccccccc333",
                        "message": "Add beta",
                        "date": "2026-07-17T07:20:00Z",
                    }
                ],
                "topics": ["python"],
            },
        ],
    }
    assert (
        second.markdown
        == """# Recent Activity in Starred Repositories
_2 active repos with 3 new commits_

## [python](https://github.com/topics/python)
- [org/alpha](https://github.com/org/alpha) [2](https://github.com/org/alpha/commits): ✨ Alpha changes
- [org/beta](https://github.com/org/beta) [1](https://github.com/org/beta/commits): Add beta

## Other"""
    )
    assert second.feed == {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "GitHub Starred Repositories Activity",
        "home_page_url": "https://github.com/RoCry/git-stargazer/releases/latest",
        "feed_url": "https://github.com/RoCry/git-stargazer/releases/download/latest/feed.json",
        "items": [
            {
                "id": "https://github.com/org/alpha",
                "url": "https://github.com/org/alpha",
                "title": "org/alpha: ✨ Alpha changes",
                "content_text": (
                    "# org/alpha\n\n2 commits\n\n### ✨ Alpha changes\n\n### Alpha project\n\n- Add alpha\n- Fix alpha"
                ),
                "content_html": (
                    '<div class="repo-summary">\n<h3>✨ Alpha changes</h3>\n</div>\n'
                    '<div class="repo-description">\n<h4>Alpha project</h4>\n</div>\n'
                    '<div class="commit-list">\n<div class="commit-item">• Add alpha '
                    '<a href="https://github.com/org/alpha/commit/aaaaaaa111">'
                    "<code>aaaaaaa</code></a></div>\n"
                    '<div class="commit-item">• Fix alpha '
                    '<a href="https://github.com/org/alpha/commit/bbbbbbb222">'
                    "<code>bbbbbbb</code></a></div>\n</div>\n"
                    '<div class="repo-footer">\n<p><em>'
                    '<a href="https://github.com/org/alpha/commits">2 commits</a>'
                    "</em></p>\n</div>"
                ),
                "date_published": "2026-07-17T08:00:00+00:00",
                "tags": ["python"],
            },
            {
                "id": "https://github.com/org/beta",
                "url": "https://github.com/org/beta",
                "title": "org/beta",
                "content_text": "# org/beta\n\n1 commits\n\n### Beta project\n\n- Add beta",
                "content_html": (
                    '<div class="repo-description">\n<h4>Beta project</h4>\n</div>\n'
                    '<div class="commit-list">\n<div class="commit-item">• Add beta '
                    '<a href="https://github.com/org/beta/commit/ccccccc333">'
                    "<code>ccccccc</code></a></div>\n</div>\n"
                    '<div class="repo-footer">\n<p><em>'
                    '<a href="https://github.com/org/beta/commits">1 commits</a>'
                    "</em></p>\n</div>"
                ),
                "date_published": "2026-07-17T08:00:00+00:00",
                "tags": ["python"],
            },
        ],
    }
    assert json.loads(second.report_path.read_text()) == second.report
    assert second.markdown_path.read_text() == second.markdown
    assert json.loads(second.feed_path.read_text()) == second.feed
    assert request_counts["/repos/org/alpha/commits"] == 1
    assert request_counts["/repos/org/beta/commits"] == 1
    assert request_counts["/user/starred"] == 2
    assert watermark_file.exists()


@pytest.mark.asyncio
async def test_rate_limit_stops_run_cleanly(tmp_path: Path) -> None:
    project = starred_repo("org/project", "Project")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/user/starred":
            return httpx.Response(200, json=[project])
        return httpx.Response(403, headers={"X-RateLimit-Remaining": "0"})

    config = Config(
        github_token="token",
        report_date=date(2026, 7, 17),
        repo_limit=1,
        empty_streak_limit=10,
        summarizer_model=None,
        is_ci=False,
        github_output=None,
    )
    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        artifacts = await run_daily(
            config,
            transport=transport,
            commit_feed=CommitFeed(
                transport,
                watermark_file=tmp_path / "watermarks.json",
                now=lambda: NOW,
            ),
            summarizer=DisabledSummarizer(),
            report_dir=tmp_path / "reports",
            published_at=NOW,
        )

    assert artifacts.report == {
        "total_repos_count": 0,
        "active_repos_count": 0,
        "total_commits_count": 0,
        "repos": [],
    }


@pytest.mark.asyncio
async def test_empty_streak_short_circuits_commit_fetching(tmp_path: Path) -> None:
    repos = [
        starred_repo("org/first", "First"),
        starred_repo("org/second", "Second"),
        starred_repo("org/must-not-fetch", "Third"),
    ]
    requested_paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        if request.url.path == "/user/starred":
            return httpx.Response(200, json=repos)
        if request.url.path == "/repos/org/must-not-fetch/commits":
            raise AssertionError("Empty-streak policy failed to stop fetching")
        return httpx.Response(200, json=[])

    config = Config(
        github_token="token",
        report_date=date(2026, 7, 17),
        repo_limit=3,
        empty_streak_limit=2,
        summarizer_model=None,
        is_ci=False,
        github_output=None,
    )
    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        artifacts = await run_daily(
            config,
            transport=transport,
            commit_feed=CommitFeed(
                transport,
                watermark_file=tmp_path / "watermarks.json",
                now=lambda: NOW,
            ),
            summarizer=DisabledSummarizer(),
            report_dir=tmp_path / "reports",
            published_at=NOW,
        )

    assert artifacts.report["total_repos_count"] == 2
    assert "/repos/org/must-not-fetch/commits" not in requested_paths


@pytest.mark.asyncio
async def test_ci_outputs_preserve_workflow_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    github_output = tmp_path / "github-output"

    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(f"Repo limit zero should not request {request.url}")

    config = Config(
        github_token="token",
        report_date=date(2026, 7, 17),
        repo_limit=0,
        empty_streak_limit=10,
        summarizer_model=None,
        is_ci=True,
        github_output=github_output,
    )
    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        await run_daily(
            config,
            transport=transport,
            commit_feed=CommitFeed(
                transport,
                watermark_file=tmp_path / "watermarks.json",
                now=lambda: NOW,
            ),
            summarizer=DisabledSummarizer(),
            published_at=NOW,
        )

    assert github_output.read_text() == (
        "report_file=reports/recent_commits_2026-07-17.md\n"
        "report_json_file=reports/recent_commits_2026-07-17.json\n"
        "feed_file=reports/feed.json\n"
    )
