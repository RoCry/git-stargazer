from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs

import httpx
import pytest
from commit_feed import CommitFeed, RateLimitError
from github_client import GitHubClient

NOW = datetime(2026, 7, 17, 8, 0, tzinfo=timezone.utc)
REPO = {"full_name": "owner/project"}


def commit(
    sha: str,
    committed_at: str,
    *,
    author: dict[str, str] | None = None,
) -> dict:
    return {
        "sha": sha,
        "author": author if author is not None else {"login": "alice", "type": "User"},
        "commit": {
            "message": f"Commit {sha}",
            "author": {"date": committed_at},
            "committer": {"date": committed_at},
        },
    }


@pytest.mark.asyncio
async def test_not_modified_yields_no_new_commits(tmp_path: Path) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(304)

    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        feed = CommitFeed(
            transport,
            watermark_file=tmp_path / "watermarks.json",
            now=lambda: NOW,
        )

        assert await feed.new_commits(REPO) == []

    assert requests[0].headers["if-modified-since"] == "Tue, 14 Jul 2026 08:00:00 GMT"


@pytest.mark.asyncio
async def test_last_modified_advances_persisted_watermark(tmp_path: Path) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            return httpx.Response(
                200,
                headers={"Last-Modified": "Fri, 17 Jul 2026 07:30:00 GMT"},
                json=[commit("new", "2026-07-17T07:00:00Z")],
            )
        return httpx.Response(304)

    watermark_file = tmp_path / "watermarks.json"
    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        first_feed = CommitFeed(transport, watermark_file=watermark_file, now=lambda: NOW)
        assert [item["sha"] for item in await first_feed.new_commits(REPO)] == ["new"]

        reloaded_feed = CommitFeed(transport, watermark_file=watermark_file, now=lambda: NOW)
        assert await reloaded_feed.new_commits(REPO) == []

    assert requests[1].headers["if-modified-since"] == "Fri, 17 Jul 2026 07:30:00 GMT"


@pytest.mark.asyncio
async def test_missing_last_modified_advances_from_newest_commit(tmp_path: Path) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            return httpx.Response(
                200,
                json=[
                    commit("older", "2026-07-17T06:00:00Z"),
                    commit("newest", "2026-07-17T15:00:00+08:00"),
                ],
            )
        return httpx.Response(304)

    watermark_file = tmp_path / "watermarks.json"
    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        feed = CommitFeed(transport, watermark_file=watermark_file, now=lambda: NOW)
        assert [item["sha"] for item in await feed.new_commits(REPO)] == [
            "older",
            "newest",
        ]

        reloaded_feed = CommitFeed(transport, watermark_file=watermark_file, now=lambda: NOW)
        await reloaded_feed.new_commits(REPO)

    assert requests[1].headers["if-modified-since"] == "Fri, 17 Jul 2026 07:00:00 GMT"


@pytest.mark.asyncio
async def test_bot_commits_are_filtered_but_advance_watermark(tmp_path: Path) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            return httpx.Response(
                200,
                json=[
                    commit(
                        "typed-bot",
                        "2026-07-17T07:30:00Z",
                        author={"login": "renovate", "type": "Bot"},
                    ),
                    commit(
                        "named-bot",
                        "2026-07-17T07:20:00Z",
                        author={"login": "dependabot[bot]", "type": "User"},
                    ),
                    commit("human", "2026-07-17T07:10:00Z"),
                ],
            )
        return httpx.Response(304)

    watermark_file = tmp_path / "watermarks.json"
    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        feed = CommitFeed(transport, watermark_file=watermark_file, now=lambda: NOW)
        assert [item["sha"] for item in await feed.new_commits(REPO)] == ["human"]

        reloaded_feed = CommitFeed(transport, watermark_file=watermark_file, now=lambda: NOW)
        await reloaded_feed.new_commits(REPO)

    assert requests[1].headers["if-modified-since"] == "Fri, 17 Jul 2026 07:30:00 GMT"


