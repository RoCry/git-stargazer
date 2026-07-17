from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime
from email.utils import format_datetime
from typing import Any

import httpx
from log import logger


class GitHubClient:
    def __init__(
        self,
        token: str,
        *,
        timeout: float = 30,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url="https://api.github.com",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "git-stargazer",
            },
            http2=transport is None,
            timeout=timeout,
            transport=transport,
        )

    async def __aenter__(self) -> GitHubClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._client.aclose()

    async def request_commits(
        self,
        repo_full_name: str,
        *,
        modified_since: datetime,
        page: int,
        per_page: int = 100,
    ) -> httpx.Response:
        return await self._client.get(
            f"/repos/{repo_full_name}/commits",
            headers={"If-Modified-Since": format_datetime(modified_since, usegmt=True)},
            params={"per_page": per_page, "page": page},
        )

    async def starred_repo_pages(self, *, per_page: int = 100) -> AsyncIterator[list[dict[str, Any]]]:
        page = 1
        while True:
            logger.debug("Fetching starred repositories page %s", page)
            response = await self._client.get(
                "/user/starred",
                params={
                    "per_page": per_page,
                    "page": page,
                    "sort": "updated",
                    "direction": "desc",
                },
            )
            response.raise_for_status()
            repos = response.json()
            if not isinstance(repos, list):
                raise TypeError("GitHub starred repositories response must be a list")
            if not repos:
                return
            yield repos
            page += 1
