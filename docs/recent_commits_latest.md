# Recent Activity in Starred Repositories
_157 active repos with 4126 new commits_

## [ai](https://github.com/topics/ai)
- [openclaw/openclaw](https://github.com/openclaw/openclaw) [1074](https://github.com/openclaw/openclaw/commits): fix(ui): place the new-session row in its sidebar destination (#174888)

The provisional row shown while the Gateway admits a new session rendered
above the whole session list, outside agent roster groups and with its own
inset, so a nameless blob appeared between the toolbar and the list and then
jumped into place. Render it at the top of the native list, or under its
agent in the roster, with the same lead column as real rows.

Co-authored-by: Patrick-Erichsen <20157849+Patrick-Erichsen@users.noreply.github.com>
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) [703](https://github.com/NousResearch/hermes-agent/commits): Merge pull request #140203 from NousResearch/merge/record-v0.22.2-ancestry

v0.22.2 installs fast-forward to main (record v0.22.2 as an ancestor, #139099)
- [BasedHardware/omi](https://github.com/BasedHardware/omi) [159](https://github.com/BasedHardware/omi/commits): config(capture): observe shared speech on Cloud Run only (#21930)

Enable deterministic shared-speech shadow evaluation on the four
production Cloud Run processing services: backend, backend-sync,
backend-sync-backfill and backend-integration. Set
`CAPTURE_SHARED_SPEECH_MODE=shadow` and
`CAPTURE_SHARED_SPEECH_PERCENT=100` at those service overrides only. The
UID allowlist stays empty. Shadow preserves incumbent grouping and adds
bounded evaluation with identifier/numeric decision logs.

Pusher and backend-listen retain their off default and receive the
implementation through their regular release train. No account is
activated in on mode. Existing groups, transcripts, memories and effects
retain their existing behavior. Jev and smart merge settings are
unchanged.

This follows #21882 and the explicit-off rollback baseline #21931
(merged8b24990a68bd00539d36ed5f09f2e12d7e80047d), under David's
coordinator-authorized Cloud Run dark → shadow qualification. The
feature completed five read-only agentctl codex/gpt-6-luna review
rounds, with no final feature blockers. A sixth read-only review of the
explicit-off baseline and its safe YAML test-loader repair found no
P1/P2 issues; that unchanged code is now in main. This PR changes
literal configuration/rendered documentation only and leaves that
reviewed implementation unchanged; the coordinator requires another Luna
review only for material code changes. Calibration remains insufficient
for activation: David TP4/13 and FP0/6; September benchmark TP1/56 and
FP0/40, with zero held-out positives accepted. After deployment, watch
at least15minutes against the predeploy baseline and compare at
least3hours of shadow decisions to the incumbent using counts only.

Validation: regenerated the canonical runtime manifest and feature-flag
registry. Removing exactly the eight authorized Cloud Run fields
reproduces both prior parsed source and compiled manifests; dev/GKE/all
other settings are identical. Runtime-env preflight passed315tests; PR
preflight passed20checks, and the normal push gate passed. Exact-head CI
at48a1bb2890ba4e2ece1197a53de270f3585f88cb completed32successful checks
and25automatic out-of-scope skips, with no failure/pending/cancellation;
re-check after a fresh main fetch before merging. Deploy through
`bin/omi-deploy-prod wait-eligible` then `cloud-run`, approving only
this owner's run. The actual eligible explicit-off rollback source is
now `aa87e9fe37f12a55978b8567db9d41fa28a6ce39` (contains #21931 plus
current Firestore controls and queued-epoch repair), served100% on
allfour via regulartrain
[38976700010](https://github.com/BasedHardware/omi/actions/runs/38976700010).
Its exact normal-workflow rollback commands are written before any
shadow dispatch; the owner did not dispatch or approve that other
operator’s train. An older release that omits the keys does not reset
shadow because the deploy action merges environment variables. The
explicit-off watch22:56–23:11UTC completed with5minute ingestion grace,
complete queries, allfour explicitoff/0/emptyallowlist, and zero matcher
activity/errors. Allfour overall5xxrates were below the recent baseline
(backend0.0127%vs0.0219%;sync0.0473%vs0.0511%;backfill1.2653%vs1.5431%;integration0.0159%vs0.09%).
Backfill remains degraded. A separate memory-search timeout
burst8/9requests occurred in the first5minutes with no later requests on
that route; predeploy had0requests, so causality cannot be established
and recovery is not claimed. This concern remains tracked; sampled
traceback module frames did not implicate new shared-speech modules.
Owner assessment qualifies bounded non-mutating Shadow with the
exactOffrollback ready, while retaining those concerns in the watch.
Never enableOn. Full timings, revisions and aggregate watches are
recorded in the task report.

## Product invariants affected

- [INV-MEM-4](product/invariants/memory-promotion-authority.md):
canonical promotion remains the sole Long-term admission authority.
Regeneration preserves every memory intake, consolidation, promotion,
scheduler and projection setting. The only runtime changes are eight
shared-speech shadow literals on four Cloud Run services; shadow
performs no new group or memory writes.

Failure-Class: none

This is non-mutating rollout configuration with no new failure-class
implementation.
- [unslothai/unsloth](https://github.com/unslothai/unsloth) [96](https://github.com/unslothai/unsloth/commits): Studio: read whole-GPU uuid masks from nvidia-smi rows and cache the MIG set (#14017)

## Problem

Two ordinary-host regressions came in with the Studio MIG change
(#13927), both on hosts that have no MIG at all.

A valid whole-GPU UUID mask was treated as unresolved in the llama.cpp
memory probe whenever the ordinal resolvers could not map it. That
happens under `CUDA_DEVICE_ORDER=FASTEST_FIRST`, since those resolvers
only trust UUIDs under `PCI_BUS_ID`. It also happens when the separate
`index,uuid` query fails while the memory query succeeds. Either way the
successful nvidia-smi rows were thrown away. With NVML unavailable the
probe then fell through to `torch.cuda.mem_get_info`, which creates a
CUDA context, or reported no GPU when torch was absent. The embedding
server's auto GPU check reads this result, so it could switch to CPU.

Every successful NVIDIA memory probe and every auto selection also
called `get_mig_gpu_indices()`. Each call resolved the nvidia-smi path,
copied the child environment, went through the query wrapper and parsed
`nvidia-smi -L`. That cost was added to the VRAM settle poll loop on
every host.

## Fix

The memory probe now asks for `index,memory.free,memory.total,uuid` in
one nvidia-smi call. A whole-GPU UUID mask that the ordinal resolvers
cannot map is matched against those UUIDs. A UUID names its card under
any device order, so this needs no second query and no CUDA ordering.
When nvidia-smi gives no UUID column, the mask is checked with the
separate UUID query and stays unresolved if that cannot verify it. When
auto fit picks a subset of such a mask, the child is pinned to those
cards' UUIDs (whole cards only, never a MIG card) instead of keeping the
whole inherited mask, and a reordered mask orders the child the same way
a numeric mask already did (Unsloth's tensor split is moved with it; a
pass-through split keeps ascending order). MIG masks, unknown UUIDs and
repeated tokens still skip the whole-card rows, so the conservative MIG
handling is unchanged. The numeric-prefix resolver now runs only after
the in-row UUID match, so a UUID mask no longer triggers the extra
`index,uuid` query here.

The MIG set is one small cache entry with a simple rule: every
`nvidia-smi -L` probe takes a sequence number when it starts, and only
the latest-started probe of the current gpu_query static generation may
replace the entry, whatever its outcome. A good answer lives for
gpu_query's static TTL from the moment its listing was taken (60 seconds
by default, `UNSLOTH_GPU_QUERY_STATIC_TTL` honoured, including 0). A
failed, empty, superseded or invalidated listing is "unknown" and is
retried after at most 5 seconds. `get_mig_gpu_indices_or_none()` returns
None while discovery is unknown and a set (empty only for a real "no
MIG" answer) otherwise; `get_mig_gpu_indices()` keeps returning an empty
set for unknown. The physical GPU count probe already runs `nvidia-smi
-L` and publishes through the same path, so a warm memory poll is a
generation and age compare with no subprocess and no lock.

Placement uses the unknown-aware lookup: when discovery is unknown it
reads NVML (slice for a MIG card, the same reading for a whole card),
and when NVML also has nothing it keeps the CLI rows and clears any
cached NVML rows, without touching CUDA. A CLI answer with no MIG cards
also retires cached NVML rows. A UUID mask is cut at its first empty
entry, as CUDA reads it, and without a uuid column only a one-card mask
resolves. UUID subset pinning uses the MIG classification the memory
probe recorded with its uuid rows, so a later failed or uncached recheck
cannot widen the child to the whole inherited mask; when that snapshot
is itself unknown, cards the same probe's NVML rows mark as MIG are
pinned to their slice, never by the whole-GPU uuid.

## Tests

New tests in `studio/backend/tests/test_mig_gpu_masks.py`. All of them
fail on current main and pass with this change, except the unknown-UUID
guard, which passes on both:

- A whole-GPU UUID mask (full, short prefix, lowercase) under
`FASTEST_FIRST` on a single non-MIG card returns the nvidia-smi row and
never calls the torch probe.
- The same mask under `PCI_BUS_ID` still reads its card when the
separate `index,uuid` query fails and NVML is unavailable.
- A two-card UUID mask under `FASTEST_FIRST` on a three-card host keeps
only its own cards.
- An unknown UUID still ignores the whole-card CLI rows.
- With no UUID column, a token is mapped only when the UUID query
verifies it; an unknown UUID or a failed query stays unresolved.
- A subset of a FASTEST_FIRST UUID mask pins the child by UUID, a card
outside the mask is never pinned, and a MIG card keeps the inherited
mask.
- A MIG listing raced by `invalidate_static` is re-read on the next
call.
- A UUID subset stays pinned when the MIG recheck after the memory probe
fails, and a card the probe's NVML rows mark as MIG is pinned to its
slice.
- A MIG set served from gpu_query's cache keeps that listing's age; a
failed listing is unknown and is retried after the 5 second backoff, not
on every poll.
- A reordered FASTEST_FIRST UUID mask reorders the pinned child ids to
the mask order.
- The MIG set follows `UNSLOTH_GPU_QUERY_STATIC_TTL`, including 0.
- A lowercase GPU- or MIG- uuid on a MIG card gets its NVML slice
reading and pins the child to that slice.
- Three memory polls plus three auto-selection overlays run `nvidia-smi
-L` once. After the physical count probe they run it zero more times.
- `get_mig_gpu_indices` stays cached until the static generation moves.

The existing MIG suites and the related GPU memory, NVML fallback,
physical count, system poll, SM gate, VRAM settle, unified memory, Tegra
and gpu_query cache suites pass on both base and head.

---------

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>
- [kortix-ai/suna](https://github.com/kortix-ai/suna) [81](https://github.com/kortix-ai/suna/commits): fix(tests): billing journey reads Renews for an active plan and tops up a current preset (#10096)

## Problem
v0.14.0 release suite run 38967530794 (attempt 3):
`10-billing-journey:149` passed checkout and the real Stripe
subscription (`account-state` returned `subscription.status: active`),
then failed `getByText('Active', { exact: true })`. The failure
screenshot of deployed staging shows the plan card reading **Credits ·
$100/mo · Renews Nov 16** with 15,050 credits: #10007 made
`current_period_end` real, so an active plan reads "Renews <date>". The
same screenshot shows the next step is stale too: top-up presets are $25
/ $100 / $250 / $1,000 / Custom (#9814), and the spec clicks `$10`.

## Change
- The active-plan check expects `/^Renews /`.
- The top-up step picks `$25`, clicks `Add $25`, and asserts `amount:
25` on `POST /v1/billing/purchase-credits`.
Labels checked in `apps/web/translations/en.json`: `renews` = "Renews
{date}", `billing.topup.addAmount` = "Add {amount}", `amountGroup` =
"Top-up amount"; `CREDIT_PRESETS = [25, 100, 250, 1000]` in
`credit-topup-section.tsx`; `Manage billing` still renders in
`billing-tab.tsx`.

## Verification
`bun build --no-bundle` parses the spec. Browser journeys are not run on
the owner's Mac; the proof is the next release suite against deployed
staging.
- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) [60](https://github.com/QwenLM/qwen-code/commits): test(managed-agent): add the FG8c process-crash gates for monitor_run and background shells (#14163) (#14407)

* fix(core): end the managed command launcher by its command's signal

A background Shell's exit evidence is its cgroup launcher's own exit, and
the launcher replaced a signal death with exit(1). A background process
killed by SIGKILL was therefore recorded as `exited` with `exitCode: 1,
exitSignal: null`, on the child_run record and on the Broker's `:process`
row alike: a status the process never returned.

The launcher now ends itself by the signal its command died of, so the
waiter sees that signal. Only the signals that cannot be re-raised keep
the nonzero fallback: a core-dumping one would dump the launcher too, and
Node.js owns SIGUSR1 and ignores SIGPIPE. Command hooks share the
launcher and already read a null exit code as a signal kill, a branch the
old launcher left unreachable whenever only the command was killed.

Found by the FG8c process-kill gate (#14163).

* test(managed-agent): add the FG8c process-crash gates for monitor_run and background shells (#14163)

FG8c kills (or stops) a real process under a live background run and
pins what the platform does next against JDBC ground truth, in seven
cases: the packaged Harness after the dispatch committed and after the
capture started (then a cold reload on a fresh Harness), the managed
worker (SIGKILL, and SIGSTOP across the broker's 30 s worker bound), the
background process itself, the worker behind later prompts that reach
for the Runtime again, and the worker under a live Monitor watch whose
idle stop then meets the loss.

Every case asserts one :start and one :process row across every boot and
prompt, and exactly one Runtime binding at generation 1: a lost
generation is never re-minted. Records may stay open, but never settle
on evidence nobody produced; the reloaded close drains the run its
process never saw (#13986); a dead worker's release is refused without
stop proof; a stopped worker reads as neither stopped nor lost; and a
watch whose stop nobody could prove parks as recovery_blocked /
runtime_lost (#13896).

The probe's state reads and the IT's record and output reads now lead
with ma_resource's session_scope_key: filtered by the unindexed tenant
and session columns alone, every poll scanned all the inline capture
bytes the lane had written, so each later letter polled slower. The
shared broker proxy also treats a client gone mid-request as no request
instead of a sticky proxy failure.

The hosted fork's healthy allowance moves 2640 -> 2930 s for the letter
(twice its local 144 s, the FG9 convention); the 3600 s fork and the
600 s per-letter ceiling are unchanged. Seven mutation witnesses, one
per case, were each observed red. The bilingual design document records
the cases, two expectations of the round design that the merged
recovery surface does not meet, and the follow-ups.

* fix(core): keep only reachable signal names in the launcher's kept list

Node.js on Linux reports signal 6 as SIGABRT, never SIGIOT, and Linux
defines no SIGEMT, so neither name could ever reach the launcher's exit
handler. Dropping them leaves the list as exactly the set it can match.

---------

Co-authored-by: 易良 <1204183885@qq.com>
- [t8y2/dbx](https://github.com/t8y2/dbx) [56](https://github.com/t8y2/dbx/commits): chore(release): prepare v0.6.46
- [google/adk-python](https://github.com/google/adk-python) [29](https://github.com/google/adk-python/commits): fix: cap the google-genai instrumentor below 1.0 in the test extra

The test extra allowed opentelemetry-instrumentation-google-genai below 2, so a fresh install resolves 1.2b0, which records inference attributes that the telemetry functional goldens and functional_divergences.json, recorded against 0.7b1, do not explain, and those tests fail on main. This caps the test extra below 1.0 so CI installs the instrumentor the goldens are recorded against, while the all and otel-gcp extras keep allowing 1.x.

Co-authored-by: George Weale <gweale@google.com>
PiperOrigin-RevId: 1001201460
- [langgenius/dify](https://github.com/langgenius/dify) [24](https://github.com/langgenius/dify/commits): refactor(dify-ui): compose dialogs from the Design Kit anatomy (#44221)
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) [24](https://github.com/screenpipe/screenpipe/commits): Gate captured data on PII completion receipts (#7634)

* Gate captured data on versioned PII completion

* [autofix.ci] apply automated fixes

* Bound privacy processing and expose honest queue status

* Document privacy queue costs, status and rollout limits

* Stress-test PII release overhead and fix queue edge cases

* fix: preserve activities through required privacy processing

* fix: reject activity rebuilds after concurrent privacy revocation

* test: verify privacy completion and support diagnostics across platforms

* fix: release derived enterprise streams through durable privacy receipts

* fix: recheck privacy mode after preparing upload admission

* test: isolate diagnostic upload checks from stream policy changes

* docs: record derived upload validation and paired capture timings

* fix: preserve protected APIs and historical replay with resumable PII processing

* fix: rediscover generated IDs after privacy trigger migration

* docs: distinguish historical PII measurements from current validation

* fix: preserve JSON scalar types in protected local projections

---------

Co-authored-by: autofix-ci[bot] <114827586+autofix-ci[bot]@users.noreply.github.com>
Co-authored-by: Ezra Ellette <ezrasellette@gmail.com>
- [docling-project/docling](https://github.com/docling-project/docling) [9](https://github.com/docling-project/docling/commits): fix(odf): move hidden ODT sections to the invisible content layer (#4860)

Signed-off-by: Ankit Kumar <ankitkumar19473@gmail.com>
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) [7](https://github.com/google-gemini/gemini-cli/commits): fix(cli): forward termination signals from bootstrap parent to child process (#29790)
- [lutzroeder/netron](https://github.com/lutzroeder/netron) [6](https://github.com/lutzroeder/netron/commits): Update to eslint 10.13.0
- [pykeio/ort](https://github.com/pykeio/ort) [6](https://github.com/pykeio/ort/commits): feat: impl `Hash` for `MemoryInfo`
- [steipete/oracle](https://github.com/steipete/oracle) [4](https://github.com/steipete/oracle/commits): fix(browser): restrict live tabs to trusted ChatGPT hosts

Parse HTTPS URLs and require the exact ChatGPT hostname before attaching or harvesting, rejecting title-only matches, URL prefixes, and userinfo lookalikes. Document the selection rule and cover it with a regression. Fix the nearby shutdown/reattach test race by awaiting runtime-hint persistence instead of polling for a short interval.

Co-authored-by: Sebastien Tardif <sebtardif@ncf.ca>
- [github/spec-kit](https://github.com/github/spec-kit) [3](https://github.com/github/spec-kit/commits): docs: define shared catalog contracts (#4977)

* docs: define shared catalog contracts

Document the current catalog source, precedence, trust, fetch, cache, validation, failure, provenance, search, and release-selection contracts across extensions, presets, integrations, workflows, workflow steps, and bundles. Add cross-primitive characterization coverage without changing production behavior.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

Copilot-Session: af29eafb-3a48-4e47-99af-6af5ee947d32

* docs: clarify catalog behavior differences

Narrow the catalog contracts to preserve whitespace override handling, validation phases, recoverable versus fatal source errors, malformed-entry shadowing exceptions, and integration release-history fallback. Add characterization coverage for the newly documented differences.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

Copilot-Session: af29eafb-3a48-4e47-99af-6af5ee947d32

* docs: complete catalog edge-case contracts

Document command-specific bundle validation bypass, shared versus catalog-specific redirect checks, and broad stale-cache fallback. Add characterization coverage for removing invalid raw bundle sources and malformed-JSON cache fallback.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

Copilot-Session: af29eafb-3a48-4e47-99af-6af5ee947d32

* docs: identify existing catalog base

Clarify that specify_cli.catalogs already provides shared source-entry, URL-validation, and config-loading primitives for extensions and integrations, and name the import and subclass patch points a broader migration must preserve.

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

Copilot-Session: af29eafb-3a48-4e47-99af-6af5ee947d32

---------

Copilot-Session: af29eafb-3a48-4e47-99af-6af5ee947d32
- [Kiln-AI/Kiln](https://github.com/Kiln-AI/Kiln) [1](https://github.com/Kiln-AI/Kiln/commits): chore: mark Claude 4 Sonnet on OpenRouter deprecated in model list (#1936)

OpenRouter no longer lists anthropic/claude-sonnet-4, and Kiln's paid
smoke test for that entry returns 404 Not Found.


Claude-Session: https://claude.ai/code/session_01Xm27vxtSrsuys3ByseEvo5

Co-authored-by: Claude <noreply@anthropic.com>
- [zylon-ai/private-gpt](https://github.com/zylon-ai/private-gpt) [1](https://github.com/zylon-ai/private-gpt/commits): fix(tools): check {name, artifact_id} refs in knowledge_search and tabular analysis (#2412)

Models copy the artifact_id of a neighbouring file from a listing (ids look
alike), so a search is scoped to the wrong document and the answer misses
data. Each artifact is now passed as {name, artifact_id}; the server checks the
name against the id's file and rejects a mismatch with the correct
artifact_id, which the model uses to fix its next call.

Also stops an artifacts list that falls entirely outside the request scope
from widening the search to the whole collection, and lets the tool prompts
find the list tool under the backend's names.

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

## [ai-agent](https://github.com/topics/ai-agent)
- [trycua/cua](https://github.com/trycua/cua) [49](https://github.com/trycua/cua/commits): fix(spaces): name the app blocked from the Local Network in cua doctor, the daemon log and Turn on (CUA-1819) (#5378)

* fix(spaces): say which app is blocked from the local network, from the daemon (CUA-1807 follow-ups)

- cua doctor: host.local_network now comes from the cua daemon, the process
  that talks to the VMs, and names the app macOS holds responsible for it
  (responsibility_get_pid_responsible_for_pid). Before, the CLI connected
  from its own process, so a terminal with access read "ok" while the
  daemon was blocked. An older daemon falls back to the CLI's own probe and
  says it did not check the daemon.
- Daemon log: a volume re-attach to a local VM with no route names the
  Local Network cause instead of "still starting", and identical re-attach
  failures are logged at warn once per 10 minutes (with a repeat count).
- Turn on / Turn off: a failure with a known cause (Local Network, disk,
  the two-VM limit) reads in plain words through create's failure_cause,
  in the shared core, so SwiftUI and Electron both get it.
- The Local Network error names the responsible app for a bare daemon too.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* chore: lockfiles for cua-spaces' new cua-vmm dependency

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* docs(cua-sdk): Rust reference for Space::spacesd_unreachable_cause and the re-attach rate limit

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) [10](https://github.com/CherryHQ/cherry-studio/commits): fix(prompt-management): expose global prompts from editors (#21673)

<!-- Template from
https://github.com/kubevirt/kubevirt/blob/main/.github/PULL_REQUEST_TEMPLATE.md?-->
<!--  Thanks for sending a pull request!  Here are some tips for you:
1. Consider creating this PR as draft:
https://github.com/CherryHQ/cherry-studio/blob/main/CONTRIBUTING.md
-->

### What this PR does

Before this PR:

The Agent and Assistant editor prompt tabs listed only linked prompts,
so global prompts available in the composer appeared missing and had no
management path from the editor.

After this PR:

The prompt tabs identify the current Agent/Assistant scope, explain
where global prompts are managed, and show a persistent Manage Global
Prompts button, including for an empty linked list. It opens Settings →
Prompts only after the editor has saved its current values and
successfully closed. Failed saves and invalid required names keep edits
visible. Edits made during a pending close cancel that navigation
attempt; repeated management clicks wait for outstanding writes and
persist any reversion to the original values before navigating. Explicit
Close retains the existing failed-edit discard option. Composer behavior
and prompt visibility/binding rules are unchanged.

<!-- (optional, in `fixes #<issue number>(, fixes #<issue_number>, ...)`
format, will close the issue(s) when PR gets merged)*: -->

Fixes #19754

### Why we need it and why it was done in this way

The following tradeoffs were made:

Keep the existing scoped list and link to the existing settings
management surface. Navigation stays in each edit dialog and is passed
to the shared tab as a callback. The close-before-action hook accepts
asynchronous close results and skips navigation when closure is refused.
The autosave hook exposes its pending drain so both editors await
outstanding writes before checking whether the current form is
unchanged. Both persist from live form values and advance their saved
baselines on successful writes; the Assistant baseline uses a captured
form snapshot rather than waiting for a resource refetch. After
flushing, closure rechecks both the form snapshot and its remaining
diff. This preserves reversions and prevents an unchanged-form shortcut
from bypassing an in-flight write.

The following alternatives were considered:

Showing global and linked prompts together would require distinguishing
management and binding actions in the same list. The existing settings
page already supports scope badges and editing.

Links to places where the discussion took place: <!-- optional: slack,
other GH issue, mailinglist, ... -->

https://github.com/CherryHQ/cherry-studio/issues/19754

### Breaking changes

None.

<!-- optional -->

If this PR introduces breaking changes, please describe the changes and
the impact on users.

### Special notes for your reviewer

Validation:

- `pnpm test:renderer
src/renderer/components/resourceCatalog/dialogs/edit/__tests__/EditDialogs.test.tsx
src/renderer/components/resourceCatalog/dialogs/components/__tests__/useDebouncedAutoSave.test.tsx
src/renderer/hooks/__tests__/useCloseBeforeAction.test.ts
src/renderer/components/resourceCatalog/dialogs/edit/__tests__/ResourceEditDialogHost.test.tsx`
— 4 files / 98 tests passed. Four deferred-save regressions reproduced
premature closure before the fix: revert a description during either
management-triggered saving or background autosave, then click
management again. Both editors now await the first write and the
reversion write before navigation. Additional coverage preserves a
failed reversion across another management click, verifies recovery
after correcting it, and exercises reverted Assistant custom-parameter
arrays. Earlier failure, invalid-name, concurrent-edit, explicit-close,
and model-settings navigation regressions all pass.
- `pnpm typecheck:web` — passed.
- `pnpm exec eslint
src/renderer/components/resourceCatalog/dialogs/components/EditDialogShared.tsx
src/renderer/components/resourceCatalog/dialogs/components/__tests__/useDebouncedAutoSave.test.tsx
src/renderer/components/resourceCatalog/dialogs/edit/AssistantEditDialog.tsx
src/renderer/components/resourceCatalog/dialogs/edit/AgentEditDialog.tsx
src/renderer/components/resourceCatalog/dialogs/edit/__tests__/EditDialogs.test.tsx`
— passed.
- `pnpm exec oxlint --deny-warnings
src/renderer/components/resourceCatalog/dialogs/components/EditDialogShared.tsx
src/renderer/components/resourceCatalog/dialogs/components/__tests__/useDebouncedAutoSave.test.tsx
src/renderer/components/resourceCatalog/dialogs/edit/AssistantEditDialog.tsx
src/renderer/components/resourceCatalog/dialogs/edit/AgentEditDialog.tsx
src/renderer/components/resourceCatalog/dialogs/edit/__tests__/EditDialogs.test.tsx`
— passed.
- `pnpm exec oxfmt --check
src/renderer/components/resourceCatalog/dialogs/components/EditDialogShared.tsx
src/renderer/components/resourceCatalog/dialogs/components/__tests__/useDebouncedAutoSave.test.tsx
src/renderer/components/resourceCatalog/dialogs/edit/AssistantEditDialog.tsx
src/renderer/components/resourceCatalog/dialogs/edit/AgentEditDialog.tsx
src/renderer/components/resourceCatalog/dialogs/edit/__tests__/EditDialogs.test.tsx`
and `git diff --check` — passed.
- `pnpm check --plan` — inspected; renderer test scope. No full local
suite was run.

The save/close guard was self-reviewed and verified using real dialog
primitives in renderer integration tests. No additional interactive
Electron session was run for this correction. Initial interactive macOS
validation confirmed the scope explanation, editor closure, and
navigation to prompt settings; Windows/Linux were not interactively
tested. The new description is translated in all 13 renderer locales. No
storage changes, upgrade migration, or user-guide update are required.

<!-- optional -->

### Checklist

This checklist is not enforcing, but it's a reminder of items that could
be relevant to every PR.
Approvers are expected to review this list.

- [x] Branch: This PR targets `main`
- [x] PR: The PR description is expressive enough and will help future
contributors
- [x] Code: [Write code that humans can
understand](https://en.wikiquote.org/wiki/Martin_Fowler#code-for-humans)
and [Keep it simple](https://en.wikipedia.org/wiki/KISS_principle)
- [x] Refactor: You have [left the code cleaner than you found it (Boy
Scout
Rule)](https://learning.oreilly.com/library/view/97-things-every/9780596809515/ch08.html)
- [x] Upgrade: Impact of this change on upgrade flows was considered and
addressed if required
- [x] Documentation: A [user-guide update](https://docs.cherry-ai.com)
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
[Prompts] Find global prompt management directly from Agent and Assistant editors, with clearer scope labels.
```

---------

Signed-off-by: lick <2188718831@qq.com>

## [ai-agents](https://github.com/topics/ai-agents)
- [slopus/happy](https://github.com/slopus/happy) [371](https://github.com/slopus/happy/commits): android: tests: scopes are cancelled and joined before their database and server close (leaked failures otherwise land on the next runTest as UncaughtExceptionsBeforeTest); the presence collector's interrupt is not printed
- [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) [6](https://github.com/lemomo-ai/lemo-opuscar/commits): gallery workflow: actions on Node 24 (checkout v7, setup-python v7, upload-pages-artifact v5, deploy-pages v5)

Claude-Session: https://claude.ai/code/session_0117omdC7f2crw1uum7XGDqq
- [lycorp-jp/sim-use](https://github.com/lycorp-jp/sim-use) [2](https://github.com/lycorp-jp/sim-use/commits): Merge pull request #156 from mvanhorn/fix/110-ios-device-root-launch-retry

fix: retry transient missing physical-device accessibility roots
- [steipete/agent-scripts](https://github.com/steipete/agent-scripts) [2](https://github.com/steipete/agent-scripts/commits): fix: harden helper failures and refresh browser tooling

Fix failed browser navigation, authenticated restricted-package verification, missing relay token paths, malformed caption entities, unknown fleet membership, and Swift attribute backtracking. Add regression coverage and refresh Puppeteer Core to 25.14.0.

Consolidates #49, #50, #51, #52, #53, and #54.

Co-authored-by: Sebastien Tardif <sebtardif@ncf.ca>

## [android](https://github.com/topics/android)
- [librepods-org/librepods](https://github.com/librepods-org/librepods) [20](https://github.com/librepods-org/librepods/commits): android: rename noise_control widget resources to listening_control
- [square/leakcanary](https://github.com/square/leakcanary) [14](https://github.com/square/leakcanary/commits): Merge pull request #2992 from square/leak-trace-object-ids

Read object ids unsigned, and print each leak trace object's id

## [bookmarks](https://github.com/topics/bookmarks)
- [omnivore-app/omnivore](https://github.com/omnivore-app/omnivore) [2](https://github.com/omnivore-app/omnivore/commits): Merge branch 'main' of github.com:omnivore-app/omnivore
- [shaarli/Shaarli](https://github.com/shaarli/Shaarli) [1](https://github.com/shaarli/Shaarli/commits): Merge pull request #2292 from shaarli/dependabot/npm_and_yarn/source-map-js-1.2.2

build(deps): bump source-map-js from 1.2.1 to 1.2.2

## [cli](https://github.com/topics/cli)
- [openclaw/imsg](https://github.com/openclaw/imsg) [3](https://github.com/openclaw/imsg/commits): fix: report rejected bridge helper paths (#351)

Report the rejected --dylib path when an explicit bridge helper is missing, rather than listing automatic discovery paths that were not tried. Preserve unconfigured discovery and document the authoritative explicit-path behavior.

The diagnostic regression fails before and passes after; focused launch/locator tests, docs tests, lint, independent review, and exact-head CI validate the change.

Related to #334; its broader configuration proposal remains open.
- [wader/fq](https://github.com/wader/fq) [1](https://github.com/wader/fq/commits): Merge pull request #1415 from wader/bump-gomod-golang-x-net-0.61.0

Update gomod-golang-x-net to 0.61.0 from 0.60.0

## [e-ink](https://github.com/topics/e-ink)
- [usetrmnl/trmnl-firmware](https://github.com/usetrmnl/trmnl-firmware) [12](https://github.com/usetrmnl/trmnl-firmware/commits): Refreshed the merged image on an upload-only build (#711)

`pio run -t upload` builds only firmware.bin, so since the merge moved onto
"buildprog" it flashed without refreshing merged_firmware.bin or the
versioned copies. Upload now depends on "buildprog".

Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
- [arnegiacomo/fugleramme](https://github.com/arnegiacomo/fugleramme) [3](https://github.com/arnegiacomo/fugleramme/commits): chore(assets): #33 add Geothlypis formosa, Vireo griseus and Contopus virens (#270)

4 plates:
- Kentucky Warbler (Geothlypis formosa), 2 variants
- White-eyed Vireo (Vireo griseus), 1 variant
- Eastern Wood-Pewee (Contopus virens), 1 variant

Co-authored-by: Arne Munthe-Kaas <arnegiacomo@gmail.com>

## [embedded](https://github.com/topics/embedded)
- [nanopb/nanopb](https://github.com/nanopb/nanopb) [4](https://github.com/nanopb/nanopb/commits): Fix enum_to_string and enum_validate for enums with aliases

With allow_alias, several names can have the same value, and both
functions got a case label for each name, so the generated .pb.c fails
to compile with "duplicate case value". Emit one case per value. For an
alias, <Enum>_name() returns the first name defined for the value, as
protobuf's EnumDescriptor::FindValueByNumber() does.
- [hathach/tinyusb](https://github.com/hathach/tinyusb) [3](https://github.com/hathach/tinyusb/commits): Merge pull request #4237 from rhgndf/wch-usbhs-connect-disconnect

Add support for connect/disconnect in WCH USBHS

## [esp32](https://github.com/topics/esp32)
- [esphome/esphome](https://github.com/esphome/esphome) [25](https://github.com/esphome/esphome/commits): [ci] Rename merge conflict label to has-conflicts (#20969)
- [crosspoint-reader/crosspoint-reader](https://github.com/crosspoint-reader/crosspoint-reader) [16](https://github.com/crosspoint-reader/crosspoint-reader/commits): Update Plugin Hub repository references

Change Plugin Hub repository URLs from jadehawk/PluginHub.crosspoint-plugin to crosspoint-reader/crosspoint-plugin-hub to reflect the repository migration
- [platformio/platform-espressif32](https://github.com/platformio/platform-espressif32) [11](https://github.com/platformio/platform-espressif32/commits): Add new uPesy boards & Update old uPesy boards (#1250)

Added boards:

- EDU ESP32
- ESP32C3 Basic
- ESP32C3 Mini
- ESP32S3 Basic
- [arendst/Tasmota](https://github.com/arendst/Tasmota) [6](https://github.com/arendst/Tasmota/commits): Fix hostByName returning negative values when lookup failed
- [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) [2](https://github.com/78/xiaozhi-esp32/commits): fix(audio): refresh Slovak voice prompts (#2321)

Replace the 16 Slovak prompt recordings with the WAV files contributed by @marekbujko in #2297.

Convert to mono 16 kHz Ogg Opus with 16 kbps encoding and 60 ms packets, normalize loudness with peak headroom, and preserve the original timing and pauses.

Refs #2297.

Co-authored-by: Marek Bujko <114984527+marekbujko@users.noreply.github.com>
- [rmk-rs/rmk](https://github.com/rmk-rs/rmk) [2](https://github.com/rmk-rs/rmk/commits): Merge pull request #1290 from rmk-rs/daily_review/20261016-source-review
- [ESPARGOS/pyespargos](https://github.com/ESPARGOS/pyespargos) [1](https://github.com/ESPARGOS/pyespargos/commits): Improve IQ reference calibration under antenna interference

Use a stronger wired REFTX with lower RX gain and a higher onset
signal threshold.
- [espressif/arduino-esp32](https://github.com/espressif/arduino-esp32) [1](https://github.com/espressif/arduino-esp32/commits): fix(httpclient): Time out reading a body when the server goes silent (#12990)

* fix(httpclient): Time out reading a body when the server goes silent

writeToStreamDataBlock() waited for the rest of a body for as long as
connected() held. A server that stops sending part way through a body
without closing the connection leaves connected() true, so getString()
and writeToStream() never returned. Give up after _tcpTimeout without
data and return HTTPC_ERROR_READ_TIMEOUT, as handleHeaderResponse()
already does for the headers.

* fix(httpclient): Wait between empty reads of a TLS body

NetworkClientSecure::read() returns at once when no data has arrived,
so readBytes() returns 0 without waiting for its timeout, and the body
loop polled the socket without pause through every gap in a TLS body.
Wait 1 ms before retrying, as the loop already does when available()
is 0.

---------

Co-authored-by: Lucas Saavedra Vaz <32426024+lucasssvaz@users.noreply.github.com>
- [platformio/platformio-core](https://github.com/platformio/platformio-core) [1](https://github.com/platformio/platformio-core/commits): Remove redundant chardet depends for MacOS (#5530)

`charset_normalizer` has shipped fixed macOS ARM wheels for years now. Drop the un-needed chardet depends.

## [ethereum](https://github.com/topics/ethereum), [foundry](https://github.com/topics/foundry), [solidity](https://github.com/topics/solidity)
- [foundry-rs/forge-std](https://github.com/foundry-rs/forge-std) [1](https://github.com/foundry-rs/forge-std/commits): fix(ci): buffer the action update cooldown (#931)

Dependabot reads Git tag dates without the time of day, so a seven-day
GitHub Actions cooldown can select commits before the shared scanner's
seven-day minimum has elapsed, as seen in
[foundry-rs/foundry#17616](https://github.com/foundry-rs/foundry/pull/17616).
Increase the GitHub Actions cooldown to eight days to absorb that
rounding while preserving the scanner's existing minimum-age check.

[Dependabot's tag-date
extraction](https://github.com/dependabot/dependabot-core/blob/main/common/lib/dependabot/git_metadata_fetcher.rb#L358)
omits the time component.

Prompted by: @DaniPopes

Co-authored-by: DaniPopes <57450786+DaniPopes@users.noreply.github.com>
- [foundry-rs/foundry-toolchain](https://github.com/foundry-rs/foundry-toolchain) [1](https://github.com/foundry-rs/foundry-toolchain/commits): fix(ci): buffer the action update cooldown (#189)

Dependabot reads Git tag dates without the time of day, so a seven-day
GitHub Actions cooldown can select commits before the shared scanner's
seven-day minimum has elapsed, as seen in
[foundry-rs/foundry#17616](https://github.com/foundry-rs/foundry/pull/17616).
Increase the GitHub Actions cooldown to eight days to absorb that
rounding while preserving the scanner's existing minimum-age check.

[Dependabot's tag-date
extraction](https://github.com/dependabot/dependabot-core/blob/main/common/lib/dependabot/git_metadata_fetcher.rb#L358)
omits the time component.

Prompted by: @DaniPopes

Co-authored-by: DaniPopes <57450786+DaniPopes@users.noreply.github.com>

## [font](https://github.com/topics/font)
- [lxgw/LxgwWenKai](https://github.com/lxgw/LxgwWenKai) [6](https://github.com/lxgw/LxgwWenKai/commits): Bump version to v1.530
- [lxgw/yozai-font](https://github.com/lxgw/yozai-font) [2](https://github.com/lxgw/yozai-font/commits): Update README.md
- [lxgw/kose-font](https://github.com/lxgw/kose-font) [1](https://github.com/lxgw/kose-font/commits): Revise font series section and add star history

Updated section titles and added star history chart.

## [gif](https://github.com/topics/gif), [image-processing](https://github.com/topics/image-processing), [jpeg](https://github.com/topics/jpeg), [libvips](https://github.com/topics/libvips), [png](https://github.com/topics/png), [webp](https://github.com/topics/webp)
- [davidbyttow/govips](https://github.com/davidbyttow/govips) [3](https://github.com/davidbyttow/govips/commits): Keep animated frames intact in Flip, Rotate 180, Zoom and Resize (#558)

Several transforms treated the stacked frames of a multi-page image as one tall image:

- Flip(DirectionVertical) and Rotate(Angle180) reversed the frame order.
  They now map each loaded page through the operation and restack, via a
  new vipsMapPages helper that vipsExtractAreaMultiPage also uses.
- Zoom left the page height at the pre-zoom value, so an x2 y2 zoom read
  as twice as many half-frames. It now scales the page height by yFactor.
- ResizeWithVScale rounded the strip height and the page height
  separately, so whenever pageHeight*scale wasn't whole the strip came
  out a few rows short and libvips dropped the page height (the #350
  'toilet roll'). When the roundings disagree, the vertical scale is now
  chosen so the strip is exactly pages*newPageHeight, as vips_thumbnail
  does. Output is unchanged when they already agree.
- ResizeWithVScale, Zoom and Flip count loaded pages as
  Height()/PageHeight() rather than Pages(), like Rotate after #555.

Fixes #554

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
- [cshum/imagor](https://github.com/cshum/imagor) [2](https://github.com/cshum/imagor/commits): fix(s3storage): buffer the body when the blob size is unknown (#855)

Since #618 Put always sends ContentLength, which is 0 when the loader
does not know the size (an HTTP origin answering without Content-Length).
S3 then rejects the default CRC32 checksum with BadDigest, or with
AWS_REQUEST_CHECKSUM_CALCULATION=when_required stores an empty object.

When the size is unknown, read the body into memory and send its real
length.
- [libvips/libvips](https://github.com/libvips/libvips) [2](https://github.com/libvips/libvips/commits): cache: entry pointer must be cleared inside mutex (#5250)

Follow up to commit 128fa68 that separates the pointer clearing
from the unref to prevent a possible (but rare) race condition

## [macos](https://github.com/topics/macos)
- [yetone/magpie](https://github.com/yetone/magpie) [64](https://github.com/yetone/magpie/commits): gateway: a key held to accounts is told only of the image and video models they serve (#2579)

A gateway key held to some accounts was told, in /v1/models' image and
video lists (drawerObjects, videomakerObjects), of every image and video
model its held models named, whether or not an account the key may use
serves it. Its chat list already applied accountServes; the two media
lists applied modelAllowed alone. Both now apply both, as entryAllowed
does. Reported by ggbdpq; the patch and test are ump45nose's
(fix/2579-image-video-account-serves, 592cc4db), with a t.Cleanup added
and the doc comments and failure message reworded.

Siblings: the other modelAllowed-only callers are not model lists (the
codex and desktop subagent picks, chatGPTSearchers, quotas_scope, which
handles accounts in card(), and videoModelHeld). The Drawers/Videomakers
uses in draw.go, video.go and drawing_route.go resolve a model, they do
not list them.

Run at this commit's tree (base 6f950653f):
- With the fix removed, TestGatewayKeyAccountsHoldTheImageAndVideoLists
  fails: "a key whose account serves no image or video model is told of
  image [grok/grok-imagine-image grok/grok-imagine-image-quality], video
  [grok/grok-imagine-video grok/grok-imagine-video-1.5]". With it, it and
  TestGatewayKeyModelsHoldTheImageAndVideoLists pass.
- gofmt -l: clean. go vet ./...; GOOS=linux go vet -tags nogui;
  GOOS=windows go vet (with and without -tags nogui): clean. Builds for
  darwin, linux (nogui) and windows: ok.
- go test -tags nogui -timeout 45m ./... with pipefail, sandbox HOME:
  every package ok, EXIT=0 (internal/gateway 1315s).

Co-authored-by: ggbdpq <67929842+ggbdpq@users.noreply.github.com>
Co-authored-by: ump45nose <52391318+ump45nose@users.noreply.github.com>
- [Beingpax/VoiceInk](https://github.com/Beingpax/VoiceInk) [8](https://github.com/Beingpax/VoiceInk/commits): Merge pull request #1017 from Beingpax/direct-typing-paste-method

Add direct typing paste method
- [FluidInference/FluidAudio](https://github.com/FluidInference/FluidAudio) [4](https://github.com/FluidInference/FluidAudio/commits): docs: add Dictaty to showcase (#1042)

Adds Dictaty to the end of Documentation/Showcase.md, keeping the
chronological order.

Dictaty is a native macOS menu bar dictation app. It uses FluidAudio for
on-device ASR with Parakeet TDT v3 (`AsrModels`, FluidAudio 0.17.4).

Website: https://dictaty.com/en

Thanks for maintaining FluidAudio and the list.
- [jundot/omlx](https://github.com/jundot/omlx) [4](https://github.com/jundot/omlx/commits): feat(muse-spark): read and write the mlx-lm 0.32.2 checkpoint layout (#4604)
- [acsandmann/rift](https://github.com/acsandmann/rift) [2](https://github.com/acsandmann/rift/commits): perf: optimize stackline
- [Clipy/Clipy](https://github.com/Clipy/Clipy) [1](https://github.com/Clipy/Clipy/commits): Disable HTML clipboard support by default (#758)
- [steipete/RepoBar](https://github.com/steipete/RepoBar) [1](https://github.com/steipete/RepoBar/commits): chore: prepare RepoBar 0.10.1 release (#149)

## [offline-first](https://github.com/topics/offline-first)
- [pubkey/client-side-databases](https://github.com/pubkey/client-side-databases) [15](https://github.com/pubkey/client-side-databases/commits): Merge pull request #547 from pubkey/ccr-9b80774a-n98yyg

Add PGlite and SQLite Wasm projects, update RxDB to 17 and TestCafe to 3
- [loro-dev/loro](https://github.com/loro-dev/loro) [1](https://github.com/loro-dev/loro/commits): fix: keep binary import exact when JSON drops value bits

JSON-relayed history no longer fails known-history checks with UsedOpID, while default binary import stays exact. JsonLossy is opt-in via JSON import and import_*_with_history_mode.

Enable serde_json float_roundtrip on loro-internal's normal dependency, and integer-encode counters only when fract() is 0.

## [openai](https://github.com/topics/openai)
- [BerriAI/litellm](https://github.com/BerriAI/litellm) [78](https://github.com/BerriAI/litellm/commits): fix(bedrock)!: block realtime replay after an input-first start and reject malformed Nova Sonic session settings (#46936)

* fix(bedrock): block realtime replay after input starts the session and reject non-string instructions and voice

* test(bedrock): name the malformed realtime setting test for its string cases

* fix(bedrock): replay the opening realtime message until Bedrock accepts the stream and refuse any fallback after commit

Also rejects a malformed modalities, input_sample_rate_hertz or tools setting with invalid_type, dropped under drop_params.

* fix(bedrock): replay a refused opening message on any fallback and reject OpenAI voices and non-string audio formats

* fix(realtime): read the client scope only when the websocket has one and reject any-case OpenAI and empty Bedrock voices

* test(bedrock): cover realtime replay, refusal and committed failure through a real proxy

Fix the scripted Bedrock peer's port import and the nested tool call cell's stale expected events, so the Nova Sonic integration file collects again
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) [40](https://github.com/OpenHands/OpenHands/commits): feat(secrets): ask for requested secrets inline in the chat (#18575)
- [gptme/gptme](https://github.com/gptme/gptme) [21](https://github.com/gptme/gptme/commits): fix(test): reset _kernel_mode_frozen in backend selection test (#4399)

test_registration_defers_backend_selection did not reset _kernel_mode_frozen,
so when a prior test in the suite called _resolve_kernel_backend() the flag
was True and _should_use_kernel() returned bool(None)=False before reaching
the cache-rebuild path. Add monkeypatch to reset it alongside _kernel_mode_cache.

Git-Session-Id: ddf69daa-2a7e-4399-84ce-7a5593b4238e
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) [3](https://github.com/SYSTRAN/faster-whisper/commits): Raise an error for languages unsupported by a model (#1564)

* Raise an error for languages unsupported by a model

Close: https://github.com/SYSTRAN/faster-whisper/issues/1228
- [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) [1](https://github.com/PDFMathTranslate/PDFMathTranslate/commits): security: upgrade gradio to 6.x to address CVE advisories

Bump gradio from <5.36 (5.35.0) to >=6.16.0,<7, which fixes all 7
advisories against 5.35.0: CVE-2026-28414, CVE-2026-49119,
CVE-2026-28416, CVE-2026-48545, CVE-2026-28415, CVE-2026-27167 and
CVE-2026-10783.

- gradio_pdf >=0.0.24 (first release supporting gradio 6)
- move theme/css/head from gr.Blocks() to launch() per Gradio 6 API

## [playwright](https://github.com/topics/playwright)
- [browser-use/browser-use](https://github.com/browser-use/browser-use) [18](https://github.com/browser-use/browser-use/commits): Clean up failed browser reconnect initialization (#6102)

A canceled or failed browser reconnect leaves its replacement connection
open and publishes an incomplete session manager. Close the replacement
client and clear its manager and focus before propagating the original
error.

Regression tests cover cancellation and connection errors during target
discovery and automatic attachment. The regression fails against the
original source. Five session tests, one live Chromium recovery test,
pre-commit, and Pyright pass. This change does not replay actions or
restore an unresponsive upstream browser.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Changes the CDP reconnect failure path and cancellation handling;
success-path behavior is unchanged but incorrect cleanup here could
affect auto-reconnect reliability.
> 
> **Overview**
> **Fixes leaked state when `reconnect()` fails or is cancelled
mid-setup.** Previously, a partial reconnection could leave a
replacement CDP WebSocket client running and expose a half-built
`SessionManager` on the session.
> 
> `reconnect()` now wraps the post-`start()` initialization (session
manager, `setAutoAttach`, focus restore, proxy auth, WS drop callback)
in `try`/`except BaseException`. On any failure it immediately clears
`_cdp_client_root`, `session_manager`, and `agent_focus_target_id`, then
runs shielded async cleanup to `stop()` the replacement client and
`clear()` the manager before re-raising the original error or
`CancelledError`.
> 
> New CI tests simulate failures during `Target.setDiscoverTargets` /
`Target.setAutoAttach` (connection error, task cancel, and cancel during
client `stop`) and assert the session is left with no client, manager,
or focus and that cleanup ran.
> 
> <sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit
e16388ba6e2975f539f597b9e81ab3a69451ee3d. Bugbot is set up for automated
code reviews on this repo. Configure
[here](https://www.cursor.com/dashboard/bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated description by cubic. -->
---
## Summary by cubic
A failed or cancelled browser reconnect now cleans up its replacement
CDP client, session manager, and focus target before propagating the
original error or cancellation.

- The cleanup runs to completion even when the reconnect task is
cancelled mid-teardown, then re-raises the cancellation.
- Regression tests cover cancellation and connection errors during
target discovery, automatic attachment, and cleanup shutdown.

<sup>Written for commit e16388ba6e2975f539f597b9e81ab3a69451ee3d.
Summary will update on new commits.</sup>

<a
href="https://cubic.dev/pr/browser-use/browser-use/pull/6102?utm_source=github"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-light.svg"><img
alt="View guided diff"
src="https://www.cubic.dev/buttons/review-in-cubic-light.svg"></picture></a>
<a
href="https://www.cubic.dev/action/auto-fix/pr/browser-use/browser-use/6102?returnTo=https%3A%2F%2Fgithub.com%2Fbrowser-use%2Fbrowser-use%2Fpull%2F6102&source=description"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/turn-on-auto-fix-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/turn-on-auto-fix-light.svg"><img
alt="Turn on auto-fix"
src="https://www.cubic.dev/buttons/turn-on-auto-fix-light.svg"></picture></a>

<!-- End of auto-generated description by cubic. -->
- [daijro/camoufox](https://github.com/daijro/camoufox) [5](https://github.com/daijro/camoufox/commits): Merge pull request #870 from JWriter20/fix/867-identity-encoding

Read response bodies sent with Content-Encoding: identity (#867)

## [python](https://github.com/topics/python)
- [vinta/awesome-python](https://github.com/vinta/awesome-python) [59](https://github.com/vinta/awesome-python/commits): remove disable-model-invocation: true
- [serhii-londar/open-source-mac-os-apps](https://github.com/serhii-londar/open-source-mac-os-apps) [26](https://github.com/serhii-londar/open-source-mac-os-apps/commits): Generate README
- [confident-ai/deepeval](https://github.com/confident-ai/deepeval) [25](https://github.com/confident-ai/deepeval/commits): Merge pull request #3474 from confident-ai/deepeval-setup-script

Deepeval setup script
- [adafruit/circuitpython](https://github.com/adafruit/circuitpython) [18](https://github.com/adafruit/circuitpython/commits): Merge pull request #11623 from MakerClassCZ/vectorio-polygon-modulo

Avoid modulo in Polygon pixel test
- [doronz88/pymobiledevice3](https://github.com/doronz88/pymobiledevice3) [15](https://github.com/doronz88/pymobiledevice3/commits): Merge pull request #2041 from doronz88/pytcp-0.3.8

build: Require pmd-pytcp 0.3.8
- [nltk/nltk](https://github.com/nltk/nltk) [11](https://github.com/nltk/nltk/commits): Merge pull request #3978 from alvations/fix-depgraph-contains-cycle-20261016

Fix DependencyGraph cycle detection, dead on every parsed graph
- [dbcli/mycli](https://github.com/dbcli/mycli) [9](https://github.com/dbcli/mycli/commits): Merge pull request #2376 from dbcli/RW/populate-docker-history-file

Populate Docker history file with examples
- [xlwings/xlwings](https://github.com/xlwings/xlwings) [8](https://github.com/xlwings/xlwings/commits): Merge pull request #2790 from xlwings/lite-to-png-docstrings

enhanced to_png docs
- [lakehq/sail](https://github.com/lakehq/sail) [3](https://github.com/lakehq/sail/commits): chore: update docs dependencies (#2792)
- [pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) [3](https://github.com/pymupdf/PyMuPDF/commits): Revert "setup.py: require python<3.15 if we contain layout code."

This reverts commit d26267910362d1a2424c07a56edec13008637c2b.

It is thought better to set require_python `>=3.11`, and let install pass/fail
depending on whether onnxruntime is available.
- [enactic/openarm](https://github.com/enactic/openarm) [2](https://github.com/enactic/openarm/commits): website: Add FAQ entry for OpenArm Cell shutting off during calibration (#627)

During zero-position calibration in OpenArm Cell, wiring around the
elbow or other joints can enter the detection area of the area sensors
and trigger the Reach-In Stop. Explain the cause and ask users to secure
the wiring along the arm.

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [KoljaB/RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) [2](https://github.com/KoljaB/RealtimeSTT/commits): Merge pull request #332 from ANDROIDHASSAN/fix/client-sends-empty-language

fix: start the server with the client's empty language
- [vacanza/holidays](https://github.com/vacanza/holidays) [2](https://github.com/vacanza/holidays/commits): Update Australia holidays: start NT observance rules in 1973 (#3922)

Signed-off-by: Ryan Duguid <ryanduguid@users.noreply.github.com>
Co-authored-by: Ryan Duguid <ryanduguid@users.noreply.github.com>
Co-authored-by: ~Jhellico <jhellico@gmail.com>
- [locustio/locust](https://github.com/locustio/locust) [1](https://github.com/locustio/locust/commits): Merge pull request #3561 from SulimanAbdulrazzaq/test/no-network-in-test-main

Use a local server instead of www.locust.io in two test_main tests
- [pyocd/pyOCD](https://github.com/pyocd/pyOCD) [1](https://github.com/pyocd/pyOCD/commits): info: add probe capabilities and trace port configuration

## [rust](https://github.com/topics/rust)
- [embassy-rs/embassy](https://github.com/embassy-rs/embassy) [13](https://github.com/embassy-rs/embassy/commits): Merge pull request #7282 from rockboynton/rockboynton/fix-uart-early-flush-return

stm32/usart: fix early BufferedUart flush
- [sigoden/dufs](https://github.com/sigoden/dufs) [5](https://github.com/sigoden/dufs/commits): chore: update SECURITY.md
- [probe-rs/probe-rs](https://github.com/probe-rs/probe-rs) [2](https://github.com/probe-rs/probe-rs/commits): swd: let an AP write finish before the next read (#4483)

## [swift](https://github.com/topics/swift)
- [supabase/supabase-swift](https://github.com/supabase/supabase-swift) [7](https://github.com/supabase/supabase-swift/commits): chore(deps): make swift-clocks a test-only dependency (#1583)
- [mattt/ollama-swift](https://github.com/mattt/ollama-swift) [3](https://github.com/mattt/ollama-swift/commits): Bump version to 1.9.0
- [apple/swift-openapi-generator](https://github.com/apple/swift-openapi-generator) [1](https://github.com/apple/swift-openapi-generator/commits): Fix up access modifier in Extensions.swift (#975)

### Motivation

When building in certain environments, the fact that Argument Parser was
imported publicly, but Foundation wasn't, and URL was getting conformed
to ExpressibleByArgument, got caught by the stricter validation and
caused a build error.

### Modifications

Properly import Foundation publicly and make the initializer public.

### Result

Generator can be built again in certain environments.

### Test Plan

Validated that this fixes it.
- [scinfu/SwiftSoup](https://github.com/scinfu/SwiftSoup) [1](https://github.com/scinfu/SwiftSoup/commits): Merge pull request #472 from saltcoffee/fix/url-validation

Fix URL protocol validation for control characters
- [steipete/Trimmy](https://github.com/steipete/Trimmy) [1](https://github.com/steipete/Trimmy/commits): ci: publish signed Trimmy releases from Actions

Move signed and notarized app, matching dSYM, Linux CLI, Sparkle appcast, and Homebrew cask publication into CI. Preserve existing download names and update-feed identity. Require a signed annotated tag, dated changelog, exact-commit push CI, and a complete verified artifact inventory before publication.

Add a default no-publish dispatch that exercises signing, notarization, archive verification, launch smoke, and Sparkle signing. Retire local publishing wrappers while retaining read-only verification and app-specific packaging.

Validated with release-policy and Homebrew tests, packaging-script tests, Actionlint, and independent review. No release or version tag was created for this migration.

## [typescript](https://github.com/topics/typescript)
- [Snapchat/Valdi](https://github.com/Snapchat/Valdi) [9](https://github.com/Snapchat/Valdi/commits): Internal Change

GitOrigin-RevId: 4517c9899960351622db63cec23190105a045752
- [MarkEdit-app/MarkEdit](https://github.com/MarkEdit-app/MarkEdit) [8](https://github.com/MarkEdit-app/MarkEdit/commits): Enhance EditorDocumentTests
- [ZingerLittleBee/ServerBee](https://github.com/ZingerLittleBee/ServerBee) [2](https://github.com/ZingerLittleBee/ServerBee/commits): docs(push): record sandbox acceptance and remaining gates (#218)
- [gibbok/typescript-book](https://github.com/gibbok/typescript-book) [1](https://github.com/gibbok/typescript-book/commits): Translate snippet comments into each book language (#286)

* Translate remaining snippet comments into each book language

* website

* books

## Other
- [facebook/idb](https://github.com/facebook/idb) [92](https://github.com/facebook/idb/commits): Install releases from facebook/fb rather than a local tap

Summary:
`homebrew.py install <tag>` no longer writes a release's attached formulae into the `idb-local/builds` tap. A release now installs from `facebook/fb` itself, so the local tap only ever holds CI builds:

- The tag must be the release facebook/fb carries, which is the `tag` recorded in the tap's `idb-release.json`. Any other tag is refused, with a message naming the release the tap carries.
- brew's clone of facebook/fb must already resolve that version. If it doesn't, the install stops before changing anything and says to run `brew update`, rather than letting `brew install` quietly install a different version.
- Formulae already installed from facebook/fb are left for `brew install` to upgrade in place. Local builds are replaced without asking, and anything from elsewhere still needs confirmation.
- `builds` and the picker mark only that release as installable, and name the release facebook/fb carries on every other row.

CI builds install from `idb-local/builds` exactly as before.

___

landed-with-radar-review

Differential Revision: D124844961

fbshipit-source-id: 14e7577605990a06e9c66d0e94e988a07739f06c
- [nicklockwood/SwiftFormat](https://github.com/nicklockwood/SwiftFormat) [80](https://github.com/nicklockwood/SwiftFormat/commits): Fix Windows build action
- [Ephemeral-AI-Lab/layerfs](https://github.com/Ephemeral-AI-Lab/layerfs) [55](https://github.com/Ephemeral-AI-Lab/layerfs/commits): Merge issue340-node-multiagent: LayerFS × dsh integration (#346)

This merges the LayerFS × dsh integration into main. The pieces:
- the dsh-layerfs bundle (Host plugin, client plugin, view model, the layerfs-dsh-minimalist preset);
- the LayerFS tab, panel, project picker and Init with progress, plus the storage routes and drawer;
- the demo workspace, whose sessions replay the design preview's stories on Sim or Live;
- the SDK changes it needs: named project Sandboxes, create intent and cleanup, and close lock order;
- core's Init import accounting and store.stats.

The branch's own commits carry their own LOC records. The dsh scope (dsh/packages) was added to tools/production_loc.py on this branch.

Production LOC: 87702 -> 93942 (delta +6240)
Scope: core 85857 -> 86110; SDK/application adapter 1845 -> 2092; dsh 0 -> 5740.
Reference absent (retired R9c; last counted 65,417 at tree 498dd1917812).
Method: tools/production_loc.py --root SNAPSHOT --json with the branch's counter, SHA-256 09f2b9028cf4480a076b706e38a6a1742f4eddf63cfbe9445c7829c81f9d86bc. The first parent is exact: 3dd27f4292c74713f6b412995601822075f9786d. The expected merge tree ca9063221df01cf5e8e741eb3675b66471dbb621 is identical to the branch tip fefab3a00, because main had no commits the branch lacked. The pinned main counter cb9cdb1a gives the same first-parent total (87702) and 88202 for the tree without the dsh scope.

Checks: dsh npm test (host, sim, cli, mock, view trace) and sdk/js tests on this tree; the dsh web Sim and Live demo runs are recorded on #346. No CI, release or performance qualification.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [jdx/mise](https://github.com/jdx/mise) [42](https://github.com/jdx/mise/commits): chore(deps): cargo update and bump zip to 9 for the symlink advisory (#14577)

<!-- entire-trail-link-start -->
https://entire.io/gh/jdx/mise/trails/813
<!-- entire-trail-link-end -->

`zip` before 9.0.0 applies Unix permissions through extracted symlinks
without checking the target stays inside the destination
(GHSA-4684-h2q9-2vcp). mise extracts downloaded `.zip` tool archives
with `ZipArchive::extract` (`mise_util::file::unzip`), so this moves
mise's own `zip` dependency to 9.x. `cargo deny check` was failing on
the advisory in CI for every open PR.

Per the maintainer's call this PR also runs a full `cargo update` rather
than keeping the lockfile focused. It is run with
`CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=allow` so the resolver does
not fall back to older Rust-1.88-compatible crates (a plain `cargo
update` downgraded `aws-sdk-s3` and pulled in an `lru` version with
RUSTSEC-2026-0253). Changes beyond the lockfile:

- `zip` 8 → 9 in the three manifests that declare it. `ZipFile::name()`
now returns a `Result`, so the two SLSA content-check errors that print
an entry name fall back to `<unreadable name>`.
- `rattler` 0.53 → 0.54 and `rattler_conda_types` 0.56 → 0.57, which the
updated `rattler_solve` requires. The conda backend's test helper builds
a `PackageRecord` with the new `BuildString` type.

`xx` is now 2.6.3, which uses zip 9 (jdx/xx#308, #310). `zip` 8.6.0 (via
aube and ubi) and 7.x (via `zipsign-api`) remain in the lockfile where
those crates still pin them; mise does not call their zip extraction.
aube's own bump is jdx/aube#1756 and needs a release before mise can
pick it up.

Validated with clippy (`-D warnings`, `--locked`), the conda and
`mise-util` tests, and a clean `cargo deny check` (advisories, bans,
licenses, sources) with a fresh advisory db.

*AI-assisted — Tool: Claude Code; model: Anthropic/Claude Sonnet 5.5;
version: unavailable.*

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Touches archive extraction and a broad dependency refresh
(Conda/rattler, compression, networking); behavior changes are mostly
upstream, with small API fixes for zip 9 and rattler_conda_types.
> 
> **Overview**
> Bumps **mise’s direct `zip` dependency from 8 to 9** so archive
extraction used for downloaded tool `.zip` files is not affected by the
symlink permission advisory (GHSA-4684-h2q9-2vcp). The same `zip = "9"`
change is applied in **mise-util** and **mise-brew-relocation**;
**`ZipFile::name()`** now returns a `Result`, so SLSA zip validation
errors use `<unreadable name>` when a name cannot be read.
> 
> Runs a **full `cargo update`** (with resolver flags so CI does not
pull incompatible Rust versions), which notably upgrades **`rattler` /
`rattler_conda_types`** and the rest of the Conda stack. The conda
backend test helper switches to **`BuildString::new_unchecked`** for
package build strings.
> 
> **`deny.toml`** adds an advisory ignore for remaining transitive **zip
7.x/8.x** copies (e.g. zipsign-api, aube, ubi) that mise does not use
for extraction. The fnox daemon test expectation now treats **Windows**
as platform-supported alongside the Unix targets, matching **fnox-client
1.40**.
> 
> <sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit
867af608e08043966d112eb62b75bb2bdd6518b4. Bugbot is set up for automated
code reviews on this repo. Configure
[here](https://www.cursor.com/dashboard/bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai
-->

## Summary by CodeRabbit

* **Bug Fixes**
* Archive validation reports now show a clear fallback when an entry
name cannot be read, including when flagging unsafe paths or symbolic
links.
* **Chores**
* Updated package and archive tooling versions. Existing feature
settings remain unchanged.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->

---------

Co-authored-by: Claude Sonnet 5.5 <noreply@anthropic.com>
- [XiaoMi/xiaomi-miloco](https://github.com/XiaoMi/xiaomi-miloco) [40](https://github.com/XiaoMi/xiaomi-miloco/commits): Merge pull request #596 from XiaoMi/docs/release-v2026.10.16-announce

docs: announce v2026.10.16 in README What's New
- [perkeep/perkeep](https://github.com/perkeep/perkeep) [35](https://github.com/perkeep/perkeep/commits): webui: add an indexed EXIF detail view

Photo metadata was indexed but unavailable from the detail page. Add an
authenticated search endpoint that reads EXIF rows on demand, preserving
directories, tag IDs, and numeric precision without growing the corpus or
default descriptions.

Expose a read-only EXIF aspect on file and photo-permanode detail pages.
Group tags by directory, expand long values, and link camera make/model to
literal-safe searches. Distinguish missing metadata from loading errors.

Center initial detail searches around the requested item and fall back to
an exact reference when it is outside the surrounding query, so file-only
URLs work without losing photo navigation context. Cover the API and UI
with storage, HTTP, and browser regression tests, and document the view.
- [Mentra-Community/MentraOS](https://github.com/Mentra-Community/MentraOS) [33](https://github.com/Mentra-Community/MentraOS/commits): Merge pull request #4820 from Mentra-Community/codex/nimo-capture-proof-support

Support capture-qualified NIMO publication and explicit Core authoring intake
- [thingsboard/thingsboard](https://github.com/thingsboard/thingsboard) [32](https://github.com/thingsboard/thingsboard/commits): Merge branch 'rc'
- [openai/codex](https://github.com/openai/codex) [28](https://github.com/openai/codex/commits): Render slash command prefixes as composer prompt markers (#54742)

## What changed

- Display the leading `/` in the prompt marker instead of the editable text, sharing prefix state with shell mode's `!`.
- Preserve command prefixes and text element offsets across submission, queuing, history, and external editing. Keep prefixes literal in plain-text composers.
- Track composer-owned slash command elements separately, omit them from exported draft elements, and refresh them when command availability changes.
- Let backward deletion at the start of the text remove the prompt prefix while preserving selected-text deletion and Vim Replace recovery.

## Testing

Add regression coverage for slash prompt cursor placement, prefix deletion, history search highlighting, dynamic command availability, and Vim Replace restoration, including Unicode text. Update rendering snapshots for the slash prompt marker.

GitOrigin-RevId: 0da42da8e98bf7885f9b0ba2c8d5ad4f44d6847e
- [ChrisBuilds/terminaltexteffects](https://github.com/ChrisBuilds/terminaltexteffects) [27](https://github.com/ChrisBuilds/terminaltexteffects/commits): Check that committed demos match the code they show (#297)

Record every demo with a fixed seed and store a fingerprint of its frames and render settings in demos.json. tests/test_demo_freshness.py re-records each demo on Linux with Python 3.10+ and fails, naming the re-render command, when code changes what a demo shows. All demos are re-rendered with the seed.

Closes #295
- [binwiederhier/ntfy](https://github.com/binwiederhier/ntfy) [23](https://github.com/binwiederhier/ntfy/commits): Prep v2.31.1 release: release notes, install docs

Move the unreleased server notes to v2.31.1 (released October 16, 2026) with a short intro, and bump
install.md to 2.31.1.
- [earendil-works/pi](https://github.com/earendil-works/pi) [14](https://github.com/earendil-works/pi/commits): docs(ai,coding-agent): generate models.json reference from schemas (#11038)

* docs(ai,coding-agent): generate models.json reference from schemas

Add npm run generate:references, which renders docs/models-configuration.md
from the models.json TypeBox schemas, and describe provider and model fields
in those schemas. Overrides get their own descriptions without defaults, and
compat sections cover the Responses API aliases.

closes #10790

* Modify changelog

* docs(ai,coding-agent): use shared thinkingLevelMap and promptCache schemas

Replace the per-use schema helpers with fixed schemas whose descriptions
hold for both models and modelOverrides entries.
- [block/buzz](https://github.com/block/buzz) [12](https://github.com/block/buzz/commits): Fix iOS channel crash from unbounded scroll depth (#8407)

### Summary

Opening a channel on iOS 27.0.1 could terminate Buzz when a reversed,
lazily loaded timeline reported an unbounded scroll extent. Flutter
forwarded `Infinity` to the native navigation bar, and UIKit threw
`CALayerInvalidGeometry` while setting the scroll view offset.

Use the finite viewport depth for that unbounded case, preserving the
scrolled-under appearance. Reject non-finite offsets at the native
platform boundary as a final safety check.

### Validation

- Added tests: a Flutter widget regression for an unbounded reversed
timeline, and an iOS native regression for a non-finite platform-channel
offset.
- Reproduced the original crash by tapping `#general` on an iPhone SE
running iOS 27.0.1. With this change, the channel rendered and survived
repeated back-and-reopen cycles. Native logging confirmed the channel
now sends finite offsets where it previously sent `Infinity`.
- The native regression passed on iOS 26.5 and 27.0 simulators with
Xcode 27.0. Flutter widget tests and `flutter analyze` passed.
- A full channel-flow simulator run was not available: the isolated
simulator Profile build could not resolve `BuzzPushKit`. The iOS 27.0.1
physical run exercised the full channel flow.
- The full Flutter suite had eight notification and push test failures,
all reproduced on the unchanged 0.24.0 source.

---------

Signed-off-by: Tom Brow <tomb@block.xyz>
- [cline/cline](https://github.com/cline/cline) [11](https://github.com/cline/cline/commits): fix(llms): send max_completion_tokens for gpt-6 ids on OpenAI-compatible endpoints (#15137)

The reasoning-era model-id matcher only covered o1/o3/o4 and gpt-5, so
gpt-6 requests (gpt-6-sol, gpt-6.1-sol, gpt-6-1-sol) kept max_tokens and
OpenAI/Azure rejected them. Widen the gpt pattern to gpt-5 through gpt-9,
keeping the version digit single so Azure's gpt-35-turbo stays out.
- [espressif/esp-idf](https://github.com/espressif/esp-idf) [10](https://github.com/espressif/esp-idf/commits): Merge branch 'contrib/github_pr_19184' into 'master'

fix(tools): Run idf.py monitor from the directory idf.py was invoked in (GitHub PR)

Closes IDFGH-18399

See merge request espressif/esp-idf!53432
- [nelvko/clashctl](https://github.com/nelvko/clashctl) [10](https://github.com/nelvko/clashctl/commits): style(status): 在底部横线后保留空行
- [THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC) [10](https://github.com/THU-MAIC/OpenMAIC/commits): refactor(chat): retire the legacy director-graph classroom chat (#1913)

* refactor(chat): move Pi's shared parser, action schemas and store-state type out of the legacy chat owners

Pi classroom chat still imports three pieces from the legacy director-graph
chat, which #1814 retires. Give each a Pi or neutral owner first, so the
legacy files can later be deleted without touching Pi:

- The structured-output parser (createParserState, parseStructuredChunk,
  finalizeParser, looksLikeStructuredFragment, ParseResult) moves verbatim
  from lib/orchestration/stateless-generate.ts to lib/chat/structured-output.ts.
  Only two comments change: they no longer name director-graph as the reader
  of the per-call ordered indices. This also stops the Pi route from loading
  director-graph and LangGraph through the parser's module.
- lib/orchestration/tool-schemas.ts moves unchanged to lib/chat/pi/tool-schemas.ts.
- AgentLoopStoreState moves unchanged from lib/chat/agent-loop.ts to
  lib/chat/store-state.ts; the Pi request path in use-chat-sessions uses it.

The remaining legacy consumers import from the new locations until they are
removed. No behavior change.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* test(chat): cover classroom model precedence on /api/chat/pi with the real resolver

The user-route, lock and body precedence for classroom interaction is
covered with the real resolveModel only through the legacy /api/chat
route, which #1814 removes. Route-level Pi tests mock resolveModel. Add the
same four cases against /api/chat/pi, asserting the model handed to the Pi
runtime:

- a chat-adapter user route wins over the body model;
- a locked classroom slot wins over the user route;
- with no matching route, the body model is used;
- a locked classroom slot is kept despite unlisted body and route models.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* test(eval): run the whiteboard layout eval against Pi classroom chat

The whiteboard eval drove the legacy /api/chat through runAgentLoop. Point
it at /api/chat/pi, which #1814 keeps as the only classroom chat:

- one Pi request per scripted user turn, with whiteboard tools enabled as
  the app does for in-class requests;
- text and actions grouped by each agent's messageId and sealed into their
  own history message at agent_end, since one Pi request can hand the turn
  to several agents;
- the previous turn's done.directorState carried into the next request
  within a scenario run, as the app does within a session;
- an error event, a non-200 response, or a stream without done fails the
  scenario through the existing error path, which skips its remaining turns
  (previously an error event was swallowed and the turn still captured);
- a native whiteboard event fails the run, because the harness cannot see
  the native child's server-side board. Not seeing one does not prove the
  server uses the legacy child; run the eval on a server configured for it.

Scores are a new baseline and are not comparable with runs of the legacy
runner. Scenarios, capture, scoring and reporting are unchanged.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* fix(eval): settle queued actions and cancel the request when a whiteboard turn fails

Review of the Pi whiteboard runner (#1913) found two lifecycle gaps on the
failure paths it added:

- A turn that failed (an SSE error, a native whiteboard event, or EOF without
  done) returned and disposed the scenario without waiting for its queued
  actions. The state manager drives shared store singletons, so a pending
  action could finish inside the next scenario and land in its screenshot.
  Every turn exit now settles the action queue first. A queued rejection is
  handled while the stream is still open and is logged at settle time, as on
  the success path, without replacing the turn's own error.
- Stopping early only released the reader lock, so the request kept running.
  Each turn's request now has its own AbortController, aborted on exit, and an
  unfinished response body is cancelled before the lock is released.

runScenario is exported with its CLI settings passed in, and main() runs only
when the file is the entry point, so an offline Vitest suite can exercise the
real function: failed turns settle before returning, the native early exit
aborts and cancels, a concurrent action rejection is not unhandled, and the
success path keeps one Pi request per turn, messageId grouping, directorState
carry-over and score:null on scorer failure.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* test(eval): run the answering and answer-content evals on Pi; retire premature-end

Both evals drove the legacy single-step director prompt and agent prompt,
which #1814 retires. Run them on the real Pi director in process instead
(eval/orchestration/pi-harness.ts): the Pi config helpers supply agent
configs and budgets, whiteboard tools are on as for classroom requests,
thinking is off, and the legacy child runtime is pinned. The harness skips
the HTTP route, so route authorization and tool-capability checks are not
exercised.

- answering classifies by the first recorded call_agent attempt in the
  director tool trace: TEACHER, OTHER_AGENT (another or a non-existent agent),
  NO_DISPATCH (none recorded; wrong, kept in the denominator), or ERROR (a
  failed run, excluded as before). A later recorded attempt never rescues
  the first.
- answer-content judges the full reply of the first recorded teacher attempt.
  A failed run, no recorded teacher attempt, or a first one that is skipped,
  marked isError or empty scores 0. The judge, opening window, threshold and
  all-samples denominator are unchanged. Pi's short teacher replies make the
  two metrics nearly coincide, and the score includes routing.
- Both score only what the trace records. A schema-rejected attempt is not
  recorded, so a later one can score, and a legacy child's partial text after
  a provider failure is judged. Scores can be overstated. Real-chain tests
  (real Pi loop and agent SDK, scripted StreamFn) pin both limits.
- The old prompt A/B variants are removed; results are a Pi baseline.
- premature-end is retired: its single END decision has no Pi counterpart,
  and the close gate does not show a question was answered.
- The three remaining eval scripts load with tsx --conditions=import, so
  ESM-only dependencies resolve.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* refactor(chat): always run classroom chat on Pi and fail builds that still opt out

The classroom chat hook, the /api/chat/pi route and PlaybackChromeRoot no
longer read NEXT_PUBLIC_PI_CHAT_ENABLED. The hook sends every turn through
the existing Pi single-request path; the frontend no longer calls the legacy
/api/chat loop (fetchStatelessChat and the runAgentLoop tail are removed).
The Pi branch itself is unchanged apart from indentation.

isPiChatEnabled and its readDefaultOnBoolean helper are removed. The
independent courseware-reference gate stays default-off.

next.config.ts now exports a phase function. In the production-build phase
it fails when NEXT_PUBLIC_PI_CHAT_ENABLED is set to anything other than '',
'true' or '1' (exact match), which covers every value that used to select
the legacy runtime. The error names the value and points to the Classroom
model setting, the google native preset for Gemini, and the administrator
for managed configurations. Other phases do not check the flag. The fixed
env pin for the flag is removed.

This is an intermediate step of #1814 PR 3: the legacy route, director graph
and agent loop are still present and are removed in a follow-up commit, and
Docker/Compose wiring and docs still describe the old rollback.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* refactor(chat): remove the legacy director-graph classroom chat backend

The frontend has run every classroom turn on /api/chat/pi since the previous
commit, so nothing reaches the legacy stack any more. Remove it:

- app/api/chat/route.ts (no stub, redirect or 410; /api/chat/pi stays)
- lib/orchestration/{stateless-generate,director-graph,ai-sdk-adapter,
  director-prompt,prompt-builder}.ts and lib/chat/agent-loop.ts
- summarizers/{conversation-summary,message-converter}.ts
- the director, agent-system and agent-system-wb-* templates, the
  speech-guidelines and whiteboard-reference snippets, and their prompt and
  snippet IDs

Pi's default legacy child, the shared structured-output parser, the Pi
tool schemas, the shared summarizers, the registry and the protocol types
are unchanged. Dependency declarations are left for a follow-up commit.

Tests:
- Drop the legacy chat route from the model-authorization tests and the
  coverage matrix. The mixed compatibility cases keep their six and eight
  stage assertions, and the exhaustive resolver call-site scan is unchanged.
  The locked-classroom case now goes through /api/chat/pi.
- Retire chat-route-user-routes (its precedence cases are rebuilt on the Pi
  route in route-model-precedence), the agent-loop async-state test, and the
  conversation-summary test.
- Keep the #511 intent as a history input contract on Pi:
  toHistoryMessages keeps the human challenge as a user turn in order, and
  buildUserPrompt still reports it after a later agent reply.
- Move the role, peer-context and language-directive prompt checks onto
  Pi's buildChildPrompt. Keep the PBL and placeholder-lint template tests and
  the getActionDescriptions LaTeX guard.
- Add middleware cases for POST /api/chat (401 without access, pass-through
  otherwise) and a Playwright spec that expects a plain 404 from the running
  app.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* build(deps): drop the unused @langchain/langgraph dependency

The legacy director graph was its only consumer and was removed in the
previous commit. Remove the root declaration and let pnpm update the
lockfile: @langchain/langgraph and @langchain/langgraph-checkpoint are no
longer installed. @langchain/langgraph-sdk stays (an optional CopilotKit
peer and a direct dependency of @ag-ui/langgraph).

@langchain/core is kept: CopilotKit requires it as a peer and pnpm would
install it anyway. partial-json and jsonrepair are kept for the Pi parser.

The re-resolution also moved vite 8.0.0's postcss from 8.5.15 to 8.5.23
(both were already in the lockfile; Next's postcss is unchanged) and
shortened four eslint-import snapshot keys without changing versions.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* build(docker): keep the Pi chat flag only as an input to the build check

NEXT_PUBLIC_PI_CHAT_ENABLED no longer selects a chat runtime; next.config.ts
only reads it to fail a production build that still opts out of Pi. Keep the
builder ARG and the Compose build-arg forwarding so an explicit false still
reaches that check, and drop the ENV line: build args are already visible to
the builder's RUN steps, and the value has nothing to configure in the image.

Remove the legacy-chat rollback comment and command from docker-compose.yml
and replace the rollback section of .env.example with a short note that the
legacy runtime is gone and which values now fail the build.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* docs: describe classroom chat after the legacy runtime removal

- Configuration docs (all six locales): drop the Pi rollback example, the
  advice to rebuild with the flag set to false and the Compose rollback
  command. Say instead that classroom chat always runs on Pi and needs a
  tool-calling Classroom model (google preset for Gemini), that the flag
  should be removed, which exact values a production build still accepts,
  and that the Compose service env_file supplies runtime values only.
- READMEs: drop the LangGraph badge and describe lib/orchestration and the
  Pi director loop as they now are.
- CHANGELOG: add the breaking change (model requirement, the flag, POST
  /api/chat answering 404 after the access gate) and the dependency removal.
- lib/prompts/README.md: point the role and length guidelines at
  lib/chat/pi/prompts.ts, correct which tests check placeholders, use a
  missing snippet in the error example, and start the whiteboard eval server
  with the native child runtime off.
- Remove the two comments that told CI and Playwright to leave the flag
  unset.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* test(chat): pin the server key on a user-route model; document answering eval limits

- route-model-precedence: when the user route switches the classroom model
  to another provider without a key of its own, assert that the model is
  built with the server key rather than the body's key.
- answering eval: state in the header comment and the generated report that
  a run which throws, is aborted or ends without done is ERROR even after it
  dispatched an agent, that ERROR samples stay out of the correct-rate
  denominator, and what the rate therefore does and does not measure. The
  scoring rules are unchanged.

Refs #1814

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
Co-authored-by: wyuc <wang-yc24@mails.tsinghua.edu.cn>
- [Y2Z/monolith](https://github.com/Y2Z/monolith) [10](https://github.com/Y2Z/monolith/commits): use the shortest encoding for data URLs, with minimal escaping
- [skypilot-org/skypilot](https://github.com/skypilot-org/skypilot) [9](https://github.com/skypilot-org/skypilot/commits): [Kubernetes] Map H100-MEGA to the nvidia-h100-mega-80gb GKE label (#11104)

The GCP catalog names the A3 Mega GPU H100-MEGA, and GKE labels A3 Mega
nodes nvidia-h100-mega-80gb. GKELabelFormatter turned H100-MEGA into the
legacy nvidia-tesla-h100-mega label, so with the GKE autoscaler the pod's
node selector never matched and the pod stayed pending until
provision_timeout. It also reported the label as H100-MEGA-80GB, which is
not a catalog name.

Map H100-MEGA to H100-MEGA-80GB before building the label, and map the
label back to H100-MEGA, in the same way H100 is handled. H100-MEGA-80GB
requests still produce the same label.

Signed-off-by: Madhav Jivrajani <madhav.jiv@gmail.com>
- [GNOME/librsvg](https://github.com/GNOME/librsvg) [8](https://github.com/GNOME/librsvg/commits): Update NEWS

Part-of: <https://gitlab.gnome.org/GNOME/librsvg/-/merge_requests/1232>
- [adafruit/Adafruit-GFX-Library](https://github.com/adafruit/Adafruit-GFX-Library) [7](https://github.com/adafruit/Adafruit-GFX-Library/commits): Merge pull request #519 from mikeysklar/esp8266-optimistic-yield

Make small drawing calls fast again on ESP8266
- [lancedb/lancedb](https://github.com/lancedb/lancedb) [7](https://github.com/lancedb/lancedb/commits): ci: ignore yanked zip, update rustls, remove unneeded deny rules (#4560)

Old versions of the zip crate have been yanked due to some rather
serious vulnerabilities. However, it is a transitive dependency via
`candle` and they have not yet released a patch.

For now I think the best course of action is to continue to ship,
knowing that we will need to address this issue as soon as candle
upgrades.

I also updated rustls since we have passed the 48 hour mark and I
removed all deny exclusions that were no longer needed.
- [facebookincubator/muse-gadget-sdk](https://github.com/facebookincubator/muse-gadget-sdk) [6](https://github.com/facebookincubator/muse-gadget-sdk/commits): esp32: Espressif ESP-Mosaico (ESP32-S31) board support (experimental) (#223)

The ESP-Mosaico: an ESP32-S31 (two RISC-V cores at 320 MHz, 16 MB PSRAM),
a square 2.16" 480x480 CO5300 AMOLED with CST9217 touch, an ES8311 codec,
a BQ27220 fuel gauge, the AI and BOOT buttons.

- components/muse/boards/board_esp_mosaico.c drives the parts itself, with
  pins and init sequences from Espressif's esp-mosaico-bsp; eFuse USER_DATA
  tells board revisions v1.0 and v1.2 apart (I2C, LCD SCL/RST, codec rail).
  Talk on AI, aux on BOOT; battery from the fuel gauge; power off through
  the board's latch. Hints from Espressif's drawing: the mic at the AI key
  (top edge), the power icon at ON/OFF (bottom, right of USB-C).
- muse_ui: a board's no_ring shows progress as a bar along the bottom edge
  instead of a circle around Muse (the panel is square).
- devices/sdkconfig.muse-esp-mosaico: target, 320 MHz, 16 MB QIO flash,
  PSRAM as Espressif's template sets it, UART console (USB-C is the S31's
  high-speed OTG), unsigned app (a signed one can't hand over to the
  board's Vibe Mode firmware, whose image it checks against our key).
- partitions_mosaico.csv keeps the board's retained first 2 MB (Vibe Mode
  in factory, sysmeta, coredump) and puts the app in ota_0 at 2 MB.
- ESP-Iris and Vibe Mode: devices/sdkconfig.muse-esp-mosaico-iris (the
  product contract the Vibe Mode firmware checks), components_mosaico/
  muse_mosaico_iris (starts ESP-Iris and the app-side recovery support, so
  later installs need no buttons), added by cmake/project.cmake from an
  esp-mosaico-utils checkout (MOSAICO_UTILS).
- tools/muse/board.sh mosaico: ESP-IDF master at 7b9cc1ac (IDF_EXPORT_S31;
  the S31 isn't in v6.0.1), builds an ESP-Iris System Update bundle, and
  flashes it with Espressif's mosaico.py iris system-update, never esptool
  (factory holds Vibe Mode).
- devices/README.md, AGENTS.md: the board, its tools and how to install.

Tested on a v1.2 board: installed through Vibe Mode, boots (display,
touch, audio self-test, battery), normal -> Vibe Mode -> normal with the
same Device ID and new boot IDs, no crash. idf.py build (C5 default),
s3-216 and the host tests (587, OK) and UI simulator pass. Not in CI: it
needs ESP-IDF master and esp-mosaico-utils.
- [fluidd-core/fluidd](https://github.com/fluidd-core/fluidd) [6](https://github.com/fluidd-core/fluidd/commits): chore: updates CHANGELOG.md and package version

Signed-off-by: Pedro Lamas <pedrolamas@gmail.com>
- [FreeRTOS/FreeRTOS-Kernel](https://github.com/FreeRTOS/FreeRTOS-Kernel) [5](https://github.com/FreeRTOS/FreeRTOS-Kernel/commits): Add release note for V11.3.2 (#1514)
- [Automattic/simplenote-android](https://github.com/Automattic/simplenote-android) [4](https://github.com/Automattic/simplenote-android/commits): Build PR prototypes on demand (#1900)
- [cactus-compute/needle](https://github.com/cactus-compute/needle) [4](https://github.com/cactus-compute/needle/commits): refactor: simplify optimizer setup in finetune_main by removing ROWS_LR and consolidating learning rate scheduling
- [KittenML/KittenTTS](https://github.com/KittenML/KittenTTS) [4](https://github.com/KittenML/KittenTTS/commits): Update api.md
- [RivoLink/leaf](https://github.com/RivoLink/leaf) [4](https://github.com/RivoLink/leaf/commits): Merge pull request #338 from DS-argus/fix/clicks-on-drawn-rows

fix: clicks on drawn rows
- [verl-project/verl](https://github.com/verl-project/verl) [4](https://github.com/verl-project/verl/commits): [trainer] fix: use 'enable_switch' instead of 'hybrid_engine' to decide whether create rollout instance on hybrid resource (#7958)

as the title

### What does this PR do?

> Add **concise** overview of what this PR aims to achieve or
accomplish. Reference related GitHub issues and PRs that help with the
review.

### Checklist Before Starting

- [x] Search for similar PRs. Paste at least one query link here: ...
- [x] Format the PR title as `[{modules}] {type}: {description}` (This
will be checked by the CI)
- `{modules}` include `fsdp`, `megatron`, `veomni`, `sglang`, `vllm`,
`rollout`, `trainer`, `ci`, `training_utils`, `recipe`, `hardware`,
`deployment`, `ray`, `worker`, `single_controller`, `misc`, `perf`,
`model`, `algo`, `env`, `tool`, `ckpt`, `doc`, `data`, `cfg`, `reward`,
`fully_async`, `one_step_off`
- If this PR involves multiple modules, separate them with `,` like
`[megatron, fsdp, doc]`
  - `{type}` is in `feat`, `fix`, `refactor`, `chore`, `test`
- If this PR breaks any API (CLI arguments, config, function signature,
etc.), add `[BREAKING]` to the beginning of the title.
  - Example: `[BREAKING][fsdp, megatron] feat: dynamic batching`

### Test

> For changes that can not be tested by CI (e.g., algorithm
implementation, new model support), validate by experiment(s) and show
results like training curve plots, evaluation results, etc.

### API and Usage Example

> Demonstrate how the API changes if any, and provide usage example(s)
if possible.

```python
# Add code snippet or script demonstrating how to use this
```

### Design & Code Changes

> Demonstrate the high-level design if this PR is complex, and list the
specific changes.

### Checklist Before Submitting

> [!IMPORTANT]
> Please check all the following items before requesting a review,
otherwise the reviewer might deprioritize this PR for review.

- [ ] Read the [Contribute
Guide](https://github.com/verl-project/verl/blob/main/CONTRIBUTING.md).
- [ ] Apply [pre-commit
checks](https://github.com/verl-project/verl/blob/main/CONTRIBUTING.md#code-linting-and-formatting):
`pre-commit install && pre-commit run --all-files --show-diff-on-failure
--color=always`
- [ ] Add / Update [the
documentation](https://github.com/verl-project/verl/tree/main/docs).
- [ ] Add unit or end-to-end test(s) to [the CI
workflow](https://github.com/verl-project/verl/tree/main/.github/workflows)
to cover all the code. If not feasible, explain why: ...
- [ ] Once your PR is ready for CI, send a message in [the `ci-request`
channel](https://verl-project.slack.com/archives/C091TCESWB1) in [the
`verl` Slack
workspace](https://join.slack.com/t/verl-project/shared_invite/zt-3855yhg8g-CTkqXu~hKojPCmo7k_yXTQ).
(If not accessible, please try [the Feishu group
(飞书群)](https://applink.larkoffice.com/client/chat/chatter/add_by_link?link_token=772jd4f1-cd91-441e-a820-498c6614126a).)
- [ ] If your PR is related to the `recipe` submodule, please also
update the reference to the submodule commit via `git submodule update
--remote` or `cd recipe && git pull origin main`.

Co-authored-by: Begunner <97716296+Begunner@users.noreply.github.com>
- [AcademySoftwareFoundation/OpenShadingLanguage](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage) [3](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/commits): ci: Cache Windows LLVM download, and retry curl downloads (#2187)

Our Windows CI often fails suriously in ways that are unrelated to
whatever changes are in a PR, and then succeeds upon retry (sometimes
after multiple retries). Often it's at the step where it's downloading
the pre-built Windows LLVM that we stashed on a Google drive (we could
not find a pre-built one with exactly the options we wanted, and we
can't build LLM from scratch in a reasonable time on the CI machines).

I finally (with some help from Claude) tracked down the source of
these failures: we're hitting Google Drive download limits!

This patch uses GHA cache action to reuse those downloads, generally
only retrieving from the Google drive the first time a branch or PR
goes through CI, which throttles usage enough to keep us under quota.

The specifics:

* Cache the unpacked LLVM (~/llvm/llvm-build) with actions/cache,
  keyed on LLVM_GOOGLE_DRIVE_ID. Both Windows jobs share the
  entry. The save step runs right after Dependencies, so a later build
  failure doesn't lose it. gh-win-installdeps.bash skips the download
  when the cache restored the directory.
* When we do download, check the result with `unzip -t`. If it is not
  a zip, fail with a clear message and print the start of the file.
* Add `--fail --retry 5 --retry-delay 10` to the curl downloads in
  gh-win-installdeps.bash, build_llvm.bash, and build_cmake.bash, to
  ride out transient network failures.
* Fix a missing `;` before `then` in gh-win-installdeps.bash.

Assisted-by: Claude Code / Claude Opus 5.5

Signed-off-by: Larry Gritz <lg@larrygritz.com>
- [anthropics/buffa](https://github.com/anthropics/buffa) [3](https://github.com/anthropics/buffa/commits): remote-derive: name primitives through ::core::primitive and call WirePayload methods by path (#719)

Fixes #707.

## What

The `buffa-remote-derive` expansions now spell the primitive types they
use as `::core::primitive::str`, `::core::primitive::u8` and
`::core::primitive::usize`. `from_wire` calls
`::buffa::WirePayload::to_str(&__buffa_payload)` and
`::buffa::WirePayload::as_slice(&__buffa_payload)` instead of using
method-call syntax.

## Why

- A type or alias named `str`, `u8` or `usize` in scope at the derive
took the primitive's place. `#[derive(MapStorage)]` beside `type usize =
u32;` failed inside the derive with E0053, and the string and bytes
derives failed the same way.
- A trait in scope, implemented for `WirePayload`, with a by-value
`to_str` or `as_slice` was called instead of the inherent method,
because method lookup tries the by-value receiver before it
auto-references. That compiled, and `from_wire` returned whatever the
trait returned.

The other method calls in the expansions (`.map` on the `Result`,
`.to_vec()` on the slice, `write_str` on the formatter) are safe: the
inherent method matches at the first lookup step, so a trait cannot take
it over.

## Implementation

- `string.rs`, `bytes.rs`, `map.rs`, `forwarders.rs`: the primitive
paths, and the two `WirePayload` calls by path, with a comment on why.
- `lib.rs`: one paragraph under "Reserved identifiers".
- Unit tests: `every_expansion()` now holds the list of expansions that
`every_binding_starts_with_the_reserved_prefix` built, so two new tests
walk the same set with `syn::visit`:
- `every_primitive_is_named_through_core_primitive`: no one-segment path
names a primitive type (all 17 are checked).
- `the_wire_payload_is_never_a_method_receiver`: no method call has
`__buffa_payload` as its receiver, and `from_wire` still reads it.
- New integration test `tests/shadowed_primitives.rs`: type aliases and
unit structs named `str`, `u8` and `usize` beside the string, bytes and
map derives (with `serde` and `arbitrary`), and a trait with by-value
`to_str` / `as_slice` that returns other data. Before the fix the file
fails to compile with 56 errors. With only the two method calls put
back, it compiles and `from_wire` returns `"shadowed"` instead of
`"wire"`.

Net change outside tests: +52/-30.

## Testing

Run locally on Windows (`x86_64-pc-windows-gnu`, toolchain 1.95.0,
protoc 33.5):

- `cargo fmt --all --check`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `cargo test --workspace`: all pass except two `buffa-types` tests that
fail on Windows only, because `SystemTime` there has 100 ns resolution;
unrelated to this crate
- `task doc`, `task test-arbitrary`
- `cargo test --manifest-path examples/custom-types/Cargo.toml`
- markdownlint

Conformance was not run.

AI-usage disclosure: Claude (Anthropic) was used as assistant.
- [Automattic/simplenote-ios](https://github.com/Automattic/simplenote-ios) [3](https://github.com/Automattic/simplenote-ios/commits): Build PR prototypes on demand (#1844)
- [buildroot/buildroot](https://github.com/buildroot/buildroot) [3](https://github.com/buildroot/buildroot/commits): package/swtpm: disable building manpages

Swtpm builds manpages using pod2man, and fails if it is not
available. The patch adds support for --disable-docs, which Buildroot
passes by default. Found while building in a container with minimal
dependencies.

Fixes: 87b9b126d23be1e95b3d2b82438f65e28f554a87 ("package/swtpm: add host package")
Signed-off-by: Fiona Klute (othermo GmbH) <fiona.klute@gmx.de>
Reviewed-by: Jarkko Sakkinen <jarkko@kernel.org>
Signed-off-by: Thomas Petazzoni <thomas.petazzoni@bootlin.com>
- [espressif/esp-adf](https://github.com/espressif/esp-adf) [3](https://github.com/espressif/esp-adf/commits): Merge branch 'bugfix/remove_esp_llm_license_field' into 'master'

fix(esp_llm): Remove invalid license fields

See merge request adf/esp-adf-internal!1591
- [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) [3](https://github.com/ghostty-org/ghostty/commits): Catalan translation of command palette (#13776)
- [openclaw/gogcli](https://github.com/openclaw/gogcli) [3](https://github.com/openclaw/gogcli/commits): build(deps): refresh eligible worker tooling (#1222)

Update Vitest to 5.0.5 and Cloudflare Workers types to 5.20261015.1 with matching lockfile entries. Preserve the worker's 24-hour release cooldown, pinned pnpm 11.28.5, security overrides, and Go requirements.

Validated with the frozen lockfile, full worker gate, independent Codex review, and exact-head CI. No production configuration or deployment changes.
- [SCons/scons](https://github.com/SCons/scons) [3](https://github.com/SCons/scons/commits): Merge pull request #4924 from adamsthws/fix/sconscript-future-flags

Do not compile SConscripts with the future flags of SCons modules
- [skiphansen/OpenEPaperLink](https://github.com/skiphansen/OpenEPaperLink) [3](https://github.com/skiphansen/OpenEPaperLink/commits): Merge branch 'master' into owm
- [sonocotta/esp32-audio-dock](https://github.com/sonocotta/esp32-audio-dock) [3](https://github.com/sonocotta/esp32-audio-dock/commits): Build ESPHome factory firmware
- [astral-sh/ty](https://github.com/astral-sh/ty) [2](https://github.com/astral-sh/ty/commits): [ty] Adopt stable macOS signing identifiers (#4743)

Adopt astral-sh/github-actions#20 so macOS releases use the stable
`sh.astral.ty` code-signing identifier across architectures. Rules tied
to the existing unprefixed x86_64 identifier will need a one-time
update.

Co-authored-by: zaniebot <242828183+zaniebot@users.noreply.github.com>
- [GameTec-live/ChameleonUltraGUI](https://github.com/GameTec-live/ChameleonUltraGUI) [2](https://github.com/GameTec-live/ChameleonUltraGUI/commits): feat: Update translations (#1033)
- [openclaw/acpx](https://github.com/openclaw/acpx) [2](https://github.com/openclaw/acpx/commits): fix(release): publish directly from repository Actions (#887)

* fix(release): publish directly from repository Actions

* style(docs): format release instructions

* fix(docs): link release workflow from published site
- [ophub/amlogic-s9xxx-armbian](https://github.com/ophub/amlogic-s9xxx-armbian) [2](https://github.com/ophub/amlogic-s9xxx-armbian/commits): Add contributors for KICKPI-K11C-V12(rk3566): zihelyu
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) [2](https://github.com/Piebald-AI/claude-code-system-prompts/commits): Update changelog for v2.1.301
- [RayWangQvQ/BiliBiliToolPro](https://github.com/RayWangQvQ/BiliBiliToolPro) [2](https://github.com/RayWangQvQ/BiliBiliToolPro/commits): chore(ci): archive Tencent SCF deploy workflow (#1236)

Move deploy-tencent-scf.yml to platforms/gitHubActions/bak/ and drop the sln entry, since Tencent SCF deployment is now handled by the stable release pipeline (publish-stable-release produces the tencent-scf.zip asset). Update both READMEs to mark the workflow as archived.
- [RfidResearchGroup/proxmark3](https://github.com/RfidResearchGroup/proxmark3) [2](https://github.com/RfidResearchGroup/proxmark3/commits): Merge pull request #3707 from TomHarkness/doc/pm5-flipper-usage-update-2

doc: update PM5-FLIPPER-USAGE.md with recent CEP/FAP fixes
- [zhongerxin/iPhone-use](https://github.com/zhongerxin/iPhone-use) [2](https://github.com/zhongerxin/iPhone-use/commits): Release 0.3.15: add iPhone system screenshot tool
- [alibaba/open-code-review](https://github.com/alibaba/open-code-review) [1](https://github.com/alibaba/open-code-review/commits): fix(config): fix bad config for providers or keys that cotains dots (self-defined) (#1661)

* main fix

* chore: write tests (AI)

* fix(config): validate dotted provider names across CLI and IDEs

---------

Co-authored-by: Kite <254839944+lizhengfeng101@users.noreply.github.com>
- [Alishahryar1/free-claude-code](https://github.com/Alishahryar1/free-claude-code) [1](https://github.com/Alishahryar1/free-claude-code/commits): patch: Fix macOS app menu-bar launch identity (#2095)

## Why

Fixes #2092. Launching the macOS app through its shell wrapper replaces
the app executable with Python. AppKit then sees Python's bundle instead
of Free Claude Code, and the menu-bar item can have a zero-height window
even though pystray reports it visible.

## How

- Run the installed uv-managed Python runtime inside a native app
executable, preserving the app's bundle identity and main thread. Enable
UTF-8 and retain the tool environment for imports and child processes.
- Build arm64 and x86_64 launchers during release staging and include
both in the existing wheel and source distribution. Select the launcher
matching the installed Python architecture.
- Create and ad-hoc sign the app through a Python installer helper.
Validate its runtime, stage replacements, preserve foreign apps and
Desktop entries, and recognize existing FCC ownership markers during
upgrades and uninstall.
- Add native macOS coverage for bundle identity, visible menu-bar
geometry, server lifecycle, duplicate launches, child processes, and
reinstall. Add Windows and Linux source-distribution rebuild checks and
require these jobs in CI.




<!-- greptile_comment -->

<!-- greptile_summary -->

<h2><a
href="https://app.greptile.com/api/retrigger?id=81926736"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source
media="(prefers-color-scheme: light)"
srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img
alt="Retrigger"
src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"
align="right"></picture></a><a
href="https://app.greptile.com/alishahryar1/github/Alishahryar1/free-claude-code/-/pull/2095"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source
media="(prefers-color-scheme: light)"
srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img
alt="View in Greptile"
src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"
align="right"></picture></a>Confidence Score: 5/5</h2>

<!-- greptile-impact-verdict --> No outstanding findings prevent
merging.

<details open><summary><h3>Summary</h3></summary>

The PR replaces the macOS shell launcher with a native executable that
keeps Free Claude Code's app identity while running its installed Python
environment.
- The macOS app keeps its identity while running the desktop app.
- Release packages carry native launchers for both Mac architectures.
- CI checks the native Mac app on Intel and Apple silicon.
</details>

<!-- greptile_confidence_score:5 -->

<sub>Reviews (2) · Last reviewed commit: ["Restore POSIX uv reuse
regression
covera..."](https://github.com/alishahryar1/free-claude-code/commit/b50bb8449e6827ba73581c09826a71b046aa1ab4)
· [Reviewed by
Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_public&utm_content=alishahryar1/free-claude-code)</sub>

<!-- /greptile_comment -->
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) [1](https://github.com/anthropics/claude-agent-sdk-python/commits): chore: bump bundled CLI version to 2.1.302
- [anthropics/claude-code](https://github.com/anthropics/claude-code) [1](https://github.com/anthropics/claude-code/commits): chore: Update CHANGELOG.md and feed.xml
- [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) [1](https://github.com/anthropics/claude-cookbooks/commits): feat(managed_agents): add agent security review cookbook (#926)
- [databendlabs/openraft](https://github.com/databendlabs/openraft) [1](https://github.com/databendlabs/openraft/commits): ci: refresh contributors monthly

Keep contributor credits current without manual refreshes.
Open a pull request only when generated files change.
- [dtolnay/thiserror](https://github.com/dtolnay/thiserror) [1](https://github.com/dtolnay/thiserror/commits): Ignore deprecated_attributes_without_since pedantic clippy lint in test

    warning: `deprecated` attribute without specifying what version of the crate deprecated the item
      --> tests/test_lints.rs:64:5
       |
    64 |     #[deprecated]
       |     ^^^^^^^^^^^^^ help: add a version: `#[deprecated(since = /* version */)]`
       |
       = help: for further information visit https://rust-lang.github.io/rust-clippy/main/index.html#deprecated_attributes_without_since
       = note: `-W clippy::deprecated-attributes-without-since` implied by `-W clippy::pedantic`
       = help: to override `-W clippy::pedantic` add `#[allow(clippy::deprecated_attributes_without_since)]`

    warning: `deprecated` attribute without specifying what version of the crate deprecated the item
      --> tests/test_lints.rs:71:9
       |
    71 |         #[deprecated]
       |         ^^^^^^^^^^^^^ help: add a version: `#[deprecated(since = /* version */)]`
       |
       = help: for further information visit https://rust-lang.github.io/rust-clippy/main/index.html#deprecated_attributes_without_since

    warning: `deprecated` attribute without specifying what version of the crate deprecated the item
      --> tests/test_lints.rs:76:5
       |
    76 |     #[deprecated]
       |     ^^^^^^^^^^^^^ help: add a version: `#[deprecated(since = /* version */)]`
       |
       = help: for further information visit https://rust-lang.github.io/rust-clippy/main/index.html#deprecated_attributes_without_since

    warning: `deprecated` attribute without specifying what version of the crate deprecated the item
      --> tests/test_lints.rs:84:9
       |
    84 |         #[deprecated]
       |         ^^^^^^^^^^^^^ help: add a version: `#[deprecated(since = /* version */)]`
       |
       = help: for further information visit https://rust-lang.github.io/rust-clippy/main/index.html#deprecated_attributes_without_since
- [eradman/entr](https://github.com/eradman/entr) [1](https://github.com/eradman/entr/commits): Set git user.name in system tests

In a Debian docker image only setting git user.email raises the warning
"Author identity unknown".
- [fishjar/kiss-translator](https://github.com/fishjar/kiss-translator) [1](https://github.com/fishjar/kiss-translator/commits): fix(options): 修复服务配置添加菜单中二级子菜单无法弹出的问题 (#1182)

- 限制 DropdownRoot 仅在 MuiSelect 下拉菜单中生效，恢复通用 MuiMenu 的原生弹层和定位能力
- 为二级菜单外层增加事件穿透，确保展开状态下仍可直接点击切换其他分类
- 补充 OptionsTheme 下点击展开与切换分类的单元测试
- [huggingface/lerobot](https://github.com/huggingface/lerobot) [1](https://github.com/huggingface/lerobot/commits): refactor(motors): one rustypot-backed SerialMotorsBus for Feetech and Dynamixel (#4672)

* refactor(motors): drive the Feetech and Dynamixel buses through rustypot

The Feetech and Dynamixel buses reached the wire through the vendors'
pure-Python SDKs, behind a layer shaped like them (port and packet
handlers, group sync readers and writers), and carried their own control
tables: addresses, sizes, sign bits, resolutions, baud rate codes and
model numbers transcribed from the vendor manuals, plus the code applying
them -- byte order, sign encoding, the ID sweep and its timeout.

rustypot implements both protocols in Rust, releases the GIL for the
whole transaction, and states and applies those facts itself. Each family
now names its servo definitions in `_servos()`, the rustypot controller
classes. The base bus resolves a model to one of them (rustypot spells
XL330M288 where LeRobot writes xl330-m288) and a register name by
lowering it, and on connect opens a `rustypot.Bus` with each motor's
definition. Models of one family therefore share a port -- STS and SCS,
XL430 and XL330 -- each read and written in its own byte order and sign
encoding. Retries, sync reads on servos without Sync Read, and the bus
scan are rustypot's as well.

Feetech's `protocol_version` goes: STS and SCS differ in byte order, in
whether they answer Sync Read and in which registers they have, and the
definition knows all three. The handshake accepts any model number a
definition covers, `scan_port()` sweeps the bus itself in place of
`broadcast_ping()`, and `setup_motor()` reaches a new motor at whatever
id it answers through the motor's own definition. `disconnect()` is safe
on a closed bus and releases the port even when disabling torque fails.

Gone: both tables.py, encoding_utils.py, the SDK-shaped protocols, the
`MotorsBus` alias, and deepdiff from the motor extras. pyserial stays in
them for `lerobot-find-port`. rustypot 1.10.0 is the first release that
carries the servo metadata and the multi-definition `Bus`.

The devices that relied on the old surface follow: HopeJR's hand drops
`protocol_version` and sync-reads its SCS servos, OpenArm Mini asks the
bus for the motor resolution, and LeKiwi clamps wheel speeds to the
sign-magnitude range of Goal_Velocity.

Tests replace the byte-level SDK mocks with an in-memory `rustypot.Bus`
keyed by motor id and register name. The IO helpers shared by both
families are tested once, on the base bus.

* docs: document the rustypot-backed motor buses

The install steps stop sending users to the vendor SDKs, the hardware
guide lists the servos rustypot defines and points new models at rustypot
rather than at control tables that no longer exist, and the API page
documents SerialMotorsBus and both family buses.

* build(deps): rustypot 1.11.0, and one serial-motors extra

rustypot 1.11.0 finds a servo model by name with its exact model number,
states what differs between families (homing offset sign, operating mode
values, factory baud rate, whether the EEPROM has a lock), turns the
torque of a whole bus on or off, scans with a broadcast ping, and sets a
new motor's id and baud rate. LeRobot's bus is about to rely on all of it.

One bus class will drive both families, so there is one extra to point
users at: serial-motors installs rustypot and pyserial. feetech and
dynamixel stay, as the names the setup guides use, and now alias it.

* refactor(motors): one SerialMotorsBus for Feetech and Dynamixel

FeetechMotorsBus and DynamixelMotorsBus had become a list of rustypot
classes plus a handful of facts about each family: which way the homing
offset goes, which operating mode value means position control, whether
the drive mode is a register, which acceleration and firmware registers
exist, and the Feetech lock. rustypot 1.11.0 states those facts in its
servo definitions, so SerialMotorsBus is now the one, concrete bus:

- each motor's model is looked up with rustypot.find_model, which gives
  its exact model number and its definition. The handshake and the motor
  search check that exact number again, so an SM8512BL set up as an
  sts3215 is refused, though both share a control table;
- calibration reads and writes the homing offset where the register
  exists (not on the SCS), compares the drive mode where it is a register
  (Dynamixel) and applies it in software elsewhere (Feetech), and centres
  a joint with the homing offset sign of the definition;
- the firmware check runs on the motors that report a firmware major and
  minor version (Feetech); configure_motors writes the acceleration
  registers a motor has; set_operating_mode("position") writes each
  motor's own value for a mode named the same on every family;
- torque goes on or off through rustypot's Bus.set_torque, which tries
  every motor, moves the Feetech lock with the torque, and reports the
  motors that failed: one that does not answer no longer leaves the
  motors after it under torque, and the error names it;
- setup_motor has rustypot change the id and the baud rate (torque off
  and lock open first), with no reopening of the bus, and puts the port
  back at the default rate even when that fails. The motor search tries
  the default baud rate, then the factory one, then the rest in a fixed
  order, with a broadcast ping where the servo answers one, which covers
  a USB adapter's latency once. scan_port takes the model it looks for,
  releases the port when a scan fails, and reports ids only;
- a status packet is waited for 50 ms, not a second, so one lost reply
  costs a 30 Hz loop a tick (the SDKs waited about 35 to 50 ms).

FeetechMotorsBus and DynamixelMotorsBus stay for one release as
deprecated aliases (FeetechMotorsBus still accepts protocol_version), and
so do their OperatingMode and TorqueMode enums. A missing rustypot points
to the serial-motors extra. Resetting the calibration of an SCS no longer
writes a homing offset it does not have. On Dynamixel, is_calibrated no
longer compares the id stored in the calibration file, like Feetech.

* refactor(robots,teleoperators): drive the motors through SerialMotorsBus

The SO, Koch, OMX, LeKiwi, HopeJR and OpenArm Mini devices built a
FeetechMotorsBus or a DynamixelMotorsBus and wrote operating modes as the
value of a family's enum. They now build a SerialMotorsBus and name the
mode: set_operating_mode("position"), "extended_position", "velocity", or
"current_based_position" for the Dynamixel grippers. DriveMode comes from
lerobot.motors.

* docs: one SerialMotorsBus for Feetech and Dynamixel

The hardware guide builds its example robot on SerialMotorsBus, names
operating modes, and says what the definitions settle between families.
The API page documents SerialMotorsBus and DriveMode, and mentions the
two family classes as deprecated aliases.

* refactor(motors): fold the I/O helpers into their callers, drop scan_port

With the torque and the motor setup handled by rustypot, _write,
_sync_read and _sync_write each had a single caller: write, sync_read and
sync_write now talk to the rustypot bus themselves. _read stays, shared by
read and ping, and always raises; its raise_on_error and err_msg
parameters, which only ping used, go, and ping catches the error instead
of asking not to get one. The Feetech firmware check reads the major and
minor versions with one sync read each rather than two reads per motor.

scan_port goes: nothing in LeRobot calls it, and rustypot's Bus.scan and
Bus.broadcast_scan do the same for anyone who needs it.

The tests that went through the private helpers now go through read,
write, sync_read and sync_write against the in-memory bus.

* fix(motors): restore the port after a failed motor search, check a set-up motor

setup_motor started its cleanup only after finding the motor. The search
walks the baud rates, so a motor that was not there left the port on the
last rate tried, and anything done next on the same bus went unanswered.
The search now runs inside the try whose finally puts the port back at the
default rate.

A motor answers the id and baud rate writes before they take effect, and
nothing checked that they did. setup_motor now reads the model number back
at the new id and the default baud rate, and raises if the motor does not
answer there with the model it is configured as.

* refactor(motors): check selections before writing, raise on sync-read errors, document the bus

- set_operating_mode() and set_half_turn_homings() check every selected motor before
  writing any register, so an unsupported motor leaves no partial configuration.
- sync_read() raises on a motor's error status, as read() does.
- Register names normalise whatever their case; set_baudrate() and ping() need a
  connected bus; resolution() raises for a model that counts no steps; the firmware
  check compares the motors of each servo definition on their own.
- Each model is looked up once, and the bus opens rustypot's Bus through _open_bus()
  and reaches it, typed, through _connected_bus.
- Errors name motors by motor ID; docstrings follow the documentation format and its
  cross-references. The hardware tutorial and the motor API page gain the serial-motors
  extra, the SCS limits, a migration note and the DriveMode members.
- Tests cover write and sync-read error statuses, sync writes no motor answers,
  calibrated commands and calibration mismatches of each family, through bus helpers
  shared by the family suites.

* fix(motors): raise when a motor refuses an access, not on an alarm

A status byte also carries conditions a motor reports while it carries the access out:
a Feetech status only reports alarms (input voltage, temperature, current, load), and on
protocol 2 bit 7 is the alert of a latched hardware fault. Raising on them stopped a
control loop on a gripper squeezing an object, and made ping() miss an overloaded motor.

read(), write(), sync_read() and ping() now fail only when the status says the motor
refused the access: an error number on protocol 2. The protocol-1 servos LeRobot drives
are Feetech ones, which never refuse through their status.

* fix(motors): ask the servo definition whether a status refuses the access

rustypot 1.13.1's ServoDefinition.refuses tells a refusal from an alarm for every
servo it defines, so the bus no longer keeps its own copy of the rule, which assumed
every protocol-1 servo is a Feetech one. The serial-motors extra now needs rustypot
1.13.1, and the tutorial links rustypot's servo guide at that version.
- [jqlang/jq](https://github.com/jqlang/jq) [1](https://github.com/jqlang/jq/commits): Disable colored output on a dumb terminal (#3552)

Enable colored output by default only when the TERM environment variable
is set to a value other than dumb, as git and grep do, so that users no
longer need to pass -M or set NO_COLOR on terminals that cannot display
escape sequences. Colored output is now disabled not only for TERM=dumb
but also when TERM is unset or empty. The -C option still enables colors
in all these cases. On Windows, colored output is still decided by
ANSICON and the console mode, and TERM is not checked.
- [react/yoga](https://github.com/react/yoga) [1](https://github.com/react/yoga/commits): Avoid fmod when rounding layout results to the pixel grid (#2041)

copysign(x - trunc(x), x) is bit-identical to fmod(x, 1.0) for every
double but avoids the libm fmod loop, which is slow on Android's bionic.
roundValueToPixelGridDouble runs six times per node on every layout
pass.

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [shidenggui/easytrader](https://github.com/shidenggui/easytrader) [1](https://github.com/shidenggui/easytrader/commits): Add removal notice
- [TactilityProject/Tactility](https://github.com/TactilityProject/Tactility) [1](https://github.com/TactilityProject/Tactility/commits): App Hub, Setup, BT, tt, posix http, and more (#697)
- [tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro) [1](https://github.com/tensorflow/tflite-micro/commits): Enable parse_headers in Bazel CI and fix missing header dependencies (#3879)

Enable parse_headers on TFLM cc_library targets (tflm_cc_library and signal/ packages) and pass --process_headers_in_dependencies in --config=ci so header-only libraries and standalone headers are checked by layering_check in OSS CI.

Scoping parse_headers to TFLM targets (rather than globally in .bazelrc) avoids parsing headers in external repositories such as @flatbuffers. Also remove obsolete -parse_headers exclusions and add missing header dependencies caught by standalone header parsing.

BUG=n/a