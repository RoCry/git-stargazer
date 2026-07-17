# Commit feed owns the freshness protocol

The "what's new since last run" protocol (watermark storage, conditional requests via `If-Modified-Since`/`Last-Modified`, since-filtering, bot filtering, watermark write-back, freshness window) was smeared across `CacheManager`, `GitHubClient`, and `main.py`, coordinated through a shared constant — which produced a silently-swallowed write-back bug and naive/aware timezone mixing, with zero tests. We concentrate the whole protocol in one deep commit-feed module whose interface is essentially `new_commits(repo)`, and demote the GitHub client to a thin transport adapter with an injectable httpx transport (live HTTP in prod, `MockTransport` in tests). All timestamps inside the feed are UTC-aware.

## Considered Options

- **Keep a separate watermark-store module (the old `CacheManager`)** — rejected: it fails the deletion test; it was a dict with persistence while the protocol logic lived in its callers, so bugs had no locality.
- **Record/replay HTTP fixtures (vcr-style) instead of a transport seam** — rejected: pins tests to captured traffic and hides the conditional-request state machine instead of exercising it.

## Consequences

- Freshness bugs, and the tests for them, concentrate in one module.
- The GitHub client carries no report- or freshness-level concerns; anything policy-shaped lives above the transport seam.
