from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class EmptyStreakDecision:
    count: int
    should_stop: bool


def select_repos(
    repos: Iterable[Mapping[str, Any]],
    *,
    excluded_names: set[str],
    limit: int,
    is_active: Callable[[Mapping[str, Any]], bool],
) -> list[Mapping[str, Any]]:
    if limit <= 0:
        return []

    selected: list[Mapping[str, Any]] = []
    for repo in repos:
        if str(repo["full_name"]) in excluded_names or not is_active(repo):
            continue
        selected.append(repo)
        if len(selected) == limit:
            break
    return selected


def advance_empty_streak(*, current: int, has_commits: bool, limit: int) -> EmptyStreakDecision:
    count = 0 if has_commits else current + 1
    return EmptyStreakDecision(
        count=count,
        should_stop=limit > 0 and count >= limit,
    )
