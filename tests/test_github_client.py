from __future__ import annotations

from urllib.parse import parse_qs

import httpx
import pytest
from github_client import GitHubClient


@pytest.mark.asyncio
async def test_starred_transport_yields_updated_pages_until_empty() -> None:
    requests: list[httpx.Request] = []
    responses = [
        [{"full_name": "org/first"}],
        [{"full_name": "org/second"}],
        [],
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=responses.pop(0))

    async with GitHubClient("token", transport=httpx.MockTransport(handler)) as transport:
        pages = [page async for page in transport.starred_repo_pages(per_page=25)]

    assert pages == [
        [{"full_name": "org/first"}],
        [{"full_name": "org/second"}],
    ]
    assert [parse_qs(request.url.query.decode()) for request in requests] == [
        {"per_page": ["25"], "page": ["1"], "sort": ["updated"], "direction": ["desc"]},
        {"per_page": ["25"], "page": ["2"], "sort": ["updated"], "direction": ["desc"]},
        {"per_page": ["25"], "page": ["3"], "sort": ["updated"], "direction": ["desc"]},
    ]
