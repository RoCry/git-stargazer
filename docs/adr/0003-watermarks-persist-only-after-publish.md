# Watermarks persist only after publish

During the 2026-07-30 → 2026-08-02 release outage (see ADR-0002), the workflow saved the watermark cache before the release step, so watermarks kept advancing while nothing was published — those days' commits can never appear in the feed. The cache-save steps (watermarks and report cache) now run after the release step. A failed publish rolls the run back: the next run restores the previous watermarks, refetches the unpublished commits, and includes them in that day's report. Publishing is at-least-once; do not move the save steps back above the release step.

## Considered Options

- **Save caches immediately after generation (old order)** — rejected: a publish failure silently and permanently drops commits from the feed.

## Consequences

- A failed publish costs duplicate GitHub API fetches on the next run; same-day merge and the empty-streak bound keep that cheap.
- The pages push runs last and is not part of the publish gate; a pages-only failure does not roll anything back.
