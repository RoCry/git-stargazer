# Recent Activity in Starred Repositories
_150 active repos with 2921 new commits_

## [125khz](https://github.com/topics/125khz), [iso14443a](https://github.com/topics/iso14443a), [mifare](https://github.com/topics/mifare), [nfc](https://github.com/topics/nfc), [rfid](https://github.com/topics/rfid), [simulate](https://github.com/topics/simulate)
- [RfidResearchGroup/proxmark3](https://github.com/RfidResearchGroup/proxmark3) [4](https://github.com/RfidResearchGroup/proxmark3/commits): tune docs for default port 18888
- [RfidResearchGroup/ChameleonUltra](https://github.com/RfidResearchGroup/ChameleonUltra) [2](https://github.com/RfidResearchGroup/ChameleonUltra/commits): Merge pull request #441 from triplesprawl/fix-missing-keys

fix: static and staticnested return well-formatted keys

## [ai](https://github.com/topics/ai)
- [openclaw/openclaw](https://github.com/openclaw/openclaw) [600](https://github.com/openclaw/openclaw/commits): refactor(macos): deslop macos (#163892)

Consolidate duplicate macOS request, configuration, runtime, voice, capture, and presentation code under existing owners, removing 1,002 net production lines while retaining every Native shell feature and window.

Fix session menu and preview caches retaining another Gateway's rows/history after primary replacement. Bind cached data and delayed reads to the owning Gateway lease while preserving cache reuse across reconnects. Add seven regression cases to the existing isolated Gateway socket fixture.

Preserve configuration keys, persisted data, protocol fields, visible UI, update recovery, and service authority. No SDK or dependency changes.
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) [487](https://github.com/NousResearch/hermes-agent/commits): fix(plugin-catalog): mark hermes-workflows' /tmp disclosure as deliberate

#131398 added a risk disclosure quoting the plugin's own /tmp handoff
file to the description, and the no-tmp lint (Python lints) went red on
main and on every PR's merge commit. The line documents third-party
behavior; dropping the path would weaken the disclosure, so it gets the
opt-out marker instead.
- [BasedHardware/omi](https://github.com/BasedHardware/omi) [180](https://github.com/BasedHardware/omi/commits): fix(stt): let only the serving owner fence recovery on a managed leg (#20393)

## What

`socket_is_finishing()` (`backend/utils/stt/resilient_stream.py`) no
longer descends into a managed leg's raw transport. For a managed
`LiveLegSocket` (it has `leg_outcome`), "is the session tearing down" is
decided only by `leg_outcome.owner_closing`. Unmanaged/legacy sockets
keep their `_finishing` latch. One regression test file.

## Why (prod)

Since #20343, `LiveLegSocket.send` calls `raw.finish()` as transport
cleanup after a rejected send. When a failover replays the capture ring
into Soniox and Soniox's 2,000-item send queue overflows
(`capacity_full`), that cleanup sets the raw Soniox `_finishing` latch.
`ListenReceiver._failover_stt_socket` and the Soniox reconnect path call
`socket_is_finishing()`, read the raw latch as client teardown, and
return without trying a successor — the session ends (`stt_live_session
… outcome=exhausted`, client closed). Independent review finding 2
reproduced it (owner_closing=False, raw finishing=True, backup
attempts=0). Listen logs at the evening peak show 6–11 sessions per 25
minutes lost this way, mostly `modulate→soniox` chains; on image
`0ba6edb` (before #20343) the same chains recovered.

This is the minimal hotfix for that regression. The queue overflow
itself (replay is a burst) and the long-term recovery design are in
#20391; this does not conflict with it in intent and #20391 will
supersede this code.

## Serving behaviour changes

| File:line | Old | New |
| --- | --- | --- |
| `backend/utils/stt/resilient_stream.py` `socket_is_finishing` | Any
`_finishing` on the managed wrapper or its raw transport blocked
recovery | Managed legs: only `leg_outcome.owner_closing` blocks
recovery; unmanaged sockets unchanged |

Effect: after a provider death caused by our own transport cleanup,
recovery tries the next capable provider again, as on `0ba6edb`.
Client-initiated teardown still sets `owner_closing` before flushing
(#20343/#20350), so it still blocks recovery.

## Tests

`tests/unit/test_recovery_fence_managed_leg.py` (4 cases) plus the
neighbouring suites `test_live_stt_resilient_stream.py`,
`test_stt_session_failover.py`, `test_live_evidence_settlement.py`,
`test_parakeet_failover_exhausted.py`: 110 passed locally.

## Product invariants affected

None.

Failure-Class: none

🤖 Generated with [Claude Code](https://claude.com/claude-code)


<!-- This is an auto-generated description by cubic. -->
<a
href="https://cubic.dev/pr/BasedHardware/omi/pull/20393?utm_source=github"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-light.svg"><img
alt="Review in cubic"
src="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"></picture></a>
<!-- End of auto-generated description by cubic. -->
- [kortix-ai/suna](https://github.com/kortix-ai/suna) [78](https://github.com/kortix-ai/suna/commits): feat(test): local test attestation gate (#8850)

## Problem
CI no longer runs the suite on `main` push. Nothing proves a PR head was
tested.

## Change
- `pnpm test` writes `tests/test-attestation.json`: `{source_hash, head,
passed, lanes, at}`.
- `source_hash` = sha256 of every file the commit would contain, minus
the attestation (no self-reference).
- Lanes: `core`, `packages`, `db-suites` (+ `browser` when run). Plain
`pnpm test` now also runs package quality (`packages`).
- `db-suites` (API/CLI flows + DB suites) records `skipped-no-db` when
Docker is absent. It is the only lane that may skip; never a pass.
  - Filtered or sharded runs write nothing.
- `pnpm test:verify` (`tests/verify-attestation.mjs`): exit 0 green, 1
missing/stale/red; `--strict` exits 3 on `skipped-no-db`; `--rev <sha>`
checks any commit without a checkout.
- `.githooks/pre-push` rejects a stale/red attestation on every branch
push (not deletions, tags, `scratch/*`); `main` also needs `--strict`.
- Fixes four db-suites that were red on `main`: port 5447 shared by two
migration suites, a fixture `id` with no default, and two RLS suites
that assumed a CI-image Postgres (`uid()` deparse, `postgres`
BYPASSRLS).
- Docs: AGENTS.md Default delivery (also: dev deploy is a deliberate
dispatch), testing and contributing skills.

## DB lanes without Docker
No clean in-sandbox Postgres: the lane needs GoTrue over HTTP, `docker
exec pg_dump` for the auth schema, and the migration-contract suites
start their own containers. Decision: record `skipped-no-db`; the merge
gate holds DB-touching PRs.

## Verified
Full `pnpm test` green on the final tree (core/packages/db-suites pass);
verify exit 0; fresh push accepted, stale push rejected by the hook;
skipped-no-db exits 0 / 3 with `--strict`. `--no-verify` skips client
hooks: the merge gate re-checks.

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/kortix-ai/codesmith/suna/pr/8850?autoLogin=true&ref=codesmith_pr_footer"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img
alt="View with [code]smith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a>
<a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1793581316&installation_model_id=434224&pr_number=8850&ref=codesmith_pr_footer&repository=kortix-ai%2Fsuna&return_to=https%3A%2F%2Fgithub.com%2Fkortix-ai%2Fsuna%2Fpull%2F8850&signature=a173d5635b072a1c5a172de47c06c7563bf38a45856d4fba4b1dd923bfce409a"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img
alt="Autofix with [code]smith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith-bot</code> with what you
need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->
- [unslothai/unsloth](https://github.com/unslothai/unsloth) [77](https://github.com/unslothai/unsloth/commits): Studio: make carried rows a faintly frosted, darker copy (#12562)

A carried sidebar chat, sidebar section header, or model picker Pinned row
now reads as a see-through pill a shade darker than its list in both
themes, with a faint blur and a fainter hairline. The section header copy
gets the same pill; it had no surface before.
- [Kiln-AI/Kiln](https://github.com/Kiln-AI/Kiln) [65](https://github.com/Kiln-AI/Kiln/commits): Merge pull request #1891 from Kiln-AI/dchiang/KIL-833/align-the-judge-title

chore: rename the judge review step to Align the Judge
- [langgenius/dify](https://github.com/langgenius/dify) [47](https://github.com/langgenius/dify/commits): test(api): stabilize shared fixtures and type-check scopes (#42801)
- [google/adk-python](https://github.com/google/adk-python) [41](https://github.com/google/adk-python/commits): refactor(workflow): decouple replay interceptor from _ToolNode and fix rehydration edge cases

- Remove `_ToolNode` import and `isinstance(node, _ToolNode)` checks from `_replay_interceptor.py` so all non-`wait_for_output` `rerun_on_resume` nodes share the same completion fast-forward behavior.
- Tighten `finished_after_resume` in `_rehydration_utils.py` so intermediate `function_call` / `function_response` events, `partial` streaming chunks, and failed events do not mark a node as finished.
- Clear stale `error_code` in `_rehydration_utils.py` when a subsequent non-partial, non-error direct event arrives on retry.
- Use `elif event.branch:` when matching interrupt responses in `_rehydration_utils.py` so a direct interrupt response on a sub-branch does not overwrite an ancestor interrupt whose ID matches a branch `run_id`.
- Fix `FunctionNode(auth_config=..., rerun_on_resume=True)` returning `None` being re-executed on subsequent downstream resumes.

Co-authored-by: Shangjie Chen <deanchen@google.com>
PiperOrigin-RevId: 992641129
- [t8y2/dbx](https://github.com/t8y2/dbx) [40](https://github.com/t8y2/dbx/commits): test(transfer): cover IRIS table-only capability

Refs: #10660
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) [35](https://github.com/screenpipe/screenpipe/commits): fix: preserve scroll checkpoints with adaptive capture frequency (#7335)

* fix(capture): preserve intermediate scroll positions

* fix(capture): bound Windows scroll and refresh focus

* fix(a11y): drive Windows title refresh timer

* fix(capture): settle Windows context pixels

* fix(capture): cover Windows close animations

* fix: keep blocking UI input waits off async workers

* fix: request fresh macOS pixels on surface transitions

* docs: describe enabled coalesced scroll capture in CLI help

* fix: refresh stored pixels after visual change detection

* fix: keep excluded pixels and stale elements out of checkpoints

* [autofix.ci] apply automated fixes

* fix: synchronize capture dependency across workspace lockfiles

* fix: reject incoherent Windows context captures

* fix: scope Windows context bookkeeping and refresh coverage

* fix(a11y): guard Windows click enrichment identity

* fix: retain only the scroll frame identity guard and scoped validation

* feat: add adaptive recording detail presets

* fix: keep adaptive scroll capture independent of text processing

* Settle macOS focus transitions before pairing pixels and text

* Record native scroll comparison and settings evidence

* Refresh pixels when focus changes ahead of a pending scroll capture

* Record passing native focus and scroll mode retry

---------

Co-authored-by: louis <louis@louiss-MacBook-Pro.local>
Co-authored-by: screenpipe automation <dev@screenpipe.com>
Co-authored-by: louis <louis@mac.local.meter>
Co-authored-by: autofix-ci[bot] <114827586+autofix-ci[bot]@users.noreply.github.com>
Co-authored-by: screenpipe worker <worker@screenpipe.local>
Co-authored-by: Ezra Ellette <ezrasellette@gmail.com>
- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) [29](https://github.com/QwenLM/qwen-code/commits): feat(managed-agent): Restore safe retired tool output collection (#13225)

* feat(managed-agent): Collect retired tool output safely

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

* chore(managed-agent): Sync retention formatting and verify collection

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

* codex: address PR review feedback (#13087)

* codex: address PR review feedback (#13087)

---------

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
Co-authored-by: Shaojin Wen <szujobs@gmail.com>
- [github/spec-kit](https://github.com/github/spec-kit) [9](https://github.com/github/spec-kit/commits): feat(mcp): add experimental version-only stdio server (#4822)

* feat(mcp): add experimental version server

Expose the stable version JSON command through an stdio-only MCP server with explicit discovery, subprocess isolation, structured errors, focused tests, and reference documentation.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix(mcp): declare schema dependency

Declare Pydantic as a direct runtime dependency and cover schema-invalid success and failure JSON payloads in the subprocess adapter tests.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix(mcp): validate child payloads strictly

Reject coercible machine-output types and cover invalid UTF-8 subprocess output as a sanitized adapter failure.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix(mcp): isolate worker module lookup

Launch the child CLI with Python safe-path mode so a project-local package cannot shadow the installed MCP worker, with a real cwd-shadow regression test.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix(mcp): preserve structured tool errors

Return explicit error CallToolResult values so MCP clients receive readable content and the unchanged structured CLI error payload, with in-memory and real stdio coverage.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* test(mcp): bound stdio integration reads

Add per-read and whole-test deadlines so a non-responsive MCP subprocess fails deterministically while context cleanup terminates the child.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

---------

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
- [herdrdev/herdr](https://github.com/herdrdev/herdr) [6](https://github.com/herdrdev/herdr/commits): fix: hidden pane memory and new pane spawn size (#4873)

* fix: stop hidden panes keeping a full-size screen copy from creation

* fix: start new panes at their laid-out size

refs #4419
- [docling-project/docling](https://github.com/docling-project/docling) [5](https://github.com/docling-project/docling/commits): feat(ocr): Allow configuring RapidOCR model size (#4500)

* feat(ocr): allow configuring RapidOCR model size

* DCO Remediation Commit for anupamkr1708 <anupraj1620@gmail.com>

I, anupamkr1708 <anupraj1620@gmail.com>, hereby add my Signed-off-by to this commit: 096ef7849c65581739df10440698792eb41ab65b

Signed-off-by: anupamkr1708 <anupraj1620@gmail.com>

* fix(html): reduce _handle_list complexity below the C901 threshold

Move the collection of <dt>/<dd> elements of a description list into a
helper, so ruff no longer fails on main after #4390.

Signed-off-by: Nikos Livathinos <nli@zurich.ibm.com>

---------

Signed-off-by: anupamkr1708 <anupraj1620@gmail.com>
Signed-off-by: Nikos Livathinos <nli@zurich.ibm.com>
Co-authored-by: anupamkr1708 <anupraj1620@gmail.com>
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) [3](https://github.com/openai/openai-agents-python/commits): fix(examples): render realtime tool events as text (#5283)
- [google/magika](https://github.com/google/magika) [2](https://github.com/google/magika/commits): Add unsupported file type (#1523)

Fixes #1482
- [lutzroeder/netron](https://github.com/lutzroeder/netron) [2](https://github.com/lutzroeder/netron/commits): Update to 9.3.1
- [pykeio/ort](https://github.com/pykeio/ort) [2](https://github.com/pykeio/ort/commits): refactor(operator): share the inplace and alias index list helpers (#660)

Signed-off-by: Onuralp SEZER <thunderbirdtr@gmail.com>
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) [1](https://github.com/google-gemini/gemini-cli/commits): fix(cli): ensure Enter and Spacebar reliably confirm selection list options (#29502)

Co-authored-by: David Pierce <davidapierce@google.com>
- [Source-Robotics/PAROL6-Desktop-robot-arm](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm) [1](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/commits): BOM update

## [ai-agent](https://github.com/topics/ai-agent)
- [trycua/cua](https://github.com/trycua/cua) [35](https://github.com/trycua/cua/commits): feat(spaces-macos): host setup that just works, your other Mac in Run on, and a built-in Lume (#4489)

* fix(spaces): host setup that survives retries, your other Mac in Run on, and a built-in Lume

- launchd: restart the host LaunchAgent idempotently (enable, wait for the
  bootout to finish, bootstrap with retries, kickstart when it is loaded
  after all) and fail in plain words instead of the raw launchctl line.
- Retry on This machine reruns the failed button; a change or Resume
  sharing starts a host service that is down.
- Permissions: ask the driver itself (disclaimed child) on every status, so
  a grant shows without a restart and only what is missing is listed.
- Run on: list your offline Macs set up for Spaces (relay meta), start on
  your other Mac when This Mac cannot run the image, one-line hints, and
  fix the menu's blank label when a machine is chosen (Sections, not
  Dividers).
- Built-in Lume: a pinned, signed, checksum-verified Lume 0.6.0 downloaded
  into $CUA_HOME/runtimes on the first macOS create (progress inline on the
  Space), with Settings, Runtimes (Automatic, Built-in, System) and
  `runtime.lume`; Remove host setup deletes it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Hv7NU2xZDx8fqykTXiaDuj

* style: format the built-in Lume test

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Hv7NU2xZDx8fqykTXiaDuj

* build: lockfiles for cua-vmm's toml_edit

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Hv7NU2xZDx8fqykTXiaDuj

* docs: regenerate the SDK and Rust references

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Hv7NU2xZDx8fqykTXiaDuj

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) [20](https://github.com/CherryHQ/cherry-studio/commits): ci(validation): report comparable CI performance metrics (#21234)

<!-- Template from
https://github.com/kubevirt/kubevirt/blob/main/.github/PULL_REQUEST_TEMPLATE.md?-->
<!--  Thanks for sending a pull request!  Here are some tips for you:
1. Consider creating this PR as draft:
https://github.com/CherryHQ/cherry-studio/blob/main/CONTRIBUTING.md
-->

> ### Branch strategy
>
> - Active development targets `main`.

### What this PR does

Before this PR: CI had no persistent performance report or comparable
baseline; elapsed time and parallel runner consumption were easy to
conflate.

After this PR: A non-blocking observer reads completed CI job/step
timestamps and publishes a summary plus a 30-day JSON artifact. It
separates initial queue, execution wall time and summed runner time, and
reports P50/P90 only from successful runs matching task scope, runner
labels and known cache state. Unknown cache contexts and old workflows
receive no baseline; reruns omit misleading queue/total elapsed values.

<!-- (optional, in `fixes #<issue number>(, fixes #<issue_number>, ...)`
format, will close the issue(s) when PR gets merged)*: -->

None.

### Why we need it and why it was done in this way

The following tradeoffs were made: Observe existing runs without
repeating tests or adding a performance threshold. Limit history to the
latest 20 successful runs of the same workflow/event. The observer uses
read-only permissions and trusted default-branch code; it becomes active
after merge to main.

The following alternatives were considered: Blocking PRs on raw elapsed
time would conflate workload, cache and runner variation. Controlled
repeated benchmarks and local multi-agent contention benchmarks remain
separate.

Links to places where the discussion took place: [CI and local
validation
proposal](https://github.com/CherryHQ/cherry-studio/blob/ci/validation-metrics/.agents/notes/proposed/process/2026-10-01-ci-and-local-validation.md).

### Breaking changes

<!-- optional -->

None. Existing required checks are unchanged.

### Special notes for your reviewer

Stack 4/4; base: ci/validation-workflow. Validation: 37
planner/workflow/metrics tests passed, plus node typecheck, full lint,
docs, formatting and actionlint. The collector produced a report from
real historical CI run 36740426367. The workflow_run observer cannot run
automatically until it reaches the default branch; no speedup claim is
made. Existing ESLint warnings remain non-blocking.

### Checklist

This checklist is not enforcing, but it's a reminder of items that could
be relevant to every PR.
Approvers are expected to review this list.

- [ ] Branch: This PR targets `main`
- [x] PR: The PR description is expressive enough and will help future
contributors
- [x] Code: [Write code that humans can
understand](https://en.wikiquote.org/wiki/Martin_Fowler#code-for-humans)
and [Keep it simple](https://en.wikipedia.org/wiki/KISS_principle)
- [ ] Refactor: You have [left the code cleaner than you found it (Boy
Scout
Rule)](https://learning.oreilly.com/library/view/97-things-every/9780596809515/ch08.html)
- [ ] Upgrade: Impact of this change on upgrade flows was considered and
addressed if required
- [ ] Documentation: A [user-guide update](https://docs.cherry-ai.com)
was considered and is present (link) or not required. Check this only
when the PR introduces or changes a user-facing feature or behavior.
- [x] Self-review: I have reviewed my own code (e.g., via
[`/gh-pr-review`](/.claude/skills/gh-pr-review/SKILL.md), `gh pr diff`,
or GitHub UI) before requesting review from others

### Release note

<!--  Write your release note:
1. Enter your extended release note in the below block. If the PR
requires additional action from users switching to the new release,
include the string "action required".
2. If no release note is required, just write "NONE".
3. Only include user-facing changes (new features, bug fixes visible to
users, UI changes, behavior changes). For CI, maintenance, internal
refactoring, build tooling, or other non-user-facing work, write "NONE".
-->

```release-note
NONE
```

---------

Signed-off-by: suyao <sy20010504@gmail.com>

## [ai-agents](https://github.com/topics/ai-agents)
- [droidrun/mobilerun](https://github.com/droidrun/mobilerun) [15](https://github.com/droidrun/mobilerun/commits): Merge pull request #473 from droidrun/develop

chore: merge develop into main for 0.6.21
- [steipete/agent-scripts](https://github.com/steipete/agent-scripts) [3](https://github.com/steipete/agent-scripts/commits): docs(codex-first): keep ultrafast opt-in

## [c](https://github.com/topics/c)
- [libvips/libvips](https://github.com/libvips/libvips) [2](https://github.com/libvips/libvips/commits): thumbnail: pass missing `fail_on` arg to loaders (#5235)

Resolves: #5195.
- [qmk/qmk_firmware](https://github.com/qmk/qmk_firmware) [1](https://github.com/qmk/qmk_firmware/commits): Add support for mini_mighty/kbd (#25878)

* Add keyboard mini_mighty_kbd.

* Update keyboards/mini_mighty/kbd/keymaps/default/keymap.c

Co-authored-by: Jack Sangdahl <jack@pngu.org>

* Update keyboards/mini_mighty/kbd/keymaps/default/keymap.c

Co-authored-by: Jack Sangdahl <jack@pngu.org>

* Update keyboards/mini_mighty/kbd/keymaps/default/keymap.c

Co-authored-by: Jack Sangdahl <jack@pngu.org>

* Update keyboards/mini_mighty/kbd/keyboard.json

Co-authored-by: Jack Sangdahl <jack@pngu.org>

* Migrated features/build options from rules.mk to keyboard.json

* Update keyboards/mini_mighty/kbd/keymaps/default/keymap.c

Co-authored-by: Drashna Jaelre <drashna@live.com>

* Added a new layout with swapped backspace and backslash as default. Renamed the old layout as "legacy".

* Removed the "legacy" layout as it's no longer needed. All shipped mini-mighty-kbd units use the default layout.

* Updated the readme build instructions to use QMK compile instead of make.

---------

Co-authored-by: Jack Sangdahl <jack@pngu.org>
Co-authored-by: Drashna Jaelre <drashna@live.com>

## [claude-code](https://github.com/topics/claude-code)
- [slopus/happy](https://github.com/slopus/happy) [12](https://github.com/slopus/happy/commits): Add explicit Google Play production submission profile
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) [2](https://github.com/Piebald-AI/claude-code-system-prompts/commits): Update changelog for v2.1.288

## [cross-platform](https://github.com/topics/cross-platform)
- [xyproto/algernon](https://github.com/xyproto/algernon) [13](https://github.com/xyproto/algernon/commits): Add plans
- [cjpais/Handy](https://github.com/cjpais/Handy) [3](https://github.com/cjpais/Handy/commits): add chinese script selector + simplify internals (#2186)
- [Snapchat/Valdi](https://github.com/Snapchat/Valdi) [1](https://github.com/Snapchat/Valdi/commits): Closes https://github.com/Snapchat/Valdi/pull/190

GitOrigin-RevId: db4cb27d007d0708e436cbdc54c6e0b736860e0c

## [embedded](https://github.com/topics/embedded)
- [hathach/tinyusb](https://github.com/hathach/tinyusb) [3](https://github.com/hathach/tinyusb/commits): ci: use Arm GNU toolchain from Arm's GitLab instead of xpack (#4080)

Arm's official build is half the download, and as a non-GitHub URL setup_toolchain caches it. It is also the build developers install, so local code-size results match CI's.
- [stlink-org/stlink](https://github.com/stlink-org/stlink) [3](https://github.com/stlink-org/stlink/commits): Merge pull request #1506 from stlink-org/fix/g0_g4

Fixes for flashing G0/G4 devices
- [linux-msm/qdl](https://github.com/linux-msm/qdl) [2](https://github.com/linux-msm/qdl/commits): Merge pull request #323 from igoropaniuk/refactor/flash-cli

qdl: split the flashing front-end from the CLI plumbing

## [esp32](https://github.com/topics/esp32)
- [esphome/esphome](https://github.com/esphome/esphome) [55](https://github.com/esphome/esphome/commits): [qmi8658] Pin motion_id in test config to fix grouped component test conflict (#20075)
- [rmk-rs/rmk](https://github.com/rmk-rs/rmk) [10](https://github.com/rmk-rs/rmk/commits): Merge pull request #1176 from rmk-rs/codex/fix-1138-layout-whitespace

fix(config): accept repeated whitespace in layout maps
- [crosspoint-reader/crosspoint-reader](https://github.com/crosspoint-reader/crosspoint-reader) [5](https://github.com/crosspoint-reader/crosspoint-reader/commits): fix: keep SD-font kerning and ligatures in edge cases (#3838)

## Summary

* **What is the goal of this PR?**
Fix five bugs in `SdCardFont`'s per-page kern matrix and ligatures. Each
has a host test that fails on develop. This is bugfixes separated from
PR #3831 to keep PR small and reviewable.

* **What changes are included?** One commit in
`lib/EpdFont/SdCardFont.{h,cpp}`:

1. **Kerning lost after a request is served from glyphs cached without
kerning.** A kern-wanting prewarm whose
glyphs are all cached by a kern-free prewarm (UI strings) tops up the
kern matrix without re-reading glyphs. It
built the matrix for the request only, and decided whether to build from
`miniKernLeftClassCount == 0`. Once a
top-up found pairs, later requests whose pairs it missed skipped the
build and drew unkerned. Example: cache
`ABCDEF` without kerning, then request `AB` and then `CD`; `C`–`D`
returns 0 instead of −5.
- The top-up now covers every cached glyph, and a `miniKernBuilt` flag
records that coverage. A full rebuild
sets it from its own kern build, and freeing the mini kern clears it.
- If the cached-glyph list cannot be allocated, the top-up covers the
request only, logs the failure, and leaves
       the flag unset so the next request builds again.
2. **Class IDs past the matrix read outside the row buffer.** A class ID
above the font's class count indexed past
the `kernRightClassCount`-byte row buffer (heap read past the allocation
under ASan) and seeked to a row past
the matrix. Such entries are now treated as unkerned when the class
tables load. Fonts are user-supplied files.
3. **The matrix loops never ended with 255 classes.**
`numLeft`/`numRight` and the loop counters were `uint8_t`, so
`newL <= numLeft` stayed true when a page used all 255 classes. The
counters are now `uint16_t`.
4. **A failed mini kern build dropped the page's ligatures.** The kern
and ligature pointers were applied together
only when the build succeeded. They are now applied whenever the tables
loaded; a failed build leaves the mini
     kern empty, so the page keeps its ligatures and kerns as none.
5. **Fonts without kern classes lost ligatures on the same cached-glyph
path.** The top-up in (1) is also what
attaches the ligature table, and it only ran when the font had kern
classes. A font with ligatures but no kern
classes drew those requests without ligatures. It now runs for every
font; without kern classes the matrix build
     returns at once and reads nothing.

Normal page prewarms are unchanged: a full rebuild still builds the
matrix for the page's codepoints, and the
  number of mini kern builds per boot is the same.

## Scope Check

- [x] I have read SCOPE.md and ROADMAP.md.
- [x] This PR is **not** a new built-in theme.
- [x] This PR is **not** a new external network connector.
- [x] This PR is **not** an interactive app, writing tool,
RSS/news/browser, media playback, or PDF feature.
- [x] The stock firmware does not already handle this well, **and** no
other popular CrossPoint fork already does.
      (Not audited; this is a bug fix in the SD-font cache.)
- [x] If this PR touches `freeink-sdk/`, `lib/hal/`, the bootloader,
OTA, or recovery code, I have coordinated with
      the relevant maintainer. (It touches none of them.)

#3831 builds on this PR and carries the same fixes into its rewrite of
the kern path.

## Additional Context

### Tests

`SdCardFontTest` gains a small kerning fixture (six Latin glyphs,
configurable class tables, an optional ligature)
and seven cases. On develop:

| Test | develop | This PR |
|---|---|---|
| `KernRequestsServedFromAKernFreeMiniStillKern` (bug 1) | fails:
`C`–`D` returns 0 | passes |
| `ClassIdsPastTheMatrixAreUnkerned` (bug 2) | ASan heap-buffer-overflow
in `buildMiniKernMatrix` | passes |
| `PagesCanUseAll255KernClasses` (bug 3) | aborts (UBSan, the loop
wraps) | passes |
| `AFailedKernBuildKeepsTheLigatures` (bug 4) | fails: no ligature |
passes |
| `LigatureRequestsServedFromAKernFreeMiniGetLigatures` (bug 5) | fails:
no ligature | passes |
| `PagesKernWithTheFontsClassMatrix`,
`RedrawsAfterAKernFreeRebuildStillKern` | pass | pass |

The last two guard the normal path and the new flag after a kern-free
rebuild.

### Device check

X3, `develop` `813aaa12` vs this PR, both with identical #3510
serial-control instrumentation, `default` env
(LOG_LEVEL=2), Pretendard 16. Three interleaved cold pairs per book,
same protocol as #3831 (cold open, 6 + 6 page
turns, 40 turns of background layout, chapter restore, Home).

| | Korean: develop | PR | Change | English: develop | PR | Change |
|---|---:|---:|---:|---:|---:|---:|
| Total page render (median) | 1,279.5 ms | 1,278.5 ms | −0.5 ms
(matched) | 1,146.5 ms | 1,144 ms | −0.5 ms (matched) |
| Font preparation (`prewarm`) | 117 ms | 116.5 ms | −0.5 ms | 32 ms |
32 ms | 0 |
| Mini kern builds per boot | 57 | 57 | 0 | 68 | 68 | 0 |
| Since-boot Min Free | 19,688 B | 19,688 B | 0 | 31,276 B | 31,276 B |
0 |
| Largest block in layout samples: min / median | 15,348 / 34,804 B |
15,348 / 34,804 B | 0 / 0 | 49,140 / 57,332 B | 49,140 / 57,332 B | 0 /
0 |
| Post-page sample: free / largest block | 71,640 / 59,380 B | 71,640 /
59,380 B | 0 / 0 | 74,016 / 61,428 B | 74,016 / 61,428 B | 0 / 0 |
| Home after exit: free / largest block | 111,740 / 98,292 B | 111,740 /
98,292 B | 0 / 0 | 112,680 / 65,524 B | 112,680 / 65,524 B | 0 / 0 |

All page landings match, and all 18 paired captures are identical in the
reading area (the full-frame differences
are in the battery footer). The fixed paths do not run in this workload,
so heap and timing are unchanged. These
runs used the commit before fix 5 was added; Pretendard has kern
classes, so fix 5 does not change its path.

* Memory / flash impact: static RAM unchanged. Flash +294 B (plain
`default` builds). The cached-glyph list is a
temporary allocation of up to 2 KB (`miniGlyphCount` × 4 B, at most 512
glyphs) during a kern top-up only.

### Verification

- `pio run -e default` passes. Formatted with `./bin/clang-format-fix
-g`.
- Host tests: 431/431 pass. The SD-font tests also pass under
ASan/UBSan.

---

### AI Usage

Did you use AI tools to help write this code? _**YES**_ — AI tools
assisted with the code review that found these
bugs, the fixes, testing, and this description.
- [arendst/Tasmota](https://github.com/arendst/Tasmota) [4](https://github.com/arendst/Tasmota/commits): Berry: safely collect partially constructed native closures (#25093)

* Berry: safely collect partially constructed native closures

* Update be_func.py

---------

Co-authored-by: s-hadinger <49731213+s-hadinger@users.noreply.github.com>
- [rzeldent/esp32-smartdisplay](https://github.com/rzeldent/esp32-smartdisplay) [2](https://github.com/rzeldent/esp32-smartdisplay/commits): Modified boards
- [1technophile/OpenMQTTGateway](https://github.com/1technophile/OpenMQTTGateway) [1](https://github.com/1technophile/OpenMQTTGateway/commits): [BOARD] Add ISNO Super build environment (ESP32-S3, dual CC1101 433 + 868/915 MHz) (#2378)

The ISNO Super is an open-hardware ESP32-S3 board carrying two CC1101
sub-GHz radios (433 MHz and 868/915 MHz) combined on a single antenna
through a passive LC diplexer. This environment builds on the
esp32dev-multi_receiver RF stack; it drives the 868/915 MHz radio (868
in the EU, 915 in the US) and parks the 433 MHz one using the existing
RF_MODULE_SECONDARY_CS hook in commonRF.cpp.

Signed-off-by: Olivier Delafosse <olshad@gmail.com>
- [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) [1](https://github.com/78/xiaozhi-esp32/commits): feat(lilygo): add T-Circle-S3 V1.1 board (#2286)

The T-Circle-S3 V1.1 revision differs from V1.0 only in the microphone: V1.0
uses an MSM261S4030H0R on standard I2S (BCLK 7, WS 9, DATA 8), V1.1 an
MP34DT05-A on PDM (CLK 9, DATA 8). Everything else - display, touch, speaker,
LEDs - is identical.

A PDM microphone cannot be read by an I2S standard-mode receiver, so V1.1
hardware captures nothing on the existing board and the wake word never
triggers. Board identity affects OTA compatibility, so this is a new board
rather than a change to the existing one.

Capture runs at 32 kHz rather than the 16 kHz the wake-word engine uses. The
ESP32-S3 derives the PDM clock as 64x the sample rate, so 16 kHz would give
only ~1.02 MHz, below the MP34DT05-A minimum, where the microphone stays in
power-down and its data line reads as a constant - indistinguishable from
absent hardware. 32 kHz gives ~2.05 MHz and the audio service resamples down
to 16 kHz for the detector.

The board uses the shared NoAudioCodecSimplexPdm codec, with a thin subclass
driving the MAX98357A SD_MODE pin (GPIO45) alongside the output channel.

Tested on physical V1.1 hardware: Wi-Fi provisioning, device activation, MQTT
session, wake word, microphone capture, speaker playback, display and touch.
A multi-turn conversation was run with the device speaking several long
responses - no false wake-word triggers, no self-transcription, no spurious
state transitions. Device-side AEC cannot engage without a playback reference
channel, which this hardware does not provide; server-side AEC is unaffected.

No existing board is modified.

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
- [espressif/arduino-esp32](https://github.com/espressif/arduino-esp32) [1](https://github.com/espressif/arduino-esp32/commits): ci(wokwi): Require wokwi-client with WOKWI_CLI_SERVER fix (#12964)
- [espressif/idf-extra-components](https://github.com/espressif/idf-extra-components) [1](https://github.com/espressif/idf-extra-components/commits): Merge pull request #838 from espressif/feat/esp_ext_part_tables_v1.0.0

feat(esp_ext_part_tables): Release stable v1.0.0 version
- [JasonYANG170/AIOT-Phone](https://github.com/JasonYANG170/AIOT-Phone) [1](https://github.com/JasonYANG170/AIOT-Phone/commits): docs: add bilingual READMEs and language navigation

## [extension](https://github.com/topics/extension)
- [brookhong/Surfingkeys](https://github.com/brookhong/Surfingkeys) [2](https://github.com/brookhong/Surfingkeys/commits): feat(llm): chat as a named agent out of settings.llmAgents

`/agents <name>` switches the chat's system prompt to one the user defined,
keeping the conversation, and the choice belongs to the site and is stored
beside it -- a site you asked a translator about answers as the translator when
you come back to it. `extra: {agent: "translator"}` opens straight into one.

`extra.system` is gone, since an inline prompt in a mapping was a choice the
chat could neither name nor remember; a script still passing one is told so.
The `/` completion now lists what each command does, which is why CursorPrompt
takes a candidate whose searchable part is only the name.
- [fishjar/kiss-translator](https://github.com/fishjar/kiss-translator) [1](https://github.com/fishjar/kiss-translator/commits): feat(webui): 跨浏览器一致的 textarea 拉伸手柄、内置样式选择与会话高度锁定 (#1137)

* ✨ feat(webui): 实现跨浏览器一致的 textarea 自定义缩放手柄

- 【新增】创建 TextareaResizeGrip 组件，提供拖拽与键盘调整高度的统一交互体验
- 【新增】开发 useTextareaHeightLock 钩子，在 InputBase root 上锁定高度，避免与 autosize 竞态

🌐 i18n(i18n): 添加手柄无障碍标签多语言支持

- 【国际化】为 field_resize_height 添加 zh/en/zh_TW/ja/ko/tr/vi 多语言文案
- 【国际化】更新俄语 i18n 资源

♻️ refactor(styles): 替换原生 resizer 样式并实现高度锁定机制

- 【重构】移除 ::-webkit-resizer 渐变斜纹样式，避免与新手柄视觉冲突
- 【重构】新增 kt-height-locked CSS 规则，使用 !important 压制 textarea 行高写高

✅ test(tests): 补充手柄与高度锁定功能测试

- 【测试】为 TextareaResizeGrip 和 useTextareaHeightLock 添加完整单元测试
- 【测试】更新相关组件测试以适配 resize:none 与内容门控渲染逻辑

* ✨ feat(webui): 实现输入框拉伸手柄样式自定义功能

- 【新增】添加14种自定义手柄样式，包括双同心弧、三同心弧、角部圆胶囊等
- 【新增】新增设置页面手柄样式选择器，支持实时预览与样式切换
- 【新增】实现手柄样式与高度锁定联动，隐藏样式时自动释放高度锁定
- 【新增】支持多语言界面下的手柄样式文本本地化
- 【重构】优化手柄组件渲染逻辑，提升跨浏览器一致性
- 【重构】改进高度锁定机制，解决React重渲染导致的锁定状态丢失问题
- 【性能】优化手柄样式解析逻辑，减少不必要的样式计算
- 【测试】完善手柄组件测试用例，覆盖所有样式变体与交互场景

* ♻️ refactor(webui): 优化锁定态文本区域最小高度计算逻辑

- 【重构】定义锁定态最小目标高度常量（64px），通过叠加热区内边距实现
- 【重构】更新钳制函数，统一使用新常量作为锁定态下限
- 【测试】更新视图组件测试用例，验证锁定高度从40px调整为64px

* ✨ feat(webui): 完善 textarea 缩放手柄 ARIA 区间自洽性与样式配置派生

- 【新增】将 ARIA 播报下界随锁定态取同一钳制托底：锁定态（value 为有限数）真实可调下界为 LOCKED_MIN_TARGET_HEIGHT_PX（64px），未锁定回落路径才是 MIN_TARGET_HEIGHT_PX（40px）；valuemin/valuemax/valuenow 三者构成自洽区间，valuenow 落在 [valuemin, valuemax]
- 【新增】扩展 aria-keyshortcuts 完整播报键盘契约：ArrowUp/Down 调整 + Escape 显式解锁（与双击等价），辅助技术经该属性获知全部键盘入口
- 【新增】样式选项改由 TEXTAREA_GRIP_STYLE_KEYS 单一事实源派生，移除 JSX 内联硬编码选项与对应 i18n 键字面量，降低维护成本
- 【新增】窗口模式 textarea CSS 增加 height:auto !important 中和 TextareaAutosize 写入的内联高度，使 flex:1 + align-items:stretch 拉伸在未锁定短文本窗口态生效；resize/overflow 仍归 TranCont 内联样式全态接管
- 【修复】释放判据改用原文（text）而非译文（trText）：新请求发起时 trText 先被清空，若监听 trText 会在重译同一原文时误删会话高度记忆；仅原文清空才彻底解锁
- 【测试】新增 ARIA 下界契约测试：锁定态 valuemin=64、valuemax≥64、valuenow 落在 [valuemin, valuemax]；未锁定态 valuemin=40
- 【测试】更新病态视口护栏测试：innerHeight 低于锁定下界（64px）时 ARIA 区间仍自洽，三者同落 64px
- 【测试】新增重译同一原文会话高度记忆测试：新请求内部 setTrText("") 只是中间态，释放判据须跟原文走，记忆必须存活
- 【测试】更新样式设置页面测试：以渲染面取代源码正则提取，验证下拉选项 value 集合与单一事实源恒等、顺序一致
- 【测试】更新样式设置 i18n 键对账测试：正则提取器已无提取对象，活性自检失去意义，改为渲染面断言
- 【测试】更新 Popup CSS 规则测试：height 唯一合法形态为中和 TextareaAutosize 的 auto !important，固定像素/计算值高度与 resize 覆盖仍一律禁止

* ✨ feat(webui): 统一 textarea 缩放手柄 ARIA 播报下界钳制口径

- 【新增】ARIA 播报下界恒取钳制托底 LOCKED_MIN_TARGET_HEIGHT_PX（64px），三条可调路径（clampHeight/pointermove/clampGripMemoryHeight→applyHeight）不区分锁定态一律托底 64，未锁定回落播报 40 即失实
- 【新增】valuetext 与 valuenow 同源同钳，读屏播报口径一致；valuenow 按有效上界钳制，保证 [valuemin, valuemax] 自洽
- 【新增】锁定态覆盖规则以更高特异度（3 class + :not([attr]) + 元素）显式钉回 100%，与注入顺序解耦，避免长译文溢出固定高度滚动失效
- 【修复】释放判据改用原文（text）而非译文（trText）：新请求发起时 trText 先被清空，若监听 trText 会在重译同一原文时误删会话高度记忆
- 【测试】锁定态 valuemin=64、valuemax≥64、valuenow 落在 [valuemin, valuemax]；未锁定态valuemin=64
- 【测试】新增重译同一原文会话高度记忆测试：新请求内部 setTrText("") 只是中间态，释放判据须跟原文走，记忆必须存活
- 【测试】更新样式设置页面测试：以渲染面取代源码正则提取，验证下拉选项 value 集合与单一事实源恒等、顺序一致
- 【测试】更新样式设置 i18n 键对账测试：正则提取器已无提取对象，活性自检失去意义，改为渲染面断言
- 【测试】更新 Popup CSS 规则测试：height 唯一合法形态为中和 TextareaAutosize 的 auto !important，固定像素/计算值高度与 resize 覆盖仍一律禁止

* ✨ feat(webui): 区分锁定态与未锁定态的 textarea 缩放手柄 ARIA 播报下界口径

- 【新增】锁定态 aria-valuemin 取 LOCKED_MIN_TARGET_HEIGHT_PX（64，经手柄可达的最小高度），未锁定态取 MIN_TARGET_HEIGHT_PX（40，补测回落值的托底下界），使短字段实测高度不再被托高播报
- 【新增】未锁定态 aria-valuenow 逐字播报补测回落实测值（fallbackHeight），不再被锁定下界 64 托底，保证读屏播报真实高度
- 【新增】valuetext 与 valuenow 同源同钳，读屏播报口径一致；valuenow 按有效上界钳制，保证 [valuemin, valuemax] 自洽
- 【新增】锁定态覆盖规则以更高特异度（3 class + :not([attr]) + 元素）显式钉回 100%，与注入顺序解耦，避免长译文溢出固定高度滚动失效
- 【修复】释放判据改用原文（text）而非译文（trText）：新请求发起时 trText 先被清空，若监听 trText 会在重译同一原文时误删会话高度记忆
- 【测试】锁定态 valuemin=64、valuemax≥64、valuenow 落在 [valuemin, valuemax]；未锁定态 valuemin=40、valuenow 逐字等于实测值
- 【测试】新增未锁定短字段播报测试：实测高度 47 时 aria-valuenow 逐字为 47，不再被托高到 64
- 【测试】新增锁定态越界防御测试：锁定值 47 仍按 [64, valuemax] 钳制播报为 64，防 prop 直传越界回归
- 【测试】更新样式设置页面测试：以渲染面取代源码正则提取，验证下拉选项 value 集合与单一事实源恒等、顺序一致
- 【测试】更新样式设置 i18n 键对账测试：正则提取器已无提取对象，活性自检失去意义，改为渲染面断言
- 【测试】更新 Popup CSS 规则测试：height 唯一合法形态为中和 TextareaAutosize 的 auto !important，固定像素/计算值高度与 resize 覆盖仍一律禁止

* ✨ feat(webui): 区分锁定态与未锁定态的 textarea 缩放手柄收缩 no-op 守卫

- 【新增】拖拽收缩守卫：会话起点低于锁定下限时，目标仍低于下限的移动为 no-op，避免锁定路径反向抬高导致高度与 slider 播报同步跳变
- 【新增】键盘箭头键收缩守卫：未锁定且当前高度低于锁定下限时，向上箭头收缩请求为 no-op，增高请求与自 ≥64 基线的减高不受影响
- 【测试】新增未锁定短字段收缩 no-op 测试，验证减高键不得经锁定路径反向抬到 64
- 【测试】新增增高与自 ≥64 基线减高测试，确认增高键与基线减高仍走锁定路径
- 【测试】新增拖拽收缩守卫边界测试，验证目标恰达 64 时恢复锁定路径

## [free](https://github.com/topics/free)
- [public-apis/public-apis](https://github.com/public-apis/public-apis) [32](https://github.com/public-apis/public-apis/commits): Merge pull request #7613 from locio-au318/add-chargealong

Add ChargeAlong API
- [gibbok/typescript-book](https://github.com/gibbok/typescript-book) [1](https://github.com/gibbok/typescript-book/commits): Improve Brazilian Portuguese translation and align TypeScript examples (#268)

* Improve Brazilian Portuguese translation accuracy and terminology

* Align pt-BR code snippets with English source and retain Portuguese comments

* Polish pt-BR terminology and technical comments after review

* Refine three pt-BR type-inference comments

* Update website

* books

## [go](https://github.com/topics/go), [golang](https://github.com/topics/golang)
- [wader/fq](https://github.com/wader/fq) [3](https://github.com/wader/fq/commits): Merge pull request #1406 from wader/bump-gomod-gopacket-1.7.3

Update gomod-gopacket to 1.7.3 from 1.7.2
- [d2lang/d2](https://github.com/d2lang/d2) [2](https://github.com/d2lang/d2/commits): Update MathJax-Go to the latest merged parity fixes

Update MathJax-Go to the latest merged parity fixes. Local and hosted checks passed at the tested commit.

- sent from alixander's Codex

## [html](https://github.com/topics/html), [css](https://github.com/topics/css)
- [rushter/selectolax](https://github.com/rushter/selectolax) [16](https://github.com/rushter/selectolax/commits): Fix `attrs` reading freed memory when it outlives its node
- [tdewolff/minify](https://github.com/tdewolff/minify) [4](https://github.com/tdewolff/minify/commits): Merge pull request #1042 from tdewolff/dependabot/github_actions/pypa/cibuildwheel-4.2.1

Bump pypa/cibuildwheel from 4.2.0 to 4.2.1

## [ios](https://github.com/topics/ios)
- [fastlane/fastlane](https://github.com/fastlane/fastlane) [9](https://github.com/fastlane/fastlane/commits): [internal] Derive which cops the plugin template's RuboCop config drops (#30337)

prepare_rubocop_config listed fastlane's own cops by hand, so a new cop in internal/rubocop broke `fastlane new_plugin`'s rubocop until it was added there, and plugin_generator_spec only reported `expected 0, got 2`. The list is now derived from the cops the internal requires define, checked by a dedicated spec, and the plugin spec prints RuboCop's output on failure. The generated file is byte-identical.
- [supabase/supabase-swift](https://github.com/supabase/supabase-swift) [7](https://github.com/supabase/supabase-swift/commits): chore(android): cross-compile and test the SDK on Android (#1415)

First step toward Android support. Cross-compiles the whole SDK and its unit
tests for Android and runs them on an emulator. 1273 tests pass on API 35 /
arm64-v8a; the macOS suite is unchanged at 1411.

Two portability fixes were needed:

- Android's Foundation does not vend `POSIXErrorCode`. The WebSocket close
  mapping now matches on the platform's own `ENOTCONN`/`EPROTO` constants,
  which are in scope everywhere and keep the Darwin-vs-Linux errno
  difference the original change was for.
- ConcurrencyExtras only implements `withMainSerialExecutor` where it can
  swap the runtime's global executor hook, which rules out Android. The
  existing Windows passthrough is generalised to cover both, and gains the
  async overload the call sites actually use.

Five Realtime tests drive a `TestClock` and rely on that serial executor to
know the task they are waking already reached its `sleep`. With a
passthrough they race: three hang, two observe a half-finished sequence.
They are skipped on Android and Windows through one condition trait rather
than five scattered `#if`s, and still run everywhere else.

Notably `URLOpener.live` compiles to an empty closure on Android, so
`signInWithOAuth` would hang, and there is no default `AuthLocalStorage`.
Full platform support — a CI job, a dynamic library product for JNI
consumption, and closing those gaps — is follow-up work.

## [keyboard](https://github.com/topics/keyboard)
- [duckyb/urchin](https://github.com/duckyb/urchin) [2](https://github.com/duckyb/urchin/commits): Merge pull request #26 from Jadefalkner/tenting-bottom-by-jadefalkner

Add tenting bottom case with TOTEM feet
- [joe-scotto/scottokeebs](https://github.com/joe-scotto/scottokeebs) [1](https://github.com/joe-scotto/scottokeebs/commits): Add RHYPR keys for window arrangement

## [llm](https://github.com/topics/llm)
- [jundot/omlx](https://github.com/jundot/omlx) [32](https://github.com/jundot/omlx/commits): fix(engine_pool): start idle timers at lease completion (#4125)

* fix(engine_pool): start idle timers at lease completion

* test: move idle completion tests into existing modules

---------

Co-authored-by: jundot <jundot@users.noreply.github.com>
- [cactus-compute/needle](https://github.com/cactus-compute/needle) [3](https://github.com/cactus-compute/needle/commits): refactor: remove unnecessary comments in test_compare_runs_a_file for clarity

## [machine-learning](https://github.com/topics/machine-learning)
- [stefan-jansen/machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) [5](https://github.com/stefan-jansen/machine-learning-for-trading/commits): Present the notebooks' design decisions without the repair history (#1141)

Thirty-two notebooks explained a choice by narrating what an earlier version of
the same notebook did wrong: "an earlier version of this notebook fixed a
reporting checkpoint in advance", "the previous version of this cell emitted the
union of the four", "it used to require the advance to equal `step` exactly",
"this case study reached 2026-09-14 with no such check". A reader working the
material gets the repository's repair log instead of the method, and a dated
incident in a teaching notebook is not something they can act on.

Every passage keeps the reasoning and the measurements that earned it and states
the alternative in the subjunctive: what a per-period walk would cost, what a
`tr.family = 'gbm'` clause in the query would refuse, what a policy reading
`case.answerable` would measure. Nothing is deleted except the claim that we
once did it the other way.

Markdown and comments only. Each pair is folded in with
`notebook_provenance.py sync-prose`, which refuses a moved code cell, so every
notebook keeps the outputs and the `executed_at` of the run that produced them;
the four notebooks that carry no stamp are synced with jupytext. No computed
value moves and nothing is re-run.
- [EthicalML/awesome-production-machine-learning](https://github.com/EthicalML/awesome-production-machine-learning) [2](https://github.com/EthicalML/awesome-production-machine-learning/commits): Stop the currency check reporting an unanswered repository as deleted (#825)

The check read the GraphQL `data` block and ignored `errors`, so any alias that
came back null was listed under "Unreachable (deleted or private)". GitHub
returns null for a repository it cannot resolve, but also for one it simply
failed to answer for: a rate limit, a timeout, a transient backend error. The
two cases were indistinguishable to the script and the second was reported as
the first.

This month's run (#823) showed it: `mosaicml/composer` and `mosaicml/streaming`
were both reported unreachable while both are public, live and unarchived. An
error carrying no path is worse, because it applies to every alias in the batch
— with 50 repositories per request, one bad response could have reported 50
projects as deleted.

A repository is now reported unreachable only when GitHub answers NOT_FOUND for
it twice, once in its batch and again in a query of its own. Anything that did
not answer is retried in smaller batches with a backoff, and whatever still has
not answered is listed under "Could not be checked" and excluded from the
findings count, so a run that half failed cannot read as a clean one.

Adds a standard-library self-test covering the four cases, since this
classification cannot be reproduced on demand against the live API, and runs it
in the workflow before the live check.
- [skypilot-org/skypilot](https://github.com/skypilot-org/skypilot) [2](https://github.com/skypilot-org/skypilot/commits): [CI] Nightly: run the Kubernetes jobs-consolidation lane with gRPC enabled (#10933)

Every nightly smoke lane runs with SKYPILOT_ENABLE_GRPC off, so the
skylet gRPC code path (tunnel setup, SetJobInfoWithoutJobId, GetJobTable
and the other skylet RPCs) has no scheduled coverage. The separate-
controller gRPC lane (--kubernetes --grpc --no-resource-heavy) currently
has nine tests that are red on master because regressions on that path
went unnoticed; the consolidation-mode lane with gRPC on is green.

Add smoke-tests-kubernetes-grpc-jobs-consolidation, the existing
jobs-consolidation lane with --grpc, wired the same way as the other
lanes: it gates publish-and-validate-both, appears in the run summary,
and is named in the Slack failure notice. Timeout matches the
jobs-consolidation lane (210m); the one manual run so far took 89m.

Evidence on master 6e5b2d274:
- smoke-tests build 13357 (--kubernetes --grpc --jobs-consolidation
  --no-resource-heavy): 303 of 305 jobs passed. The two failures,
  test_pool_autoscaling_scale_up_to_max_then_down_to_zero and
  test_managed_jobs_storage, are labelled flaky in Test Engine (56% and
  45% reliability) and passed on rerun in builds 13358 and 13359.

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
- [amitness/learning](https://github.com/amitness/learning) [1](https://github.com/amitness/learning/commits): Update: September 2026
- [lakehq/sail](https://github.com/lakehq/sail) [1](https://github.com/lakehq/sail/commits): feat: improve Flight client configuration (#2708)

## [middleware](https://github.com/topics/middleware)
- [thingsboard/thingsboard](https://github.com/thingsboard/thingsboard) [11](https://github.com/thingsboard/thingsboard/commits): Merge pull request #16252 from thingsboard/rc

Merge rc into master
- [bloomberg/blazingmq](https://github.com/bloomberg/blazingmq) [3](https://github.com/bloomberg/blazingmq/commits): Test: Add basic authorization tests

Signed-off-by: Taylor Foxhall <tfoxhall@bloomberg.net>

## [openai](https://github.com/topics/openai)
- [gptme/gptme](https://github.com/gptme/gptme) [57](https://github.com/gptme/gptme/commits): fix(webui): redirect after deleting active conversation (#4140)

* fix(webui): redirect after deleting active conversation

Git-Session-Id: a0b7

* test(webui): start non-selected delete test on the selected route

Git-Session-Id: 6bdf9966-2c50-52c0-8e2c-e04ae741653a

* fix(tauri): handle auto-advance race in first-run E2E click step

The wizard can advance past the Local setup step between isExisting()
returning true and click() executing (sidecar connected so fast that
checkProviderAndAdvance() fired before the click). The click then throws
"element wasn't found". Wrap the click in try/catch and let the
connected-signal waitUntil in step 8 handle the now-advanced state.

Git-Session-Id: 11f0271a-5fe5-4508-bdd5-4af9783ea656

* test(webui): wait for handler completion before asserting no-op case

After clicking Delete, the second test now waits for `onDelete` to be
called rather than waiting only for the mock to be called. The mock
resolves before the handler finishes its remaining async steps, so
the previous route/selection assertions could fire before those steps
completed. Waiting for the `onDelete` callback ensures the handler has
run all its state-update and navigation logic before we assert nothing
changed.

Git-Session-Id: c9989582-53bc-52fa-ba02-ac1653e14fbb
- [BerriAI/litellm](https://github.com/BerriAI/litellm) [31](https://github.com/BerriAI/litellm/commits): fix(proxy): stop queued registry read-throughs spending the resync budget (#44277)

* fix(proxy): stop queued registry read-throughs spending the resync budget

RegistryReadThrough.attempt serializes misses behind one lock, but every
request that was queued behind the first one still spent a unit of the
20-per-5s resync budget and re-ran the DB resync, even though the first
request had already loaded the object. A burst of more than 20 requests
for a model created on another worker therefore exhausted the budget and
the rest got 400 "Invalid model name".

attempt now checks whether the key is already loaded once it holds the
lock and returns early without touching the budget. Models check the
router's model names and deployment ids, guardrails and agents reuse
their existing registry lookups.

* test(proxy): gate the queued read-through test on events and cover each registry's loaded check

The queued-requests test now holds the first resync on an asyncio.Event instead of
a timed sleep and records calls in a recorder with tuple and frozenset state. New
tests show the model, guardrail and agent read-throughs each answer an object that
is already loaded without reading the database, so rewiring any registry's loaded
check now fails a test

* test(proxy): keep the queued read-through recorder inside its test and type the agent registry fixture
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) [5](https://github.com/OpenHands/OpenHands/commits): feat(automations): filter the automations dashboard by creator (#17814)

Co-authored-by: openhands <openhands@all-hands.dev>
- [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) [3](https://github.com/PDFMathTranslate/PDFMathTranslate/commits): doc: readme
- [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) [1](https://github.com/ggml-org/whisper.cpp/commits): whisper : add check for ttype in whisper and parakeet (#4091)
- [microsoft/markitdown](https://github.com/microsoft/markitdown) [1](https://github.com/microsoft/markitdown/commits): Consolidate tests by format and strengthen regression coverage (#2579)

## [python](https://github.com/topics/python)
- [vinta/awesome-python](https://github.com/vinta/awesome-python) [152](https://github.com/vinta/awesome-python/commits): Merge branch 'general-rule'
- [browser-use/browser-use](https://github.com/browser-use/browser-use) [30](https://github.com/browser-use/browser-use/commits): Update the Cloud signup credit in the skill reference to $1 (#5982)

Browser Use Cloud now grants eligible new signups a one-time $1 credit
instead of $15 (browser-use/cloud#6265, live since Oct 2). The Cloud
skill reference still told agents $15, so this changes that one sentence
in `skills/cloud/references/api-v4.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- This is an auto-generated description by cubic. -->
---
## Summary by cubic
Updates the Cloud skill reference to reflect that eligible new signups
now receive a one-time $1 credit instead of $15, matching the live
change shipped in browser-use/cloud#6265.

<sup>Written for commit 49795ba9aa9bbc4209782e9dcbc4b7ecf1abddba.
Summary will update on new commits.</sup>

<a
href="https://cubic.dev/pr/browser-use/browser-use/pull/5982?utm_source=github"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-light.svg"><img
alt="Review in cubic"
src="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"></picture></a>

<!-- End of auto-generated description by cubic. -->
- [adafruit/circuitpython](https://github.com/adafruit/circuitpython) [18](https://github.com/adafruit/circuitpython/commits): Merge pull request #11490 from ladyada-eagleclaw/fix/rgbmatrix-argument-validation

Validate RGBMatrix arguments before reserving a display bus
- [dbcli/mycli](https://github.com/dbcli/mycli) [12](https://github.com/dbcli/mycli/commits): Merge pull request #2301 from dbcli/RW/add-python-3-15-trove-classifier

Add Python 3.15 trove classifier
- [confident-ai/deepeval](https://github.com/confident-ai/deepeval) [8](https://github.com/confident-ai/deepeval/commits): .
- [arnegiacomo/fugleramme](https://github.com/arnegiacomo/fugleramme) [7](https://github.com/arnegiacomo/fugleramme/commits): chore(assets): #33 add Colinus virginianus (#203)
- [pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) [2](https://github.com/pymupdf/PyMuPDF/commits): tests/: Updates to work with latest mupdf master.

This reverts recent change, as mupdf behaviour is now back to being the same as
on 1.28.x.

Revert "tests/: update test_4182() to match recent change to mupdf master."

This reverts commit 67c43d11ddf3ed45d0862f3068b4b54d8dee89c1.
- [coleifer/huey](https://github.com/coleifer/huey) [1](https://github.com/coleifer/huey/commits): Tidy up checklist doc for deployment
- [coleifer/peewee](https://github.com/coleifer/peewee) [1](https://github.com/coleifer/peewee/commits): Docs trim
- [lemon24/reader](https://github.com/lemon24/reader) [1](https://github.com/lemon24/reader/commits): Fix spurious B018 flake8 warning.
- [norvig/pytudes](https://github.com/norvig/pytudes) [1](https://github.com/norvig/pytudes/commits): Remove outdated performance comment in markdown

## [recommender-system](https://github.com/topics/recommender-system)
- [lancedb/lancedb](https://github.com/lancedb/lancedb) [3](https://github.com/lancedb/lancedb/commits): perf(remote): size blob file handles from one descriptor take (#4349)
- [gorse-io/gorse](https://github.com/gorse-io/gorse) [2](https://github.com/gorse-io/gorse/commits): Add `UpdateAt` to items and users (#1392)

## [rust](https://github.com/topics/rust)
- [ZingerLittleBee/ServerBee](https://github.com/ZingerLittleBee/ServerBee) [121](https://github.com/ZingerLittleBee/ServerBee/commits): refactor: remove unused packages and shallow wrappers (#195)

Remove unused workspace scaffolding and inline redundant wrappers. Preserve Zod 4.3.6 and retain behavioral coverage.
- [durch/rust-s3](https://github.com/durch/rust-s3) [28](https://github.com/durch/rust-s3/commits): Refresh all open PR dispositions after publishing audit fixes
- [acsandmann/rift](https://github.com/acsandmann/rift) [13](https://github.com/acsandmann/rift/commits): chore: 0.6.4
- [embassy-rs/embassy](https://github.com/embassy-rs/embassy) [5](https://github.com/embassy-rs/embassy/commits): Merge pull request #7155 from Gentherm-Public/mspm0-fix-uart-hang

mspm0: fix buffered uart bug where tx occasionally hangs forever
- [probe-rs/probe-rs](https://github.com/probe-rs/probe-rs) [5](https://github.com/probe-rs/probe-rs/commits): Faster flashing, and J-Link in CMSIS-DAP mode (#4407)
- [google/comprehensive-rust](https://github.com/google/comprehensive-rust) [2](https://github.com/google/comprehensive-rust/commits): Add main fn to extending other traits slide (#3300)
- [google/wasefire](https://github.com/google/wasefire) [2](https://github.com/google/wasefire/commits): Upgrade all dependencies (#1158)
- [paritytech/parity-common](https://github.com/paritytech/parity-common) [2](https://github.com/paritytech/parity-common/commits): Bump to 10.2 (#983)
- [rust-embedded/awesome-embedded-rust](https://github.com/rust-embedded/awesome-embedded-rust) [2](https://github.com/rust-embedded/awesome-embedded-rust/commits): Fix dead links in README
- [sharkdp/fd](https://github.com/sharkdp/fd) [1](https://github.com/sharkdp/fd/commits): Merge pull request #2148 from sharkdp/dependabot/cargo/crossbeam-channel-0.5.17

build(deps): bump crossbeam-channel from 0.5.16 to 0.5.17

## [swift](https://github.com/topics/swift)
- [apple/swift-async-algorithms](https://github.com/apple/swift-async-algorithms) [2](https://github.com/apple/swift-async-algorithms/commits): Fix AsyncAlgorithms 1.3 availability macro typo (#453)

The `#else` branch declared `AsyncAlgorithms_v1_3` with the macro name
`AsyncAlgorithms 1.2`, so that branch defined `AsyncAlgorithms 1.2` twice
and never defined `AsyncAlgorithms 1.3`.

Issue: https://github.com/apple/swift-async-algorithms/issues/452
- [MarkEdit-app/MarkEdit](https://github.com/MarkEdit-app/MarkEdit) [2](https://github.com/MarkEdit-app/MarkEdit/commits): Respect the scroll strategy in 2nd attempt (#1776)
- [apple/swift-openapi-generator](https://github.com/apple/swift-openapi-generator) [1](https://github.com/apple/swift-openapi-generator/commits): Bump minimal Swift tools version to 6.2 (#962)

The support window is 3 latest minor Swift versions. CI i already
running for Swift 6.2, 6.3 and 6.4 only. Updating the Swift tools and
the package to match this.

## [vue](https://github.com/topics/vue)
- [Kuingsmile/PicList](https://github.com/Kuingsmile/PicList) [4](https://github.com/Kuingsmile/PicList/commits): :hammer: Refactor: split some vue files to smaller components
- [slidevjs/slidev](https://github.com/slidevjs/slidev) [1](https://github.com/slidevjs/slidev/commits): fix: keep c#, c++ and f# languages in code blocks and magic move (#2760)

## Other
- [openai/codex](https://github.com/openai/codex) [50](https://github.com/openai/codex/commits): Use the app-server default output cap for TUI workspace commands (#50477)

## What changed

Remove the fixed 64 KiB output cap from `WorkspaceCommand` and send
`output_bytes_cap: None` in `command/exec` requests so bounded commands use
the app-server default. Preserve `disable_output_cap` for commands that need
uncapped output, including Git diffs.

GitOrigin-RevId: 6f2ed0d127d9ff2317670851894ae4988f7c7508
- [square/leakcanary](https://github.com/square/leakcanary) [24](https://github.com/square/leakcanary/commits): Merge pull request #2982 from square/shark-dive-harness-starts-the-agent

Have the harness start the investigation, and cut the skill to a pointer
- [earendil-works/pi](https://github.com/earendil-works/pi) [23](https://github.com/earendil-works/pi/commits): fix(tui,coding-agent): convert non-PNG images for Kitty in Image

Kitty-protocol terminals only accept PNG. pi-tui now exposes
setImageTranscoder(); Image converts JPEG/GIF/WebP through it and shows
the text fallback without one. coding-agent registers a photon-based
transcoder, so images from extensions and all ToolExecutionComponent
hosts render.

closes #10292
- [awesomedata/awesome-public-datasets](https://github.com/awesomedata/awesome-public-datasets) [22](https://github.com/awesomedata/awesome-public-datasets/commits): Update README sha: b945ed864b0df062d320eefe472757fe51147732
- [facebook/idb](https://github.com/facebook/idb) [22](https://github.com/facebook/idb/commits): Confirm pose and display changes

Summary:
Add opt-in `--wait` support to physical rotation and hinge setters. Each command writes the requested pose exactly once, then performs bounded authoritative readback before returning.

Add `--wait-for-display` for callers that also require two identical active-display snapshots. JSON output reports the requested and observed pose, stable display, confirmation result, elapsed time, and sample count; timeouts emit the same result before exiting nonzero. Existing non-waiting setter and getter output remains unchanged.

Expose current display geometry separately from display identity so legacy single-display runtimes can report interface rotation without inventing a UUID.

Reviewed By: cute-jumper

Differential Revision: D122898945

fbshipit-source-id: fa7c4e1797d797cc13c8e758c51cc7209125602f
- [Mentra-Community/MentraOS](https://github.com/Mentra-Community/MentraOS) [20](https://github.com/Mentra-Community/MentraOS/commits): Merge pull request #4412 from Mentra-Community/aisraelov/16-kb-page-sizes-google-play

Build the LC3 native library with 16 KB page alignment
- [jdx/mise](https://github.com/jdx/mise) [19](https://github.com/jdx/mise/commits): docs: tighten the landing-page video and smooth its soundtrack (#13916)

<!-- entire-trail-link-start -->
https://entire.io/gh/jdx/mise/trails/399
<!-- entire-trail-link-end -->

The landing-page demo now offers a 4:44 full tour and a 1:16 quick
overview instead of the 7:16 reel. Project switching is the first
demonstration, retained scenes keep their original reading time, and
visible chapter buttons let viewers jump directly to a feature.

Redesign the opening, install card, and poster with larger type and add
command/result callouts drawn from the real terminal captures. Arrange
the original soundtrack independently of picture cuts, removing abrupt
jumps and the near-silent break while preserving the song's natural
ending. Remove the paragraph and extra fullscreen button beneath the
player.

The renderer and docs cache deliver both editions, including their
chapter metadata, and can still restore older successful renders as a
fallback.

Validation: documentation build with rendered videos, showreel typecheck
and tests, scoped lint, and desktop/mobile playback checks. Both native
60/120 fps tour files retain their frame rates; the overview is 60 fps.
The final AAC mix measures -16.6 LUFS and -2.8 dBTP. Live capture
generation was not rerun; rendering uses the committed real-shell
capture set.

*AI-assisted — Tool: Codex; model: OpenAI/unavailable; version:
unavailable.*

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Changes are scoped to docs site media, VitePress theme, and showreel
build scripts; no runtime product or auth paths are affected.
> 
> **Overview**
> The landing-page demo is split into a **~4:44 full tour** and a
**~1:16 quick overview**, with editorial cuts (`edit.ts`), new brand
intro/outro cards, and command callouts from real captures (`film.ts`).
Sound for those films uses independently arranged original song plus
picture-synced effects (`film-music.ts`, `film-audio.ts`), while
`--edition source` keeps the full source reel for tooling.
> 
> The **home player** adds tour/overview toggles, clickable chapter
jumps, and a runtime badge; the caption paragraph under the video is
removed. **Build and deploy** render both MP4s and WebVTT chapter
tracks, extend `showreel.data.ts` with overview metadata, and update
CI/cache staging so overview assets and `SHOWREEL_OVERVIEW_CHAPTERS`
ride along—or are cleared when restoring older cache fallbacks.
> 
> <sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit
bc417dbaffbe978273358b652fa90aca2829b53c. Bugbot is set up for automated
code reviews on this repo. Configure
[here](https://www.cursor.com/dashboard/bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai
-->
## Summary by CodeRabbit

* **New Features**
* Added a quick overview edition alongside the full showreel, with
edition controls, chapter navigation, and edition-specific runtimes.
* Updated the showreel’s visuals, soundtrack, and chapter tracks for
both editions.
* **Updates**
* Showreel chapters now follow the edited film timeline, with revised
labels and timing.
  * Added documentation for the editions and their audio.
* **Bug Fixes**
* Improved showreel recovery when a site build is retried, including
handling unavailable overview files.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->
- [buildroot/buildroot](https://github.com/buildroot/buildroot) [18](https://github.com/buildroot/buildroot/commits): package/ca-certificates: Replace c_rehash with openssl rehash

The upcoming bump of libopenssl to 4.0.2 removes the c_rehash script:

https://openssl-library.org/post/2026-04-14-openssl-40-final-release/
https://github.com/openssl/openssl/blob/openssl-4.0.2/CHANGES.md#openssl-40

"* Removed `c_rehash` script tool.  Use `openssl rehash` instead."

Note that c_rehash was already described as obsolete in the release
notes for OpenSSL 3.0.2 and 3.0.3.

Signed-off-by: Bernd Kuhls <bernd@kuhls.net>
Cc: Martin Bark <martin@barkynet.com>
[Fiona: add note about how long c_rehash has been considered obsolete]
Signed-off-by: Fiona Klute <fiona.klute@gmx.de>
- [signalapp/libsignal](https://github.com/signalapp/libsignal) [13](https://github.com/signalapp/libsignal/commits): backups: Add new sticker fields
- [block/buzz](https://github.com/block/buzz) [12](https://github.com/block/buzz/commits): refactor(relay): bind HTTP tenants through one shadow-aware helper (#8062)

Adds `bind_tenant()`, a single helper that resolves the community from
the request `Host` and records the NIP-FI shadow verdict when binding
fails. Ten protected HTTP handlers previously duplicated the Host lookup
and called `observe_unbound` in their own failure branches, so each one
had to remember the observer call. Moving those ten handlers onto the
helper makes recording the verdict part of binding itself, and
`observe_unbound` becomes private to the shadow module. Each caller
keeps its existing rejection response, so Off/Enforce behavior is
unchanged.

`bind_community()` stays directly callable. Routes exempt from NIP-FI
(invite claim, webhooks, NIP-05 and NIP-11 metadata) keep using it, and
the WebSocket and audio upgrades record their own verdicts before they
bind. A new protected HTTP handler should bind through `bind_tenant()`.

🤖 Authored by Duncan (agent) on behalf of Will.

Signed-off-by: Will Pfleger <pfleger.will@gmail.com>
Co-authored-by: Duncan <dcfd242e557282d7a1e2cf2e6877522682f1e5c6156dc92ca7d90eaedd3b0f95@buzz.block.builderlab.xyz>
- [cline/cline](https://github.com/cline/cline) [12](https://github.com/cline/cline/commits): feat(llms): opt-in Langfuse tracing for BYOK providers plus env tags, metadata and environment (#14787)

* feat(llms): opt-in Langfuse tracing for BYOK providers plus env tags, metadata and environment

Langfuse tracing was limited to the cline and cline-pass providers, so an
operator pointing LANGFUSE_* credentials at their own instance could not trace
OpenRouter or any other BYOK provider. CLINE_LANGFUSE_ALL_PROVIDERS=1 now opts
third-party providers in. They are exported only through the isolated direct
exporter and never through the host OTLP relay, so BYOK prompts cannot reach a
collector the operator did not configure themselves.

Benchmark and isolated-environment runs can label every trace from the
environment: LANGFUSE_TRACING_ENVIRONMENT sets the Langfuse environment on the
direct exporter, CLINE_LANGFUSE_TAGS adds comma-separated trace tags, and
CLINE_LANGFUSE_METADATA adds trace metadata as a JSON object or key=value
pairs. Env values merge under the runtime's own attributes, and env-only
attributes propagate even when a call supplies none of its own.

* docs(llms): state that Langfuse tracing covers streamed language requests only

Dedicated image generation uses the AI SDK's generateImage, which takes no
telemetry option and has no Langfuse integration hook, so it has never been
traced for any provider. Document that scope in the resolver and the runbook
rather than implying the BYOK opt-in covers it.
- [huggingface/AnyLanguageModel](https://github.com/huggingface/AnyLanguageModel) [9](https://github.com/huggingface/AnyLanguageModel/commits): Bound MLX test responses (#285)
- [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) [8](https://github.com/nicobailon/visual-explainer/commits): fix: keep sources visible and hide the narrow nav scrollbar (#106)

* fix: keep sources visible and hide the narrow nav scrollbar

Sources were in a collapsed grey <details> toggle that readers missed. The template now renders them as a visible section, and the style guide says never to collapse them.

On narrow screens the sticky section nav showed a grey scrollbar under the links. The diagrams reference now says to hide it, fade the right edge, and keep buttons outside the scrolling list.

* fix: style the template sources label with the existing label classes
- [input-output-hk/daedalus](https://github.com/input-output-hk/daedalus) [7](https://github.com/input-output-hk/daedalus/commits): Merge pull request #3424 from DripDropz/sl/release-11.5.0

chore(release): bump version to 11.5.0 and update CHANGELOG
- [lovyan03/LovyanGFX](https://github.com/lovyan03/LovyanGFX) [7](https://github.com/lovyan03/LovyanGFX/commits): Merge pull request #952 from ainyan03/release_1.2.32

Release 1.2.32
- [KittenML/KittenTTS](https://github.com/KittenML/KittenTTS) [6](https://github.com/KittenML/KittenTTS/commits): Update README.md
- [usetrmnl/trmnl-firmware](https://github.com/usetrmnl/trmnl-firmware) [6](https://github.com/usetrmnl/trmnl-firmware/commits): Isolate PlatformIO platforms in release builds (#666)

espressif32 6.12 and pioarduino share framework-arduinoespressif32 in
one core dir, so alternating them broke TRMNL_X builds. With
PIO_CORE_ROOT set (as the workflow now does), each platform builds in
its own core dir.

Also rename the "trmnl" alias to "trmnls" (it clashed with the env,
building envs twice) and drop duplicate envs.

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [anthropics/buffa](https://github.com/anthropics/buffa) [5](https://github.com/anthropics/buffa/commits): fix(types): reject non-string Any JSON fallback payloads (#498)

Unregistered `Any` type URLs currently accept object, array, number, and
boolean `value` payloads and silently replace them with empty bytes.
Return a descriptive deserialization error for these malformed inputs so
payload data cannot disappear unnoticed.

Missing, `null`, and empty-string payloads retain their existing
empty-byte behavior. Valid base64 strings and registered-type decoding
are unchanged. Regression tests cover both a missing registry and an
installed registry without the requested type, including valid and
invalid base64 controls.

Fixes #487.

Validation:
- `task lint`
- `task test` (with repository-pinned protoc 33.5)
- `cargo test -p buffa-types --features json fallback_base64`
- Both required Rust review agents reported no findings.

---------

Co-authored-by: Iain McGinniss <309153+iainmcgin@users.noreply.github.com>
- [ccusage/ccusage](https://github.com/ccusage/ccusage) [4](https://github.com/ccusage/ccusage/commits): fix(codex): count unreported compaction usage (#1821)

* fix(codex): count unreported compaction usage

Match token_usage_record responses to compacted markers and add usage
omitted from Codex's cumulative token counts. Suppress records already
covered by an advancing snapshot so local compaction stays counted once.

Deduplicate response IDs across copied sessions, including parents outside
the report's date range, and preserve deterministic attribution and speed
tier merging in serial and parallel aggregation.

Rework the contribution from ccusage/ccusage#1805 for the current adapter.

Co-authored-by: Henry Teo <96536361+HenryTeo27@users.noreply.github.com>

* fix(codex): parse usage records with JSON whitespace

Allow the line classifier to fall back to its whitespace-aware scan for
turn contexts and nested token counts with spaces after type colons.
This prevents valid JSONL from silently omitting normal request usage
when calculating totals alongside compaction records.

* fix(codex): retain counted compaction IDs in replay history

Keep matched parent response IDs independently of usage emission, so a
retained child log missing the intervening cumulative snapshot cannot
count an already-accounted compaction again in a date-bounded report.

Collect identities during the existing parent pass. Normal report parsing
does not allocate the optional history map, and ordinary replay matching
continues to use only token-count deltas.

Add a regression covering the loader and serial/parallel reports with a
missing child snapshot. This addresses Cubic's review finding on #1821.

* fix(codex): preserve valid pending usage across invalid records

Keep the latest valid response ID when an invalid or already-accounted
record is ignored. Clearing it before validation prevented cumulative
snapshots from consuming the pending compaction usage and counted it twice.

Add exact-total regressions for missing IDs, timestamps, empty usage, and
duplicate completed responses. This addresses Pullfrog's review on #1821.

* docs(codex): clarify duplicate compaction attribution

---------

Co-authored-by: Henry Teo <96536361+HenryTeo27@users.noreply.github.com>
- [ChrisBuilds/terminaltexteffects](https://github.com/ChrisBuilds/terminaltexteffects) [4](https://github.com/ChrisBuilds/terminaltexteffects/commits): Enable measured row caching for six additional effects
- [raspberrypi/debugprobe](https://github.com/raspberrypi/debugprobe) [4](https://github.com/raspberrypi/debugprobe/commits): Update README.md with new Pico SDK version requirement.

The firmware's default target board, debug_probe, requires Pico SDK
2.3.0 or newer. Therefore, this documentation for this requirement has
been hoisted into the "Hacking" section.
- [a2aproject/A2A](https://github.com/a2aproject/A2A) [3](https://github.com/a2aproject/A2A/commits): docs: add Salt to partners list (#2265)

Closes #2266.

[Salt](https://saltapp.ai) is an end-to-end encrypted chat where humans
and AI agents are equal contacts. Every public Salt agent publishes a
signed A2A AgentCard (e.g.
https://saltapp.ai/api/.well-known/agent-card.json for Salt itself) and
a `did:web` identity, so other A2A-aware tooling can discover and
identify Salt agents. Agents on Salt message, ask a human with tappable
buttons, invoice and get paid, inside an end-to-end encrypted chat.

One-line addition to `docs/partners.md`, alphabetically ordered,
following the existing format.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YQeHtC1zW2DtEs3qk5PvtK

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
Co-authored-by: Sampath Kumar <sam1990kumar@gmail.com>
- [antonmedv/fx](https://github.com/antonmedv/fx) [3](https://github.com/antonmedv/fx/commits): Harden `:w !cmd`

Bound the wait for stdin with WaitDelay, so a child left behind by the
command, as with `:w !tool &`, can't freeze the UI. Pass the command line
to cmd.exe as is, with /S /C, since exec.Command's quoting breaks cmd.exe
quoting. Report a command killed by a signal as "signal: interrupt" rather
than "shell returned -1". Share the "written" message between :w to a file
and to a command. Tests pin SHELL to sh and skip on Windows.
- [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) [3](https://github.com/ghostty-org/ghostty/commits): macos: honor window-save-state=never for restorable windows (#14506)

With `window-save-state = never`, normal terminal windows are still
marked `isRestorable`. Ghostty disables saving through
`NSQuitAlwaysKeepsWindows`, but AppKit continued taking persistent-UI
window snapshots in my reproduction on macOS 27.2 (26B5091g).

Make `TerminalController.windowDidLoad()` also honor `never` when
setting `window.isRestorable`, and only assign the restoration class and
identifier when that flag is enabled. This adds no work to move, resize,
or rendering callbacks.

For newly created windows, `default` and `always` retain the existing
behavior, including the exclusion of windows launched with a custom
command. The follow-up commit also covers windows that are already open:
on config reload, each terminal window re-syncs its restoration state
through the same path used at window creation. Windows started with a
custom command stay excluded.

### Reproduction and measurements

I reproduced intermittent roughly 500 ms stalls while repeatedly
focusing left/right between several Ghostty windows and other
applications in OmniWM's Niri layout. `window-save-state = never` was
set before restarting Ghostty.

The issue reproduced on 1.3.1 and an unmodified build of `76895d97b`. In
the latter, paired process samples showed
`NSPersistentUIWindowSnapshotter` waiting through
`SLSConnectionSynchronizeSLSCATransaction`, alongside Ghostty's main
thread waiting on the connection lock under
`SLSConnectionSetLastSLSCATransaction`.

Comparing unmodified and patched builds of the same commit over two
approximately 20-second navigation captures:

| Measurement | Unmodified | Patched |
| --- | ---: | ---: |
| Focus presses | 113 | 129 |
| Successful Ghostty AX frame-write attempts | 2,155 | 2,995 |
| Ghostty AX frame-write attempts around 500 ms | 5 | 0 |
| Slowest Ghostty AX frame-write attempt | 539.8 ms | 22.5 ms |
| Ghostty main-thread samples in the CA/SkyLight connection-lock wait |
2,205 / 12,544 | 0 / 12,173 |

The persistent-UI snapshot worker was absent from the patched sample,
and navigation feels noticeably smoother. These are aggregate samples
from one before/after pair with different input counts, not a controlled
end-to-end latency benchmark. Both Ghostty builds used ReleaseLocal with
the same ReleaseFast core, while OmniWM remained the same instrumented
Debug process.

### Validation

- `macos/build.nu --action test`: 275 passed, 1 skipped, 0 failed.
- New `macos/Tests/Terminal/TerminalControllerRestorationTests.swift`:
reload flips restoration on an open window between `never`, `default`
and `always`; custom-command windows stay non-restorable across reloads;
surface-level config changes leave it alone.
- `macos/build.nu --configuration ReleaseLocal`: passed.
- Strict SwiftLint on both changed files: passed.
- Manual navigation reproduction with the patched build: noticeably
smoother, with the results above.

### AI disclosure

I used OpenAI Codex to assist with diagnosis, implement the two-line
change, run verification, analyze the captures, and draft this
description. I reproduced the issue and tested the patched app
interactively.
- [KlipperScreen/KlipperScreen](https://github.com/KlipperScreen/KlipperScreen) [3](https://github.com/KlipperScreen/KlipperScreen/commits): Power devices fix (#1775)

* fix: power panel empty when built before moonraker reply

fixes: #1774

* feat: log power device toggles to the notification panel

* refactor: simplify splash check_power_status
- [sushi-labs/sushiswap](https://github.com/sushi-labs/sushiswap) [3](https://github.com/sushi-labs/sushiswap/commits): fix(web): enable single-sided presets before pool creation (#2316)

* fix(web): enable single-sided presets before pool creation

* fix(web): hide disabled concentrated liquidity fee tiers

* fix(web): scope liquidity wallet checks to EVM

Validation: both review-disconnect tests currently fail because the review dialog does not yet have a connection checker.

* fix(web): require EVM connection in liquidity review

Show the EVM wallet connection button when the wallet disconnects during liquidity review, keeping the final Add Liquidity action behind the existing connection checker.

Validation: 914 web unit tests passed; formatting, lint, and web typecheck passed.
- [tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro) [3](https://github.com/tensorflow/tflite-micro/commits): Namespace tensorflow/lite/micro/c/ and remove TF_LITE_STATIC_MEMORY (#3797)

Isolate TFLM C API types and functions in tensorflow/lite/micro/c/ under namespace tflite::micro with dedicated TENSORFLOW_LITE_MICRO_C_*_H_ header guards, and permanently remove TF_LITE_STATIC_MEMORY across the repository.

BUG=#3777
- [THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC) [3](https://github.com/THU-MAIC/OpenMAIC/commits): feat(config): openmaic.yml, capability slots and server-side model configuration (RFC #1701) (#1765)

* ci: run CI for the provider-config integration branch

Development of the provider configuration RFC (#1701) lands on
integration/provider-config; build it on push and run CI for pull
requests into it, as with earlier integration branches.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* feat(config): capability slot registry and stage-to-slot mapping (#1726)

* feat(config): capability slot registry and stage-to-slot mapping

First P0 step of the provider configuration RFC (#1701, tracked in
#1725): define the capability slot forest and map every LLM stage key
to exactly one slot. Pure data with no callers yet, so there is no
behavior change.

Requirements are checked on the slot that declares them and are not
passed down to child slots, so agent.title can use a model without
tool calling even though agent requires it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* test(config): pin every stage destination and the capability roots

Review found that the station and root assertions derived their
expectations from the module under test: re-pointing a single-stage
station or dropping a capability root still passed. The tests now
compare against an independently written stage table and root list,
and pin agent.title as config-only. Also document that browserless
outlines still run on the generate-classroom model.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* test(config): pin slotForStage and full slot lineages

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(config): provider presets and the openmaic.yml schema (#1727)

* feat(config): provider presets and the openmaic.yml schema

Second P0 step of the provider configuration RFC (#1701, tracked in
#1725).

- lib/config/provider-presets.ts: one preset per built-in registry
  entry, plus the token plans as multi-capability presets whose stage
  recommendations become slot recommendations. Registry ids that
  collide across capabilities get explicit preset ids.
- lib/server/model-config/openmaic-yml.ts: parse and validate the
  operator's openmaic.yml (or the file named by OPENMAIC_CONFIG):
  ${VAR} interpolation, strict schema, and cross-checks that every
  assignment names a declared provider whose preset offers the slot's
  capability. Every problem is reported with its path.
- instrumentation.ts: an invalid file refuses to start. Without a file
  nothing changes, and nothing resolves models through the file yet.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): harden openmaic.yml validation after review

- Look providers up by own key only, so "constructor:m" is not taken
  for a declared provider.
- Refuse non-mapping objects YAML produces (an unquoted timestamp
  becomes a Date that the schema would accept as an empty object), and
  refuse a YAML alias that refers back to itself instead of overflowing
  the stack.
- Accept lowercase variable names; refuse a "${" with no closing
  brace, checked on the text as written, never on substituted secrets.
- Cross-check the entries that are valid on their own even when the
  schema rejects others, so every problem is reported at once without
  duplicate errors for declared-but-invalid providers.
- Name the three valid assignment shapes when a value has none of them.
- Test the boot path: an invalid file exits with code 1 before any
  schedule starts; a valid one boots.
- Ignore a root openmaic.yml in git.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): keep secrets out of openmaic.yml diagnostics

Review round 2:

- Read only variables the environment itself has, as non-empty
  strings: ${constructor} or an inherited value is not a variable.
- Never print a value that came from ${VAR}, and report YAML syntax
  errors by reason and position without js-yaml's source excerpt,
  which can quote a literal key.
- Keep the base URL requirement on presets: SearXNG from its registry
  entry, and Azure OpenAI and self-hosted MinerU, which have no usable
  default endpoint.
- Check slot names and valid model references even inside an entry
  that fails the schema, and report a failed placeholder once rather
  than again as an empty value.
- Boot test for the no-file case.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* refactor(config): validate openmaic.yml in two phases

Rounds 1-3 of review kept finding edge cases in one feature: running
the cross-checks on the half-valid parts of a file the schema had
rejected, so that every problem showed at once. It hid problems inside
a rejected entry, lost a __proto__ slot key, and built misleading
provider errors from failed placeholders. That feature is gone.

Validation now runs in two phases. Phase 1 is the document itself:
placeholders, key names (checked on the document as written, since the
schema drops a __proto__ key), and the schema. Any problem there stops
before phase 2, the references between entries, which therefore only
ever sees a fully valid file. Each phase reports all of its problems,
one per path.

YAML syntax errors now report only their position: js-yaml's reason
can quote source text too (an alias or tag name), not just its excerpt.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(api)!: generate-classroom takes requirement + uploaded materials; capabilities follow server config (#1728)

Narrows POST /api/generate-classroom to { requirement, materialIds? }; capabilities follow server configuration; materials go through the owner material library (upload, reference by id, delete); new GET /api/generate-classroom/capabilities; skill docs updated.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* feat(config): resolve a slot through the configuration layers (#1729)

* feat(config): resolve a slot through the configuration layers

Third P0 step of the provider configuration RFC (#1701, tracked in
#1725). resolveSlot walks from a slot to its capability root and
returns the first assignment it meets, consulting the deployment layer
(openmaic.yml, locked) before the workspace layer at every node. An
explicit null disables the subtree; nothing assigned up to the root is
unassigned, with no fallback to any vendor. The result carries the
provider, preset, registry entry, effective base URL, key, model, call
options, fallback, where it was resolved and whether it is locked, and
the requested slot's own requirements checked against the model
catalogue (met, unmet or unknown).

Pure and uncalled for now, so there is no behavior change.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): lock only written slots and trust the catalogue only where it applies

Review round 1:

- locked now means the requested slot itself is written in the
  deployment layer. Inheriting a deployment value does not lock a slot,
  since the workspace may still assign it (source and resolvedAt still
  report where the value came from).
- A custom OpenAI-compatible endpoint borrows the OpenAI registry for
  transport only, so its preset no longer trusts that model catalogue:
  requirements there resolve to unknown.
- The fallback is checked against the slot's requirements too, and the
  result exposes fallbackRequirements so retries can refuse it.
- A malformed reference fails with a path-qualified SlotResolutionError
  that does not echo the value, which is often a misplaced key.
- Requirement tests use named catalogue models instead of picking one
  from the catalogue at run time.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): order layers deployment-first and keep references out of errors

Review round 2:

- resolveSlot no longer depends on the order its caller passes the
  layers in: deployment layers always come first, for assignments and
  provider lookup alike.
- Resolution errors name the path and the preset, never a value taken
  from the reference, so a key pasted into the provider position does
  not end up in a log.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* test(config): cover catalogue aliases and fallback capability errors

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(classroom)!: save server-generated classrooms through server persistence (#1730)

Server-side classroom generation saves the finished course create-only into the request owner's library with media in the owner's asset pool; jobs move to PostgreSQL with owner-scoped polling; /api/classroom is removed; legacy data/classrooms files are imported once in the background. Adds @openmaic/storage 0.36.0 PgAssetStore.releasePending.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* feat(config): translate the legacy configuration into a deployment layer (#1731)

* feat(config): translate the legacy configuration into a deployment layer

Deployments without openmaic.yml keep working: provider variables,
server-providers.yml, DEFAULT_MODEL, MODEL_ROUTES and MODEL_FALLBACK are
translated into the openmaic.yml shape and serve as the deployment layer
for resolveSlot.

- Providers: each configured entry becomes a provider under its preset
  id; force-disabled entries are left out; AliDocMind's key pair goes
  into credentials.
- DEFAULT_MODEL goes on the llm root. Every other slot that serves stages
  gets what those stages used before (their route, or else the default
  model), written only where inheritance would give something else, so
  an unrouted stage under a routed parent stays on the default model.
- Stages that now share a slot but had different routes, models whose
  provider has no server configuration, and stages that used the
  browser's model but would now inherit a server one become startup
  notices, never failures.
- MODEL_FALLBACK attaches to every chat assignment without its own.
- When openmaic.yml exists it wins, with a notice if legacy variables
  are also set.

Nothing reads the layer yet; routes switch over in P1 (#1725).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): follow the agent driver's rules and keep notices value-free

Review round 1:

- The agent never used DEFAULT_MODEL: it needs a valid maic-agent-driver
  route and is off otherwise, so the translation writes agent: null where
  it would inherit a server model (and a notice for a route that does
  not work today). Unrouted conversation titles reuse the driver's model
  with thinking off, as the title generator does.
- Notices name registry ids only; a credential pasted into a model
  variable is never repeated.
- Provider entries and route options are checked against the new schema
  and left out with a notice (field names only) instead of producing a
  file that would not parse; driver-only options are dropped elsewhere.
- A route with its own fallback never falls back to MODEL_FALLBACK, even
  when that fallback cannot carry over; the retry model is part of the
  comparison with the inherited value.
- Force-off switches without a configured entry are reported, a legacy
  configuration made only of them is detected, and translating one adds
  a deprecation notice.
- loadDeploymentLayer reads the process environment and working
  directory like the legacy loaders, instead of taking parameters it
  could only partly honor.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): compare routes by behavior, validate references, name only known ids

Review round 2:

- Stages sharing a slot are compared by what the route changes for them
  (model, thinking, fallback), with bare ids read as openai models and a
  route to DEFAULT_MODEL counted as no route; api and contextWindow are
  inert outside the driver.
- A model reference carries over only when it names a provider from the
  providers section and forms a valid reference.
- Section keys and force-off ids are named in notices only when they are
  registry ids with a preset.
- Retries now follow the slot; where a call site picked its retry model
  by another label (scene types under scene-content, browserless
  generation), the change is reported.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): chat references need a chat entry; one notice for retries

Review round 3:

- A model reference carries over only when its provider was translated
  from the providers section, not merely declared by another section
  under the same id.
- Routes are compared by the retry model that takes effect, so leaving
  out a fallback equals repeating MODEL_FALLBACK.
- The per-call-site retry notices kept missing cases (streaming and
  calls outside server-managed routing never retry today). They are
  replaced by one notice, given whenever a retry model is configured,
  that retries now follow the slot.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* refactor(config)!: translate only providers and the default model (#1732)

* refactor(config)!: translate only providers and the default model

MODEL_ROUTES does not map one to one onto slots: several stages share a
slot, the agent driver and conversation titles have rules of their own,
and retries are picked by call-site labels. Emulating that took most of
the translation and still ended in notices that are easy to miss.

The translation now carries over only the unambiguous part: providers,
DEFAULT_MODEL as the llm root and MODEL_FALLBACK as its fallback (the
agent stays null, as it never used DEFAULT_MODEL). A deployment that
sets MODEL_ROUTES without openmaic.yml gets LegacyRoutesError asking it
to write the per-stage models as slots. loadDeploymentLayer is not wired
into startup yet; that happens when routes switch to resolveSlot (P1).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): say what a dropped MODEL_FALLBACK loses

Without DEFAULT_MODEL there is no assignment to hold MODEL_FALLBACK, and
calls that retried on it (server providers picked in the browser) stop
retrying; the notice says so. thinkingSchema is module-private again.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(persistence): workspace model configuration with keys encrypted at rest (#1733)

* feat(persistence): workspace model configuration with keys encrypted at rest

The store behind the web settings of RFC #1701 (#1725, P1): one row per
workspace (owner) in workspace_model_config, the same shape as
openmaic.yml without policy.

- Provider secrets (apiKey, credentials) are sealed per provider with
  AES-256-GCM under OPENMAIC_SECRET_KEY, bound to the provider id, and
  never stored in the config column. Without the variable, a secret is
  created once in data/instance-secret.key (the Docker volume).
- A secret sealed under another instance secret is reported as
  unreadable ("enter again"), and a save that brings no new secret for
  that provider keeps it, so a misconfigured secret cannot destroy keys.
- Saves replace the document with a compare-and-swap on the revision,
  after the owner's identity lock; two concurrent first saves cannot
  both land (PostgreSQL contract test).
- A claim moves the anonymous configuration to the account unless the
  account has its own (core participant, order 900).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(persistence): publish the instance secret atomically; force the races in tests

Review round 1:

- The generated secret is written and flushed under a private name,
  then published with an exclusive link, so no process can read it half
  written and exactly one of two starting processes creates it. A file
  that is not a complete generated secret (empty, truncated) is refused
  instead of deriving a key anyone could compute.
- The PostgreSQL test holds both first saves at their insert until both
  have read the missing row, and holds the row lock for the update case
  until both saves queue behind it (checked by backend pid, not by any
  lock waiter in the database).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(persistence): verify the written secret; require full GCM tags

Review round 2:

- The generated secret is written in full, read back and checked before
  it is published; the temporary file is removed on any failure.
- Sealed values open only with a 12-byte IV and a full 16-byte tag
  (authTagLength), so a shortened tag cannot weaken authentication.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(config): resolve slots at request time over deployment, workspace and defaults (#1734)

* feat(config): resolve slots at request time over deployment, workspace and defaults

The runtime half of RFC #1701 resolution (#1725, P1):

- deploymentConfig(): the deployment layer, loaded once per process.
  The legacy translation now splits into the deployment's providers and
  a separate default layer (DEFAULT_MODEL, MODEL_FALLBACK) that locks
  nothing and ranks below the workspace, as DEFAULT_MODEL ranked below
  the model a user picked.
- workspaceLayer(owner) reads the web settings; requestWorkspaceId(req)
  names the request's owner (none for an owner minted by the request).
- lookupSlot walks deployment and workspace over the whole tree first;
  the defaults are a second walk, so a default on a child never outranks
  a workspace choice higher up.
- resolveStageModel builds the language model: the configured slot, else
  what the request still names the old way (deprecated), else the
  defaults, else a loud error; a slot turned off fails whatever the
  request names. A workspace provider's endpoint is checked like a
  caller-supplied one and gets the transport that refuses redirects.
- resolveSlot gains the default source, and reports which layer declared
  the provider, its proxy and credentials.

Nothing calls it yet; call sites switch next.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): keep request identity and workspace endpoints inside their bounds

Review round 1:

- A refused owner credential throws InvalidOwnerCredentialError (401)
  instead of resolving with the deployment's models and keys.
- A retired request owner gets no workspace: canonicalizing it would
  hand an old anonymous cookie the claiming account's settings. Only
  background work, which names a stored owner, is forwarded.
- A workspace provider may not be Amazon Bedrock (which falls back to
  the server's AWS credential chain) or set a proxy (which routes around
  the checked, redirect-refusing transport); the deployment still may.
- Test seams for the deployment config and the workspace loader, and
  tests for identity, forwarding and caching.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): read only the named owner's settings; refuse unmet requirements

Review round 2:

- workspaceLayer reads exactly the owner it is given. Forwarding through
  a claim let a request whose owner was claimed between its check and the
  read see the account's settings; background work passes the owner it
  works for now instead.
- A model the catalogue says does not meet the slot's requirement is
  refused before anything is built (SlotRequirementError), without
  consulting the request.
- Tests: a database failure fails the call without falling back, a
  workspace provider without a key never gets the deployment's, and the
  transport each provider source gets.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* test(identity): exempt the model settings lookup from cookie forwarding

requestWorkspaceId resolves the owner only to pick whose model settings a
generation call uses, and returns no response of its own, like the
vision prompt helper already listed.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(config)!: resolve every LLM call through its capability slot (#1735)

* feat(config)!: resolve every LLM call through its capability slot

The LLM call sites of RFC #1701 switch to slot resolution (#1725, P1):

- resolveModel resolves a stage through its slot for the request's or
  job's workspace: the deployment and workspace configuration first; the
  model and key a request names (x-model, x-model-routes, body fields)
  only for a slot left unassigned, deprecated; then the defaults an
  older deployment set with DEFAULT_MODEL. Routes that read headers get
  this through resolveModelFromRequest; the chat routes pass their
  workspace; background work (agent runs, titles, generation jobs)
  passes the owner it works for now.
- Retries follow the slot: a slot-resolved model carries its slot's
  fallback (lib/ai/model-fallbacks.ts), which callLLM and the outline
  stream use; only a model from the request path still retries on
  MODEL_FALLBACK. A fallback that cannot meet the slot is not used.
- The agent driver resolves the agent slot: tool calling required,
  api defaults to openai-completions, thinking.effort still refused.
  Conversation titles resolve agent.title with thinking off unless the
  title slot sets it.
- /api/generate-classroom resolves each step through its slot for the
  job's owner, its outline through course.outline.
- MODEL_ROUTES is gone: loadDeploymentLayer runs at startup and a server
  that still sets it without openmaic.yml refuses to start. The
  pbl-chat and maic-agent stage keys, which nothing resolved, are removed.

BREAKING CHANGE: MODEL_ROUTES is no longer read; write per-stage models
as slots in openmaic.yml.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): a slot fallback needs no serverManaged stamp; follow claims per stage

Review round 1:

- callLLM arms a model's attached slot fallback whether or not the caller
  passes serverManaged (the PBL agents pass none); the stamp still gates
  MODEL_FALLBACK on the request path.
- /api/generate-classroom resolves the owner the job works for now at each
  stage, so stages after a claim follow the moved settings.

Streaming calls (agent driver, classroom chat, PBL streams) still do not
retry on a fallback model, as before this change; that is the #1725 item
on retries at every call site.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(config): resolve media and tool capabilities through their slots (#1737)

* feat(config): a provider-only reference names the provider's default model

Search and document providers mostly have no model to pick, so a slot
may name just the provider (`webSearch: tavily`); the target then has no
modelId and the adapter uses its default. Chat slots still need
providerId:modelId, checked in openmaic.yml and at resolution.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* feat(config): resolve media and tool capabilities through their slots

The capability routes and server paths of RFC #1701 (#1725, P1): text
to speech, speech recognition, images, video, web search and document
extraction resolve through their slots, like language models.

- lib/server/model-config/media.ts: the configured slot (deployment,
  then workspace); else the provider a request names the old way
  (deprecated); else the legacy defaults; else a loud error. A slot turned
  off fails whatever the request names, and while the legacy
  <CAP>_<VENDOR>_ENABLED=false switches are in effect a switched-off
  provider stays off whoever assigns it. A workspace endpoint is checked
  like a caller-supplied one and may not use a proxy.
- The legacy translation assigns the media roots the provider the server
  picked when a request named none (first configured; web search by its
  old priority; DEFAULT_IMAGE_PROVIDER for images), with the first pinned
  model.
- Routes: /api/generate/{image,video,tts,voice}, /api/transcription,
  /api/web-search, /api/parse-pdf and /api/extract-document. A TTS voice
  applies only to the provider it was chosen for; voices register on the
  tts slot's provider.
- Server paths: agent image and video generation, scene narration, the
  voice catalog and registration, web search and fetch_url, material
  extraction (the document slot's service, the asr slot for local
  transcription), browserless classroom media, and the generation
  capabilities reported by /api/health and the classroom capabilities
  endpoint.
- A provider-only reference (`webSearch: tavily`) names the provider's
  default model; chat slots still need providerId:modelId.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): keep slots authoritative on every media path

- Workspace providers reach media, search and document services only at
  their preset's endpoints; a custom endpoint or proxy is deployment-only
  (403 INVALID_URL).
- A configured or turned-off document slot decides the extraction service:
  deprecated request fields may only pick a self-contained extractor, and
  legacy operator credentials are no longer reached.
- Request paths resolve their own workspace without following a claim;
  background extraction still does.
- A configured TTS slot keeps its own model; legacy pins apply only on the
  deprecated and default paths.
- Local transcription and agent voice registration keep the connection's
  network policy flags.
- The agent's web search forwards the whole resolved configuration.
- An unusable DEFAULT_IMAGE_PROVIDER leaves the image slot unassigned with a
  notice instead of switching vendors.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): public presets only for workspaces, plan default models

- A workspace preset whose default endpoint is on the server's own network
  (self-hosted TTS, ASR, image) is deployment-only, and a workspace
  provider's endpoint runs under the public-only policy.
- A provider-only reference to a token plan means the plan's own default
  model for that capability.
- On the legacy default provider, the request's image, video and ASR model
  still applies through its allowlist, and image/video without a model is
  still MISSING_MODEL.
- An asr assignment a workspace may not use no longer blocks document
  extraction, and a refused document service answers 403.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): keep legacy search and voice choices on their old paths

- Classroom search honours the provider and key a request names while the
  webSearch slot is unassigned; only /api/web-search prefers the operator's
  configured backend, as before.
- A TTS request's voice applies unless the request chose it for another
  provider.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): legacy search model and capability discovery errors

- On the legacy default search provider, the request's search model still
  applies through the server's pins.
- Capability discovery answers a refused credential (401) or a workspace
  service it may not use (403) instead of 500.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): classroom submission refuses a workspace service with 403

A classroom submission whose materials would go to a document or speech
service the workspace may not use answers 403 INVALID_URL instead of 500, and
its material check resolves the request's own workspace without following a
claim.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): workspace image and video providers run public-only

A workspace-configured image or video provider now uses the strict public
transport for its requests and for the redirects its clip download follows,
whatever ALLOW_LOCAL_NETWORKS says; the operator's own providers and the
deprecated per-request path keep their policies.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* Revert "fix(config): workspace image and video providers run public-only"

This reverts commit 68021ded. A workspace provider cannot choose an endpoint
for media, search or document services at all: a custom base URL or proxy is
refused, and so is a preset whose default endpoint is on the server's own
network. What remains is a preset's fixed public endpoint, the same one a
deployment default uses, so these calls keep the operator's transport policy
like every other preset endpoint, and the connection no longer claims a
user-typed endpoint (userEndpoint is false).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): /api/web-search without a provider searches as before

A deprecated web search request that names no provider again means the
server's configured provider, else the default one with the request's key,
while the webSearch slot is unassigned.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): browser speech recognition does not count for extraction

An asr slot assigned to speech recognition that runs in the browser gives
server-side extraction no transcription service, so audio uploads are not
advertised or accepted for extraction.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): /api/parse-pdf honours an explicit local parser

A request that asks for a self-contained extractor (local parsing) parses
the PDF locally and sends it to no document service, whatever the document
slot names, as /api/extract-document already did.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* test(classroom): give the persistence contract its media slots

The generated-classroom PostgreSQL contract configured its image and TTS
providers through the legacy provider mocks, which slot resolution no
longer reads; it now sets the deployment's slots.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(llm): streaming calls fall back on their slot's fallback (#1739)

* feat(llm): streaming calls fall back on their slot's fallback

A stream resolved through a slot that fails before any content (the request
is refused, or the first part is a retryable error) runs once on the slot's
fallback model. A failure after content has started still reaches the caller.
The outline stream keeps its own retry and fallback handling.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(llm): the stream fallback is the call's last attempt, before any content

- The primary's own SDK retries run first; the fallback runs once, as the
  last attempt, and a failing fallback is not retried.
- No fallback once content reached the caller in any step (a tool that ran
  must not run again); after a fallback took over, later steps stay on it.
- The fallback gets the thinking options built for its own provider and
  model, not the primary's.
- Usage of a stream with a slot fallback is recorded per step, against the
  model that served the step.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(llm): stream fallback recognises transient error payloads

Providers send a stream's error part as a plain { type, message } payload
rather than an error; a transient type (overloaded, rate limited, server
error) now counts as retryable for the slot fallback, while authentication
and request errors still do not.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(config): model settings API for workspaces (#1740)

* feat(config): model settings API for workspaces

GET/PUT /api/model-config read and edit a workspace's slots and providers:
every slot with its own assignment, effective model, source and lock state;
deployment providers read-only and without credential details; workspace
keys write-only and masked. Edits are checked against the whole
configuration and a revision. The view carries the preset catalogue a
workspace may add providers from, and each provider's models per capability,
so the settings UI needs no registry code of its own.

Workspaces cannot add Bedrock, self-hosted media/search/document presets or
custom endpoints for anything but chat. POST /api/model-config/import merges
settings a browser kept, item by item under the same checks, never replacing
what the workspace or deployment already has.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* refactor(config): preset ids as client-safe data

The preset id tables move to lib/config/preset-ids.ts, which imports no
registry, so browser code (the settings import) can name presets.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): tighten the settings API's views and checks

- Effective targets name an endpoint only for the workspace's own
  providers; a deployment's endpoints never reach a response.
- A workspace provider of a local model server preset (whose default
  endpoint is the server's own network) must name its own endpoint.
- Every change is checked against the stored shape, so an import skips a
  malformed item instead of failing the batch, and PUT validates its whole
  body (400, never 500).
- Clearing a key deletes it even when the instance can no longer open it.
- A workspace provider with its own endpoint offers chat models only, and
  an OpenAI-compatible provider offers only the models it lists.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): no credentials in endpoints; key-pair presets stay in the yml

- A workspace base URL cannot carry a username or password (they would be
  stored and shown in the clear), and views never show credentials a stored
  endpoint carries.
- Presets that authenticate with a key pair (AliDocMind) are not offered to
  workspaces: the settings take one key per provider.
- An import checks each proposed provider on its own, so one malformed
  provider is skipped instead of failing the batch.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): settings neither offer nor accept switched-off providers

A provider the operator switched off for a capability (the legacy
<CAP>_<VENDOR>_ENABLED=false switches) is left out of the capability lists,
refused as an assignment, and shown as invalid where a deployment assigns it,
as the calls themselves refuse it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): recommendations name only capabilities a preset still offers

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): a provider id follows the reference grammar before it is used

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): the catalogue lists the models a search provider offers

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* fix(config): refuse a fallback on a slot whose calls never use one (#1743)

* fix(config): refuse a fallback on a slot whose calls never use one

Only language-model calls retry on a slot's fallback; a fallback on a
speech, image, video, search or document slot was accepted and silently did
nothing. Resolution now refuses it by path, so openmaic.yml fails at startup
and the model settings refuse it on save.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): openmaic.yml refuses a non-chat fallback at startup

The boot check parses openmaic.yml without resolving slots, so the refusal
also lives in the file's cross-checks.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* feat(settings): Models section with the course model map (#1741)

* feat(settings): client for the workspace model settings

A small client for /api/model-config: it caches the view per page, applies
changes against the revision it read, reloads on a stale revision (409
CONFLICT) or a slot the deployment has since locked, and treats a server
without persistence (404) as settings managed by the server.

Pure helpers behind the settings UI live beside it: slot changes from the
card picker (follow, off, a model, a fallback, the media switches), the
provider form's change (keys stay write-only: keep, replace or remove),
the first-run setup that adds a provider and fills only the empty,
unlocked slots with its preset's recommendations, and the layout of the
course model map.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* feat(settings): Models section with the course model map

A new "Models" section, first in the settings dialog and the one it opens
on. It reads and writes everything through /api/model-config:

- The model map: a pannable, zoomable canvas with the course pipeline as a
  two-row serpentine flow, the default language model above the stations
  that inherit from it, and the page types under the content station. Each
  card shows the effective model, where it comes from and a lock when the
  server sets it. Solid edges follow the parent, dashed ones mark a
  setting of the slot's own.
- Editing happens in place: a picker at the card to follow the parent,
  pick a model a provider offers (or a provider, for search and document
  slots), turn the slot off, or set a fallback for chat slots. Media
  switches turn a slot off and back on.
- While no language model is configured, the default model's card offers
  a first-run setup: pick a service, give its key, and its recommended
  models fill every empty slot.
- A Providers tab lists the server's providers (read-only) and the
  workspace's own, which can be added, edited and removed as the server's
  policy allows.

The generation toolbar's "configure provider" prompt opens this section.
Below the sm breakpoint the settings nav becomes a strip above the panel.
Strings are translated for all 12 locales.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): keep what a change does not mean to touch

- A provider edit carries only the fields the form shows: a hidden model
  list or endpoint is left out, so the server keeps it; a shown field that
  is emptied is removed. A pinned model list keeps its field on edit.
- A key the server cannot read starts as "replace" (it can also be removed),
  so a key typed for it is sent instead of the broken one being kept.
- Switching a media slot off remembers what it held; switching it back on
  restores that assignment (or nothing of its own), and when that is not
  known the caller asks instead of clearing the slot to the default.
- The first-run assignments are checked against the provider as the server
  answered it: a provider with its own endpoint serves chat only, a model
  list the user gave wins over the recommended chat models, and `llm` is
  one of the provider's own chat models. The filling can be retried against
  a reloaded view, and a refusal keeps its reason.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): recoverable first-run, root clear action, keyboard on the map

- A first-run setup that added its provider but could not assign it (a
  stale revision, say) reports to the section, which keeps a notice with
  the provider and a way on (assign its models again, or add them under
  Providers) through any reload, instead of losing it with the form.
- The picker of a root slot with a setting of its own offers to clear it,
  leaving the server's value or default.
- A card's switch restores what the slot held; when that is unknown it
  opens the picker.
- Keyboard focus on a card outside the view pans the map to it, and the
  arrow keys pan the map while it has focus.
- The provider form offers only replace or remove for an unreadable key,
  and says that a provider with its own endpoint serves chat only.

Component tests drive the provider form, the switches, the root picker,
arrow-key panning and a first-run setup that meets a conflict.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): keep picker row labels whole; one unreadable-key notice

A long note no longer truncates the row's label in the slot picker, and the
provider form stops repeating the unreadable-key warning the row already
shows.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): a lost answer to a write is an outcome, not a throw

When the server takes a change but its answer cannot be read (a truncated
body, a dropped connection), apply() no longer rejects: it reloads the view
to reconcile a change that may have been saved and returns an `unconfirmed`
outcome with the reloaded view. The first-run setup goes on when the
reloaded view has the provider it added, counts a slot write whose answer
was lost as done when the reload shows the default model set, and says so
otherwise. Busy states in the provider form, provider removal, first-run
setup and its notice are reset in `finally`.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): keyboard roving in the slot picker

The picker's rows are plain buttons (pressed for the current choice) in a
group, not listbox options without the keyboard model those promise. The
list is one Tab stop, the current choice or else the first row; ArrowUp and
ArrowDown step, Home and End jump, Enter and Space choose. The picker opens
on that row. The picker's and the card switches' busy states are reset in
`finally`, and the component tests cover the lost-answer first-run paths
and the picker keyboard.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): a write lost in transport is unconfirmed, and first run can resume

A write whose request fails in transport may still have been saved, like
one whose answer is lost: apply() now reloads the settings and returns an
`unconfirmed` outcome in both cases, with the reloaded view when that read
worked. A first-run setup whose provider add cannot be confirmed (the
reload failed too) keeps a notice that says so, and "Check again" reads the
settings and either assigns the provider's models or says it was not added.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): retry an unconfirmed provider add under the same id

The add-provider form keeps the id it tried. When the answer was lost it
closes if the reloaded settings show that provider, and otherwise retries
under the same id, so a save that did land is updated rather than joined by
a second provider; a genuinely new add still gets a fresh id. Component
tests cover this and the first-run paths where the provider add fails in
transport after the server saved it, or cannot be confirmed at all.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): 5xx answers to writes are unconfirmed; reads never go back

A server error or a gateway timeout can come after a write was saved, so a
5xx answer to a write is treated like a lost answer: the settings are read
again and the outcome is `unconfirmed` with the reloaded view. A 4xx is
still a refusal, without a reload.

Reads and adopted write answers are numbered: a read's answer is dropped
when a later read started or a write's answer was adopted after it began,
or when its revision is older than the view held. The reads that must see a
write just made (after an ambiguous write, a conflict, "Check again") start
a fresh request instead of joining one begun before the write.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): first run is done only once the default model is set

A slot write that succeeds without setting `llm` (another session turned it
off meanwhile, so only media slots were filled) no longer counts as a done
setup: the notice stays and says the default model is still missing, for
the user to pick on its card. Test views now carry `llm` resolved the way
the server answers it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): the revision decides which settings view is newer

A view with a lower revision than the one held never replaces it, whether
it comes from a read or a write's answer, and one with a higher revision
always does, whenever it arrives; the order in which reads and adoptions
were numbered only breaks ties at an equal revision (and decides while no
view is held, so a read begun before the view was forgotten does not bring
it back). A write whose answer is older than a view read meanwhile returns
the view that is current. `adopt` takes a view or null (forget it) and is
part of the client.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): send each change against the view it was worked out from

apply() takes the view a change was computed from and sends that view's
revision, rather than the revision of whatever view is held when the write
goes out. A retry of the first-run assignments that waits for a reload in
flight is therefore refused (409) when the reload shows the settings
changed, instead of overwriting a slot set meanwhile; the reload then feeds
the next attempt. The slot picker, the card switches, the provider form,
provider removal and the first-run setup all pass the view they showed.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): a provider edit sends only what changed, and rebases on a conflict

The provider form keeps the basis of an edit: the provider as the edit
began and the view it came from. A save sends only the fields changed
against that basis (a key-only edit sends the key), against the basis
view's revision. When the provider changed elsewhere meanwhile (409), the
edit moves onto the reloaded provider, keeping only what the user changed,
and the form says the provider changed before it is saved again. A 409 now
returns the reloaded view to work the change out again from.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): a refused provider add keeps its draft and picks a free id

Only an add whose outcome is unknown (a lost answer, a transport failure, a
5xx) is reconciled by looking for its id in the reloaded settings. A
confirmed refusal (a 409, another tab having added the same preset under
the same id meanwhile) saved nothing of ours: the form keeps the draft,
shows the conflict, and the retry uses an id still free in the reloaded
view.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

* refactor(settings)!: server-side model settings only; import browser settings once (#1744)

* feat(settings): one-time import of browser model settings

The settings store's migration to version 5 builds an import proposal
from the provider state earlier builds kept in the browser (keys, custom
endpoints, the chosen model, token plan enrollment, per-capability
selections) and keeps it under its own localStorage key. Once the store
has hydrated, the proposal is posted to /api/model-config/import: a 2xx
answer removes it (and the keys) from the browser, 400 drops it, and
anything else keeps it for a later load. Per-stage routes are not
imported. Clear Local Cache keeps a proposal still waiting.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* refactor(settings): stop sending provider data from the browser

Every request now leaves model and provider choice to the server, which
resolves it through the workspace's capability slots: no model, key or
base URL headers (x-model, x-api-key, x-model-routes, x-image-*,
x-video-*), no provider, key or thinking fields in chat, TTS, voice
registration, transcription, web search or document extraction bodies.
The server keeps accepting them until they are retired.

What the client still needs to know is read from the /api/model-config
view (lib/model-settings/capabilities.ts): whether a language model is
set up, which provider the tts slot names (browser speech plays locally;
voice lists follow that provider), whether speech input, image, video
and web search are available, and the course model the toolbar shows or
edits through the settings API. The scene concurrency comes from
/api/health. The unused TTS config popover and getCurrent*Config
helpers are removed.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* refactor(settings)!: remove the browser provider state and its settings UI

The settings store keeps only the user's own preferences (playback,
narration voice and speed, speech input language, outline review,
agents, layout). Providers, keys, base URLs, the model choice, thinking
settings, per-stage routes, token plan enrollment and seeds, the
per-capability provider configs and selections and their on/off
switches are gone; the version 5 migration sets them aside for the
one-time import and drops them. The narration voice now records the
provider it was picked for and applies while the tts slot names it.

The Token Plan, Model Services and Course Model sections and their
components are removed, with apply-token-plan, the server provider sync
(ServerProvidersInit, fetchServerProviders) and helpers only they used.
A Voice section keeps the per-user parts of the old speech settings:
speed, a narration test, the VoxCPM and Qwen voices, and the speech
input language, showing which services the workspace uses. The home
toolbar picks the course model through the settings API, or shows it
read-only when the deployment locks it.

e2e fixtures answer /api/model-config instead of seeding browser
providers; the managed-provider spec, which covered the removed panel,
is removed.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* feat(settings): browser speech recognition while the asr slot is unassigned

Speech input worked out of the box through the browser's own recognition,
which needs no server provider; it stays available while the asr slot is
unassigned, and turning the slot off turns speech input off.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): bind the model settings import to its owner and never lose staged keys

The import now asks for the browser's legacy import binding and sends
X-OpenMAIC-Legacy-Import, so owner resolution refuses it for any owner
that does not hold the browser (409 LEGACY_IMPORT_NOT_BOUND keeps the
proposal for a later load); the import route joins FENCED_ENDPOINTS.
Its completion is the proposal's own key, apart from the course ledger.

Staging reports whether it succeeded. When the proposal cannot be
written (a full storage, an unreadable proposal waiting), the migration
keeps the old settings in legacyModelSettings and every load retries,
writing the store back without them once staged. Nothing logged quotes
the proposal or an error message: fixed text, item ids, error names.

Older shapes are normalised before the proposal is built (version 0
default model, the single TTS model setting, global TTS/ASR model ids,
a TTS provider's model field, the flat web search key). Capabilities
the user turned off are proposed as off (null), and selected
server-configured media providers are named by their preset id.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): retry a failed read of the model settings

A failed read of /api/model-config with nothing to show is read again
with a backoff (2 s up to a minute) until one succeeds, instead of
leaving the page without capabilities for the rest of its life.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): send no provider or model with voice registration

Voice registration, deletion and auto-registration no longer send
providerId or ttsModelId: the server registers with the provider and
model the tts slot resolves to. The model still derives the voice id
and keys the session memo. The unused OpenRouter model list hook, which
called the vendor with a browser key, is removed.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): carry only an explicit speech input off into the import

Only `asrEnabled: false` becomes an off slot (`asr: null`): without an
asr slot the browser's own speech recognition would take over, which the
user had turned off. The TTS, image, video and web search switches were
per-browser toggles that availability following the slots replaces on
purpose; turning them into lasting workspace nulls would override the
deployment's defaults from then on, so they are not carried over.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): gate chat and generation on the slots they resolve

Chat and discussion resolve the classroom slot, and course generation
its outline, actions and content slots; each is now allowed whenever
those resolve to a model, even with the llm root unassigned or off
(a child assigned on its own). Settings not read yet still block
nothing. The toolbar offers "Set up model" only when a course cannot
be generated.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): import models the user added to built-in providers

A built-in chat provider whose model list held models the user added
(ids not in its catalogue) is proposed with those models, listed after
the catalogue's: a provider's model list names the chat models it
serves, so listing only the added ones would hide the catalogue.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): wait for the commit explicitly in the media overlap test

The overlap test counted 50 microtasks for the mocked commit to be
reached; with the capability read before each pass that is no longer
enough, so the test failed alone and left a pass running into the next
test. It now awaits a signal from inside the commit, flushes every
pending microtask before asserting, and releases and awaits both passes
in `finally`.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): import models the user added to an enrolled token plan

An enrolled plan's chat provider whose model list held models the user
added (ids not in the plan's own list) is proposed with them, listed
after the plan's, by the same rule as built-in providers.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): scope voice registration memos to the tts slot's provider

The session memo and in-flight map of auto-voice registration were keyed
on the voice and model only, so after the tts slot moved to another
backend serving the same model, registration was skipped and synthesis
named a voice that backend never registered. They are now scoped to the
provider the slot resolves to (provider id, registry entry, endpoint)
and the settings revision, captured once per registration.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): show the view the model settings import produced

After a successful import the page read the settings again, but that
read could join the page's first read, still in flight from before the
import, and leave the unassigned view in place. The import now hands
over the view the import route answered, and adoptNewerView lets any
read in flight finish before keeping whichever view is newer by
revision, so an older answer cannot land over it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): offer and resolve voices against the tts slot's model

With the tts slot on a model that cannot speak some voices (an OpenAI
slot on tts-1 and Marin or Cedar, which need gpt-4o-mini-tts), the
picker still offered them and synthesis on the slot's model failed.
The slot's model (its own, else the provider's default) is now the
model voices are offered under and checked against: the voice lists
hold only voices it can speak, a persisted voice it cannot speak falls
back to a compatible default, and narrator and agent bindings to such
a voice are not used.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): drop translations only the removed provider panels used

208 keys that only the removed provider settings (model services, token
plan, course model config, their dialogs and the TTS popover) used are
removed from all 12 locales: API key and base URL fields, provider and
model editors, connection tests, per-capability switches and the like.
Each was checked to have no remaining reference, literal or through a
key prefix built at run time. The TTS enablement locale test keeps the
key still in use.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(config): provider options in openmaic.yml, passed to the TTS adapters

A provider in openmaic.yml may carry `options`: non-secret,
provider-specific settings (a map of names to strings, numbers or
booleans; `${VAR}` interpolation applies). They reach the resolved
slot target, the media connection and the settings view, and the
server's TTS paths (the TTS and voice routes, scene narration, classroom
media generation, the voice-clone tools) hand them to the adapter as
its providerOptions: over a request's options for a configured slot,
under them while the slot is unassigned (the deprecated path). Voice
registration follows them too (a VoxCPM backend without runtime
registration is refused). Workspace providers cannot set options: they
are the deployment's. The legacy configuration had no equivalent.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): read the VoxCPM backend from the tts slot's options

The voice settings, the voice lists and auto-voice registration assumed
the default VoxCPM backend once the browser no longer chose one. They
now read the `backend` option of the provider the tts slot resolves to
(shown in the settings view), and the registration memo is scoped to
the provider's options as well.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): label the preset choice when adding a provider

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): media planning from the slots; stop when settings are unread

The outline route decided whether to plan images and video from the
client's x-image-/x-video-generation-enabled headers, and the client
sent them from settings it might not have read: a course could be
generated silently without media. The route now reads the workspace's
image and video slots itself (an explicit `false` header still lets an
API client opt out; `true` turns on nothing), and the client no longer
sends them.

When the model settings cannot be read even after another try,
generation stops with a message instead of leaving out narration (the
scene fails and generation pauses; the preview's first scene errors),
and a media pass or retry stands down without marking anything as
disabled.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EF6G824rLqUXidRrqrMskR

* fix(settings): pick the course model when none is set

Without a default model the toolbar showed no picker, so the course
model could only be set in Settings. It now offers the picker whenever
the workspace may set the llm slot and chat models exist, with nothing
selected until one is picked (which sets the slot; the server assigns
noth…
- [apple/swift-service-discovery](https://github.com/apple/swift-service-discovery) [2](https://github.com/apple/swift-service-discovery/commits): Bump minimal Swift tools version to 6.2 (#88)

The support window is 3 latest minor Swift versions. CI i already
running for Swift 6.2, 6.3 and 6.4 only. Updating the Swift tools and
the package to match this.
- [astral-sh/ty](https://github.com/astral-sh/ty) [2](https://github.com/astral-sh/ty/commits): Add a daily ty fuzzing workflow (#4643)
- [huggingface/lerobot](https://github.com/huggingface/lerobot) [2](https://github.com/huggingface/lerobot/commits): refactor(dtype): unify the dtype configuration of policies (#4786)

* feat(configs): make PreTrainedConfig.dtype a real torch.dtype

`dtype` was a bare string that every policy had to convert back into a
`torch.dtype` at its own call site. Nine such converters had drifted apart:
they disagreed on which dtypes they accepted and on what an invalid value
does — `ValueError`, `KeyError`, or a silent fall-through to a different
precision. Nothing in the base class owned the conversion, so each new
policy reinvented it.

Declare the field as `torch.dtype | None` and teach draccus the type once,
through the codecs registered on `PreTrainedConfig`. The on-disk form is
unchanged: `config.json` still stores the plain name `"bfloat16"`, and
`--policy.dtype=bfloat16` still works, so no checkpoint changes shape.
Names resolve against `torch` itself rather than a hardcoded allow-list,
so aliases such as `half` and any dtype a future torch release adds are
supported for free. Strings remain a serialization detail — the Python
API takes the `torch.dtype`.

Per-policy dtype restrictions are kept, with their literals translated;
they encode which precisions a policy was actually validated at, which the
base class cannot know. MolmoAct2's optimizer grouping, for one, still
assumes parameters are either bf16 or not.
- [ophub/amlogic-s9xxx-armbian](https://github.com/ophub/amlogic-s9xxx-armbian) [2](https://github.com/ophub/amlogic-s9xxx-armbian/commits): Merge pull request #3704 from FragrantOrchid/main

Provide support for fan of rk3576-lckfb-tspi-3m by using dtbo file.
- [V1EngineeringInc/V1EngineeringInc-Docs](https://github.com/V1EngineeringInc/V1EngineeringInc-Docs) [2](https://github.com/V1EngineeringInc/V1EngineeringInc-Docs/commits): Merge pull request #648 from V1EngineeringInc/zen3

add belt info
- [Alishahryar1/free-claude-code](https://github.com/Alishahryar1/free-claude-code) [1](https://github.com/Alishahryar1/free-claude-code/commits): minor: add Anthropic API provider with native Messages routing (#1967)

## Why

FCC needs direct Anthropic API access. Messages clients selecting
Anthropic should retain native tools, content blocks, thinking controls,
and response fields, including when they count conversation history
before continuing it.

## How

- Add an Anthropic provider with an API key, optional Workspace ID and
proxy, paginated model discovery, per-model conversion capabilities, and
a non-generating credential check in the standard provider modal.
- Select the native Messages contract before compatibility parsing and
local processing. Preserve native JSON and SSE payloads, replace gateway
credentials with configured upstream credentials, and retain public
model aliases.
- Accept native histories and complete tool definitions in local token
estimation. Counts remain approximate and require no upstream request.
Compatibility requests retain their existing schema and counting rules.
- Discard valid pings received before `message_start`, preserving
bounded retries and native fallback before commitment. Commit and relay
immediately at `message_start`, with no subsequent retry or fallback.
Pre-start pings do not extend the existing terminal progress deadline.
- Reuse admission, generation leases, cleanup, and candidate execution.
Native fallbacks are limited to other Anthropic models.
- Use client controls and Anthropic-hosted tools for native requests.
Use FCC protocol conversion for Responses input and compatibility
requests that fall back to Anthropic.
- Document separate API billing, native settings behavior, and fallback
limits in provider help and the README.



<!-- greptile_comment -->

<!-- greptile_summary -->

<h2><a
href="https://app.greptile.com/api/retrigger?id=73272006"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source
media="(prefers-color-scheme: light)"
srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img
alt="Retrigger"
src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"
align="right"></picture></a>Confidence Score: 5/5</h2>

<!-- greptile-risk -->

No outstanding findings block merging.

<details open><summary>Summary</summary>

The PR adds a directly billed Anthropic provider and native Messages
routing. The current code suppresses leading upstream pings until a
message starts and accepts opaque native content blocks for token
counting. Both previously reported issues are fixed.
</details>

<!-- greptile_confidence_score:5 -->

<sub>Reviews (2) · Last reviewed commit: ["fix: preserve native counting
and
pre-st..."](https://github.com/alishahryar1/free-claude-code/commit/58b92a66f61f0aef80c82008f8a08f7155d54d91)</sub>

<!-- /greptile_comment -->
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) [1](https://github.com/anthropics/claude-agent-sdk-python/commits): chore: bump bundled CLI version to 2.1.288
- [anthropics/claude-code](https://github.com/anthropics/claude-code) [1](https://github.com/anthropics/claude-code/commits): chore: Update CHANGELOG.md and feed.xml

Fixes #73861
Fixes #93672
Fixes #96300
- [apple/swift-log](https://github.com/apple/swift-log) [1](https://github.com/apple/swift-log/commits): Bump minimal Swift tools version to 6.2 (#518)

The support window is 3 latest minor Swift versions. CI i already
running for Swift 6.2, 6.3 and 6.4 only. Updating the Swift tools and
the package to match this.
- [Automattic/simplenote-android](https://github.com/Automattic/simplenote-android) [1](https://github.com/Automattic/simplenote-android/commits): [Tooling] Fix instrumented tests (#1886)
- [bufbuild/buf](https://github.com/bufbuild/buf) [1](https://github.com/bufbuild/buf/commits): Read Windows CI generator versions from make/go (#4712)
- [espressif/esp-matter](https://github.com/espressif/esp-matter) [1](https://github.com/espressif/esp-matter/commits): Merge branch 'swap_network_type' into 'main'

components/esp_matter: set network type based on feature map

See merge request app-frameworks/esp-matter!1692
- [GameTec-live/ChameleonUltraGUI](https://github.com/GameTec-live/ChameleonUltraGUI) [1](https://github.com/GameTec-live/ChameleonUltraGUI/commits): feat: Update translations (#1017)
- [iandchasse/silkscreen-pcb](https://github.com/iandchasse/silkscreen-pcb) [1](https://github.com/iandchasse/silkscreen-pcb/commits): Rev 1.01: R84 USB hot-plug damper, JLC placement corrections, docs

- R84, 1 ohm 0603 (Yageo RC0603FR-071RL; JLC C22936, Basic) in series with
  C2's ground leg. It damps the ringing an already-live USB-A source causes
  at plug-in: the modelled worst case on U2 VIN1 falls from 7.95 V to 5.60 V.
  No DC current flows in it. One GND stitching via below the cut line moved
  to make room (a board trimmed at y 62 still shows 0 unconnected); the CHRG
  track is nudged 0.2 mm.
- FT Rotation Offset (U2, U5, D2, D8) and FT Position Offset (J7, J4, U4)
  fields on the symbols and footprints, so every Toolkit run writes
  positions.csv rows that match JLC's library footprints.
- Bottom silkscreen notes enlarged; R83, R67 and C3 reference texts moved;
  D3's description reads 26.0 Vr.
- production/ regenerated (zip SHA-256 5b819f11..., 166 placed parts, 67
  LCSC codes) and checked: DRC 0 unconnected / 0 parity, Gerbers and drills
  match a fresh kicad-cli export as shape sets, netlist.ipc matches a fresh
  IPC-D-356. jlc_bom.csv, part_fields.csv and other_fabs updated; schematic
  and layout PDFs re-plotted.
- Docs: README, HARDWARE.md (hot-plug in section 3.1), DESIGN_REVIEW.md,
  fabrication README/BOM/NextPCB notes, the 2026-09-30 audit banner and
  BRING_UP section 3.2. New docs/LED_ALT.md: the TPS923610 alternate-driver
  study.
- [mattt/iMCP](https://github.com/mattt/iMCP) [1](https://github.com/mattt/iMCP/commits): Bump version to 1.6.2 (#255)
- [merbanan/rtl_433](https://github.com/merbanan/rtl_433) [1](https://github.com/merbanan/rtl_433/commits): build: Remove macos-14 from github actions
- [meshtastic/python](https://github.com/meshtastic/python) [1](https://github.com/meshtastic/python/commits): fix up protobuf generation for some 2.8.1 changes
- [OpenEPaperLink/OpenEPaperLink](https://github.com/OpenEPaperLink/OpenEPaperLink) [1](https://github.com/OpenEPaperLink/OpenEPaperLink/commits): Update D0.json
- [OpenStickCommunity/GP2040-CE](https://github.com/OpenStickCommunity/GP2040-CE) [1](https://github.com/OpenStickCommunity/GP2040-CE/commits): Pico PIO USB Update (#1698)

* Pico PIO USB Update

* Fix hub hot-replug with upstream Pico-PIO-USB

Upstream 5a37a66 breaks re-enumeration of devices behind a USB hub after a
hot unplug/replug (PS4 auth dongles authenticate at boot, then never again
after being replugged through the hub). Root-port replug is unaffected.

Bisected on hardware (Haute42 COSMOX M-Lite, hub + PS4 auth dongle):
the regression is sekigon-gonnoc/Pico-PIO-USB 30283a9 ("Fix pre packet"),
specifically moving the RX state-machine enable from
pio_usb_bus_start_receive() (after the host's TX) into
pio_usb_bus_prepare_receive() (before it). 65708d3 passes, 30283a9 fails on
the first replug, and reverting only that enable placement passes; the other
two changes in that commit are innocent.

lib/pico_pio_usb now points at upstream 5a37a66 plus one commit that moves
the enable back after TX (device mode enables explicitly at init, so it is
unchanged). It lives on a personal fork (speedypotato/Pico-PIO-USB, branch
fix-rx-enable) pending the upstream PR against sekigon-gonnoc; maintainers
may prefer to mirror it to OpenStickCommunity/Pico-PIO-USB.

The single-PIO layout and the NeoPico move to PIO1 from the previous
revision are kept; they were verified not to be the cause (the failure
reproduces identically with the two-PIO layout).

Refs: sekigon-gonnoc/Pico-PIO-USB#149, hathach/tinyusb#2971

* Bump pico_pio_usb: second hub hot-replug fix (streaming devices)

The previous bump fixed hub hot-replug for idle devices (PS4 auth dongles).
Devices that transfer every frame (PS5/P5General controllers) still failed
to come back after being unplugged from a hub: the hub's port-change report
was never received, so no unmount/mount and no re-authentication.

Bisected on hardware to sekigon-gonnoc/Pico-PIO-USB 9be1f3e, which made
pio_usb_bus_start_receive() a header inline and added a read-back spin on
the RX IRQ flags. Restoring the pre-9be1f3e shape (out-of-line RAM function,
single flag write) fixes it. Both fixes together: PS4 dongle and P5General,
direct and through a hub, 10/10 replugs each on a Haute42 COSMOX M-Lite.

lib/pico_pio_usb -> speedypotato/Pico-PIO-USB fix-rx-enable @ ba9733c
(upstream 5a37a66 + 2 commits).

Refs: sekigon-gonnoc/Pico-PIO-USB#149

* fix(p5general): Filter host reports and time out lost completions

report_received() captured the next input report from any HID device
into hash_finish_buffer, which P5GeneralDriver then forwarded to the
console as the signed hash. With other dongles or controllers on a
hub, their reports were sent instead of the P5General's, so console
auth succeeded only intermittently. Only accept reports from the
bound dongle's dev_addr/instance.

The listener also advanced its state machine and cleared hash_pending
even when the tuh_* transfer was rejected (the host has a single
shared control slot), and P5GeneralDriver only accepts a new console
request while the listener is idle. A rejected or lost completion
(USBHostManager drops len == 0 failures) therefore left the listener
in a *_wait state, ignoring every later console request until replug.

- Advance state only when the transfer was actually queued.
- Return to idle after 500 ms in any *_wait state. A late completion
  is still ignored because each handler only acts in its matching
  wait state. Handling every enumerator also clears the -Wswitch
  warnings on this switch.

* fix(usbhost): Raise HID interface and device limits

CFG_TUH_HID caps HID interfaces across all devices, not devices. Auth
dongles often expose more than one HID interface, so a hub with four
dongles could exhaust the pool; find_new_itf() then returns NULL and
the surplus interface is silently never mounted, leaving the needed
dongle unavailable depending on enumeration order.

Raise CFG_TUH_HID from 4 to 8 and CFG_TUH_DEVICE_MAX from 4 to 6 so a
full 4-port hub fits with headroom for a dongle that re-enumerates
before its old address is released. Cost: ~1 KB of RAM (bss 140292 ->
141320 on Haute42COSMOXMLite).

* fix(ps4): Recover PS4/PS5 USB auth from lost transfers

The listener set awaiting_cb before issuing each GET/SET_REPORT and
ignored the result. When the transfer could not be queued (the host
has a single control slot, busy with the hub or other devices, or the
dongle had gone), or when it failed and USBHostManager dropped the
len == 0 completion, awaiting_cb stayed set and auth stalled until the
dongle was replugged.

- Only wait for a completion when the transfer was queued, and only
  advance nonce_page / nonce_chunk once their transfer is queued, so a
  rejected call is retried on the next pass.
- Time out a completion after 500 ms and restart the dongle exchange.
- Ignore completions that arrive when none is awaited. A defensive
  range check on nonce_chunk is added before indexing ps4_auth_buffer;
  it is not reachable with the single host control slot.
- On a signing error (state byte 1), abandon the nonce and wait for the
  console's next one instead of polling forever.
- Parse up to 32 report-descriptor entries when detecting a dongle; a
  full DS4-style descriptor lists 0xF3 well past the first four.

* chore(cmake): Fix ENV{CI} check for CMake 4.x

The optional Custom.cmake include tested `DEFINED ENV(CI)`, which is
not valid CMake syntax; environment variables use braces. Older CMake
tolerated it, but CMake 4.4 rejects the if() expression and configure
fails with "Unknown arguments specified".

* feat(ps4): Track dongle candidates; rebind on unplug, rotate on failure

The PS4/PS5 USB auth listener bound the first PS4-family (0xF3) dongle
and ignored every other one, so with several dongles on a hub the rest
were never used, even after the bound one was unplugged or stopped
responding.

- Remember every PS4-family dongle interface seen in mount(). When the
  bound dongle is unplugged, bind another one that is still connected.
- When the bound dongle fails repeatedly (3 consecutive completion
  timeouts, or 2 consecutive signing errors), bind the next connected
  dongle, skipping other interfaces of the same device. If the
  console's nonce is still intact the new dongle takes it immediately;
  otherwise wait for the console's next round. Each other dongle is
  tried at most once per console nonce, so two dead dongles cannot be
  rotated between forever.
- With nothing left to try, stop re-sending the current nonce and
  return to auth_idle_state until the console starts a new round,
  instead of retrying a wedged dongle every 500 ms.
- Wait 10 ms before re-polling PS4_GET_SIGNING_STATE after "not
  ready" instead of polling back-to-back.
- Request PS4_DEFINITION from process() for each newly bound dongle
  rather than from bind(): when bind() runs from unmount(), TinyUSB
  still holds the control slot for the removed device.
- Do not re-send the nonce after a timeout during signature readback;
  ps4_auth_buffer is already partly overwritten with signature data.
- static_assert that PS4_MAX_DONGLE_CANDIDATES covers CFG_TUH_HID.

The first dongle to enumerate is still the one bound at boot, and a
dongle that signs successfully but is rejected by the console (e.g. a
PS4-only dongle in PS5 mode) is not detected.

* build(tinyusb): Upgrade TinyUSB to 0.21.0

Move lib/tinyusb off the OpenStickCommunity fork of 0.17.0 to upstream
TinyUSB 0.21.0 plus one patch, on speedypotato/tinyusb
gp2040/0.21-ctrl-timeout:

- host: add control transfer timeout (upstream still has none, and
  Pico-PIO-USB retries NAKs forever, so one device NAKing a control
  request could stall the whole host).

Upstream now queues control transfers requested while the slot is
busy, releases a still-enumerating device when its port or hub is
removed, and drops stale control completions, which covers the rest of
the previous fork-only host fixes.

The OSC fork patches are no longer needed: interval override, host
SOF callback and the ep0 size fix only touch hcd_rp2040 (GP2040-CE
hosts on Pico-PIO-USB), and the device SOF callback and
tuh_get_hub_addr_port() are unused. "Don't force boot protocol" is
intentionally dropped: it reported every HID interface as
HID_ITF_PROTOCOL_NONE, which kept KeyboardHostListener (which expects
boot keyboard/mouse reports) from ever mounting a device.

API changes in 0.21:
- usbd_edpt_xfer() takes an is_isr flag; all callers run in task or
  transfer-callback context, so pass false.
- Host class driver open() returns the number of descriptor bytes it
  consumed instead of bool (xinputh_open).
- CFG_TUD_NET_ENDPOINT_SIZE was removed; define the full-speed bulk
  endpoint size in NetDriver.
- XInputDescriptors.h now includes <cstdio> for sprintf, previously
  pulled in transitively.

Remove lib/PicoPeripherals/interval_override.*, which only existed to
satisfy the OSC hcd_rp2040 patch.

* refactor(usb): Use tusb_init() for device and host stacks

tud_init() and tuh_init() are deprecated in TinyUSB 0.21 in favour of
tusb_init(rhport, rh_init) with an explicit role. Behaviour is
unchanged: device on TUD_OPT_RHPORT, host on BOARD_TUH_RHPORT, both
at auto speed.

---------

Co-authored-by: speedypotato <speedypotato@users.noreply.github.com>
- [tidwall/tg](https://github.com/tidwall/tg) [1](https://github.com/tidwall/tg/commits): Align multilinestring boundary expectations with GEOS (#31)
- [Y2Z/monolith](https://github.com/Y2Z/monolith) [1](https://github.com/Y2Z/monolith/commits): Add a Debian install method via the pkg.haus APT archive