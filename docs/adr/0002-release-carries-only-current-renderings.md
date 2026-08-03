# Release carries only current renderings

The daily workflow uploaded two date-stamped report files per day to the single reused `latest` release. Nothing ever read them — the dated markdown duplicates the release body, and consumers only fetch the stable-named assets — but after ~16 months they hit GitHub's hard cap of 1000 assets per release, and every scheduled run from 2026-07-30 to 2026-08-02 failed at the upload step. The release now carries exactly three stable-named assets, overwritten in place each day: `recent_commits_latest.md`, `recent_commits_latest.json`, and `feed.json`. The asset count is constant, so the cap is structurally unreachable. Do not re-add date-stamped uploads. The subscriber-facing feed URL (`releases/download/latest/feed.json`) is unchanged; day-to-day history is what feed readers already retain.

## Considered Options

- **Keep dated assets, prune ones older than N days** — rejected: adds pruning machinery that can itself break, to preserve an archive nothing consumes.
- **Commit dated reports to a git branch** — rejected: grows the repo forever and complicates the currently-trivial pages publish; same no-consumer problem.

## Consequences

- No downloadable per-day archive exists anywhere; if one is ever wanted, revisit this ADR rather than uploading dated assets to the `latest` release again.
- The release body still shows the current day's report, renamed daily.
