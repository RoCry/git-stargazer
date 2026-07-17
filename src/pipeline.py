from __future__ import annotations

import json
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from commit_feed import CommitFeed, RateLimitError
from config import Config
from github_client import GitHubClient
from log import logger
from report import ReportRow, assemble_report, merge_reports, render_json_feed, render_markdown
from selection import advance_empty_streak, select_repos
from summarizer import Summarizer


@dataclass(frozen=True, slots=True)
class RunArtifacts:
    report: dict[str, Any]
    markdown: str
    feed: dict[str, Any]
    report_path: Path
    markdown_path: Path
    feed_path: Path


async def run_daily(
    config: Config,
    *,
    transport: GitHubClient,
    commit_feed: CommitFeed,
    summarizer: Summarizer,
    report_dir: Path = Path("reports"),
    published_at: datetime,
) -> RunArtifacts:
    report_path = report_dir / f"recent_commits_{config.report_date.isoformat()}.json"
    markdown_path = report_dir / f"recent_commits_{config.report_date.isoformat()}.md"
    feed_path = report_dir / "feed.json"
    existing_report = _load_report(report_path)
    excluded_names = {str(repo["name"]) for repo in existing_report["repos"]} if existing_report else set()

    selected_repos: list[Mapping[str, Any]] = []
    if config.repo_limit > 0:
        async for page in transport.starred_repo_pages():
            remaining = config.repo_limit - len(selected_repos)
            selected_repos.extend(
                select_repos(
                    page,
                    excluded_names=excluded_names,
                    limit=remaining,
                    is_active=commit_feed.is_active_repo,
                )
            )
            if len(selected_repos) == config.repo_limit:
                break

    rows: list[ReportRow] = []
    empty_streak = 0
    for repo in selected_repos:
        try:
            commits = await commit_feed.new_commits(repo)
        except RateLimitError as error:
            logger.error("%s; stopping this run", error)
            break

        summary = await summarizer.summarize(repo, commits)
        rows.append((repo, commits, summary))
        streak = advance_empty_streak(
            current=empty_streak,
            has_commits=bool(commits),
            limit=config.empty_streak_limit,
        )
        empty_streak = streak.count
        if streak.should_stop:
            logger.info(
                "Stopping after %s consecutive repositories without commits",
                empty_streak,
            )
            break

    report = assemble_report(rows)
    if existing_report is not None:
        report = merge_reports(existing_report, report)
    markdown = render_markdown(report)
    feed = render_json_feed(report, published_at=published_at)

    report_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(markdown, encoding="utf-8")
    feed_path.write_text(json.dumps(feed, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_ci_outputs(
        config,
        report_path=report_path,
        markdown_path=markdown_path,
        feed_path=feed_path,
    )
    _cleanup_old_reports(
        report_dir,
        excluded={report_path, markdown_path},
        dry_run=not config.is_ci,
    )

    return RunArtifacts(
        report=report,
        markdown=markdown,
        feed=feed,
        report_path=report_path,
        markdown_path=markdown_path,
        feed_path=feed_path,
    )


def _load_report(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise TypeError(f"Report must be a JSON object: {path}")
    return report


def _write_ci_outputs(
    config: Config,
    *,
    report_path: Path,
    markdown_path: Path,
    feed_path: Path,
) -> None:
    if not config.is_ci:
        return
    if config.github_output is None:
        raise ValueError("GITHUB_OUTPUT environment variable is required in CI")
    with config.github_output.open("a", encoding="utf-8") as output:
        output.write(f"report_file={markdown_path}\n")
        output.write(f"report_json_file={report_path}\n")
        output.write(f"feed_file={feed_path}\n")


def _cleanup_old_reports(
    report_dir: Path,
    *,
    excluded: set[Path],
    dry_run: bool,
) -> None:
    current_time = time.time()
    for path in report_dir.iterdir():
        if path in excluded or current_time - path.stat().st_mtime < 12 * 3600:
            continue
        if dry_run:
            logger.info("Would remove old report file: %s", path)
        else:
            path.unlink()
            logger.info("Removed old report file: %s", path)