@pytest.mark.asyncio
async def test_expired_watermark_falls_back_to_freshness_window(tmp_path: Path) -> None:
    watermark_file = tmp_path / "watermarks.json"

    def old_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[commit("old", "2026-07-10T08:00:00Z")])

    async with GitHubClient("token", transport=httpx.MockTransport(old_handler)) as transport:
        old_feed = CommitFeed(
            transport,
            watermark_file=watermark_file,
            now=lambda: NOW - timedelta(days=7),
        )
        await old_feed.new_commits(REPO)

    requests: list[httpx.Request] = []

    def current_handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(304)

    async with GitHubClient("token", transport=httpx.MockTransport(current_handler)) as transport:
        current_feed = CommitFeed(transport, watermark_file=watermark_file, now=lambda: NOW)
        assert await current_feed.new_commits(REPO) == []

    assert requests[0].headers["if-modified-since"] == "Tue, 14 Jul 2026 08:00:00 GMT"


@pytest.mark.asyncio
async def test_rate_limit_response_raises_domain_error(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            headers={
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "1784282400",
            },
        )

    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        feed = CommitFeed(
            transport,
            watermark_file=tmp_path / "watermarks.json",
            now=lambda: NOW,
        )

        with pytest.raises(RateLimitError, match="owner/project"):
            await feed.new_commits(REPO)


@pytest.mark.asyncio
async def test_all_commit_pages_are_returned_before_watermark_advances(
    tmp_path: Path,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        page = parse_qs(request.url.query.decode())["page"][0]
        if page == "1":
            return httpx.Response(
                200,
                headers={
                    "Last-Modified": "Fri, 17 Jul 2026 07:30:00 GMT",
                    "Link": ('<https://api.github.com/repos/owner/project/commits?per_page=100&page=2>; rel="next"'),
                },
                json=[commit("first-page", "2026-07-17T07:00:00Z")],
            )
        return httpx.Response(200, json=[commit("second-page", "2026-07-17T06:00:00Z")])

    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        feed = CommitFeed(
            transport,
            watermark_file=tmp_path / "watermarks.json",
            now=lambda: NOW,
        )

        commits = await feed.new_commits(REPO)

    assert [item["sha"] for item in commits] == ["first-page", "second-page"]
    assert [parse_qs(request.url.query.decode())["page"] for request in requests] == [
        ["1"],
        ["2"],
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status_code", "headers", "body"),
    [
        (
            403,
            {"X-RateLimit-Remaining": "42", "Retry-After": "60"},
            {"message": "You have exceeded a secondary rate limit."},
        ),
        (429, {}, {"message": "Too many requests"}),
    ],
)
async def test_all_rate_limit_shapes_raise_domain_error(
    tmp_path: Path,
    status_code: int,
    headers: dict[str, str],
    body: dict[str, str],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, headers=headers, json=body)

    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        feed = CommitFeed(
            transport,
            watermark_file=tmp_path / "watermarks.json",
            now=lambda: NOW,
        )

        with pytest.raises(RateLimitError, match="owner/project"):
            await feed.new_commits(REPO)


@pytest.mark.asyncio
async def test_feed_owns_active_repo_freshness_and_rejects_naive_times(
    tmp_path: Path,
) -> None:
    def no_request(_: httpx.Request) -> httpx.Response:
        raise AssertionError("No HTTP request expected")

    async with GitHubClient("token", transport=httpx.MockTransport(no_request)) as transport:
        feed = CommitFeed(
            transport,
            watermark_file=tmp_path / "watermarks.json",
            now=lambda: NOW,
        )

        assert feed.is_active_repo({"pushed_at": "2026-07-17T07:00:00Z"})
        assert not feed.is_active_repo({"pushed_at": "2026-07-01T07:00:00Z"})
        assert not feed.is_active_repo({"pushed_at": None})
        with pytest.raises(ValueError, match="timezone"):
            feed.is_active_repo({"pushed_at": "2026-07-17T07:00:00"})
