from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Config:
    github_token: str
    report_date: date
    repo_limit: int
    empty_streak_limit: int
    summarizer_model: str | None
    is_ci: bool
    github_output: Path | None

    @classmethod
    def from_environment(
        cls,
        environment: Mapping[str, str],
        *,
        default_date: date,
    ) -> Config:
        github_token = environment.get("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")

        is_ci = bool(environment.get("GITHUB_ACTIONS"))
        report_date_value = environment.get("TODAY")
        if not report_date_value and is_ci:
            raise ValueError("TODAY environment variable is required")

        repo_limit_value = environment.get("REPO_LIMIT", "").strip()
        empty_streak_value = environment.get("EMPTY_REPO_CONSECUTIVE_LIMIT", "").strip()
        github_output_value = environment.get("GITHUB_OUTPUT")

        return cls(
            github_token=github_token,
            report_date=(date.fromisoformat(report_date_value) if report_date_value else default_date),
            repo_limit=int(repo_limit_value) if repo_limit_value else 100,
            empty_streak_limit=(int(empty_streak_value) if empty_streak_value else 10),
            summarizer_model=environment.get("SUMMARIZER_MODEL") or None,
            is_ci=is_ci,
            github_output=Path(github_output_value) if github_output_value else None,
        )
