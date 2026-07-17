from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol


class Summarizer(Protocol):
    async def summarize(
        self,
        repo: Mapping[str, Any],
        commits: Sequence[Mapping[str, Any]],
    ) -> str | None: ...


class DisabledSummarizer:
    async def summarize(
        self,
        repo: Mapping[str, Any],
        commits: Sequence[Mapping[str, Any]],
    ) -> str | None:
        return None


class _PromptSummarizer:
    async def summarize(
        self,
        repo: Mapping[str, Any],
        commits: Sequence[Mapping[str, Any]],
    ) -> str | None:
        messages = _meaningful_messages(commits)
        if len(messages) <= 1:
            return None

        prompt = _prompt(repo, messages, commit_count=len(commits))
        raw_summary = await self._complete(prompt)
        summary = raw_summary.strip().strip('`"').strip()
        return None if summary.upper() == "NONE" else summary

    async def _complete(self, prompt: str) -> str:
        raise NotImplementedError


class LiteLLMSummarizer(_PromptSummarizer):
    def __init__(self, model: str) -> None:
        self._model = model

    async def _complete(self, prompt: str) -> str:
        from litellm import acompletion

        response = await acompletion(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        if not isinstance(content, str):
            raise TypeError("Summarizer response content must be text")
        return content


class CannedSummarizer(_PromptSummarizer):
    def __init__(self, response: str) -> None:
        self._response = response
        self.prompts: list[str] = []

    async def _complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self._response


def build_summarizer(model: str | None) -> Summarizer:
    return LiteLLMSummarizer(model) if model else DisabledSummarizer()


def _meaningful_messages(
    commits: Sequence[Mapping[str, Any]],
) -> list[str]:
    messages: list[str] = []
    for commit in commits[:20]:
        message = str(commit["commit"]["message"])
        if message.startswith("Merge pull request"):
            continue
        messages.append(message.splitlines()[0])
    return messages


def _prompt(repo: Mapping[str, Any], messages: Sequence[str], *, commit_count: int) -> str:
    bullets = "\n".join(f"- {message}" for message in messages)
    return f"""Repository: {repo["full_name"]}
Description: {repo.get("description") or "No description"}
Recent commits: {commit_count}

Commit details:
{bullets}

Generate `<EXACTLY ONE emoji> <minimalistic title with no more than 80 characters>`.
If nothing meaningful, return `NONE`."""
