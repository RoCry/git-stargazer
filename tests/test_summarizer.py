from __future__ import annotations

import pytest
from summarizer import CannedSummarizer, DisabledSummarizer

REPO = {"full_name": "owner/project", "description": "A useful project"}


def commit(message: str) -> dict:
    return {"commit": {"message": message}}


@pytest.mark.asyncio
async def test_merge_commits_are_left_out_of_summary_prompt() -> None:
    summarizer = CannedSummarizer("✨ Focused changes")

    summary = await summarizer.summarize(
        REPO,
        [
            commit("Merge pull request #12 from owner/branch"),
            commit("Add feature\nwith details"),
            commit("Fix bug"),
        ],
    )

    assert summary == "✨ Focused changes"
    assert "Merge pull request" not in summarizer.prompts[0]
    assert "with details" not in summarizer.prompts[0]
    assert "- Add feature" in summarizer.prompts[0]
    assert "- Fix bug" in summarizer.prompts[0]


@pytest.mark.asyncio
async def test_one_meaningful_commit_skips_summarization() -> None:
    summarizer = CannedSummarizer("must not be used")

    summary = await summarizer.summarize(
        REPO,
        [
            commit("Merge pull request #12 from owner/branch"),
            commit("Only meaningful change"),
        ],
    )

    assert summary is None
    assert summarizer.prompts == []


@pytest.mark.asyncio
@pytest.mark.parametrize("response", ["NONE", " none ", '"NONE"', "`NONE`"])
async def test_none_response_yields_no_summary(response: str) -> None:
    summarizer = CannedSummarizer(response)

    summary = await summarizer.summarize(REPO, [commit("First change"), commit("Second change")])

    assert summary is None


@pytest.mark.asyncio
async def test_summary_strips_quotes_and_backticks() -> None:
    summarizer = CannedSummarizer('  `"✨ Clear result"`  ')

    summary = await summarizer.summarize(REPO, [commit("First change"), commit("Second change")])

    assert summary == "✨ Clear result"


@pytest.mark.asyncio
async def test_disabled_summarizer_returns_no_summary() -> None:
    summary = await DisabledSummarizer().summarize(REPO, [commit("First change"), commit("Second change")])

    assert summary is None
