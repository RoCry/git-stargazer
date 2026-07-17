from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

import httpx
from github_client import GitHubClient


class RateLimitError(RuntimeError):
    pass


class CommitFeed:
    def __init__(
        self,
        transport: GitHubClient,
        *,
        watermark_file: Path = Path("watermarks.json"),
        now: Callable[[], datetime],
        freshness_window: timedelta = timedelta(days=3),
    ) -> None:
        self._transport = transport
        self._watermark_file = watermark_file
        self._now = _as_utc(now())
        self._freshness_window = freshness_window
        self._watermarks = self._load_watermarks()

    def is_active_repo(self, repo: Mapping[str, Any]) -> bool:
        pushed_at = repo.get("pushed_at")
        if not pushed_at:
            return False
        return _parse_datetime(str(pushed_at)) > self._now - self._freshness_window

    async def new_commits(self, repo: Mapping[str, Any]) -> list[dict[str, Any]]:
        repo_name = str(repo["full_name"])
        cutoff = self._now - self._freshness_window
        watermark = self._watermarks.get(repo_name)
        if watermark is not None and watermark >= cutoff:
            has_watermark = True
            modified_since = watermark
        else:
            has_watermark = False
            modified_since = cutoff

        raw_commits: list[dict[str, Any]] = []
        last_modified: datetime | None = None
        page = 1
        while True:
            response = await self._transport.request_commits(
                repo_name,
                modified_since=modified_since,
                page=page,
            )
            if response.status_code == 304:
                break
            if _is_rate_limit(response):
                raise RateLimitError(f"GitHub rate limit reached while fetching {repo_name}")
            response.raise_for_status()

            page_commits = response.json()
            if not isinstance(page_commits, list):
                raise TypeError("GitHub commits response must be a list")
            raw_commits.extend(page_commits)

            if last_modified_value := response.headers.get("Last-Modified"):
                page_last_modified = _as_utc(parsedate_to_datetime(last_modified_value))
                last_modified = (
                    max(last_modified, page_last_modified) if last_modified is not None else page_last_modified
                )
            reached_cutoff = any(
                _commit_datetime(commit) <= modified_since
                if has_watermark
                else _commit_datetime(commit) < modified_since
                for commit in page_commits
            )
            if reached_cutoff or "next" not in response.links:
                break
            page += 1

        if last_modified is not None:
            next_watermark = last_modified
        elif raw_commits:
            next_watermark = max(_commit_datetime(commit) for commit in raw_commits)
        else:
            next_watermark = None

        if next_watermark is not None:
            self._watermarks[repo_name] = next_watermark
            self._save_watermarks()

        comparison = (
            (lambda committed_at: committed_at > modified_since)
            if has_watermark
            else (lambda committed_at: committed_at >= modified_since)
        )
        return [commit for commit in raw_commits if not _is_bot(commit) and comparison(_commit_datetime(commit))]

    def _load_watermarks(self) -> dict[str, datetime]:
        if not self._watermark_file.exists():
            return {}

        data = json.loads(self._watermark_file.read_text())
        if not isinstance(data, dict) or data.get("version") != 2 or not isinstance(data.get("watermarks"), dict):
            raise ValueError("Unsupported watermark file format")

        cutoff = self._now - self._freshness_window
        watermarks = {repo: _parse_datetime(value) for repo, value in data["watermarks"].items()}
        return {repo: timestamp for repo, timestamp in watermarks.items() if timestamp >= cutoff}

    def _save_watermarks(self) -> None:
        self._watermark_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": 2,
            "watermarks": {repo: timestamp.isoformat() for repo, timestamp in sorted(self._watermarks.items())},
        }
        temporary_file = self._watermark_file.with_suffix(f"{self._watermark_file.suffix}.tmp")
        temporary_file.write_text(json.dumps(data, indent=2) + "\n")
        temporary_file.replace(self._watermark_file)


def _commit_datetime(commit: Mapping[str, Any]) -> datetime:
    return _parse_datetime(str(commit["commit"]["committer"]["date"]))


def _parse_datetime(value: str) -> datetime:
    return _as_utc(datetime.fromisoformat(value.replace("Z", "+00:00")))


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("Timestamp must include a timezone")
    return value.astimezone(timezone.utc)


def _is_bot(commit: Mapping[str, Any]) -> bool:
    author = commit.get("author")
    if not isinstance(author, Mapping):
        return True
    return author.get("type") == "Bot" or "[bot]" in str(author.get("login", ""))


def _is_rate_limit(response: httpx.Response) -> bool:
    if response.status_code == 429:
        return True
    if response.status_code != 403:
        return False
    return (
        response.headers.get("X-RateLimit-Remaining") == "0"
        or "Retry-After" in response.headers
        or "rate limit" in response.text.lower()
    )
