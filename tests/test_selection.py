from __future__ import annotations

from selection import advance_empty_streak, select_repos


def repo(name: str, *, active: bool = True) -> dict:
    return {"full_name": name, "active": active}


def test_selection_excludes_then_checks_activity_then_applies_limit() -> None:
    repos = [
        repo("org/already"),
        repo("org/inactive", active=False),
        repo("org/first"),
        repo("org/second"),
        repo("org/beyond-limit"),
    ]

    selected = select_repos(
        repos,
        excluded_names={"org/already"},
        limit=2,
        is_active=lambda candidate: candidate["active"],
    )

    assert [item["full_name"] for item in selected] == ["org/first", "org/second"]


def test_selection_with_nonpositive_limit_selects_nothing() -> None:
    assert (
        select_repos(
            [repo("org/project")],
            excluded_names=set(),
            limit=0,
            is_active=lambda candidate: candidate["active"],
        )
        == []
    )


def test_empty_streak_increments_and_stops_exactly_at_limit() -> None:
    first = advance_empty_streak(current=0, has_commits=False, limit=2)
    second = advance_empty_streak(current=first.count, has_commits=False, limit=2)

    assert (first.count, first.should_stop) == (1, False)
    assert (second.count, second.should_stop) == (2, True)


def test_nonempty_result_resets_empty_streak() -> None:
    result = advance_empty_streak(current=7, has_commits=True, limit=2)

    assert (result.count, result.should_stop) == (0, False)


def test_nonpositive_empty_streak_limit_never_stops() -> None:
    for limit in (0, -1):
        result = advance_empty_streak(current=999, has_commits=False, limit=limit)

        assert (result.count, result.should_stop) == (1000, False)
