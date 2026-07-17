# Git Stargazer

Watches the authenticated user's starred GitHub repositories and publishes a daily activity report.

## Language

**Starred repo**:
A GitHub repository the user has starred; the universe this tool watches.

**Freshness window**:
The trailing number of days (default 3) within which activity counts as recent.

**Active repo**:
A starred repo pushed within the freshness window.
_Avoid_: recent repo

**New commits**:
Human commits in a repo since its watermark (or since the freshness window on first sight). Bot commits never count.

**Watermark**:
The per-repo timestamp of the newest activity already reported; carried between runs.
_Avoid_: cache timestamp, commit timestamps cache

**Commit feed**:
The concept that answers "what is new in this repo since the last run"; owns watermarks and the freshness window.
_Avoid_: cache manager

**Selection**:
Choosing which starred repos to fetch this run: already-reported repos are excluded, a repo limit caps the rest.

**Empty streak**:
A run of consecutive fetched repos yielding no new commits; a long enough streak stops fetching, since starred repos arrive newest-updated first.
_Avoid_: empty repo limit

**Report**:
One day's structured record of active repos and their new commits.

**Same-day merge**:
Combining a re-run's report with the day's existing report; repos already in the day's report are not refetched.

**Summary**:
The one-line caption (one emoji + short title) describing a repo's new commits.

**Summarizer**:
The producer of summaries; may be disabled, in which case repos simply have no summary.
_Avoid_: LLM, AI (in interfaces and report vocabulary)

**Rendering**:
An artifact derived from the report: the Markdown page or the JSON Feed.
_Avoid_: RSS (the feed is JSON Feed)

**Topic group**:
A cluster of active repos sharing GitHub topics, used to organize the Markdown rendering.
