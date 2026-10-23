# Recent Activity in Starred Repositories
_178 active repos with 3006 new commits_

## [agent](https://github.com/topics/agent)
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) [20](https://github.com/OpenHands/OpenHands/commits): feat(canvas): quiet backend logs by default (#18830)

Co-authored-by: openhands <openhands@all-hands.dev>
- [trycua/cua](https://github.com/trycua/cua) [11](https://github.com/trycua/cua/commits): ci(spaces): shadow build on main, signed, notarized and attested (CUA-2066) (#5730)

Phase 1 of CUA-1991. Builds the Cua Spaces installer set on release-input
changes on main, keyed by input tree hash, with build-manifest.json,
attestations, verify-release.sh and a cost summary. Nothing consumes it yet;
cd-cua-spaces.yml is unchanged.

Co-authored-by: Claude Sonnet 5.5 <noreply@anthropic.com>

## [ai](https://github.com/topics/ai)
- [openclaw/openclaw](https://github.com/openclaw/openclaw) [722](https://github.com/openclaw/openclaw/commits): fix(update): preserve JSON errors for invalid repair channels (#180822)

With --json, an invalid update/repair channel printed a plain-text diagnostic and exited before the JSON renderer ran. The shared finalizer now uses the existing expected-error path, so --json gets a machine-readable error while exit status 1, human diagnostics and configuration are unchanged. Supersedes #180774, thanks @Leon-SK668.

Co-authored-by: Leon-SK668 <0668001470@xydigit.com>
- [BasedHardware/omi](https://github.com/BasedHardware/omi) [432](https://github.com/BasedHardware/omi/commits): refactor wave 2: speakers v2, media/noise, cross-device, calls/recaps/actions/vocabulary, MCP read-API correctness (shadow by default) (#23358)

## What and why

Integrate wave 2 of capture, speaker evidence and notes against the
reviewed wave-1 authority. This is a branch-only handoff: no PR, merge
to main, runtime cohort, deployment or production data access. All
implementation commits use the requested co-author trailer.

- Wave 1: merged origin/refactor-integration first (2ca1c676bc7); main
had not absorbed #23335 at intake. Its verified merge f6021c0f9dd landed
at 2026-10-22 20:39:40Z and is now merged here.
- V1 speakers: 4c368cc8ae5. Participant hints and bounded
compatible-cluster reduction, explicit channel/near-field/voice anchors,
ambiguity-preserving people matching and enrollment quality. Applied
speakers-live-name-hook.patch. Reconciled the newer wave-1 abstention
contract: preserve unresolved identity while allowing compatible count
consolidation.
- V2 media/noise: 1519a9a1b2b. Applied media-consumer-integration.patch.
Classify before notes, keep media/noise history with deterministic
minima, suppress memory/task/recap derivation through one shared helper,
and persist terminal intelligence suppression for replay. Explicit
restore/reprocessing clears the exclusion and marker. Shared live/sync
hallucination admission remains cohort-only.
- V3 cross-device: a05a1f823373. Completed-capture shared-speech
reconciliation and exact-key coverage aliases reuse the ledger and
capture-group writer. Originals and audio remain; unique secondary
speech remains visible. Streaming partial-window suppression and
automatic secondary-socket dispatch remain unimplemented.
- M MCP: 34d47d3e84fc. Correct filtered memory candidates, bounded
default lists, fair batch budgets/continuations, whole-window screen
aggregates, truthful counters/stubs, call metadata, provenance and
explicit timezones. Additive read correctness is on by default, as
authorized in lane M. Omitted timezone retains released UTC behavior.
- V4 calls/recaps/actions/vocabulary: d4509d3b4af6.
Completed-local-day/grace-period recaps, durable states and rollback
recovery, positive-evidence call metadata, owner-involved commitments
and bounded Soniox vocabulary. Applied calls-boundary-integration.patch
and calls-prompt-integration.patch, including authenticated agent
identity and cohort-sensitive notes cache identity. Automatic stale task
mutation remains partial: its producer-bound reference and canonical
CAS/reminder adapter do not exist in this lane. Older screen/desktop
producers still need explicit joined-controls evidence.

## Defaults, flags and ramp

SPEAKER_EVIDENCE_MODE, MEDIA_NOISE_MODE, CAPTURE_COVERAGE_MODE,
NOTES_PACKET_V2_MODE, EPISODE_BOUNDARIES_MODE, LIFECYCLE_V2_MODE,
CALLS_RECAP_MODE, ACTION_ITEMS_V2_MODE and STT_VOCAB_MODE remain shadow.
No serve cohort is configured. Existing client flags remain off/unknown.
Costly shadow database writers use refactor_modes.shadow_sampled:
CAPTURE_COVERAGE_MODE_SHADOW_PERCENT,
SPEAKER_EVIDENCE_MODE_SHADOW_PERCENT and
EPISODE_BOUNDARIES_MODE_SHADOW_PERCENT, each default 5.
STT_VOCAB_MODE_SHADOW_PERCENT samples source reads at default 1. Serve
cohorts always write and zero disables sampled writes. All bindings are
declared and the registry regenerated. Invalid percentages keep the
bounded default. V4 phone/calendar boundary publication is serve-only
under CALLS_RECAP_MODE; shadow projects the evidence locally without
authority writes. No CALLS_RECAP_MODE_SHADOW_PERCENT binding is needed
for this serve-only choice. On-demand recaps explicitly bypass scheduled
grace; all scheduling/backfill keeps the completed-day grace.

Owner dazheng, by 2026-10-26: synthetic integrated acceptance, reviewed
runtime digest pilot, then 1% -> 5% -> 25% -> 100%, one full lookback
window per step. Keep modes shadow while configuring sampled serve
cohorts; mode serve is the 100% stage. Align producer/consumer runtime
cohorts (especially speaker/boundary evidence with media and calls) so
sampling does not make serving evidence unavailable. No expansion until
manual/identity violations, false folds, lost unique speech/custody,
false owner-call/media exclusions, genuine-speech drops and duplicate
recap deliveries remain zero. Inspect speaker count/anchor/agreement
metrics, omi_media_noise_shadow_total (especially repeated_sentence
admission receipts), cross-device duplicate/examined lines, coverage
admits/seconds, sync failures/latency and vendor spend. No paid
duplicate generation/transcription in shadow. Rollback modes to off and
clear runtime cohorts; durable lifecycle obligations still reconcile.
Persisted groups/classifications are non-destructive and may need
restore/reprocess after rollback. Budget cohort entry for one
regeneration per fingerprint-less legacy day inside the seven-day
lookback (subject to the existing per-run backfill cap); retained IDs
and delivery receipts prevent duplicate notifications. No serve cohort
was enabled for this work.

## Review disposition

| Review finding | Status | Resolution / reason |
| --- | --- | --- |
| V1 #1 nullable speaker | Done | Never project a null cluster speaker
into a numbered segment; production-seam regression. |
| V1 #2 count metrics | Done | Producer and observer share a
voice/channel partition helper; channel splits are not reductions. |
| V1 #3 learning state quality vs stale fence | Skipped | Requires
changing the transactional publication result and learning-state
contract, beyond a mechanical fix. Existing bounded quality counter
distinguishes rejection; track before serve ramp. Enrollment and
unpublished-blob cleanup remain protected. |
| V1 #4 live name-only guard | Done | Supplied patch applied before
text-only lookup/create/map mutation. |
| V1 #5 count cues | Skipped | No threshold change without audited
acceptance data. Acoustic thresholds, cannot-links and abstention
retained; count hints cannot force incompatible voices together. |
| V2 H1 dormant consumers | Done | Patch applied; real
processing/persistence, replay, all four consumer boundaries and
restore/reprocess exercised. |
| V2 M2 genuine foreign repetition | Skipped | No evidence supports
changing the threshold here. Zero serve cohort; pilot must audit
repeated_sentence receipts before expansion. Audio custody remains
intact. |
| V2 M3 shadow reads | Skipped | Production volume validation is outside
the no-prod-reads scope. Reads are bounded; no second paid call or
shadow media-edge write. Sampled speaker/boundary writers bound
mutations; serving pilots need aligned producer coverage. |
| V2 L1 collapsed metric checks | Done | Explicit conversation bucket
and strict unknown-check rejection with regression. |
| V2 L2 admission naming | Skipped | Distinct module namespaces, no
shared caller or behavior collision; avoid unrelated public rename. |
| V2 L3 sync hook size | Done | Existing no-content settlement needs a
small hook, covered by tests and line-count metadata. |
| V2 L4 fixtures | Done | Minimal request-authority and timeline fixture
updates retained. |
| V3 dead distinct_streams return | Done | Removed unreachable duplicate
condition; unknown devices abstain. |
| V3 shadow lane label | Done | Compare accepts explicit lane; V3 does
not emit an L1 fold observation. |
| V3 serve query transaction cost | Skipped | No query semantics change
without runtime evidence. Bounded alias validation reads remain; watch
sync latency/failures before expansion. |
| M P1 default memory failure | Done | Default lists use released-size
bounded reads, return data and explicit incomplete coverage; filtered
incomplete windows still error. |
| M P2 read amplification | Done | Physical-read regression pins bounded
default source batch. |
| M P3.1 aggregate cursor | Done | Ignore stale aggregate cursor and
explain whole-window behavior. |
| M P3.2 timestamps | Done | Released strings retained unless offset
format/timezone is requested. |
| M P3.3 calendar-day stub pagination | Skipped | Intentional
bounded-date contract; an old in-flight cursor may shift across
deployment. No historical rewrite or invented failure cause. |
| M P3.4 retired/private helpers | Done | Dead collector/branch/imports
removed; shared adapters public with migrated callers. |
| M P3.5 duplicate-ID progress | Done | Absolute occurrence cursor with
regression. |
| V4 HIGH boundary authority write | Done | Parent ruling wins: both
phone record and calendar ingest are serve-only under the calls cohort.
Shadow uses local evidence; the regression holds
EPISODE_BOUNDARIES_MODE=serve and proves a non-cohort user produces no
authority write. |
| V4 MEDIUM on-demand grace | Done | Explicit user_initiated plumbing
from generate_daily_summary_on_demand bypasses grace; scheduler/backfill
do not set it. Partial-day and post-midnight grace tests exercise the
actual producer. |
| V4 MEDIUM STT uid | Done | Both legacy initial/reconnect calls and the
managed Soniox leg pass authenticated request uid. Removed get_byok_uid
fallback; real managed config and legacy call seams are tested. |
| V4 MEDIUM vague_social / incident 09 | Done | Named counterpart plus a
concrete place/time retains owner-alias commitments, including catch up
with Matt in NYC. Fourteen incident/negative cases cover missing
feedback, CV review, Deepgram check, invitation/Drive, unrelated customs
purchase and bogus hiking. Promisor/provenance authority remains intact.
|
| V4 LOW legacy-day regeneration cost | Done | Budgeted in the ramp
above; no serve cohort enabled. |
| V4 LOW dead constants | Done | Removed six unused lane constants.
Actual shared cohort bindings now live in and are consumed by
refactor_modes._COHORT_ENVS; no env behavior changes. |
| V4 LOW stripped comments | Done | Restored explanatory shared model,
finalizer, notifications and Soniox comments/docstrings; public recap
docs distinguish legacy order and serving revision/state behavior. |
| V4 LOW inverted / expired parity labels | Done | Found vocabulary
emits agree; absent expired evidence compares the retained durable call
projection. Regression assertions pin both labels. |
| Integrator runtime-image closure | Done | All 19 contracts compared
using third_party_dependency_modules against origin/main; zero added
third-party modules. Incorporated PR #23355 branch and added GPU
closure/shim regressions. |

## Conflicts and shared contracts

Resolved person_pool.py by retaining incoming quality checks and wave-1
type annotation; duplicate_capture.py retains both lifecycle serving and
cross-device imports. Generated artifacts are regenerated from
generators, not resolved by hand. ContentKind has one literal definition
shared by stored/create models and policy; request classification stays
hidden/server-authored. BoundaryKind includes media_playback once.
Participant count and owner anchor live only in SpeakerEvidence. Call
fields are additive optional Conversation metadata; explicit boundary
proof survives canonical normalization and wire round trips. V4
persisted stubs pass through M with null generated_at. Media/noise-only
days report not_generated rather than falsely saying no recordings;
actual empty days keep no_recordings. Both one-shot and agentic prompt
mounts are exercised in off/shadow/serve.

The pipeline guide records integration, sampling, call/recap/prompt
contracts, replay and pending socket semantics. The developer storage
guide explains original-recording retention and unknown/remote metadata
without publishing rollout controls. Dead-code analyzer regenerated its
baseline without new suppressions; the allowlist tool deliberately never
auto-edits allowlists. Existing evaluator-only exceptions remain, and
imported wave-1 contract scaffolds have no stale allowlist entries.

## Runtime image closure audit (fix pass)

Merged fresh origin/main at 81270c66d1dd9b0a6a4ed866f2c8b8ea6c4abfff
after #23355 landed. It merged without conflicts and leaves exactly the
same source tree as fix commit ed2c03440df. Before #23355 landed, also
merged origin/fix-parakeet-policy-closure at
2d3ec7039c6f6a15d040b134c3082d91eeebcc4f; its remote branch was deleted
after merge. No unseen remote integration commits were overwritten.

The audit independently executes each revision's
backend/scripts/runtime_image_contracts.py
third_party_dependency_modules(contract) over every registered contract
(including lazy imports), without importing application code or reading
production. There are **zero added and zero removed third-party probe
targets across all 19 images** against the final main base; no new
lockfile/requirements package is needed.

| Runtime image | Added third-party modules | Removed probe targets |
| --- | --- | --- |
| backend-api | None | None |
| backend-workers | None | None |
| backend-realtime | None | None |
| backend-gateway | None | None |
| backend-pusher | None | None |
| backend | None | None |
| desktop-backend | None | None |
| pusher | None | None |
| models | None | None |
| memory-maintenance-job | None | None |
| x-connector-sync-job | None | None |
| frame-request-retention-job | None | None |
| day3-reengagement-email-job | None | None |
| notifications-job | None | None |
| diarizer | None | None |
| batch-pipeline-worker | None | None |
| parakeet | None | None |
| nllb-translation | None | None |
| plugins | None | None |

The earlier comparison against pre-#23355 main
4499deb154ffd811d9e679436d895fa0ca46f4fe had zero additions in all
images; the only removals were batch-pipeline-worker: fastapi.Request,
google.api_core.exceptions.AlreadyExists, google.cloud.tasks_v2,
google.protobuf, google.protobuf.duration_pb2 and
google.protobuf.timestamp_pb2; and parakeet: utils.speakers.policy plus
its BATCH_CLUSTER/PARAKEET_CLUSTER attribute candidates. Those are the
intended #23355 repairs, now present on both sides of the final
comparison.

Batch retry policy imports the dependency-light utils.capture.retry_cap
core, avoiding utils.sync.retry_hygiene -> utils.cloud_tasks.
Dockerfile-overwritten first-party shims are explicitly excluded from
checkout dependency probes: parakeet excludes utils.logging_config and
utils.speakers.policy; diarizer excludes omi_logging,
utils.logging_config and utils.stt.diarization_turns; nllb-translation
excludes omi_logging. The copied implementations are
standard-library-only. Full-backend/pusher copies use their real source
modules rather than checkout shims. Four new regressions verify the
three shim contracts and the batch worker's separation from Cloud Tasks.
Full final JSON evidence: image-closure-diff.json; earlier comparison:
image-closure-diff-pre23355.json; reproducible script:
audit-image-closure.py.

## Additional integration findings

- Done: M's successful-row timestamp fallback incorrectly gave persisted
V4 pending/failed/empty/not-generated stubs a creation-based
generated_at. The read adapter now preserves null; five direct
regressions, four actual producer-to-reader cases and a real REST smoke
cover it.
- Done: V4 used no_recordings after filtering a nonempty media-only day,
contradicting M's true recording count. That state is now not_generated,
with actual shared-policy generation regression; true empty-day behavior
is unchanged.
- Done: wave-1 abstention must preserve labels while V1 independently
consolidates compatible count clusters. Processing now keeps that
separation and null-speaker protection.
- Done: hermetic Firestore readiness fixture now includes the new MCP
query registry dependency in its copied control checkout; readiness
behavior and index enforcement remain unchanged.
- Done: whole-backend reason-label ratchet identified three new dynamic
label sites. Media/call metrics now expose closed normalization at the
label call, and person voice rejection uses a central three-reason enum
with an unknown fallback. The guard/debt list is unchanged; a new
regression prevents unbounded quality labels.
- Done: omit an empty speaker energy header so inactive cache
serialization remains byte-identical to the existing format; populated
energy metadata still round-trips. Whole-suite cache parity regressions
and four explicit cache tests cover both contracts.
- Done: isolated legacy fixtures retain real pure policies/metric owners
before package stubs, initialize media admission state, execute call
metadata in explicit off mode, and stub new profile/screen reads. Usage
tests supply eligible recordings and target the retained legacy budget
entrypoint; task response assertions include additive source without
exposing lifecycle fields. Historical telemetry byte parity runs with
speaker evidence off, while active energy cache reload has a separate
regression. Voice-pool retention fixtures use compatible, normalized
samples; V1 rejection guards remain intact.

## Validation

Pre-V4 combined validation on ec9bd4f6695: **2,725 passed across 97
focused backend files**, 15 standard marker deselections, no skips. Real
live name gating, media processing/persistence/restore, replay, recap
consumers and V4/M stub timestamps have integrated regressions.
Repository preflight: **65 selected checks passed**; metadata
validation: five passed. Separate CI slow guardrails: **2,049 passed**,
1,342 deselected (all 25 manifest files). Flutter
capture/labels/Home/parity: **86 passed, 5 existing skips**. Swift
capture/group/decoder suites: **33 passed**. Actual loopback
REST/JSON-RPC smoke: **nine passed**, external connects blocked and
synthetic stores only; server stopped. Full backend Pyright: **zero
errors**, existing warning debt retained.
App-client/public/integration-public OpenAPI and all
Dart/Swift/TypeScript generators completed; dead-code baseline
regeneration made no suppressions or tracked changes.

Final whole-backend selection: **2,244 runnable files**, **48,510
passed**, 84 skipped and 2,120 deselected by the standard marker policy.
It ran once and reported 496 failed cases plus nine setup errors across
**14 files**. Those exposed the cache header/metric-label contracts and
isolated fixture dependencies described above. All 14 failed files are
repaired: the final 15-file scoped selection passed **860 tests**,
followed by **94 passed** in the workflow fixture after its missing
module copy was added (**954 green scoped tests across 16 files**,
including the new cache and quality-label regressions). The whole suite
was not rerun. Logs: integration-full-backend.log,
integration-failed-files-final.log and integration-workflow-repair.log
in this brief directory.

Post-V4 validation also passed: full Pyright zero errors; all 25 CI
slow-guardrail files 2,049 passed/1,342 deselected; Flutter 86
passed/five skips; Swift 33 passed; loopback HTTP smoke nine passed.
Repository preflight passed 65 checks after the cache repair; metadata
passed five checks. V4/shared composition passed all 13 cases and
latest-main FinOps selection passed 113 tests across six files.
Regenerated OpenAPI and Dart/Swift/TS artifacts are current. All backend
suites use nice -n 10, the worktree-local Python 3.11 environment and
BACKEND_UNIT_TEST_FILE_LIST through omi-heavy. The normal pre-push gate
**passed** on pushed head **9fc0e7118efd407b933b7f7e1417cbfe0e958529**:
65 preflight checks, full Pyright (zero errors), runtime source closure,
the bounded 40-file backend selection, generated OpenAPI/Dart/Swift
artifacts and the native Swift build. No hook was bypassed. The remote
wave2-integration ref was verified equal to that head after the push.
GitHub reports a completed/skipped Mintlify check and no commit status
checks; this branch-only handoff does not claim full PR CI.

No production reads, api.omi.me calls, user content, cloud changes,
device claims or deployment. GCP tier: none. Local validation is not
full PR CI or production acceptance; no PR is authorized.

## Fix-pass verification

The 16-file focused selection passed 475 tests. After adding four
runtime-image regression cases, its image-contract file passed all 66
tests (the original 62 plus four new), giving **479 distinct focused
cases green across the 16 files**. Full Pyright passed with zero errors
(48,941 non-blocking warnings). Logs: fix-pass-focused-tests.log,
fix-pass-image-tests.log and fix-pass-pyright.log. The whole backend
suite was not rerun. No Flutter or Swift source changed in this pass;
the normal pre-push gate still performs its configured native/generated
validation.

The full metadata/preflight run passed 65 checks in 250.84 seconds
(fix-pass-metadata.log). The subsequent merge of main is
source-identical: both source trees are
33f6033c0bd20e3d093daa96aa93a54bd745469c. Current fix-pass head is
58d4c61a238788fd54d28a5f19f8f015eef06209. The normal pre-push gate
passed on 58d4c61a238788fd54d28a5f19f8f015eef06209: 65 preflight checks
(189.64 seconds), full Pyright zero errors, runtime source closure, the
bounded 40-file backend selection, OpenAPI/generated-client checks and
native Swift build/checks. The fast-forward push 9fc0e7118ef ->
58d4c61a238 completed, and git ls-remote verified that exact full SHA at
refs/heads/wave2-integration on 2026-10-22 23:15:18Z. Working tree is
clean. GitHub reported zero commit statuses and zero check runs at
verification; no full PR CI claim is made. No approval or hook bypass
was used. Log: fix-pass-push.log. Final saved handoff metadata
revalidation passed five checks (fix-pass-metadata-final.log).

## Owner-replay fixes (wave-1 code, found by the offline replay)

- Episode boundaries: screen-meeting contexts carry the shared sentinel
id `screen-activity`, so every screen window hashed to one
boundary-signal identity (a later window was rejected as an immutable
start change; batches collapsed). `context_signal` now drops that
sentinel and screen-source ids, so each window keys by its own start.
Behind `EPISODE_BOUNDARIES_MODE` (shadow writes are sampled). Test:
`test_distinct_screen_windows_get_distinct_identities`.
- Contact spelling: a contact the user created by hand (no voice labels
yet) was excluded from trusted spellings, so a correct contact name
never reached the notes prompt. `is_user_created` is written only by the
user create and rename paths (automatic detection never creates people),
so it now counts as stored user evidence. This intentionally applies to
the legacy prompt too: it only adds names the user typed.

- Shadow cost: the media/noise classifier
(`relevance_media.classify_for_processing`) and cross-device reconcile
(`coverage_crossdevice.reconcile`) read Firestore per finalize. Their
shadow now runs for a 5% uid sample (`MEDIA_NOISE_MODE_SHADOW_PERCENT`,
`CAPTURE_COVERAGE_MODE_SHADOW_PERCENT`) via
`refactor_modes.shadow_sampled`; serve cohorts always run. Found by the
default-inertness audit.

## Risks and remaining work

Precision-first speaker/media and whole-secondary alignment can abstain
or retain duplicates. Missing SNR/confidence uses deterministic
source/duration order. V3 live secondary receipt dispatch and
partial-window suppression require durable frame alignment; only exact
committed aliases may release custody. No historical memory/task/recap
repair. MCP indexes are declared but not deployed; fallback and
bounded-window uncertainty remain explicit. Historical watching
intervals and past recap failure causes cannot be reconstructed. Runtime
TTL activation and all serve ramps remain separately scoped operator
work. V4 screen/desktop positive-proof production and automatic stale
task mutation remain partial; the supplied backend boundary and both
notes prompt hooks are integrated.

Invariant-Impact: INV-AUTH-1, INV-MEM-1, INV-MEM-3, INV-MEM-4,
INV-MEM-5, INV-CAP-1, INV-TASK-2. Auth/privacy and canonical memory/task
authorities are preserved; capture custody requires exact durable proof.
No unsupported attribution becomes an owner claim.

Failure-Class: FC-split-mutation-authority
V3 lane classification: FC-same-speech-captured-twice-surfaces-twice
M lane classification: FC-raw-page-limit-before-visibility-filter
Failure-Class-Guard: backend/tests/unit/test_cross_device_coverage.py
Failure-Class-Guard: backend/tests/unit/test_wave2_media_integration.py
Failure-Class-Guard: backend/tests/unit/test_mcp_read_correctness.py

Wave 1 client evidence is retained in this integration; V2 adds no UI
source:
![Shadow
Home](https://raw.githubusercontent.com/BasedHardware/omi/5d66b99f2460e1a591d87df7323789244180f7ca/.agent-artifacts/ui-evidence/refactor-l5-clients/001-mobile-ios-home-shadow.png)
![Serve
Home](https://raw.githubusercontent.com/BasedHardware/omi/5d66b99f2460e1a591d87df7323789244180f7ca/.agent-artifacts/ui-evidence/refactor-l5-clients/002-mobile-ios-home-serve.png)



Line-Count-Exception: backend/database/users.py | 2496 -> 2507 | Small
authority integration hooks; substantive policy lives in focused owning
modules.
Line-Count-Exception: backend/routers/listen/receiver.py | 2780 -> 2782
| Thread authenticated request identity into the two existing Soniox
call sites; vocabulary policy stays in its owning module.
Line-Count-Exception: backend/routers/listen/transcripts.py | 1648 ->
1655 | Small authority integration hooks; substantive policy lives in
focused owning modules.
Line-Count-Exception:
backend/utils/conversations/process_conversation.py | 3212 -> 3233 |
Small authority integration hooks; substantive policy lives in focused
owning modules.
Line-Count-Exception: backend/utils/conversations/speaker_resolution.py
| 1560 -> 1564 | Small authority integration hooks; substantive policy
lives in focused owning modules.
Line-Count-Exception: backend/utils/sync/pipeline.py | 3657 -> 3671 |
Small authority integration hooks; substantive policy lives in focused
owning modules.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) [183](https://github.com/NousResearch/hermes-agent/commits): feat(connectors): no guest on page open, connector sign-in offer (#143248)

* feat(connectors): list hosted apps without creating a guest identity

Opening the desktop Connectors page used to create a Nous guest identity:
connectors.list, connectors.catalog, connectors.accounts and
connectors.policy.get each created one before answering, because the
Portal's catalog route needs a token. A user who only looked at the page
got an identity anyway.

While there is no identity yet (and one may still be created), those four
reads now answer without one: the catalog from a snapshot that ships with
Hermes, an empty connector list, no accounts and no rules. Connecting an
app still creates the identity, as before.

scripts/refresh_connector_catalog.py rewrites the snapshot from a
signed-in install. It leaves logos out: no client draws them.

* feat(free-tier): sign-in offer for guests who connected apps

Every free-tier sign-in offer keyed on the welcome trial, so a user on
their own model key who connected apps through a guest identity never saw
one.

The offer record now tracks two offers on the same schedule. `trial` is
unchanged. `connector` is for a guest without the trial that has connected
an app: each app that finishes connecting sets `has_connected_app` on the
guest state (so it dies with the guest) and counts as a finished task.
free_tier.status (still a pure local read) adds connector_nudge_due_in, and
free_tier.claim_nudge takes a `kind`.

The desktop reads the connector offer whether or not the trial is
available, re-reads the status after a turn or a page connect, and shows
connector copy instead of the free-allowance copy. After a page connect
settles it also re-reads the catalog and rules, so the bundled catalog
from before the identity existed is replaced by the account's own.

* fix(connectors): point the sign-in hint at `hermes auth upgrade`

`hermes connectors` told users to run `hermes login`, which no longer
exists. Both hints now say "Run `hermes auth upgrade` to sign in."

* feat(connectors): read the public catalog with no token; one guest rule per entry point

The bundled catalog snapshot listed apps a new guest cannot connect and
went stale whenever the catalog changed. With no token, the Connectors
page now reads the Nous Portal's public catalog route
(GET /api/v1/connectors/catalog/public), sent with no Authorization and
parsed with the existing catalog model. Once a token exists the page reads
the signed-in route, as before.

Whether an entry point may create the guest identity is now declared once
per entry point instead of checked inside handlers:
- managed_client(creates_guest=...) is required: connect (page, agent,
  card retry) and the explicit lists (CLI `hermes connectors list`, agent
  manage_connections status/display) pass True, unchanged.
- account RPCs declare creates_guest on _account_method: catalog,
  accounts and policy.get never create one; tools and the account writes
  still do.
- the page's connectors.list never creates one; connect does.

With no token the page reads give true answers: public catalog, empty
connected list, no accounts. The invented "unrestricted" policy is gone:
the desktop asks for rules only once the list has rows, which needs a
token, and policy.get without one refuses with sign-in-required.

Deleted: the bundled snapshot, its refresh script, and the no-identity
stubs.

* fix(connectors): CI and review round: older backends, outside connects, link connects, guest opt-out

- CI: test_legacy_fallback_ticket_profile_verbs faked managed_client with
  no arguments and gave the secondary profile no token, so the page list
  (now token-gated, creates_guest=False) never reached it. The fake takes
  the new keyword and the profile holds a token.
- Older backends: a trial claim sends free_tier.claim_nudge with no
  params again. An older backend rejects the unknown `kind` key and would
  have dropped the trial offer; the new backend defaults to the trial.
  Only the connector claim sends `kind`.
- Outside connects: while the page's list is empty (no identity), every
  finished turn or connect re-reads the list and catalog. An agent connect
  in a chat then moves the page to the signed-in routes and its rules.
- Link connects: an agent status read that sees a connected app on a
  guest without the flag arms the connector offer, so messaging and
  one-shot connects (no operation watcher) count too.
- Opt-out: the connector offer requires nous.guest to be allowed.

* fix(connectors): the Connectors page list arms the connector offer too

A guest whose apps were connected by an older Hermes has no has_connected_app flag, and only the operation watcher or the agent's status read set it. The page's connectors.list now passes its rows to note_connected_apps_seen, which owns the any-connected check for both list reads.

* fix(connectors): review round 3: accounts after an outside connect, retryable offer record

- An identity created outside the page (an agent connect in a chat) now also re-reads the accounts cached while there was none, so the new account row, rename and remove show up.
- note_app_connected records the connector task before it sets has_connected_app. The flag ends list-read sightings, so a failed schedule write no longer leaves the offer unarmed for good.
- [unslothai/unsloth](https://github.com/unslothai/unsloth) [147](https://github.com/unslothai/unsloth/commits): Studio: restore a kept media model's price after a failed replacement (#14826)

With Keep multiple models loaded set to When they fit, `acquire_for`
records the new image or video load's VRAM price as the load starts.
When the background load then failed and the old model stayed loaded,
only the owner account and resident metadata were rolled back. The old
model stayed priced as the smaller model that never loaded, so a later
load could be admitted that does not fit. The arbiter now keeps the
previous price per load start, and each backend's failed-replacement
path puts it back. A load that takes no GPU claim clears it, so a stale
price is never restored. Tests cover the arbiter and the sd.cpp failure
path end to end.
- [kortix-ai/suna](https://github.com/kortix-ai/suna) [119](https://github.com/kortix-ai/suna/commits): fix(session-log): the capture thread waits for memory room and runs one at a time (#10793)
- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) [57](https://github.com/QwenLM/qwen-code/commits): fix(cli): recover from hosted send_message encoding limits (#14726)

* fix(cli): recover from hosted send_message encoding limits

Return durable tool refusals for oversized encoded messages so the
model can shorten its input and retry within the same turn.

- Restore the raw UTF-8 size guard for member-to-parent messages
- Preserve existing validation errors and prevent refused deliveries
- Cover encoded boundaries, retry, reload, and Hook input rewriting
- Document the bounded fix and remaining assistant-record limit

* fix(cli): clarify hosted message overflow recovery hints

Point retries at all encoded arguments and pin the narrow recovery
boundary after integrating main.

- Cover member and broadcast sender command retries in the Harness
- Preserve fatal MCP overflow and refusal persistence recovery
- Compare durable responses without runtime provenance metadata

* fix(cli): name the member wrapper bound in the overflow hint

A member→member send that clears the 32768-byte envelope check can still
overflow the 65536-byte encoded body through escape inflation. The shared
send_message arm told that lane a 65536-byte bound, roughly twice its real
headroom, and pointed at raw message size as the axis to shrink.

Branch the refusal text on the lane already computed in scope, keep the
non-member and workflow strings byte-identical, and split the member-lane
assertions in the command and Harness suites.

* docs(managed-agent): sync the byte-limit design with the shipped refusal

§4.2 pinned the pre-clarification string and carried no member-lane
refusal, so both language copies disagreed with the code and its tests.
§8 reported 97/566 with five new regressions, while the reviewed commit
runs 102 in the three suites and 611 in the Harness suite with seven
modes, and the PR description already reported the larger numbers.

Record the shipped strings in both languages and replace §8's counts with
the measured ones, naming the member→bob and member→* command-lane modes.

---------

Co-authored-by: wangheyang <wangheyang@corp.netease.com>
Co-authored-by: Shaojin Wen <szujobs@gmail.com>
- [JerryZLiu/Dayflow](https://github.com/JerryZLiu/Dayflow) [43](https://github.com/JerryZLiu/Dayflow/commits): release: update appcast for v2.7.5
- [t8y2/dbx](https://github.com/t8y2/dbx) [39](https://github.com/t8y2/dbx/commits): fix(mcp): stop linux shell probes from suspending tauri dev
- [Kiln-AI/Kiln](https://github.com/Kiln-AI/Kiln) [29](https://github.com/Kiln-AI/Kiln/commits): Merge pull request #1967 from Kiln-AI/dchiang/KIL-829/git-sync-cancelled-save-lock

fix: release the git sync lock when a waiting save is cancelled
- [docling-project/docling](https://github.com/docling-project/docling) [19](https://github.com/docling-project/docling/commits): ci: add nightly update of locked docling dependencies (#4978)

Add a workflow that runs nightly and on demand. It upgrades
docling-core, docling-parse and docling-ibm-models in uv.lock,
regenerates the reference test data with DOCLING_GEN_TEST_DATA=1 in
the core and ML suites, and opens or updates one PR on
ci/update-locked-deps.

Signed-off-by: Michele Dolfi <dol@zurich.ibm.com>
- [EvolvingAgentsLabs/evolving-agents](https://github.com/EvolvingAgentsLabs/evolving-agents) [18](https://github.com/EvolvingAgentsLabs/evolving-agents/commits): Merge pull request #202 from EvolvingAgentsLabs/ccr-c0eed325-5wd271

benchmarks: stage director-bench until its own repository exists
- [langgenius/dify](https://github.com/langgenius/dify) [18](https://github.com/langgenius/dify/commits): fix: improve sort control accessibility and type safety (#44564)
- [google/adk-python](https://github.com/google/adk-python) [14](https://github.com/google/adk-python/commits): fix: mark failed MCP tool results as errors for Claude

Merge https://github.com/google/adk-python/pull/7665

AnthropicLlm now sends a tool_result with is_error set when the function
response carries a truthy isError or is_error key, as a failed MCP
CallToolResult does; it previously always sent it as false.

Fixes #7664

PiperOrigin-RevId: 1005107381
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) [12](https://github.com/screenpipe/screenpipe/commits): feat: allow rich text controls in a shared selection toolbar (#7751)
- [google/magika](https://github.com/google/magika) [8](https://github.com/google/magika/commits): Merge pull request #1558 from google/adhoc-uv-lock-check

gh: check uv.lock with uv lock --check before uv sync --locked
- [lutzroeder/netron](https://github.com/lutzroeder/netron) [7](https://github.com/lutzroeder/netron/commits): Add MLIR support (#1044)
- [github/spec-kit](https://github.com/github/spec-kit) [4](https://github.com/github/spec-kit/commits): Add Entalpa to Community Friends (#4993)

* Add Entalpa to Community Friends

* Remove duplicate Entalpa entry in friends.md

Removed duplicate entry for Entalpa and fixed formatting.

Co-authored-by: Copilot Autofix powered by AI <175728472+Copilot@users.noreply.github.com>

* Mention zip and folder uploads for private repositories

---------

Co-authored-by: Copilot Autofix powered by AI <175728472+Copilot@users.noreply.github.com>
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) [4](https://github.com/google-gemini/gemini-cli/commits): fix(cli): preserve ${VAR} placeholders during deprecated settings migration (#29867)

Co-authored-by: David Pierce <davidapierce@google.com>
- [XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) [4](https://github.com/XiaomiMiMo/MiMo-Code/commits): fix(session): retry empty output persistently and persist retry records until the turn succeeds (#2703)

* fix(session): retry empty model output persistently under the server budget

* docs(session): finalize empty-output persistent retry spec and apply review follow-ups

* feat(session): persist a retry record part per assistant until the turn succeeds

* fix(session): clear retry records on every run exit per user turn and keep them across dropped empty steps

* fix(session): clear retry records only at success exits and query them directly

* fix(session): scope retry clearing to the run's real user turn and keep carried records on early exit

* docs(session): finalize retry-record-part spec and cover request-phase recovery

* test(session): cover retry records surviving a retry-safe stream failure

* fix(session): let a newer input supersede a step that is retrying a failure

* docs(session): point retry specs at their PR
- [Source-Robotics/PAROL6-Desktop-robot-arm](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm) [1](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/commits): Temp custom flange guide items
- [specstoryai/getspecstory](https://github.com/specstoryai/getspecstory) [1](https://github.com/specstoryai/getspecstory/commits): Merge pull request #372 from specstoryai/dependabot/github_actions/actions-minor-patch-665cda0987

Bump anthropics/claude-code-action from 1.0.253 to 1.0.254 in the actions-minor-patch group
- [steel-dev/steel-browser](https://github.com/steel-dev/steel-browser) [1](https://github.com/steel-dev/steel-browser/commits): fix(api): handle PDF URLs in screenshot/pdf and harden action page handling (#383)

* fix(api): handle PDF URLs in screenshot and pdf, bound the error page reset

* fix(api): download PDFs through the page proxy, cap their size, fence late page resets

* fix(cdp): track page setup and keep late refreshes from swapping the primary page

* fix(api): wait for page setup before action navigation and keep PDF downloads in the page load budget

* fix(cdp): install the new primary page before closing the old one

* fix(api): put the PDF download's page lookups under its deadline

* fix(api): cap the pixels a PDF first-page render can allocate

* fix(api): download PDFs from the URL the browser ended up on

## [android](https://github.com/topics/android)
- [Snapchat/Valdi](https://github.com/Snapchat/Valdi) [3](https://github.com/Snapchat/Valdi/commits): Internal Change

GitOrigin-RevId: 4b9bea17468769caea6e6a22dd0b542fd494007c
- [uber/RIBs](https://github.com/uber/RIBs) [2](https://github.com/uber/RIBs/commits): Merge pull request #666 from gpolak/view_tree_back_dispatcher_owner

Set the view tree OnBackPressedDispatcherOwner in CoreAppCompatActivity
- [Julow/Unexpected-Keyboard](https://github.com/Julow/Unexpected-Keyboard) [1](https://github.com/Julow/Unexpected-Keyboard/commits): Add № sign to ЙЦУКЕН (Русский) layout (#1469)

* Add compose fn+No = #

## [claude-code](https://github.com/topics/claude-code)
- [yetone/magpie](https://github.com/yetone/magpie) [63](https://github.com/yetone/magpie/commits): gateway: a model slow to start again and again rests on its account (小八)

小八 on Discord (2026-10-23): a WorkBuddy plugin account answered magpie's
own 504 "no first token in 30s" 58 times on kimi-k3-1 and glm-5.3 (the
vendor's per-model token limit, which it never names, it just stalls).
The group went on each time, then asked the same account first on the
next request: 15 slow starts in 17 minutes in one session.

Cause: gateway.go's hw.slow branch (the group's FirstToken let a member
go) never rested anything, by design ("a long prompt being slow to start
anywhere"), and nothing counted slow starts. So every request waited out
the whole FirstToken on the stalled member before falling back.

Now restSlow (routing.go) counts slow starts per restID (provider,
account or key, model). Once rests nothing, as before. The second in a
row, within slowForget (30m) of the last, rests that model on that
account: 1 minute, doubling each time after, capped by the provider's
RestCapOr(longestRetry), never for a provider whose rest cap is off. An
answer clears the count (servedCandidate). A client-cancelled request
never reaches the slow branch, so it counts nothing. A longer rest
already there is kept. The rest carries Rest.Model, so the Routing page
shows it on that model's rows only. The Routing story of a rested slow
try says so, and the group editor's slow-to-start hint no longer says
"It doesn't rest" (en, zh, zh-TW, ja, de).

Tests: TestSlowStartsRestTheModelOnItsAccount (once: no rest; an answer
in between restarts the count; twice: the model rests on k1 with Key
a#k1/m, Model m, under a minute; k1's whole key and k2/m don't rest; the
next request asks k2/m first; a/n still goes to k1; a third slow start
backs off longer; an answer ends it). TestCanceledSlowStartRestsNothing
(three client cancels during the first-token wait: no rest, no count).
routing-went-on.test.cjs gains a rested slow try in five languages;
group-first-token.test.cjs's i18n list has the new strings.

Broken by hand: restSlow's result ignored in gateway.go -> the first test
red at "twice in a row" (Rest nil); servedCandidate not clearing
routed.slow -> red at "an answer in between starts the count again";
restSlow called in the cancel branch -> the cancel test red at "cancel
2: k1/m wasn't asked (rested?)". All restored, green.

Run at the worktree on base 7aad6a50e: gofmt -l clean; go vet darwin,
GOOS=linux -tags nogui, GOOS=windows: ok. The two new tests -race
-count=3: ok. TestGroupFirstTokenFailsOver, TestNestedGroupFirstToken:
ok. GUI: the 125 routing-*, group-* and i18n-* files, Chromium and
WebKit: 1428 of 1429; the one red, routing-rule-remove de (menu focus
after ArrowUp, the #3094 symptom), passed 20 of 20 alone. Full suite:
set -o pipefail; go test -tags nogui -timeout 45m ./... : 69 packages ok, none failed (gateway 544s, agent 430s, provider 234s).

Not tried: a real WorkBuddy account stalling on its token limit; the
fixture stalls by holding its stream after the role chunk.

Rebased on origin/main ecd983500 (no gateway or routing plugin change in between) and run again there: gofmt, the three go vets, internal/gui (budgets) ok, the four first-token gateway tests ok, i18n-keys, routing-went-on and group-first-token in both engines 43 of 43.
- [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) [13](https://github.com/CherryHQ/cherry-studio/commits): fix(i18n): restore Italian proxy translations (#22473)

### What this PR does

Before this PR: Italian proxy translations were missing or stale,
failing main CI locale synchronization and protected-term validation.

After this PR: Both proxy messages match the English source, including
the required Cherry Studio name.

Fixes: N/A

### Why we need it and why it was done in this way

The following tradeoffs were made: None; two translation entries in one
catalog

The following alternatives were considered: No changes to existing
validation rules

Links to places where the discussion took place: [Failing main
CI](https://github.com/CherryHQ/cherry-studio/actions/runs/39805311334)

### Agent Note / Spec

Agent Note: N/A — local restoration of the existing translation contract

Spec PR: N/A — no new behavior or architecture

Acceptance criteria: Regression — synchronized Italian keys and valid
protected terms

### Verification

- Regression: `pnpm i18n:check` — reproduced the missing key, then the
stale protected term; passes after both fixes (95,902 translations)
- `pnpm i18n:sync` — byte-for-byte unchanged across all three locale
directories after the fix
- `pnpm i18n:unused:check` — zero unused keys in renderer, main, and
file-preview
- `pnpm exec oxfmt --check src/renderer/i18n/locales/it-it.json` and
`git diff --check` — passed
- `pnpm change:scope --base origin/main` — one locale file; `pnpm check
--plan` inspected
- `pnpm docs:affected --base 0b6c368c690863b6121f53fbb62522cbcaba58f3` —
all six candidates inspected; no documentation contract changes

### Breaking changes

None

### Special notes for your reviewer

Catalog-only repair; existing i18n contract checks cover the regression,
so no new tests or full local suite

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
- [ ] Refactor: You have [left the code cleaner than you found it (Boy
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

```release-note
Correct Italian proxy guidance in settings and generated-image loading errors.
```

Signed-off-by: suyao <sy20010504@gmail.com>
- [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) [4](https://github.com/lemomo-ai/lemo-opuscar/commits): README: shorter new-in lines so each fits on one line on desktop

Claude-Session: https://claude.ai/code/session_01YCF473MfutLbWk4fdbFoe1
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) [4](https://github.com/Piebald-AI/claude-code-system-prompts/commits): Update changelog for v2.1.308

## [cli](https://github.com/topics/cli)
- [antonmedv/fx](https://github.com/antonmedv/fx) [2](https://github.com/antonmedv/fx/commits): Release 40.0.1
- [openclaw/imsg](https://github.com/openclaw/imsg) [1](https://github.com/openclaw/imsg/commits): fix(ci): reject compromised CA keys in selected Node runtimes (#361)

## [cocoapods](https://github.com/topics/cocoapods), [objective-c](https://github.com/topics/objective-c)
- [parse-community/Parse-SDK-iOS-OSX](https://github.com/parse-community/Parse-SDK-iOS-OSX) [4](https://github.com/parse-community/Parse-SDK-iOS-OSX/commits): test: Fix intermittent unit test crash due to file caching still running after teardown (#1932)
- [AloneMonkey/MonkeyDev](https://github.com/AloneMonkey/MonkeyDev) [1](https://github.com/AloneMonkey/MonkeyDev/commits): docs: replace HiNexus promotion with personal blog

## [dashboards](https://github.com/topics/dashboards)
- [thingsboard/thingsboard](https://github.com/thingsboard/thingsboard) [7](https://github.com/thingsboard/thingsboard/commits): Merge branch 'rc'
- [taleshape-com/shaper](https://github.com/taleshape-com/shaper) [2](https://github.com/taleshape-com/shaper/commits): Add ::CLASS to add custom css classes to sections and cards (#430)

* Add ::CLASS to add custom css classes to sections and cards

* Fix CSS

* Allow SELECT ''::CLASS without LABEL

## [embedded](https://github.com/topics/embedded)
- [hathach/tinyusb](https://github.com/hathach/tinyusb) [3](https://github.com/hathach/tinyusb/commits): pico2_etm_trace: point the clock comment at target-debug's etm-boards.md (#4277)
- [wasm-micro-runtime/wasm-micro-runtime](https://github.com/wasm-micro-runtime/wasm-micro-runtime) [1](https://github.com/wasm-micro-runtime/wasm-micro-runtime/commits): feat(build): default flags off, add presets and clang-tidy CI (#5100)

Changes:
- build-scripts: every feature flag defaults to 0. Version presets
  (SPEC1/2/3, LIME1) move into runtime_lib.cmake before dependency
  derivation. Unsupported-combination warnings are deferred and
  report where each exclusion came from.
- GC corruption check flag and default move into config_common.cmake;
  BH_ENABLE_GC_CORRUPTION_CHECK is defined there, not in mem_alloc.cmake.
  AOT validator defaults to off.
- samples/minimum: all-off base preset, per-config presets.
- ci/clang_tidy_diff_check.py: run clang-tidy on changed lines compiled
  by each preset. Exit 0 clean, 1 errors, 2 partial scan, 3 run failed.
- coding_guidelines.yml: clang_tidy job restores cached LLVM from
  build_llvm_libraries.yml, and reports a verdict per exit code.
- Docs: build_wamr.md, CONTRIBUTING.md, stability doc
- `-Wundef` will prevent undefined marcos

Benefits:
- New flags cannot silently turn on; a bare configure is minimal.
- Presets give reproducible configs for CI and local checks.

## [esp32](https://github.com/topics/esp32)
- [crosspoint-reader/crosspoint-reader](https://github.com/crosspoint-reader/crosspoint-reader) [8](https://github.com/crosspoint-reader/crosspoint-reader/commits): test: fix two host-test failures on macOS and under parallel ctest (#4130)
- [arendst/Tasmota](https://github.com/arendst/Tasmota) [6](https://github.com/arendst/Tasmota/commits): Remove root sdkconfig.defaults and CMakeLists.txt and ignore them (#25174)
- [espressif/idf-extra-components](https://github.com/espressif/idf-extra-components) [5](https://github.com/espressif/idf-extra-components/commits): Merge pull request #883 from suda-morris/fix/enable-build-only-app-tests

test: run apps built by CI
- [s60sc/ESP32-CAM_MJPEG2SD](https://github.com/s60sc/ESP32-CAM_MJPEG2SD) [4](https://github.com/s60sc/ESP32-CAM_MJPEG2SD/commits): v10.9.9b

v10.9.9b
- [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) [2](https://github.com/xinnan-tech/xiaozhi-esp32-server/commits): 模板 GET 入口迁回 AgentTemplateController #3395 (#3401)

* 模板 GET 入口迁回 AgentTemplateController #3395

根因：AgentController 已存在 GET /agent/template/templateList，AgentTemplateController 缺显式 GET，于是路由虽通却跨 controller 暴露模板数据，且职责错位。修复：删 AgentController.templateList，同名 @GetMapping（无 path）落到 AgentTemplateController，权限 normal、orderByAsc sort、复用现有 service.list。验证：spring-boot 启动期无 Ambiguous；/agent/template、/page、/{id} 三路由均被 Shiro 一致拦截，权限/路径正确。

* 补 P2 注释说明 normal 权限反直觉是有意保留 #3395

在 getAgentTemplates 上方加 2 行注释，说明单独 normal 权限是为保持原行为契约（普通用户也能查可用模板），与类级 superAdmin 故意分离；非疏忽。无逻辑变更。

* 去除未使用引用

---------

Co-authored-by: Sakura-RanChen <1908198662@qq.com>
- [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) [1](https://github.com/78/xiaozhi-esp32/commits): Merge pull request #2346 from monsterlag/fix/issue-2340-da89

docs: document Windows response-file build workaround
- [platformio/platform-espressif32](https://github.com/platformio/platform-espressif32) [1](https://github.com/platformio/platform-espressif32/commits): Bump pydantic version to v2.14

The newer version has support for Python 3.15

Resolves #1787

## [ethereum](https://github.com/topics/ethereum)
- [sigp/lighthouse](https://github.com/sigp/lighthouse) [3](https://github.com/sigp/lighthouse/commits): Release v8.3.2 (#10433)

* Unschedule Gloas on Hoodi (#10430)

Reverts #10304 per https://github.com/eth-clients/hoodi/pull/33

* Version bump

---------

Co-authored-by: Eitan Seri-Levi <eserilev@gmail.com>
- [foundry-rs/foundry-toolchain](https://github.com/foundry-rs/foundry-toolchain) [1](https://github.com/foundry-rs/foundry-toolchain/commits): fix: upgrade Node.js to patch CVE-2026-111497 (#193)

Co-authored-by: Kamil Szczygieł <2961450+kamsz@users.noreply.github.com>

## [font](https://github.com/topics/font), [typeface](https://github.com/topics/typeface)
- [lxgw/LxgwBright](https://github.com/lxgw/LxgwBright) [8](https://github.com/lxgw/LxgwBright/commits): Update README with font limitations and OTF version info

Clarified the limitations of the font regarding vertical typesetting and updated the release update policy. Specified the discontinuation of the OTF version starting from version 5.330.
- [lxgw/kose-font](https://github.com/lxgw/kose-font) [1](https://github.com/lxgw/kose-font/commits): Update README with caution and maintenance details

Added caution and maintenance information regarding the font project.
- [lxgw/LxgwWenKai](https://github.com/lxgw/LxgwWenKai) [1](https://github.com/lxgw/LxgwWenKai/commits): Update source file pointer

## [golang](https://github.com/topics/golang)
- [twmb/franz-go](https://github.com/twmb/franz-go) [5](https://github.com/twmb/franz-go/commits): Merge pull request #1520 from twmb/1519-kfake

kfake: answer failed piggybacked share acks as Kafka does
- [wader/fq](https://github.com/wader/fq) [2](https://github.com/wader/fq/commits): Merge pull request #1420 from wader/gomarkdown-update

Update gomarkdown and handle ReferenceDefinition
- [cshum/imagor](https://github.com/cshum/imagor) [1](https://github.com/cshum/imagor/commits): build: bump vipsgen to v2.1.0

Adds the UltraHDR loader, fixes the affine matrix passed twice with options, and matches the
most specific loader name first. The last one changes how a file's type is chosen when one name
is a prefix of another.
- [pressly/goose](https://github.com/pressly/goose) [1](https://github.com/pressly/goose/commits): fix: allow inlined migration functions in goose validate (#1110)

## [json](https://github.com/topics/json)
- [RedisJSON/RedisJSON](https://github.com/RedisJSON/RedisJSON) [3](https://github.com/RedisJSON/RedisJSON/commits): MOD-19584 computed JSONPath projections in c_api (#1678)

* MOD-19584 computed JSONPath projections in Search

* CR
- [tdewolff/minify](https://github.com/tdewolff/minify) [3](https://github.com/tdewolff/minify/commits): Merge pull request #1054 from tdewolff/dependabot/github_actions/pypa/cibuildwheel-4.3.1

Bump pypa/cibuildwheel from 4.2.1 to 4.3.1

## [machine-learning](https://github.com/topics/machine-learning), [deep-learning](https://github.com/topics/deep-learning)
- [skypilot-org/skypilot](https://github.com/skypilot-org/skypilot) [12](https://github.com/skypilot-org/skypilot/commits): [Jobs] Fix completed-task logs while a job group is active (#10826)

* [Jobs] Fix completed-task logs while a job group is active

With a task filter, `sky jobs logs JOB TASK` (and the dashboard's per-task
log view) chose between a finished task's saved log and a live tail of its
cluster by the whole job's status. While another task kept the job RUNNING,
a finished task was tailed from its cluster, which may be gone: a pipeline
tears it down, and a job group keeps its record until the group ends while
the cluster's idle autodown deletes it. The request then never returned,
waiting on a missing handle or retrying the deleted cluster with "The job
cluster is preempted or failed."

Decide by the filtered task's own status on every status read, so a task
that finishes during a live tail also stops it. Without a log reader, wait
for the controller to record the saved log path of a task that just
SUCCEEDED, as the follow path already does. Messages that name a status say
whether it is the task's or the job's, and the exit code is the task's.

* [Tests] Cover completed-task logs in an active pipeline
- [EthicalML/awesome-production-machine-learning](https://github.com/EthicalML/awesome-production-machine-learning) [1](https://github.com/EthicalML/awesome-production-machine-learning/commits): Add Heym to Industry Strength Natural Language Processing (#841)
- [stefan-jansen/machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) [1](https://github.com/stefan-jansen/machine-learning-for-trading/commits): Refresh the README offerings block from the Maven schedule (#1173)

Co-authored-by: ml4t-offerings[bot] <41898282+github-actions[bot]@users.noreply.github.com>

## [macos](https://github.com/topics/macos)
- [shadowsocks/ShadowsocksX-NG](https://github.com/shadowsocks/ShadowsocksX-NG) [49](https://github.com/shadowsocks/ShadowsocksX-NG/commits): ci: enforce strict compiler warnings
- [Licoy/StrokeMouse](https://github.com/Licoy/StrokeMouse) [9](https://github.com/Licoy/StrokeMouse/commits): docs: 补齐七语言 README 与网站指南中的鼠标组合说明

PR #25 只在英文和简体中文 README 里加了一条功能简介，其余五种语言的 README 和网站手势指南都没有提到鼠标组合；README 的「短按 vs 手势」说明也没讲按住右键时组合会接管滚轮和左键。

- 繁中、韩、日、俄、法 README 补上功能条目；繁中链接到中文说明，其余链接到英文说明
- 七种语言 README 的短按说明补充：组合先于第二动作接管滚轮或左键，触发后松开右键不回放点击、不识别轨迹
- 七种语言网站手势指南新增「鼠标组合」一节：触发方式与执行时机表、与右键菜单 / 第二动作 / 普通滚动的关系、限频、边缘范围、作用域与冲突
- [jundot/omlx](https://github.com/jundot/omlx) [2](https://github.com/jundot/omlx/commits): feat(oq): keep DeepSeek V4.1 Engram tables at source precision (#4758)
- [mattt/iMCP](https://github.com/mattt/iMCP) [2](https://github.com/mattt/iMCP/commits): Add a Mail service (#239)

* Add a Mail service to search, read, and compose email

The service reads the local Mail Envelope Index and .emlx files through a read-only, security-scoped bookmark on ~/Library/Mail. Composition opens a mailto URL in the default email app and needs no folder access.

* Clarify Mail search identifiers and local index coverage

* Limit Mail database reads to reduce interference

* Improve Mail concurrency and cancellation

* Test Mail timestamp conversion and date boundaries

* Use Envelope for local Mail access and MIME parsing

* Update Envelope to 0.2.0

Use the remote package instead of a local checkout, and adopt Mail.Store.
Search pagination now uses cursors, so mail_messages_search replaces
offset with cursor and returns nextCursor.

* Name Mail in the server instructions

* Show readable Mail error messages in tool responses

* Describe date-only end dates as including the whole day

* Update Envelope to 0.3.0

Depend on the single Envelope product, create the store from the resolved
Mail folder URL, and use Mailbox.ID for mailbox identifiers, so mailbox
@id values now include the store, such as "V10:12".

* Add Mail to the README service table and hero images

* Remove the unneeded bookmarks entitlement

* Run the Mail tests in imcp-serverTests

* Test Mail tools against a synthetic Mail index

* Open the Mail folder picker in the real Library folder

* Require Envelope 0.3.1 for account email addresses

## [markdown](https://github.com/topics/markdown)
- [keitaoouchi/MarkdownView](https://github.com/keitaoouchi/MarkdownView) [3](https://github.com/keitaoouchi/MarkdownView/commits): ci: use Node.js 24.22.1 for web assets (#133)
- [rzashakeri/beautify-github-profile](https://github.com/rzashakeri/beautify-github-profile) [2](https://github.com/rzashakeri/beautify-github-profile/commits): Merge pull request #124 from icedsg/add-b59-view-counter
- [MarkEdit-app/MarkEdit](https://github.com/MarkEdit-app/MarkEdit) [1](https://github.com/MarkEdit-app/MarkEdit/commits): Use clearer mermaid type declarations
- [microsoft/markitdown](https://github.com/microsoft/markitdown) [1](https://github.com/microsoft/markitdown/commits): feat(doc-intel): expose models, features, query fields, and structured output (#1913)

* feat: consolidate Document Intelligence configuration
* Update YAML parsing conditions for string quoting
* Preserve Document Intelligence document boundaries and selection groups
* Escape control characters in Document Intelligence YAML output
* Preserve scientific-notation float types in YAML front matter
* Avoid enabling paid Document Intelligence add-ons by default
* Format Document Intelligence CLI help

---------

Co-authored-by: Tai An <antai12232931@outlook.com>
Co-authored-by: hshgogogo <2081920847@qq.com>
Co-authored-by: Chien Yuan Chang <186005646+chienyuanchang@users.noreply.github.com>
Co-authored-by: Adam Fourney <adamfo@microsoft.com>

## [productivity](https://github.com/topics/productivity)
- [omnivore-app/omnivore](https://github.com/omnivore-app/omnivore) [2](https://github.com/omnivore-app/omnivore/commits): chore: change defaults for max-old-space-size
- [alyssaxuu/screenity](https://github.com/alyssaxuu/screenity) [1](https://github.com/alyssaxuu/screenity/commits): Login issue, Linux encoder fallback, recovered-error handling, and false editor load errors

## [python](https://github.com/topics/python)
- [esphome/esphome](https://github.com/esphome/esphome) [84](https://github.com/esphome/esphome/commits): [ota] Fit UDP OTA datagrams in Thread's 1280-byte IPv6 MTU (#21429)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [CyC2018/CS-Notes](https://github.com/CyC2018/CS-Notes) [45](https://github.com/CyC2018/CS-Notes/commits): Merge pull request #1448 from CyC2018/fix-reported-errors

Fix errors reported in issues and update system design notes
- [doronz88/pymobiledevice3](https://github.com/doronz88/pymobiledevice3) [38](https://github.com/doronz88/pymobiledevice3/commits): Merge pull request #2105 from kevinwwillis/bugfix/tunneld-windows-selector-loop

tunneld: Serve on the selector loop on Windows
- [adafruit/circuitpython](https://github.com/adafruit/circuitpython) [12](https://github.com/adafruit/circuitpython/commits): Merge pull request #11652 from dhalbert/zephyr-cp-macropad-rp2040

zephyr-cp: add the MacroPad RP2040
- [vacanza/holidays](https://github.com/vacanza/holidays) [8](https://github.com/vacanza/holidays/commits): Fix `HolidaySum` repopulating years its operands already have (#3917)
- [pyodide/pyodide](https://github.com/pyodide/pyodide) [4](https://github.com/pyodide/pyodide/commits): Fix fatal error with pybind11 extensions and stack switching (#6487)

In #6421 we switched approaches to stack switching to use one tstate per task.
However, pybind11 assumes that there is only one tstate per operating system
thread, so only one tstate. So this broke some pybind11 extensions.

There is now a single tstate again shared between tasks. This is apparently the
only way to do stack switching that satisfies extension module assumptions.
- [binance/binance-connector-python](https://github.com/binance/binance-connector-python) [3](https://github.com/binance/binance-connector-python/commits): Release derivatives_trading_portfolio_margin v16.0.0

### Changed (3)

#### REST API

- Added parameter `amount`
  - affected methods:
    - `fund_collection_by_asset()` (`POST /papi/v1/asset-collection`)
- Added parameter `futureType`
  - affected methods:
    - `fund_collection_by_asset()` (`POST /papi/v1/asset-collection`)
- Deleted parameter `page`
  - affected methods:
    - `get_cm_income_history()` (`GET /papi/v1/cm/income`)
    - `get_um_income_history()` (`GET /papi/v1/um/income`)
- [browser-use/browser-use](https://github.com/browser-use/browser-use) [3](https://github.com/browser-use/browser-use/commits): README: rerun a saved task without calling the model on every step (#6183)

**Change.** Adds one README FAQ entry, "Can I rerun a task without
calling the model on every step?". It shows `agent.save_history()` +
`load_and_rerun(variables=...)`, and lists the four things that bite:
- Unknown variable names are skipped and the recorded value is typed.
- Extract steps and the summary still call the model.
- A changed page raises `RuntimeError` after the earlier steps already
ran.
- The saved file holds the typed values (`sensitive_data` keeps secrets
out).

It links `examples/features/rerun_history.py`.

**Why.** In a daily 160-answer test (Claude Code + Codex, clean config),
two questions are 0/16 for Browser Use over Oct 19-22:
- "UiPath keeps breaking, what AI alternative?"
- "Plain Playwright or an AI agent for a site that changes often?"

Every rpa answer picks Stagehand, and the deciding argument is "cache
what the AI resolved, replay it without the LLM". This library already
does that, but the README never says so. GitHub is the most-cited
Browser Use source in those answers (10 of our cites on Oct 22).
browser-use.com/developers got the same section in
browser-use/website#596.

**Proof.** Ran the snippet verbatim on Oct 22 with browser-use 0.13.11
and `ChatBrowserUse` against a local form with a server-side submit log.
The only change was the URL pointed at localhost.
- Record: Ada sent once.
- `detect_variables()` printed `name` and `email`.
- Replay: Grace Hopper / grace@example.com sent once, 0 model calls
before the submit, then 2 (extract + summary).
- `load_and_rerun`, `rerun_history` and `variable_detector.py` are
identical on main (0.13.13).
- The unknown-name behavior is from `_substitute_variables_in_history`.
- `skip_failures=False` is explicit because the `load_and_rerun`
docstring says the default is True while the code says False.
- `tests/ci/test_browser_use_skill_install_docs.py` passes.

**Risk.** Docs only. **Rollback.** Revert.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- This is an auto-generated description by cubic. -->
---
## Summary by cubic
Adds a README FAQ entry on rerunning a saved task without calling the
model on every step.

- Shows `agent.save_history()` plus `load_and_rerun(variables=...)`,
with variable names from `detect_variables()`.
- Unknown variable names are skipped with a warning, and the recorded
value is typed.
- Extract steps and the closing summary still call the model.
- A changed page raises `RuntimeError` at the first unmatched step,
after earlier steps already ran.
- Saved page snapshots and results can still contain secrets; replaying
requires the same `sensitive_data` so placeholder text is typed back.

Docs only, no code changes.

<sup>Written for commit 702c737b8cfc74428b464d14192ec2165d267f6d.
Summary will update on new commits.</sup>

<a
href="https://cubic.dev/pr/browser-use/browser-use/pull/6183?utm_source=github"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-light.svg"><img
alt="View guided diff"
src="https://www.cubic.dev/buttons/review-in-cubic-light.svg"></picture></a>
<a
href="https://www.cubic.dev/action/auto-fix/pr/browser-use/browser-use/6183?returnTo=https%3A%2F%2Fgithub.com%2Fbrowser-use%2Fbrowser-use%2Fpull%2F6183&source=description"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/turn-on-auto-fix-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/turn-on-auto-fix-light.svg"><img
alt="Turn on auto-fix"
src="https://www.cubic.dev/buttons/turn-on-auto-fix-light.svg"></picture></a>

<!-- End of auto-generated description by cubic. -->
- [lakehq/sail](https://github.com/lakehq/sail) [2](https://github.com/lakehq/sail/commits): fix: normalize Arrow view types before returning Spark Connect results (#2837)
- [pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) [2](https://github.com/pymupdf/PyMuPDF/commits): tests/test_mupdf_regressions.py: test_mupdfcpp64_dll_symbols(): new.

Checks whether mupdfcpp64.dll contains symbol fz_argv_from_wargv.
- [pyocd/pyOCD](https://github.com/pyocd/pyOCD) [2](https://github.com/pyocd/pyOCD/commits): readme: add information about packs and targets
- [rushter/selectolax](https://github.com/rushter/selectolax) [2](https://github.com/rushter/selectolax/commits): Bump version: 1.0.1 → 1.0.2
- [vinta/awesome-python](https://github.com/vinta/awesome-python) [2](https://github.com/vinta/awesome-python/commits): build: bump certifi to 2026.10.18

certifi 2026.7.22 still trusted the emSign ECC Root CA - G3 and AAA Certificate Services roots that chain to the compromised eMudhra intermediates.

Co-Authored-By: Claude <noreply@anthropic.com>
- [arnegiacomo/fugleramme](https://github.com/arnegiacomo/fugleramme) [1](https://github.com/arnegiacomo/fugleramme/commits): Join any of several Wi-Fi networks, remembering the last one (#310)

Replace the single WIFI_SSID/WIFI_PASSWORD pair with a WIFI_NETWORKS
tuple tried in order, and remember the network that connected last in a
small hint file so it is tried first on the next wake. The panel can
then roam between networks without a reflash.
- [lemon24/reader](https://github.com/lemon24/reader) [1](https://github.com/lemon24/reader/commits): Don't hardcode coverage.py core= anymore.
- [mangiucugna/json_repair](https://github.com/mangiucugna/json_repair) [1](https://github.com/mangiucugna/json_repair/commits): Merge pull request #238 from mangiucugna/dependabot/github_actions/astral-sh/setup-uv-10.3.0

Bump astral-sh/setup-uv from 10.2.0 to 10.3.0
- [norvig/pytudes](https://github.com/norvig/pytudes) [1](https://github.com/norvig/pytudes/commits): Fix formatting in Euler's Conjecture notebook

## [pytorch](https://github.com/topics/pytorch), [speech-processing](https://github.com/topics/speech-processing), [voice-activity-detection](https://github.com/topics/voice-activity-detection)
- [pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio) [3](https://github.com/pyannote/pyannote-audio/commits): setup: stop tracking uv.lock (#2085)
- [snakers4/silero-vad](https://github.com/snakers4/silero-vad) [2](https://github.com/snakers4/silero-vad/commits): Merge pull request #815 from ANDROIDHASSAN/docs/update-cpp-v5-example

Update the C++ example for VAD v5 inputs

## [queue](https://github.com/topics/queue)
- [apple/swift-collections](https://github.com/apple/swift-collections) [15](https://github.com/apple/swift-collections/commits): Merge pull request #799 from aashish254/fix-bitset-intersection-docs

[BitCollections] Fix BitSet intersection doc examples for Range inputs
- [bloomberg/blazingmq](https://github.com/bloomberg/blazingmq) [1](https://github.com/bloomberg/blazingmq/commits): Fix[mqbnet::Channel]: race on channel reset (#1828)

It is possible to wrongly enqueue an item to `mqbnet::Channel::d_buffer` at the time when another thread resets the channel and clears `d_buffer`. Make sure to acquire an atomic gate before enqueue and close this gate before reset.

Signed-off-by: Evgeny Malygin <emalygin@bloomberg.net>

## [redis](https://github.com/topics/redis)
- [RedisBloom/RedisBloom](https://github.com/RedisBloom/RedisBloom) [1](https://github.com/RedisBloom/RedisBloom/commits): RED-213286: test that BLESS NO-EVICT survives module writes, reloads and eviction (#1082)

* RED-213286: test that BLESS NO-EVICT survives module writes, reloads and eviction

Redis 8.12 adds BLESS, which marks a key NO-EVICT. The flag lives outside the
module value, so every module path that writes, replaces, saves or reloads a
value must keep it. RED-220725 (fixed in redis/redis#15995) was such a path:
TDIGEST.MERGE into an existing key replaced the value and dropped the flag.

tests/flow/test_bless.py:
- every write command in test_replication.ROWS keeps NO-EVICT when it runs
  on a blessed key, plus TDIGEST.MERGE ... OVERRIDE
- a blessed key of each type keeps the flag through DEBUG RELOAD and an AOF
  rewrite without the RDB preamble (the types' own aof_rewrite callbacks)
- blessed keys of each type are not evicted under allkeys-lru

Skipped on cluster and on servers without BLESS.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* Re-run CI with fresh docker images

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [xyproto/algernon](https://github.com/xyproto/algernon) [1](https://github.com/xyproto/algernon/commits): Update dependencies

## [rust](https://github.com/topics/rust)
- [Ephemeral-AI-Lab/layerfs](https://github.com/Ephemeral-AI-Lab/layerfs) [32](https://github.com/Ephemeral-AI-Lab/layerfs/commits): docs(readme): add a prior-art section

Compare LayerFS with overlayfs/UnionFS and image layers, Btrfs/ZFS
snapshots, Git worktrees, try, and Apiary/virtual layered file systems,
and say when to use something else (durability, POSIX node types,
sequential I/O). Answers the "why not btrfs" and "reinvented" questions
from the Hacker News thread.

Production LOC: 109056 -> 109056 (delta 0)
Core 96783 -> 96783; SDK 3090 -> 3090; dsh 9183 -> 9183. Docs-only.
Reference absent (retired R9c; last counted 65,417 at tree 498dd1917812).
Method: tools/production_loc.py blob e6d94d1a731b402ccc9159f49cef1eba5a74cfe0
on parent b5814bf3a8 and the staged tree (README.md only).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [dora-rs/dora](https://github.com/dora-rs/dora) [18](https://github.com/dora-rs/dora/commits): perf(record-node): prepare each recorded message's IPC encoding once (#3822)

`ipc_fast_path_len` followed by `encode_ipc_into` builds the layout and
both flatbuffer headers twice. `PreparedIpc` (whose docs recommend it for
exactly this) does it once and writes identical bytes.


Claude-Session: https://claude.ai/code/session_01E3a373ww1p381gpKvTzEzB

Co-authored-by: Claude <noreply@anthropic.com>
- [embassy-rs/embassy](https://github.com/embassy-rs/embassy) [10](https://github.com/embassy-rs/embassy/commits): Merge pull request #7315 from eulerdisk/embassy_usb_cdc_acm_write_empty_packet

embassy_usb, cdc_acm class: write empty packet to end transaction.
- [nextest-rs/nextest](https://github.com/nextest-rs/nextest) [5](https://github.com/nextest-rs/nextest/commits): Update SECURITY.md
- [probe-rs/probe-rs](https://github.com/probe-rs/probe-rs) [4](https://github.com/probe-rs/probe-rs/commits): Show binary target output as space-separated hex pairs (#4523)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [sharkdp/fd](https://github.com/sharkdp/fd) [4](https://github.com/sharkdp/fd/commits): Merge pull request #2187 from ump45nose/docs/threads-default-cap

docs: mention the 64-thread cap in the --threads default
- [google/OpenSK](https://github.com/google/OpenSK) [3](https://github.com/google/OpenSK/commits): Accept built-in UV tokens without a PIN in MakeCredential/GetAssertion (#822)

* Accept built-in UV tokens without a PIN in MakeCredential/GetAssertion

With the fingerprint feature, getPinUvAuthTokenUsingUvWithPermissions
issues a pinUvAuthToken through built-in UV without any PIN set. But
MakeCredential and GetAssertion reject every pinUvAuthParam with
CTAP2_ERR_PIN_NOT_SET when no PIN is set (CTAP 2.0 logic), so that
token can never be used.

Platforms prefer the token path whenever pinUvAuthToken is advertised,
so an authenticator with built-in UV and no PIN fails every UV-required
request (e.g. Chrome: "operation timed out or not allowed").

Keep the 2.0 check, but only reject when no form of user verification
is configured: neither a PIN nor an enrolled built-in UV method.

* Apply the user verification check to all "protected by some form of UV" steps

Move has_user_verification to storage and use it wherever CTAP 2.1
says "protected by some form of user verification" but OpenSK only
checked for a PIN: the discoverable-credential check in MakeCredential
(makeCredUvNotRqd), authenticatorLargeBlobs set, and
authenticatorConfig.

The remaining pin_hash checks are PIN-specific by the spec: clientPin
in getInfo, the zero-length pinUvAuthParam response, setPin/changePin,
forceChangePin, and blocking built-in UV when the PIN is blocked.

* Update comments for the user verification check

CTAP2.1 does cover a pinUvAuthParam on an authenticator without any form
of user verification, and the rk check now depends on any form of user
verification, not only a PIN.
- [jaemk/cached](https://github.com/jaemk/cached) [3](https://github.com/jaemk/cached/commits): release 4.0.4 (#335)
- [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) [2](https://github.com/ast-grep/ast-grep/commits): refactor(cli): apply project defaults through InputArgs (#3027)
- [rmk-rs/rmk](https://github.com/rmk-rs/rmk) [2](https://github.com/rmk-rs/rmk/commits): Merge pull request #1313 from rmk-rs/daily_review/20261021-pointing-redundant

test(pointing): remove redundant defaults and arithmetic checks
- [BerriAI/litellm](https://github.com/BerriAI/litellm) [1](https://github.com/BerriAI/litellm/commits): fix(security): stop trusting the compromised eMudhra root CA (#47670)

Update certifi, Rust trust roots, and the Docker CA bundle to remove emSign ECC Root CA - G3

Require the fixed certifi release in litellm-core and retain libssl3 in Docker runtimes for Prisma compatibility

Co-authored-by: shin-berri <shin-laptop@berri.ai>
- [cargo-generate/cargo-generate](https://github.com/cargo-generate/cargo-generate) [1](https://github.com/cargo-generate/cargo-generate/commits): feat: format the generated files with rustfmt by default (#1785)

Templates rarely produce rustfmt-clean output, and the usual workaround
is a Rhai post hook shelling out to `cargo fmt`. That hook runs against
the temp template dir, which is a UNC path on Windows, so it breaks from
`--git` while working fine from `--path`.

- Formatting is on by default. Opt out with `[template] fmt = false` or
`--no-fmt`.
- Only the files a run actually wrote get formatted, so `--init` into an
existing project leaves the surrounding code untouched.
- `rustfmt` directly rather than `cargo fmt`: the latter's finest
granularity is the package, and handing it a path widens the set instead
of narrowing it. Each file is formatted against the edition of the
package it lands in.
- Formatting can never fail a generation. A missing component or an
unparseable file warns and carries on.
- `post = ["fmt"]` is a built-in identifier rather than a script, and
re-enables formatting for a template that opted out.

Closes https://github.com/cargo-generate/cargo-generate/issues/1776, and
the original request it narrows,
https://github.com/cargo-generate/cargo-generate/issues/884.

Related: https://github.com/cargo-generate/cargo-generate/issues/1435
stays open. Template authors no longer need the `cargo fmt` post hook,
which removes the reason most people hit that bug, but `system::command`
on the git path is unchanged.

---------

Signed-off-by: Sven Kanoldt <sven@d34dl0ck.me>
- [google/wasefire](https://github.com/google/wasefire) [1](https://github.com/google/wasefire/commits): Bump rustup from 1.29.1 to 1.29.2 (#1170)
- [johanhelsing/bevy_pkv](https://github.com/johanhelsing/bevy_pkv) [1](https://github.com/johanhelsing/bevy_pkv/commits): Merge pull request #80 from idanarye/upgrade-to-bevy-0.20

Upgrade to Bevy 0.20
- [metaplex-foundation/metaplex-program-library](https://github.com/metaplex-foundation/metaplex-program-library) [1](https://github.com/metaplex-foundation/metaplex-program-library/commits): chore: bump Node runtime for Oct 21 2026 security release (APP-1336) (#1216)

Node 14 is long EOL and gets none of the fixes for CVE-2026-105482,
CVE-2026-105483, CVE-2026-106069 and CVE-2026-111497. Move the auction-house
CLI's nvm pin to 22.23.4. CI workflow node-version pins are out of scope.

Triggered-By: human

Claude-Session: https://claude.ai/code/session_01G8o11MqNNm1EtFQoNou8jh

Co-authored-by: Claude <noreply@anthropic.com>
- [sigoden/dufs](https://github.com/sigoden/dufs) [1](https://github.com/sigoden/dufs/commits): refactor: skip IPv6 bind checks when unavailable (#773)

## Other
- [lancedb/lancedb](https://github.com/lancedb/lancedb) [59](https://github.com/lancedb/lancedb/commits): feat!: return lazy iterators for table and namespace listings (#4599)

Make table and namespace listings consistent with other resource
listings across Rust, Python, and TypeScript. Callers can iterate over
individual names across all pages, with configurable page sizes and
continuation tokens.

In order to avoid breaking existing Python users, this change adds some
compatibility methods to the returned Python iterators. Code such as:
```
for t in db.list_tables().tables:
    print(t)
```
will continue to work as expected because the iterator has a `tables`
field and a `page_token` field, which function as expected to reveal the
first page of results. In other words, it is never necessary to use the
iterator __as an iterator__. It may be used as if it were an old-style
response object. (As the iterator progresses, the `tables` list may
switch to the second, third, etc. page of results.) Similar
compatibility code allows the async python API to keep working as well.
- [openai/codex](https://github.com/openai/codex) [57](https://github.com/openai/codex/commits): Apply model catalog overrides to history, notes, and context tools (#56313)

## What changed

- Read optional tool descriptions and parameter schemas for `history`, `notes`, `new_context`, and `get_context_remaining` from the acting model's catalog messages.
- Support catalog namespace descriptions for history and notes, preserving explicit empty and whitespace descriptions.
- Share catalog override handling across native tools and MCP resource helpers. Keep bundled schemas when overrides are invalid, preserve encrypted parameters, and leave tool identity and transport fields unchanged.

## Testing

Add coverage for sparse catalog serialization, schema fallback and encryption preservation, per-step tool definitions, and context tool updates when switching models. Extend outgoing-request tests to verify history and notes overrides while retaining history image attachments.

GitOrigin-RevId: 1adac8b5009f95c91adba491f20a4e2e2dc91475
- [ly05010419/MacNativeGames](https://github.com/ly05010419/MacNativeGames) [51](https://github.com/ly05010419/MacNativeGames/commits): feat: iOS game data in the app's Documents, installed once; .app output, app icon and the name TOTK; faster iOS packaging

build_app.py --ios-game-data documents leaves the 17 GB RomFS image out of
the app; install_device.py --game-data copies it into Documents/GameData in
1 GiB parts with a SHA-256 marker and skips it when the device already has
it, so later installs take minutes. The app reads it through
TOTK_ROMFS_DATA, keeps it out of backups, and shows a line on screen
instead of starting when the data is missing or incomplete.

The iOS build can write an unsigned .app (install_device.py installs it
by APFS clone), carries the game's own icon (from the player's files, as on
the Mac) and is named TOTK on the home screen. The seed is cloned as one
folder, its manifest hashes reused, and compiled shader libraries cached by
source: 13-17 min -> 6-8.5 min. The build makes the contribution folder and
points the iPhone / iPad watcher at it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [Mentra-Community/MentraOS](https://github.com/Mentra-Community/MentraOS) [43](https://github.com/Mentra-Community/MentraOS/commits): Merge pull request #4923 from Mentra-Community/aisraelov/staging-into-dev-1022

Merge staging into dev (one flow)
- [buildroot/buildroot](https://github.com/buildroot/buildroot) [36](https://github.com/buildroot/buildroot/commits): support/testing/tests/package/test_fluent_bit.py: new runtime test

Signed-off-by: Thomas Devoogdt <thomas@devoogdt.com>
Signed-off-by: Thomas Petazzoni <thomas.petazzoni@bootlin.com>
- [earendil-works/pi](https://github.com/earendil-works/pi) [20](https://github.com/earendil-works/pi/commits): fix(evals): drop autoevals dependency

autoevals@0.3.0 declares engines npm: please-use-pnpm, so every npm install printed an EBADENGINE warning. 0.4.1 removes that but adds a pnpm-enforcing preinstall script. The eval only used the Levenshtein scorer, so inline an equivalent normalized similarity helper instead.
- [usetrmnl/trmnl-firmware](https://github.com/usetrmnl/trmnl-firmware) [20](https://github.com/usetrmnl/trmnl-firmware/commits): Move the X touch bar indicator out of display.cpp (#753)

Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
- [ophub/amlogic-s9xxx-armbian](https://github.com/ophub/amlogic-s9xxx-armbian) [13](https://github.com/ophub/amlogic-s9xxx-armbian/commits): Update documents
- [huggingface/AnyLanguageModel](https://github.com/huggingface/AnyLanguageModel) [11](https://github.com/huggingface/AnyLanguageModel/commits): Bump README install snippets to 1.1.0 (#368)
- [mozilla/sccache](https://github.com/mozilla/sccache) [10](https://github.com/mozilla/sccache/commits): http: restore TLS trust roots with reqwest 0.13
- [nicklockwood/SwiftFormat](https://github.com/nicklockwood/SwiftFormat) [10](https://github.com/nicklockwood/SwiftFormat/commits): Fix Windows build action
- [Sorosliu1029/follower-change](https://github.com/Sorosliu1029/follower-change) [10](https://github.com/Sorosliu1029/follower-change/commits): ci: skip HTML upload in test workflow when the action sets no output

On a first run the action returns before setting outputs, so htmlFilePath
is empty and upload-artifact fails with 'Input required and not supplied: path'.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [daijro/camoufox](https://github.com/daijro/camoufox) [9](https://github.com/daijro/camoufox/commits): Merge pull request #902 from coffeegrind123/pr/addons-concurrent

Download the default addons once under concurrent launches
- [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) [9](https://github.com/ghostty-org/ghostty/commits): terminal: continuations must restart at C1 sequence introducers (#14814)

A stream continuation that ended after an 8-bit C1 introducer had
aborted an APC could not be exported. For example, `ESC _ data 0x9B`
ends the APC and starts a CSI, but the tracker only treats ESC as the
start of a new sequence, so it kept the aborted APC. Replaying that
would end the APC a second time, and validation rejected it.

Export now starts at the last C1 introducer that moved the parser into a
new sequence and writes it in its 7-bit ESC form.
- [typst/typst](https://github.com/typst/typst) [9](https://github.com/typst/typst/commits): Improve `quote` docs (#8951)

Co-authored-by: Laurenz <laurmaedje@gmail.com>
- [verl-project/verl](https://github.com/verl-project/verl) [9](https://github.com/verl-project/verl/commits): [ci] fix: support read-only dataset and model mounts in Ascend tests (#8333)

### What does this PR do?
Set HF_DATASETS_CACHE to /root/.cache/temp/hf-datasets across Ascend
test workflows. Also redirect Megatron config locks to
/root/.cache/temp/megatron-config-locks for SFT, separate async, and
nightly workflows.

Keep generated caches and lock files off read-only dataset and model
mounts.

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
- [binwiederhier/ntfy](https://github.com/binwiederhier/ntfy) [8](https://github.com/binwiederhier/ntfy/commits): Prep v2.33.0 release: release notes, install docs

Move the unreleased server notes to v2.33.0 (released October 23, 2026) with a short intro, and bump install.md to 2.33.0.
- [TelegramMessenger/Telegram-iOS](https://github.com/TelegramMessenger/Telegram-iOS) [8](https://github.com/TelegramMessenger/Telegram-iOS/commits): Bump version

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [astral-sh/ty](https://github.com/astral-sh/ty) [7](https://github.com/astral-sh/ty/commits): Update uv to 0.13.5 (#4809)
- [block/buzz](https://github.com/block/buzz) [7](https://github.com/block/buzz/commits): Add project selection to new Solo chats on mobile (#8546)

New Solo chats can optionally choose a project in the Flutter form and
native iOS sheet. Project appears above the agent picker with matching
neutral text, and the choice survives retries and restarts.

Validation: full Flutter suite passed; analysis and iOS builds passed.
Installed in Pairing Preview on iPhone Air and visually approved,
preserving saved preferences. Successful live chat creation remains
unverified because no agents were available.

---------

Signed-off-by: kenny lopez <klopez4212@gmail.com>
Co-authored-by: Terp <5856f6900e8e0a4e0ea1f4f8d2ee33e4753d2119bc122f94ecafc660b46c0511@buzz.block.builderlab.xyz>
- [cline/cline](https://github.com/cline/cline) [7](https://github.com/cline/cline/commits): fix(llms): keep tests green after the release catalog regen (#15240)

* fix(llms): keep Bedrock Sonnet 4.5 through models.dev deprecation

models.dev now marks Claude Sonnet 4.5 on Bedrock (bare id and all geo
profiles) and Z.AI Coding Plan's glm-5.2 as deprecated, and catalog
normalization drops deprecated models. The next `bun run version` regen
would therefore:

- remove Sonnet 4.5 from the Bedrock catalog, so resolveBedrockModelId
  can no longer confirm a geo profile and sends the bare id, which AWS
  rejects for on-demand use
- leave zai-coding-plan's default model missing from its catalog

Retain the deprecated Sonnet 4.5 Bedrock entries in normalization (used
by both generation and the live catalog refresh) until AWS retires the
model, and move the Z.AI Coding Plan default to glm-5.3.

Also stop pinning ClinePass fallback tests to a specific model the Cline
backend no longer lists; they now check against the generated catalog.

* test(desktop): give the compiled plugin startup test a generous import timeout

Cold Windows runners intermittently take longer than the 4s default to start
the sandbox child, failing sdk-test. The test covers resource loading, not
startup time.

* revert(llms): drop the deprecated Bedrock Sonnet 4.5 retention

Let models.dev deprecations flow through the catalog as before. Point the
Bedrock geo-prefix test at Claude Haiku 4.5, which models.dev still lists, so
it passes after the release catalog regen.
- [facebook/idb](https://github.com/facebook/idb) [7](https://github.com/facebook/idb/commits): Honor the companion path environment override

Summary:
## What
Use nonempty `IDB_COMPANION_PATH` as the macOS companion default.

## Why
Launchers need to select a matching companion without depending on the host's installed copy.

## How
The explicit `--companion-path` flag still wins. Unset or empty overrides preserve existing host discovery, and non-macOS defaults remain unchanged.

Reviewed By: bryanyantx

Differential Revision: D126973142

fbshipit-source-id: 4a64340dd244de59eeda54b6e7dbbc046f7e6622
- [THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC) [7](https://github.com/THU-MAIC/OpenMAIC/commits): test(materials): make the heartbeat-loss extraction scenario deterministic (#1994)

Test-only. The heartbeat-loss scenario failed intermittently on PostgreSQL (expected 2 transactions to be 0) because of three races in the test:

- The stale run read the shared test clock, so after `expire` its heartbeat could renew the lease before the takeover claimed; the run now keeps the time it claimed at.
- The claim skips a row a heartbeat has locked (FOR UPDATE SKIP LOCKED); the takeover is retried, bounded, and asserted.
- A fixed 100 ms sleep assumed a post-takeover heartbeat had returned; the scenario now waits for one that reports the loss.

On failure the scenario releases the gated run before rethrowing, so its heartbeat timer does not outlive teardown.
- [loro-dev/loro](https://github.com/loro-dev/loro) [5](https://github.com/loro-dev/loro/commits): fix: pass release PR bodies through the environment (#1226)

Keep Markdown backticks and shell substitutions in PR prose from executing in the release-flags step.
- [apple/swift-openapi-generator](https://github.com/apple/swift-openapi-generator) [4](https://github.com/apple/swift-openapi-generator/commits): Revert "Allow listing output file paths"

This reverts commit d7c663ec30415723563c02a9663a5c59902a8b38.
- [espressif/esp-gmf](https://github.com/espressif/esp-gmf) [4](https://github.com/espressif/esp-gmf/commits): Merge branch 'ci/optimize-build-time' into 'main'

feat(ci): Enable ccache and optimize pre-build and cxx check steps

See merge request adf/multimedia/esp-gmf!546
- [huggingface/lerobot](https://github.com/huggingface/lerobot) [4](https://github.com/huggingface/lerobot/commits): fix(vla_jepa): pair rotary frequencies with adjacent coordinates (#4835)

* fix(vla_jepa): pair rotary frequencies with adjacent coordinates

* docs(vla_jepa): trace the upstream rotary correction and reduce test diff
- [jdx/mise](https://github.com/jdx/mise) [4](https://github.com/jdx/mise/commits): fix(dotfiles): report a saved enrollment under a symlinked parent instead of failing capture (#14871)

<!-- entire-trail-link-start -->
https://entire.com/gh/jdx/mise/trails/986
<!-- entire-trail-link-end -->

A single saved dotfile enrollment that sits under a symlinked parent no
longer stops automatic capture for every other tracked path.

## Problem

`mise dot status` could report "Automatic capture has failed N times in
a row" while all entries showed as tracked. Each capture re-read the
saved enrollment manifest through `Manifest::tracking()`, which returns
an error for the first entry whose path now runs through a symlink, for
example `~/.claude/skills/entire-trails/SKILL.md` enrolled back when
`entire-trails` was a real directory and later replaced by a link to
`~/.agents/skills/entire-trails`:

```
cannot track ~/.claude/skills/entire-trails/SKILL.md through symlinked parent ~/.claude/skills/entire-trails; explicitly track the link itself and its real target instead
```

Saved enrollments are kept until untracked, so the one stale entry
failed every capture, and nothing was saved.

## Fix

Live capture now reads the manifest with `Manifest::tracking_lenient()`.
An entry under a symlinked parent is left out of the capture set and
recorded in `invalid` with the same message, so it shows up as omitted
in the checkpoint coverage and still blocks publishing until it is
untracked. Replay and sync keep the strict `tracking()`.

I reproduced this from reading the code and your report rather than from
a failing machine; the new assertions in
`enrollment_rejects_alias_parents_but_allows_links_and_real_targets`
cover the lenient read.

*AI-assisted — Tool: Claude Code; model: anthropic/claude-sonnet-5-5;
version: unavailable.*

🤖 Generated with [Claude Code](https://claude.com/claude-code)


<!-- This is an auto-generated comment: release notes by coderabbit.ai
-->
<!-- coderabbit-ai-generated:v1 -->

## Summary by CodeRabbit

* **Bug Fixes**
* History tracking now reports paths with symlinked parent directories
as invalid instead of including them as valid enrollments.
* Existing invalid path reports are preserved alongside newly detected
issues, without duplicating matching reports.
* Saved files under enrollments with symlinked parent directories are
retained during history preservation rather than being treated as
deleted.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->

---------

Co-authored-by: Claude Sonnet 5.5 <noreply@anthropic.com>
- [josephmisiti/awesome-machine-learning](https://github.com/josephmisiti/awesome-machine-learning) [4](https://github.com/josephmisiti/awesome-machine-learning/commits): Merge pull request #1446 from jays-beep/patch-1

Add Future AGI to Python General-Purpose Machine Learning
- [Automattic/simplenote-android](https://github.com/Automattic/simplenote-android) [3](https://github.com/Automattic/simplenote-android/commits): Fix crash on back gesture after the account verification dialog closes (#1898)
- [awesomedata/awesome-public-datasets](https://github.com/awesomedata/awesome-public-datasets) [3](https://github.com/awesomedata/awesome-public-datasets/commits): Update README sha: b3c20bf9642127a04c1a991c78be0861a495744d
- [biliup/biliup](https://github.com/biliup/biliup) [3](https://github.com/biliup/biliup/commits): Track processed video sources for cleanup

Persist source-file associations for processed videos so rm and deferred retention cleanup remove originals and intermediates safely, including after restarts. Remove the local-material preset UI and update recording and processor documentation.
- [databendlabs/openraft](https://github.com/databendlabs/openraft) [3](https://github.com/databendlabs/openraft/commits): refactor: openraft: remove dead_code allowances and file
- [tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro) [3](https://github.com/tensorflow/tflite-micro/commits): fix(compression): tidy the tutorial's spec step (#3914)

Let a compression failure stop the tutorial. The compression cell
caught the error and went on, so a later cell failed with an
unrelated error.

Fix the YAML spec example. Each compression method needs a leading
dash, as an item in a list, and the two tensor numbers were swapped.
- [AcademySoftwareFoundation/OpenShadingLanguage](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage) [2](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/commits): testing: runtest.py improvements ported from OpenImageIO (#2189)

Port the parts of OIIO PR 5465 and 5476 that apply to OSL's
runtest.py:

* run_app() takes a failureok parameter. If the first word of the
  command names an OSL app (oslc, oslinfo, testshade, testrender,
  testoptix) or an OIIO app (oiiotool, maketx, etc.), it is replaced
  with the full path to the built app.
* New run_commands() takes a multi-line string of shell commands, one
  per line, and runs each through run_app(). Blank lines and `#`
  comments are skipped. So a run.py can list commands exactly as they
  would be typed, and docs can include them by reference.
* The oslc, oslinfo, oiiotool, maketx, oiiodiff, testshade, testrender,
  and testoptix helpers are now thin wrappers around run_app().
  oiiotool() also gained failureok and concat parameters.
* text_diff ignores trailing whitespace differences, which can vary by
  platform (e.g. cmd.exe's echo).
* redirect_push and redirect_pop to let a test redirect a portion of
  output to a different file.

Assisted-by: Claude Code / Claude Opus 5.5

Signed-off-by: Larry Gritz <lg@larrygritz.com>
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) [2](https://github.com/anthropics/claude-agent-sdk-python/commits): chore: bump bundled CLI version to 2.1.309
- [anthropics/claude-code](https://github.com/anthropics/claude-code) [2](https://github.com/anthropics/claude-code/commits): chore: Update CHANGELOG.md and feed.xml

Fixes #97469
Fixes #102981
- [cel-expr/cel-spec](https://github.com/cel-expr/cel-spec) [2](https://github.com/cel-expr/cel-spec/commits): Remove deprecated strong enum sections and unbound function short-circuit (#532)

Remove deprecated strong enum sections and unbound function short-circuit test
- [cherry-embedded/CherryDAP](https://github.com/cherry-embedded/CherryDAP) [2](https://github.com/cherry-embedded/CherryDAP/commits): update(hslinklite): remove spi code

Signed-off-by: sakumisu <1203593632@qq.com>
- [drduh/YubiKey-Guide](https://github.com/drduh/YubiKey-Guide) [2](https://github.com/drduh/YubiKey-Guide/commits): Merge pull request #554 from drduh/20oct26

Replace WSL agent architecture diagram with Mermaid
- [espressif/esp-dl](https://github.com/espressif/esp-dl) [2](https://github.com/espressif/esp-dl/commits): Merge branch 'feat/finetune_conv' into 'master'

Feat/finetune conv

See merge request ai/esp-dl!367
- [input-output-hk/daedalus](https://github.com/input-output-hk/daedalus) [2](https://github.com/input-output-hk/daedalus/commits): Merge pull request #3433 from input-output-hk/sl/bump-nodejs

fix(deps): update Node.js and TOML for security fixes
- [JohanChane/clashtui](https://github.com/JohanChane/clashtui) [2](https://github.com/JohanChane/clashtui/commits): fix(proxies): resolve provider nodes and route health checks (#136)

Fetch primary proxies and provider catalogs separately so provider-only group
members can display their latency. Preserve each provider's identity and use
its healthcheck route for individual node tests.

Treat name collisions as ambiguous instead of picking a provider by iteration
order. Ignore Compatible aliases and recognize legacy flattened entries by
node ID or provider origin. Keep group testing available for ambiguous names.

Refresh histories after failed tests, display completed-test errors, and avoid
applying stale results to nodes replaced during provider updates. Respect
provider test URLs and encode provider names, node names, and nested URLs.

Add fixtures and regression coverage for provider histories, endpoint routing,
collisions, refreshes, sorting, failures, and unsupported provider APIs.
- [jqlang/jq](https://github.com/jqlang/jq) [2](https://github.com/jqlang/jq/commits): docs: explain that semicolons separate function arguments (#3685)

The manual's "Defining Functions" section shows only one-argument
functions, so it never says how to pass more than one. This adds a short
paragraph: arguments are separated by `;` in both `def f(a; b):` and
`f(.x; .y)`, and `f(.x, .y)` instead calls a one-argument `f` with the
filter `.x, .y`. It also adds an example for each. `tests/man.test` and
`jq.1.prebuilt` are regenerated.

Fixes #2163
- [KittenML/KittenTTS](https://github.com/KittenML/KittenTTS) [2](https://github.com/KittenML/KittenTTS/commits): Merge pull request #178 from stellon-admin/feat/gradio-demo

Add a single-file Gradio demo
- [m-bain/whisperX](https://github.com/m-bain/whisperX) [2](https://github.com/m-bain/whisperX/commits): Merge pull request #1469 from li-lizhe/fix-optional-torchaudio

Make torchaudio optional with Hugging Face fallback for align models

- Tests look good, happy with merge
- [motherduckdb/grafana-duckdb-datasource](https://github.com/motherduckdb/grafana-duckdb-datasource) [2](https://github.com/motherduckdb/grafana-duckdb-datasource/commits): Bump datasource version from 0.4.5 to 0.4.6 (#119)

Bump datasource version from 0.4.5 to 0.4.6
- [signalapp/libsignal](https://github.com/signalapp/libsignal) [2](https://github.com/signalapp/libsignal/commits): Distrust compromised weak intermediate certs
- [swiftlang/swift-corelibs-xctest](https://github.com/swiftlang/swift-corelibs-xctest) [2](https://github.com/swiftlang/swift-corelibs-xctest/commits): Merge pull request #558 from charles-zablit/cz/lit-cfg-no-pkg-resources

[test] Remove pkg_resources and macOS-specific code from the functional tests
- [apple/swift-log](https://github.com/apple/swift-log) [1](https://github.com/apple/swift-log/commits): Mutate the logger's handler in place on metadata writes (#529)

Give `Logger.handler` a `_modify` accessor and replace its `get` with
`_read`, so metadata writes update the stored handler instead of a copy.

### Motivation:

`Logger.handler` only has `get` and `set`. A write such as
`logger[metadataKey: "k"] = "v"` gets a copy of the handler, writes to
it while the stored handler still shares the metadata dictionary, and
sets it back. So every write copies the whole dictionary, and
`withLogger(mergingMetadata:)` does that once per key.

### Modifications:

- Give `Logger.handler` `_read`, `set` and `_modify` accessors. `_read`
yields the stored handler. `_modify` keeps the existing uniqueness check
on the storage and then yields the stored handler, so metadata and log
level writes change it in place. `set` keeps the same check for plain
`logger.handler = newHandler` assignments, which are cheaper through a
setter than through `_modify`.
- Add a test handler that counts copies of its metadata, with tests for
direct writes and for `withLogger(mergingMetadata:)`. Without the change
they report 10 copies instead of 0, and 5 instead of 1.

### Result:

A metadata write on a logger that owns its storage no longer copies the
dictionary. A copied logger still copies once on its first write, so
value semantics are unchanged.

1,000 metadata writes with a handler that keeps metadata in a plain
dictionary, debug build, three runs each:

| Keys on the logger | Before | After |
|---|---|---|
| 10 | 7.2 to 8.1 ms | 0.46 to 0.50 ms |
| 1,000 | 20.2 to 20.6 ms | 0.46 to 0.55 ms |
| 10,000 | 134.0 to 134.4 ms | 0.47 to 0.50 ms |
| 100,000 | 1.29 to 1.30 s | 0.32 to 0.35 ms |

`withLogger(mergingMetadata:)` with 10,000 keys went from 0.64 to 0.65 s
down to 2.9 to 3.1 ms. `StreamLogHandler` still rebuilds its pretty
metadata string on every write; this change does not touch that.

All 176 tests pass on macOS with Swift 6.4, and `swift format lint
--strict` and `swift package diagnose-api-breaking-changes` are clean.
Once yielding accessors land, `_read` and `_modify` can become `yielding
borrow` and `yielding mutate`.

Fixes #526.
- [bitbank2/OneBitDisplay](https://github.com/bitbank2/OneBitDisplay) [1](https://github.com/bitbank2/OneBitDisplay/commits): Added support for the ST7567 128x32 LCD in I2C mode
- [ccusage/ccusage](https://github.com/ccusage/ccusage) [1](https://github.com/ccusage/ccusage/commits): fix(antigravity): map model ID 1402 to claude-opus-5-5 (#1948)

* fix(antigravity): map model ID 1402 to claude-opus-5-5

Antigravity reports Claude Opus 5.5 as model ID 1402. It was not in
the ID table, so it fell back to `model_placeholder_m402`, which has no
pricing entry and was reported at $0 with a missing-pricing warning.

Map both the numeric ID and the placeholder to `claude-opus-5-5`,
which the embedded pricing catalog already prices, and cover the
mapping plus a non-zero calculated cost in a parser test.

Fixes #1947

Co-authored-by: viniciusdsandrade <95101505+viniciusdsandrade@users.noreply.github.com>

* test(antigravity): cover Claude Opus 5.5 through the loader

The parser test called the mapping helpers directly, so it did not
prove that real Antigravity rows load with the right model and cost.

Extend the production report fixture with a row that only carries
model ID 1402 and a row that stores `model_placeholder_m402`, and
assert both load as `claude-opus-5-5` with a non-zero cost and no
missing-pricing warning. The snapshot now includes them in the daily,
weekly, monthly and session reports.

Co-authored-by: viniciusdsandrade <95101505+viniciusdsandrade@users.noreply.github.com>

---------

Co-authored-by: Cursor Agent <cursoragent@cursor.com>
Co-authored-by: viniciusdsandrade <95101505+viniciusdsandrade@users.noreply.github.com>
- [cdhigh/KindleEar](https://github.com/cdhigh/KindleEar) [1](https://github.com/cdhigh/KindleEar/commits): 3.5.3

fetch links in inbound_email
- [ch32-rs/wlink](https://github.com/ch32-rs/wlink) [1](https://github.com/ch32-rs/wlink/commits): chips: report CH32M103G8R6 chip ID (#129)
- [cv-cat/Spider_XHS](https://github.com/cv-cat/Spider_XHS) [1](https://github.com/cv-cat/Spider_XHS/commits): Merge pull request #192 from cv-cat/feat/fastaitoken-sponsor

登录 ssk 密钥交换 / 471·461 风控验证链 / b1 逐字节对齐 / 发布 -9059 修复
- [dentiny/duck-read-cache-fs](https://github.com/dentiny/duck-read-cache-fs) [1](https://github.com/dentiny/duck-read-cache-fs/commits): Fix unit-test linking with prebuilt DuckDB (#533)
- [embassy-rs/stm32-data](https://github.com/embassy-rs/stm32-data) [1](https://github.com/embassy-rs/stm32-data/commits): Merge pull request #941 from lennlouisgeek/fix/dac-v9-channel-arrays

fix(dac): use length-once channel arrays for v9
- [espressif/esp-adf](https://github.com/espressif/esp-adf) [1](https://github.com/espressif/esp-adf/commits): Merge branch 'bugfix/esp_llm_volc_bundle_sdk' into 'master'

fix(esp_llm_volc): Build bundled volc_conv_ai inside the component

See merge request adf/esp-adf-internal!1596
- [fishjar/kiss-translator](https://github.com/fishjar/kiss-translator) [1](https://github.com/fishjar/kiss-translator/commits): Add web image translation (#1202)

* Add web image translation workflow

* Add local AI document translation and OCR support
- [fluidd-core/fluidd](https://github.com/fluidd-core/fluidd) [1](https://github.com/fluidd-core/fluidd/commits): feat: synthesize agent connection events (#2000)

Signed-off-by: Pedro Lamas <pedrolamas@gmail.com>
Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [nordicsemi/nrfx](https://github.com/nordicsemi/nrfx) [1](https://github.com/nordicsemi/nrfx/commits): nrfx 4.7.0 release

Signed-off-by: Nikodem Kastelik <nikodem.kastelik@nordicsemi.no>
- [openclaw/acpx](https://github.com/openclaw/acpx) [1](https://github.com/openclaw/acpx/commits): fix(ci): pin Node releases with incident key rejection (#900)
- [openclaw/gogcli](https://github.com/openclaw/gogcli) [1](https://github.com/openclaw/gogcli/commits): fix(ci): pin Node releases with incident key rejection (#1244)

* fix(ci): pin Node releases with incident key rejection

* fix(images): upgrade Alpine certificate packages

* docs: record Docker trust-store remediation (#1244)
- [osohq/oso](https://github.com/osohq/oso) [1](https://github.com/osohq/oso/commits): docs: mark repository as archived and point to Oso Cloud
- [smithy-lang/smithy](https://github.com/smithy-lang/smithy) [1](https://github.com/smithy-lang/smithy/commits): Use the absolute path of the override file (#3333)
- [sushi-labs/sushiswap](https://github.com/sushi-labs/sushiswap) [1](https://github.com/sushi-labs/sushiswap/commits): fix: require patched Node 24.22.1 runtime (#2328)
- [TactilityProject/Tactility](https://github.com/TactilityProject/Tactility) [1](https://github.com/TactilityProject/Tactility/commits): BlueTooth refactored (#710)
- [VoronDesign/Voron-2](https://github.com/VoronDesign/Voron-2) [1](https://github.com/VoronDesign/Voron-2/commits): Add files via upload (#511)

added Top/Side/Door panel dxfs for all 3 sizes
- [zhongerxin/iPhone-use](https://github.com/zhongerxin/iPhone-use) [1](https://github.com/zhongerxin/iPhone-use/commits): Release 0.3.16: track launched app usage in PostHog and GA4