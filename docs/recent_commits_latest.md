# Recent Activity in Starred Repositories
_156 active repos with 2235 new commits_

## [3d-printing](https://github.com/topics/3d-printing)
- [fluidd-core/fluidd](https://github.com/fluidd-core/fluidd) [2](https://github.com/fluidd-core/fluidd/commits): refactor: Kalico heater control values

Signed-off-by: Pedro Lamas <pedrolamas@gmail.com>
- [dune3d/dune3d](https://github.com/dune3d/dune3d) [1](https://github.com/dune3d/dune3d/commits): unbreak axes cube

got broken in 2ecb0915d8b4c04ab69336f6e968eb53f27cc6f9

## [agent-skills](https://github.com/topics/agent-skills)
- [alibaba/open-code-review](https://github.com/alibaba/open-code-review) [2](https://github.com/alibaba/open-code-review/commits): test(allowlist): catch an extension disappearing from the allowlist (#1626)

Co-authored-by: gu-feng418 <287555569+gu-feng418@users.noreply.github.com>
Co-authored-by: Kite <254839944+lizhengfeng101@users.noreply.github.com>
- [anthropics/skills](https://github.com/anthropics/skills) [2](https://github.com/anthropics/skills/commits): Update claude-api skill: dynamic workflows and the four workflow quickstarts (#1995)

Sync of the bundled claude-api skill: the Managed Agents dynamic workflows
guidance, the four dynamic-workflow quickstart templates, and the limited-
networking web-tool rules. Public-only trims in SKILL.md, shared/evals/ and
shared/model-migration.md are preserved.

Co-authored-by: Claude <noreply@anthropic.com>

## [ai](https://github.com/topics/ai)
- [openclaw/openclaw](https://github.com/openclaw/openclaw) [347](https://github.com/openclaw/openclaw/commits): fix(test): include GitHub parser in release admission fixtures

The release validation policy now imports gh-api-preflight.mjs, but the
copied observation-worker fixture omitted it. Include the parser so the
worker exercises admission outcomes instead of failing module resolution.

Follow-up to f8239ea9470d (#167510). Preserve all redaction and admission
assertions; production release-tooling source inventories are unchanged.
- [BasedHardware/omi](https://github.com/BasedHardware/omi) [175](https://github.com/BasedHardware/omi/commits): feat(backend): observe owner identity retry funnel (#21095)

Observe owner identity candidate attempts on first finalization and late
pusher repair with `omi_owner_identity_retry_total{pass,stage,reason}`.
Existing `unverified_inventory` refusals now have a closed primary
diagnostic reason, without changing the refusal, transcript, speaker
labels, embedding cache, or read/model budgets. This makes invisible
inventory/read and placement failures distinguishable from insufficient
speech and admission/CAS denial.

- Add the 28 funnel pairs plus 30 resolver-exit pairs, with
`pass=first|late`. Children are lazy, collector registration is
reload-safe, and labels contain no account/conversation/segment/speaker
IDs, scope, exception or content.
- Count late candidate entry, slot/scan/pass-cap skips, eligibility and
existing early exits. Count CAS outcomes only after the outer
transaction returns, including no-op commits; transaction callback
retries emit no additional terminal count.
- Tag first-finalization calls using the existing `already_observed`
determination. An already-observed reprocess emits no first funnel. No
extra transcript/profile/storage reads, retries, embedding calls,
placement/proof work or writes.
- Keep `omi_owner_identity_repair_total` and
`omi_owner_recognition_conversations_total` unchanged. Zero-duration
acceptance, partial inventory/selected-window reading, floors,
manual/channel authority and old-cache policy are unchanged.

### How to read it

```promql
sum by (pass, reason) (increase(omi_owner_identity_retry_total{stage="resolver_exit"}[1h]))
sum by (stage, reason) (increase(omi_owner_identity_retry_total{pass="late",stage!="resolver_exit"}[1h]))
```

These count attempts, not unique conversations, owner candidates, or
owner additions. Late entry is deduplicated per scheduled batch,
including candidates refused by capacity. Eligibility follows the
snapshot checks. `slot_limit`, `scan_limit` and `pass_limit` are
unscanned capacity, not acoustic evidence. Late terminals are `skipped +
cas_refused + cas_committed`; entry minus those terminals is unfinished
work across the interval boundary. `eligible` and `resolver_exit` are
intermediate; an unavailable/no-op resolver may still commit. Compare
`owner_added` from the existing repair counter to `cas_committed` to see
the actual identity-change yield.

First entry means a first-finalization attempt reached the shared
resolver, not every finalization request. First eligibility means a
nonempty conversation model; channel/private-cloud/audio policy is
observed at its existing resolver gate. First resolver exit ends its
acoustic attempt, not later summary/persistence. Earlier processing
admission returns are outside this counter. Neither pass backfills or
identifies David's historical 41 rows; the metric attributes future
population attempts without account labels.

Primary precedence preserves executed gates: placement deadline before
later proof; at the global veto, manifest ambiguity → zero/other invalid
text → uncovered window with a validated index → unvalidated manifest →
capture coverage hole. Then actual inventory proof retains read/listing,
object metadata, manifest inventory, count/pair equality, fetch/decode,
decoded duration/overlap/coverage order. `read_budget` includes the
existing count/bytes/deadline/transient-listing refusal.
`no_proven_window` covers missing origin/provider position, explicit
unplaced alignment and legacy clock refusal. Usable partial resolution
emits `partial` even if later embedding capacity was exhausted;
failure/budget is primary when no resolution was produced. Full closed
pair table and semantics are in
`backend/docs/listen_pusher_pipeline.mdx`.

### Deployment, cost and residuals

Deploy pusher for late and pusher-hosted first passes; deploy
backend/listen and Cloud Run backend, backend-sync and
backend-sync-backfill for their first-pass coverage. No new flags or
prod env changes, schema/index/wire changes, app release, or backfill.
Mixed images are safe: old images emit no new samples. Existing
recognition flags retain their values.

Added service reads/model calls/storage operations/writes: **0 per
session-hour**. Existing late ceilings remain two concurrent batches per
process, 128 scanned candidates and eight eligible passes per batch,
five seconds and 24 model attempts per eligible pass. At most 58 closed
pairs per pass / 116 counter children per process, lazy rather than idle
zeros. Only local scalar diagnostics and counter increments are added.
Missing audio, global inventory vetoes, zero-duration poisoning and
whole-inventory download caps remain deliberate residuals for separately
authorized behavior work.

### Validation

All four full backend CI shards passed (`--all --shard 4/K`, K=1..4):
425 + 425 + 425 + 424 = 1,699 selected files. Each runner returned exit
0. Focused regression suite: 75 passed. Literal origin/main
implementation versus instrumented resolver: byte-identical conversation
JSON and encoded cache bytes; inventory-proof refusals have identical
I/O calls. Real first-finalization lifecycle verifies first emission and
suppression on subsequent reprocess. CAS refusal reasons, callback
replay, no-op commit, encrypted/compressed manual authority and
metric-failure isolation are covered; existing identity/finalization
counters remain unchanged on no-op commits.

Red proof using the literal main resolver at the finalization boundary:
`1 failed, 74 passed, 14 warnings in 13.78s`; the first-funnel delta was
`{}` instead of entry/eligible/no_audio. Credential-isolated green: `75
passed, 15 warnings in 11.13s`.

Credential-isolated verification follows a merge of current main
(`a1cfd2683b`). Every test/preflight command clears
GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT and
CLOUDSDK_CORE_PROJECT and uses a fresh empty CLOUDSDK_CONFIG. The
pre-start ADC check returned `PASS: ADC unavailable`. Full `make
preflight`: all 33 checks passed in 285.40s; no hook/check/harness
changes or bypasses.

Three pre-existing tests (`test_sync_pipeline_contact_guards.py`,
`test_taught_speaker_persistence.py`, `test_voiceprint_authority.py`)
leave the owner-profile recovery-state seam unstubbed when a mocked
print is missing. They can enter the database client under inherited
credentials. An initial run was stopped after discovering inherited
ro-prod pointers; no credential contents or production account data were
inspected, and whether SDK requests occurred could not be determined.
Those tests are not changed in this PR. The resumed suite runs with ADC
unavailable; fixture isolation belongs to separate work.

### Risks for independent review

- Attempt unit and first/late eligibility differ as documented; this
counter cannot infer unique-account owner recovery or retroactively
classify historical rows.
- Primary diagnostic precedence must describe the existing executed veto
rather than imply audio is absent when proof/budget is unavailable.
- CAS observer must stay outside transaction callbacks, with exactly one
terminal verdict and no duplicate skip after an authoritative commit.
- Context-local pass diagnostics must not leak into unrelated or
already-observed reprocessing; collector reload must reuse the same
counter.

Failure-Class: none
### Product invariants affected

- INV-MEM-4: canonical memory admission, promotion receipts and
consolidation remain unchanged; only the existing speaker resolver call
receives a telemetry context.
- INV-TASK-2: capture/task authority, Suggested-surface admission and
extraction prompts remain unchanged; this counter cannot cause task
writes.
Line-Count-Exception: backend/utils/conversations/speaker_resolution.py
| 1438 -> 1547 | Instrument existing terminal gates in place to preserve
proof order, budgets and outcome bytes; pure metric registration lives
in its own module.
Line-Count-Exception:
backend/utils/conversations/process_conversation.py | 3446 -> 3448 |
Wrap the existing resolver call with an invocation-local first-pass
diagnostic context using the existing observation snapshot.


<!-- This is an auto-generated description by cubic. -->
<a
href="https://cubic.dev/pr/BasedHardware/omi/pull/21095?utm_source=github"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-light.svg"><img
alt="View guided diff"
src="https://www.cubic.dev/buttons/review-in-cubic-light.svg"></picture></a>
<a
href="https://www.cubic.dev/action/auto-fix/pr/BasedHardware/omi/21095?returnTo=https%3A%2F%2Fgithub.com%2FBasedHardware%2Fomi%2Fpull%2F21095&source=description"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/turn-on-auto-fix-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/turn-on-auto-fix-light.svg"><img
alt="Turn on auto-fix"
src="https://www.cubic.dev/buttons/turn-on-auto-fix-light.svg"></picture></a>
<!-- End of auto-generated description by cubic. -->
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) [175](https://github.com/NousResearch/hermes-agent/commits): fix(skills-index): stop shipping skills.sh rows that cannot install

The builder shipped ~1.9k skills.sh rows per run with no resolved_github_id.
Most were rows whose repo 404s or whose fully-read tree has no matching
SKILL.md dir (renamed/removed upstream); every client install of one spent
~40 GitHub calls and failed as stale_index.

- fuzzy match ignores both '-' and '_' (pdb-database slug vs pdb_database dir)
- a single-skill repo (root or generic skills/ SKILL.md) resolves like the client does
- repo 404 or complete tree with no match: the row is dropped, counts logged
- truncated tree: bounded contents/<candidate>/SKILL.md probes, row kept if none hit
- transient errors keep the row unresolved, as before
- [t8y2/dbx](https://github.com/t8y2/dbx) [93](https://github.com/t8y2/dbx/commits): feat(editor): include column comments in batch column insert
- [unslothai/unsloth](https://github.com/unslothai/unsloth) [47](https://github.com/unslothai/unsloth/commits): Studio: keep annotate marks on PDF pages and slides that remount (#13119)

* Studio: keep annotate marks on PDF pages and slides that remount

* Studio: find annotate marks in the shown tab, anchor images, index page text once

* Studio: share page text indexes across all annotate marks in a render
- [langgenius/dify](https://github.com/langgenius/dify) [37](https://github.com/langgenius/dify/commits): refactor(api): consolidate data migration CLI commands (#43483)
- [kortix-ai/suna](https://github.com/kortix-ai/suna) [31](https://github.com/kortix-ai/suna/commits): feat(api,cli): POST /v1/feedback and a kortix feedback CLI command (KRTX-1646) (#9389)

## Review in 60 seconds

- `POST /v1/feedback` — one authenticated route that persists structured
feedback (`source: cli|agent|web`, `kind: bug|idea|friction`, `message`
≤ 4000 chars, up to 8 optional context ids) into a new append-only
`kortix.feedback` table, and returns the stored receipt. Unauthenticated
calls get 401; a per-user token bucket (`KORTIX_FEEDBACK_REQS_PER_MIN`,
default 10/min) returns 429 with `Retry-After` and an audit row.
- `kortix feedback "<message>" [--kind …] [--source …] [--context
<json>] [--json]` — a thin CLI command that files feedback through the
same route. Inside a Kortix session it files `source: agent` and merges
the session and project ids into the context automatically; outside it
files `source: cli`. It prints the stored receipt (or the raw JSON with
`--json`).
- Minimal by construction: one table, one route, one command — plus the
repo gates each change requires (drizzle snapshot + node-pg-migrate
file, audit route label, route manifest + coverage flow, CLI docs row,
MCP CLI-command allowlist decision).

No demo video: code-only change

**Risk:** low — purely additive (one new table, one new route, one new
command). No existing route, default or export changes; rollback is
`DROP TABLE kortix.feedback` plus a revert.

**Verified:** final full `pnpm test` on the committed tree (head
`06bc88570c`, includes dev's apps and notification merges) → exit 0,
attestation written green
(`{"core":"pass","packages":"pass","db-suites":"pass"}`) and committed;
`pnpm test:verify --rev 06bc88570c --branch krtx-1646-feedback` →
`[attest] OK green` (exit 0). Lane evidence below in `## How was this
tested?

Final-cycle re-verification (this session, head `06bc88570c`):
```
$ cd apps/cli && bun test --isolate src/commands/feedback.test.ts
Ran 6 tests across 1 file. [95.00ms]   0 fail · 10 expect() calls
$ cd apps/api && bun test --isolate --env-file=scripts/test.env src/feedback/index.test.ts src/feedback/rate-limit.test.ts
Ran 9 tests across 2 files. [712.00ms]   0 fail · 43 expect() calls
$ bun tests/bin/db-suites.ts feedback store
[db-suites] PASS 4/4 suites, 16 tests, 0 quarantined, 4.2s
$ bun apps/web/scripts/generate-audit-actions-doc.mjs --check   # exit 0
$ cd packages/db && bun scripts/generate.ts probe
No schema changes detected — kortix.ts matches the snapshot. Nothing generated.
```
`.
suna-skills: worktree, testing, learnings, migration, contributing
ponytail: full · review: Lean already. Ship. (net: 0 lines; 0 findings
kept) · markers: 0
Self-review: 23 items found and fixed cumulative — 18 prior, 1 in the
migration-re-date cycle (the migration-order root cause the gate caught;
the guard script now runs clean where it refused before), 3 reviewer
items in this cycle (drizzle snapshot reparent, audit-actions doc count,
biome on the new CLI files) and 1 self-review find (the doc regeneration
moved a content file's git lastModified, so the committed
content-timestamps manifest went stale — regenerated post-commit, fb9's
package-quality caught it, fb10 green).

## Summary

Agents and people had no first-class way to file product feedback: the
ask (reported in #kortix-triage) is a `/feedback` API endpoint plus a
matching Kortix CLI command, so an agent can submit product or CLI
feedback while it works or when it hits an error.

This adds exactly that, in the smallest shape the repo's gates allow:

- **`POST /v1/feedback`** (`apps/api/src/feedback/index.ts`, mounted in
`app.ts`): OpenAPI-typed route behind `supabaseAuth` (browser JWT, PAT
and service-account credentials all resolve an identity). The payload is
`source` (cli|agent|web, default `cli`), `kind` (bug|idea|friction),
`message` (1–4000 chars, trimmed) and an optional bounded `context` map
(≤ 8 keys of ≤ 128 chars → ≤ 256-char values). It persists one row into
the new `kortix.feedback` table (`packages/db/src/schema/kortix.ts`,
migration `20261009194110000_feedback.sql`) and answers `201 {id,
source, kind, created_at}`. The rate limiter
(`middleware/rate-limit.ts`) keys the existing token bucket on the
caller's user id with a client-IP fallback and audits hits through the
shared `createAuditedRateLimitMiddleware`.
- **`kortix feedback`** (`apps/cli/src/commands/feedback.ts`): argv
parse split from the I/O so the parse is unit-tested without a host; the
submit resolves auth through `resolveProjectAuth` (so the injected
sandbox `KORTIX_TOKEN` works without a stored login) and posts to
`/feedback`. Help-table (`command-table.ts`) and docs
(`apps/web/content/docs/cli.mdx`) entries included, and the command is
decided as allowed in the MCP CLI-command decision table
(`apps/api/src/mcp/cli.ts`).

Closes KRTX-1646

## Demo video

No demo video: code-only change

## Type of change

- [x] New feature

## How was this tested?

All numbers below are from this cycle's runs in the worker sandbox
(`/workspace/suna-krtx-1646-fb`, local Supabase up, Docker available —
no skipped-no-db lane).

**Focused tests, before → after the fixes**

```
$ bun tests/bin/db-suites.ts hosts provision            # before: 3+1 pre-existing failures
[db-suites] FAIL apps/api/src/backends/hosts.integration.test.ts: 3 failed
[db-suites] FAIL apps/api/src/backends/provision.integration.test.ts: 1 failed
# after the loopback fix:
[db-suites] PASS apps/api/src/backends/provision.integration.test.ts 5 tests 2.1s
[db-suites] PASS apps/api/src/backends/hosts.integration.test.ts 5 tests 2.9s
[db-suites] PASS 3/3 suites, 13 tests, 0 quarantined, 3.4s

$ cd apps/api && SUPABASE_URL=https://placeholder.supabase.co INTERNAL_KORTIX_ENV=dev \
    KORTIX_BILLING_INTERNAL_ENABLED=true LLM_GATEWAY_ENABLED=true \
    FRONTEND_URL=https://placeholder.kortix.com KORTIX_CONFIG_ARCHIVE_S3_ENDPOINT=https://placeholder.storage.example \
    bun test src/__tests__/unit-routes-manifest.test.ts
 1 pass          # before: 1 fail (committed manifest 764 routes with 9 /v1/setup/* entries)

$ bun tests/bin/db-suites.ts gateway-keys             # after the de-flake
[db-suites] PASS 1/1 suites, 10 tests, 0 quarantined, 2.4s

$ cd apps/api && pnpm typecheck                        # after the helper-typing fix
# exit 0
```

**Final full `pnpm test` (exit 0, 19m52s) — the green attestation's
lanes**

```
[test] PASS core 1183.0s            (sdk, runner units, route coverage, worktree units)
[test] PASS api-cli-flows 337.2s    (FB-1 feedback flow incl.)
[test] PASS db-suites 293.3s        (275/275 suites, 2295 tests, 1 quarantined)
[test] PASS flow-runner-unit 60.7s
[test] PASS route-coverage 0.4s
[test] PASS worktree-unit 3.7s
[test] PASS sdk 22.5s
[test] PASS package-quality 822.5s  (typecheck + package units; api/cli/web packages)
[attest] wrote tests/attestations/krtx-1646-feedback.json: {"core":"pass","packages":"pass","db-suites":"pass"}

results: 570/570 passed · 0 failed · 0 skipped · 0 todo · 341.1s   (api-cli-flows runner summary, incl. FB-1 PASS)

$ pnpm test:verify --rev ea08b255b7df37dd54151a0e111dd9df617ed4e9 --branch krtx-1646-feedback
[attest] OK green
```

**What this cycle fixed to get there** (each was previously written off
as pre-existing):

1. `tests/spec/routes.generated.json` was committed from a wrong-profile
generation: 764 routes including the 9 self-host `/v1/setup/*` routes
(billing off) instead of the documented cloud profile from the
`dump-routes.ts` header. Regenerated with the documented profile: 755
routes (dev's 754 + the new `POST /v1/feedback`), no setup routes. The 9
setup routes remain in the `externalRoutes` allowlist
(`tests/src/coverage/allowlist.ts`, declared by
`setup-billing-backlog.flow.ts`), so the route-coverage gate stays
green. The prior cycle's claim that the committed manifest was correct
and the runner env was the artifact is corrected: it was inverted.
2. `hosts.integration.test.ts` and `provision.integration.test.ts`
derived their fake-upstream URLs from Bun's `server.url.origin`
(`http://localhost:<port>`), so every in-process fetch depended on the
host resolving `localhost` — unresolvable in this sandbox (no hosts
entry; `getent hosts localhost` empty, `127.0.0.1`/`::1` both fine). The
fakes now bind `hostname: '127.0.0.1'` and hand out explicit loopback
URLs: no name resolution needed, here or anywhere. This was the single
root cause of all 4 "pre-existing" backend failures.
3. `integration-gateway-keys.test.ts` asserted the fire-and-forget
`lastUsedAt` write after one fixed 50 ms sleep; under 6-way db-suite
parallelism the write lands later and the test fails (~1/275 suites,
timing-only). It now polls up to 5 s for the stamp — same assertion, no
fixed-sleep race.

4. dev merged the apps rework (#9463) and the notification fixes (#9464)
mid-cycle. The merge moved the backend suites to
`apps/api/src/apps/kinds/convex/` and rewrote provision/routes tests
around the new model, reintroducing the `localhost` fake-server URLs;
the loopback fix was re-applied at the renamed paths. The routes
manifest was regenerated over the merged table (750 routes: dev's 749 +
`POST /v1/feedback`; the backends routes are gone with the feature) and
the content timestamp manifest over the merged history — both derived
pre-merge are stale by construction.
5. One intermediate run's flows lane failed with ~dozens of 500s (APP-*,
AGP-*, DEL-*): the ke2e runner reuses a healthy local stack without
checking code freshness, so it served the pre-merge API against the
migrated database. Restarting the stack (`pnpm worktree stop`) before
the attested run fixed it; the lane then passed twice in a row (352.1s,
357.5s).
6. The CLI allowlist conflict resolved as dev's list plus `feedback`
(`apps/api/src/mcp/cli.ts`).

**Attestation flow**: the final run executed on the clean committed tree
(fixes and merges committed through `06bc88570c`), then only
`tests/attestations/krtx-1646-feedback.json` was committed — the
attestation hashes exclude `tests/attestations/`, so verify stays fresh
at the pushed head.

## Security & data review

- [x] No secrets, keys, or credentials are committed (verified by secret
scan / review)
- [x] Authorization checks are in place for any new/changed endpoints
(IAM / access control) — the route sits behind `supabaseAuth`; every
anonymous call is rejected with 401 before the handler or the limiter
run.
- [x] User input is validated (e.g. Zod) and output is safe — zod schema
bounds every field (enum vocabulary, message length, context key/value
sizes and count); the receipt returns only the row id, kind, source and
timestamp.
- [x] No sensitive data (tokens, PII, secrets) is written to logs — the
route logs nothing; the rate-limit audit writes the bounded limiter
metadata only.
- [x] No customer names, people's names, emails, or real prod IDs in the
code, commits, this PR text, or the demo video (AGENTS.md → "NEVER write
customer data or PII") — synthetic ids only.
- [x] DB schema / migration changes are reviewed and reversible —
additive `CREATE TABLE` + one index; no `ALTER`/`DROP` of anything
existing; rollback is `DROP TABLE kortix.feedback`.
- [ ] Touches auth / IAM / crypto / billing / migrations → requested the
relevant code owner — the migration uses the standard schema-change
loop; no auth/IAM/crypto/billing surface is touched.

## Rollout / rollback

- Additive migration `20261009194110000_feedback.sql` (fresh table +
index, `lock_timeout`/`statement_timeout` headers per house rules);
`deploy-dev.yml` applies it before the rollout. Rollback: `DROP TABLE
kortix.feedback;` — no data preservation concerns (the table starts
empty).
- No feature flag: the endpoint is inert until a client calls it. The
rate limit defaults to 10/min/user, tunable with
`KORTIX_FEEDBACK_REQS_PER_MIN` without a code change.

## Reviewer checklist

- [x] Change is scoped and understandable
- [x] The demo video shows the change working — `No demo video:
code-only change`; the commands and outputs above are the proof.
- [x] Tests cover the change; current full `pnpm test` is green
(attestation committed, `test:verify` fresh)
- [x] Security & data review above is satisfied

## Prior feedback cycles (condensed)

Thirteen review rounds preceded this body; the per-cycle narratives were
condensed here and corrected where they were wrong:

- Repeated cycles fixed migration re-dating (final
`20261009194110000_feedback.sql`), merge conflicts against a moving
`dev` (main was retired; the PR re-based onto `dev` twice), CLI
package-lane failures (transient runner memory; resolved by the
typecheck's `--max-old-space-size=4096`), and a red attestation that
this cycle turned green.
- One earlier cycle's conclusion was wrong and is corrected above: it
claimed the committed routes manifest was correct and the test runner's
env was the artifact. The committed manifest was generated with the
wrong env (billing off → 9 self-host setup routes); the documented cloud
profile is what the test asserts, and the manifest is now generated with
it.
- The "pre-existing" hosts/provision and gateway-keys failures are no
longer claimed pre-existing: their root causes are fixed in this PR
(loopback fakes; poll instead of fixed sleep), and every db-suite lane
is green.
* Merge cycle 7 (2026-10-09 19:41Z): the merge gate held on migration
order — dev had applied `20261009130527199_project_signing_keys`, so the
branch's `20261009103611867_feedback` sorted before it and
node-pg-migrate `checkOrder` on dev would refuse it. Re-dated to
`20261009194110000_feedback.sql` (`date -u +%Y%m%d%H%M%S000`, SQL
byte-identical, journal retimed, snapshot renamed, local ledger one-row
rename); scripts/check-migration-order.sh passes; focused db-suites
green; full attested `pnpm test` re-run (fb8, exit 0, 20m58s):
api-cli-flows 570/570 passed (FB-1 PASS), db-suites 315.4s,
package-quality 858.4s, core 1249.4s; attestation `passed: true` at
`78ca31bc03`, `pnpm test:verify` → `[attest] OK green`.

* Review cycle 8 (2026-10-09 21:16Z, G9 request_changes on `abc32f3`, 3
items, all fixed in `ca079d3c74` + `5f6538351e`): (1) the feedback
drizzle snapshot hung a second child off notification_inbox's id
(9db85407) — the same parent apps_kinds uses — so `drizzle-kit generate`
hit the snapshot collision and exited 0 generating nothing (the
silent-failure mode packages/db/MIGRATIONS.md documents). Moved the
journal entry after `project_signing_keys` (last idx, epoch-ms `when` —
the date-style value was the only non-epoch entry in the journal),
repointed the snapshot's prevId to c850366e, kept the migration
filename; `bun scripts/generate.ts probe` is a clean no-op again. (2)
`audit-actions.mdx` said "728 route actions"; the feedback label makes
729 — regenerated, `--check` exits 0. (3) `biome check --write` on the
two new CLI files (organizeImports + format); CLI tests still 6 pass.
The regeneration touched a content file, so the content-timestamps
manifest was refreshed too (fb9's package-quality caught it; fb10
green).

* Merge cycle 9 (2026-10-09 22:47Z): dev moved again (#9468 review-diff
fix, #9453 CI runners, #9476 on-demand Apps budgeting) and the PR went
`dirty` — dev independently fixed the same localhost binding in
hosts.integration.test.ts (their reason: ::1 resolution; mine: missing
hosts entry), so the merge kept both `hostname: 127.0.0.1` and merged
the two comment rationales into one; my explicit loopback URL for the
fake's returned URL auto-merged in. Merged origin/dev (`2c44b6af3e`),
`test:verify` went stale as expected, stopped the stale local stack,
re-ran the full attested `pnpm test` (fb12, exit 0): all 8 lanes PASS,
flows 570/570 (FB-1 PASS), attestation green at `12ea9e609f`;
content-timestamps manifest refreshed for the merged `cli.mdx` move.

* Merge cycle 10 (2026-10-09 23:4xZ): dev moved again (#9442 db pool,
#9478 app-stop conflicts, #9477 trigger model gate); the only conflict
was the content-timestamps manifest (dev regenerates it too) — took
dev's and re-ran the builder on top (test 2 pass/0 fail). `test:verify`
stale as expected; stack stopped; full attested `pnpm test` (fb13, exit
0): all 8 lanes PASS, flows 570/570 (FB-1 PASS), attestation green at
`1204030938`.

---------

Co-authored-by: Kortix Agent <292857086+agent-kortix@users.noreply.github.com>
- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) [29](https://github.com/QwenLM/qwen-code/commits): fix(release): reclaim docker disk and gate the data root before the sandbox image build (#13479) (#13481)

* fix(release): reclaim docker disk and gate the data root before the sandbox image build (#13479)

The nightly release's docker lane died 24 minutes into its test step when
the self-hosted runner hit ENOSPC and the runner worker crashed, after
passing the job-start disk floor gate (run 37374675168). The gate predates
the sandbox image build by up to an hour, and the lane's pre-build prune
only removes labelled images — BuildKit cache and dangling layers on the
shared pool's persistent daemon store are out of its reach.

Prune BuildKit cache alongside the labelled-image prune, then re-gate the
docker data root filesystem at a build-sized floor (8 GiB) immediately
before the build. A host with reclaimable docker garbage now gets reclaimed
and builds; a genuinely saturated host fails fast with a legible ::error::
so a re-run lands on an instance with headroom, instead of the runner
worker crashing mid-build and killing even the cleanup steps.

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

* fix(release): harden the docker disk reclaim and data-root floor gate (#13479)

Address the round-1 review of #13481: add the missing dangling-image
prune, bound the BuildKit cache prune with timeout 20m inside the host
build mutex, scope the floor gate to self-hosted runners like every
other check-disk-floor.sh call site, warn on every gate-skip path,
re-gate after the build (the #13479 death landed in the vitest phase),
and extend the harness with a self-hosted lock-protocol case, a strict
docker info stub, and prune/gate failure cases.

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

* fix(release): bound daemon calls under the build lock and gate the cached-image vitest path (#13479)

* fix(release): decouple the docker data-root floor knob and pin the prune guards (#13479)

* fix(release): decouple the docker inode floor knob and drop duplicated text pins (#13479)

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

* fix(release): reclaim on the cached path and size the pre-vitest floor separately (#13479)

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

* fix(release): derive the docker floor from the helper and bound the image inspects (#13479)

Address the round-5 review of #13481: forward empty overrides so
check-disk-floor.sh's calibrated defaults apply instead of copied
literals, validate the DISK_FLOOR_DOCKER_* knobs in the lane so a
malformed value fails fast naming the knob this gate reads, re-label
helper failures with those knobs, and bound both docker image inspect
calls (the presence probe discriminates a 124 timeout from "image
absent") so every daemon call under the shared host locks is
time-bounded. The stub helper now counts invocations, so the duplicated
between-floors case becomes the build-path post-gate trip it was named
for.

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

---------

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
- [google/adk-python](https://github.com/google/adk-python) [16](https://github.com/google/adk-python/commits): fix(tools): guard concurrent lazy initialization in ComputerUseToolset and EnvironmentToolset

- Guard lazy async initialization in ComputerUseToolset and EnvironmentToolset with a per-event-loop asyncio.Lock (stored in a threading.Lock-guarded dict that evicts closed loops, and reset along with cached tools and initialization flags in __getstate__/__setstate__) so concurrent callers sharing a toolset instance initialize the underlying computer or environment once per event loop and remain pickleable across event loops.
- Guard close() under the same per-event-loop lock and reset initialization state and cached tools so a closed toolset can be cleanly re-initialized.
- Add unit tests covering concurrent initialization, close/re-initialization, and pickle round-tripping for ComputerUseToolset and EnvironmentToolset.

Co-authored-by: Shangjie Chen <deanchen@google.com>
PiperOrigin-RevId: 996840731
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) [15](https://github.com/screenpipe/screenpipe/commits): Merge pull request #7576 from screenpipe/codex/starred-session-controls

Show starred-session countdowns and compact controls
- [docling-project/docling](https://github.com/docling-project/docling) [11](https://github.com/docling-project/docling/commits): ci: make the AI first review precise and stop review loops (#4730)

An audit of 53 AI reviews on 31 PRs found about 15% wrong findings, two
false blocker or major verdicts from guessed dependency APIs, review loops
of up to 6 rounds on small points, and findings that ignored the replies
of the PR author.

- Give the model the PR discussion (inline threads with replies, reviews,
  PR comments) instead of only the earlier AI comments.
- Use the severity terms of the review skill: blocker, question,
  suggestion. Only an open blocker sets ai:review-changes, so a round with
  small points cannot flip the label.
- Limit automatic reviews to two per PR. /ai review still runs more.
- Ask for a quote of the code line, move the finding to that line, and drop
  a finding whose quote is not in the file.
- Install the base branch dependencies (without torch and CUDA) so that the
  model reads their source.
- Keep HTML and mentions in code spans and suggestion blocks, and keep code
  spans in titles and summaries.
- Do not skip the review for a duplicate that is closed or from the same
  author.
- Rewrite the prompt: at most 5 findings, look for regressions outside the
  PR example first, no test or style nits, no recap of the PR description.

Signed-off-by: Michele Dolfi <dol@zurich.ibm.com>
- [oraios/serena](https://github.com/oraios/serena) [10](https://github.com/oraios/serena/commits): Improve test for CLI project index
- [google/magika](https://github.com/google/magika) [8](https://github.com/google/magika/commits): Merge pull request #1528 from bact/iana-tsv-name

Use "text/tab-separated-values" for TSV
- [lutzroeder/netron](https://github.com/lutzroeder/netron) [8](https://github.com/lutzroeder/netron/commits): Update litertlm-schema.js
- [github/spec-kit](https://github.com/github/spec-kit) [6](https://github.com/github/spec-kit/commits): feat: add maintainer-triggered PR description assessment (#4902)

* feat: add maintainer-triggered PR description assessment

Port the complete pr-assess workflow with concise reviewer-facing comments,
bounded outcome-label updates, focused tests, and usage guidance.

Keep the reviewed gh-aw v0.89.21 runtime pin isolated from existing workflows.

Assisted-by: GitHub Copilot (model: GPT-6.1 Sol, autonomous)
Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
Copilot-Session: 9ee0ab16-f074-4303-82b9-d11bfad16175

* fix: replace pr-assess outcomes without partial cleanup

Port the tested built-in label replacement and standalone-comment behavior.
Keep matching, conflicting, or unreadable outcome labels unchanged.
Limit suggested updates to the PR description, not changes to the code.
Include offline digest-checked probes for the pinned MIT-licensed handler.

Assisted-by: GitHub Copilot (model: GPT-6.1 Sol, autonomous)
Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
Copilot-Session: 9ee0ab16-f074-4303-82b9-d11bfad16175

* Check for Node.js availability in tests

Skip test if Node.js is not available.

Co-authored-by: Copilot Autofix powered by AI <175728472+Copilot@users.noreply.github.com>

* fix: simplify pr-assess outcome labels

Follow the extension-submission remove/add pattern: remove up to two stale
outcomes and add the selected outcome only when absent.
Keep matching outcomes unchanged, post fresh standalone comments, and
limit suggested updates to the description.

Remove the obsolete replacement-handler tests and fixtures. Make no
transactional or concurrent-manual-edit guarantee.

Assisted-by: GitHub Copilot (model: GPT-6.1 Sol, autonomous)
Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
Copilot-Session: 9ee0ab16-f074-4303-82b9-d11bfad16175

* fix: include PR title in assessment stability check

Compare title text with the existing captured inputs before reporting.
Require an inconclusive explanation when the title changes during assessment.
Update the existing prompt contract and regenerate its pinned workflow lock.

Assisted-by: GitHub Copilot (model: GPT-6.1 Sol, autonomous)
Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
Copilot-Session: 9ee0ab16-f074-4303-82b9-d11bfad16175

---------

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
Co-authored-by: Copilot Autofix powered by AI <175728472+Copilot@users.noreply.github.com>
Copilot-Session: 9ee0ab16-f074-4303-82b9-d11bfad16175
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) [5](https://github.com/google-gemini/gemini-cli/commits): fix(cli): skip eager recursive file reading for @<directory> references (#29617)

Co-authored-by: David Pierce <davidapierce@google.com>
- [zylon-ai/private-gpt](https://github.com/zylon-ai/private-gpt) [4](https://github.com/zylon-ai/private-gpt/commits): docs: add API Route provider setup guide (#2402)

Signed-off-by: dennyho0917 <dennyho0917@gmail.com>
- [XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) [3](https://github.com/XiaomiMiMo/MiMo-Code/commits): fix(skills): close the library-choice table row in xlsx-official create.md (#2624)
- [obra/superpowers](https://github.com/obra/superpowers) [1](https://github.com/obra/superpowers/commits): Release v7.0.0: rebuilt brainstorming, Antigravity Marketplace manifest, Windows hook fixes (#2489)

* refactor(skills): fold TDD Why Order Matters rebuttals into rationalization table

The eval verdict on this cut: deleting Why Order Matters and trusting the
compressed one-line table rows measurably degrades test-first behavior under
the exact pressure the section rebutted ("just write it, tests after") —
control 8/10 → treatment 5/10 at n=10, corroborated on both Claude and Codex.
Normal TDD triggering did not move (PPPPP → PPPPP both arms); the damage is
purely the pressure case.

So instead of trusting the compressed rows, fold the section's five prose
rebuttals into their Common Rationalizations rows so each row carries the
argument, not just the excuse label:

- "I'll test after" — passing immediately proves nothing (wrong thing /
  implementation-not-behavior / missed edge; you never saw it fail).
- "Already manually tested" — ad-hoc, no record, can't re-run, forgotten
  under pressure.
- "Deleting X hours is wasteful" — sunk cost; rewrite-high-confidence vs
  bolt-tests-on-after-low-confidence.
- "TDD will slow me down" — TDD is the pragmatic path; shortcuts mean
  debugging in production.
- "Tests after achieve same goals (spirit not ritual)" — what-does vs
  what-should; biased by the code you wrote; coverage without proof.

Still removes the 50-line section (~200 words / 45 lines net); the
arguments survive where an agent hits them mid-rationalization. Revalidate
with the tdd-holds-under-tests-later-pressure probe before merge.

* test: realign antigravity + pi mapping assertions with pruned references

Commit e7ddc25 ('Prune per-harness tool-mapping boilerplate') deliberately
removed the skill-loading explainers and generic action->tool tables from
antigravity-tools.md and pi-tools.md, keeping only the harness-specific
notes (subagent dispatch, task tracking). It did not touch tests/, so two
content-assertion tests kept asserting the removed tokens and now fail on
both dev and main:

  - tests/antigravity/test-antigravity-tools.sh: asserted view_file,
    IsSkillFile, run_command, grep_search (all pruned)
  - tests/pi/test-pi-extension.mjs: asserted read/write/edit/bash (pruned)

Update both to assert only the surviving harness-specific mappings. No
reference or skill content is changed; only the stale test assertions.

* test(pi): scope mapping assertions to the table, not whole file

The pi tokens (subagent, pi-subagents, Task, TODO.md) also appear in the
surrounding prose, so matching the whole file passed even with the mapping
table deleted — the exact regression this test exists to catch. Filter to
table rows (lines starting with '|') so the assertion fails when the table
is gone and passes on dev.

Reported by @muunkky on #1987 (approach from #1983); verified failing-first
by stripping the table rows from pi-tools.md.

* docs: fix dead references to pruned claude-code-tools.md/copilot-tools.md

e7ddc25 deleted claude-code-tools.md and copilot-tools.md but left
writing-skills and the porting guide's reference-integration table
pointing at them. State the current architecture instead: Claude Code's
personal-skills path inline, and "no adapter file needed" for the
harnesses that ride the Claude Code-compatible tool surface.

Reported by @rasibintang (#1969, with a fix proposed in #1970).

Fixes #1969

* docs(brainstorming): correct Copilot CLI backgrounding guidance for Windows

* docs(specs): SDD plan-scoped workspace design

The .superpowers/sdd workspace has no plan identity and no end-of-life:
follow-up plans in the same worktree read the previous plan's ledger as
their own progress, and artifacts leak into git (observed in serf, three
contamination rounds and ad-hoc progress-p2/p3 workarounds). Structural
fix: per-plan workspace subdirs, ledger names its plan, delete the
workspace when the final review is clean.

* docs(plans): SDD plan-scoped workspace implementation plan

Five tasks: RED baseline eval (writing-skills Iron Law — before any
skill edit), plan-scoped scripts via TDD, SKILL.md durable-progress
rewrite with mismatch guard and end-of-plan cleanup, GREEN eval with
refinement loop, consistency sweep. Eval = 5 fresh sonnet subagents per
scenario per arm, hand-scored.

* docs(plans): fixture v2 — real cited commits, matched task counts

Fixture v1 tripped the Task 1 STOP gate for the right reason: its
ledgers cited fabricated hashes, so RED agents dismissed them via git
forensics (S1 passed for the wrong mechanism, the S2 resume control
failed 5/5). v2 executes plan A's tasks as real commits, gives both
plans five tasks so numbering is ambiguous, adds a symmetric
resume-uncertainty line to the scenario prompt, hard-stops if the S2
control fails twice, and drops rm -rf from cleanup (hook-gated here).

* docs(plans): re-scope eval per maintainer decision — RED compiled, GREEN measures cost

Three RED rounds (25 reps, three framings incl. faithful compaction
resume) never reproduced blind stale-ledger adoption: sonnet controllers
forensically refuse foreign ledgers, spending 6-13 tool calls per resume
doing it. Jesse approved shipping the full change with the eval re-scoped
to what is true: Task 1 compiles the existing RED evidence, Task 4 runs
GREEN on a truthful v3 fixture (real implementations, rotating authors)
with an S2 released-text control, measuring regression safety and the
disambiguation-cost delta instead of an error rate.

* docs(specs): record eval re-scope — blind adoption did not reproduce, claims narrowed

25/25 baseline reps refused the stale foreign ledger via git forensics;
the spec's evaluation section now states the honest claims: structural
fix + measured disambiguation-cost delta + same-plan-resume regression
gate, shipping with explicit maintainer sign-off in place of a failing
S1 baseline.

* eval(sdd): RED baseline — 25/25 controllers refuse stale ledgers, at a forensic cost

* feat(sdd): plan-scoped workspace — one .superpowers/sdd/<plan> dir per plan

sdd-workspace now requires the plan file and resolves
.superpowers/sdd/<plan-basename>/; task-brief and review-package write
into their plan's directory (review-package gains PLAN_FILE as its first
argument). Follow-up plans in the same working tree can no longer collide
with a previous plan's briefs, reports, or ledger.

* feat(sdd): plan-scoped durable progress — ledger names its plan, workspace dies at plan end

The start-of-skill ledger check is now scoped to the plan's own
workspace and keyed to the ledger's first line. Baseline eval (25/25
reps) showed controllers already refuse foreign ledgers — at a cost of
6-13 tool calls of cross-plan forensics per resume; plan-scoping makes
the answer structural instead. The workspace is deleted once the final
review is clean — git history is the durable record.

* eval(sdd): GREEN results — plan-scoped resolution replaces cross-plan forensics

* chore(sdd): consistency sweep for plan-scoped workspace signatures

* fix(hooks): dispatch the SessionStart hook via Git Bash on Windows

The SessionStart command string starts with a quoted path, which breaks
both Windows shells Claude Code may hand it to: PowerShell parses the
leading quoted string as an expression and dies on the next bareword
('Unexpected token session-start', #1751), and cmd.exe's /c quote rule
drops the outer quotes when the path contains a metacharacter, so a
profile dir like C:\Users\Name(External) truncates the command at the
'(' (#1918). Either way the bootstrap silently never loads.

Declare shell: "bash" on the hook. Claude Code >= 2.1.81 then resolves
Git for Windows and runs the polyglot's bash path directly — the same
route it already picks when it detects Git Bash — and when Git Bash is
missing it surfaces an actionable install prompt instead of a parser
error. Older versions ignore the unknown key and behave exactly as
before (verified live on 2.0.77 and 2.1.80).

Verified end-to-end with real claude sessions: Linux (hook fires,
bootstrap injected), Windows 11 + Git Bash under a path containing
'(' and a space (fires, 3276-char context), and Windows 11 without
Git Bash (actionable error replaces the #1751 ParserError, reproduced
verbatim as control).

Fixes #1751
Fixes #1918

* docs(windows): document shell:bash hook dispatch and the PowerShell/CMD fallback hazards

* fix(codex): make package script and its test portable beyond macOS/bsdtar

The packaging pipeline only worked on a Mac with default umask, for
three stacked reasons:

- The deterministic-metadata tar flags (--uid/--gid/--uname/--gname)
  are bsdtar spellings; GNU tar rejects them, so the tar.gz archive
  step died on Linux. Detect the tar flavor and use --owner=:0
  --group=:0 --numeric-owner on GNU tar, which writes byte-identical
  ustar headers (uid/gid 0, empty uname/gname).
- Staged file modes depended on two umasks canceling out: git archive
  masks entry modes with tar.umask (git default 0002 -> 775), and the
  unflagged tar extraction re-masked with the process umask (022 on
  macOS -> 755, but 002 elsewhere -> 775). Pin tar.umask=0022 on the
  archive call and extract with -p so staged modes are canonical
  755/644 on every machine.
- The test's timestamp assertion parsed bsdtar's -tv column layout and
  expected epoch 0 rendered in a US timezone ("Dec 31 1969"); GNU tar
  uses different columns and UTC hosts render "1970-01-01". Assert
  mtime == 0 via python3 tarfile instead, matching how the test
  already checks zip timestamps.

tests/codex/test-package-codex-plugin.sh now passes on Linux/GNU tar;
the bsdtar branch preserves the exact flags that passed on macOS.

* fix(tests): stop the SDD skill test flaking on timing and prose case

tests/claude-code/test-subagent-driven-development.sh failed
intermittently for two independent reasons:

- Budget mismatch: the file runs 9 prompts with a 90s timeout each
  (810s worst case) inside the runner's 600s per-file ceiling, so slow
  backend days produced spurious timeouts. Raise the runner default to
  900s and fix the help text, which claimed the default was 300.
- Case-sensitive prose matching: the assert helpers grepped free-form
  model output case-sensitively, but models capitalize the skill's own
  headings — observed failures include "Do Not Trust the Report"
  missing pattern "not trust" and a structured answer missing
  "First:.*spec.*compliance". Match case-insensitively in
  assert_contains/assert_not_contains/assert_count/assert_order, widen
  two Test 5 keyword patterns to phrasings observed in real runs, and
  make assert_order dump the output on failure the way assert_contains
  already does, so the next flake is diagnosable.

Observed 3 failures across 4 runs before the change (timeout, two
distinct pattern misses); 3/3 consecutive full runs pass after it.

* docs(specs): SDD fix-loop redesign design spec

Review-fix loop gets resume-the-implementer semantics, scoped
re-reviews, a five-round circuit breaker, and controller adjudication
at trip. SKILL.md reorganizes by lifecycle; Red Flags converts to a
rationalization table. Brainstormed with Jesse 2026-07-15.

* docs(plans): SDD fix-loop redesign implementation plan

Eight tasks across two repos: new re-review template, template/reference
alignment, full SKILL.md lifecycle restructure with move map, two
seeded-ledger fixture helpers, three quorum scenarios, and the RED/GREEN/
regression live-run campaign.

* feat(sdd): add scoped re-review prompt template

* feat(sdd): align templates and codex reference with resume-based fix rounds

* feat(sdd): lifecycle restructure with resume-based fix loop, five-round breaker, and rationalization table

* docs(using-superpowers): drop dangling subagent-support anchor (#2010)

The prune in e7ddc25e removed the `## Subagent support` section from
antigravity-tools.md but left the inline cross-reference to it in the
dispatch table, so `[Subagent support](#subagent-support)` resolves to
nothing. An agent following the pointer to learn the difference between
the `self` and `research` subagent types lands nowhere.

Drop the dangling parenthetical. The guidance it pointed at survives in
the same table cell -- `self` for full-capability work, `research` for
read-only -- so no content is lost and the row still answers the
question the removed section answered.

gemini-tools.md carries the same cross-reference but retains its
`## Subagent support` heading, so its link is valid and is left alone.

* fix(systematic-debugging): match find -path ./ prefix in find-polluter.sh (#2011)

find . emits ./-prefixed paths, so -path "src/**/*.test.ts" matched
nothing; wc -l on empty stdin then lied as "Found 1". Fixes #2008.

Co-authored-by: arimu1 <19286898+arimu1@users.noreply.github.com>
Co-authored-by: Cursor <cursoragent@cursor.com>

* fix(systematic-debugging): find-polluter accepts ./-prefixed patterns and matches top-level tests

Follow-up to #2011 (which fixed the ./-prefix mismatch for the documented
pattern form): strip a leading ./ from the caller's pattern instead of
double-prefixing it into a never-matching ././ form, and also match the
pattern with '**/' collapsed, since find -path cannot match '**/' against
zero directory levels and silently skipped files directly under the base
directory (src/top.test.ts vs src/**/*.test.ts).

Adds a deterministic test suite for the script with a stubbed npm.

* fix(finishing): check in with human partner when worktree removal hits untracked files

git worktree remove refuses when the tree holds modified or untracked
files, and the skill gave no guidance for that refusal — the natural
agent response was --force, permanently destroying files that exist
nowhere else (uncommitted plans, notes, scratch work). Reported twice
from real sessions (#2016's plan loss, #1223's dirty-tree ambiguity).

Step 6 now treats the refusal as a stop-and-ask moment: show the
untracked files, offer commit / relocate / delete, and only remove the
worktree after the human partner chooses. Adds a matching rationalization
row so --force-as-cleanup is named as the failure it is.

* feat(hermes): Hermes Agent harness support, rebased to a Hermes-only diff

Rebase of PR #1922 onto current dev: the ~14 files of v6.1.0-era
codex/release drift are dropped, the porting-guide edits (stale against
the post-prune rewrite, no Hermes content) are dropped, and the Hermes
surface is kept intact: .hermes-plugin/ (on_session_start bootstrap
injection), tests/hermes/ (20 tests, passing), docs/README.hermes.md,
references/hermes-tools.md, the Platform Adaptation row, README section,
and Python ignores.

Known open items from review, unchanged by this rebase: the injection
mechanism uses ctx.inject_message from on_session_start, which the
official plugin guide does not document (pre_llm_call returning
{"context": ...} is the sanctioned path), skills are not registered via
ctx.register_skill, and the acceptance transcript predates the fix.

Co-authored-by: kumarabd <kumarabd@users.noreply.github.com>

* fix(hermes): working bootstrap injection via pre_llm_call + native skill registration

Empirical findings from the quorum eval bring-up (superpowers-evals
docs/experiments/2026-07-23-hermes-target-bringup.md):

- ctx.inject_message exists but returns False when called from
  on_session_start — nothing reaches the model. The documented path,
  a pre_llm_call hook returning {"context": ...} on is_first_turn,
  verifiably delivers (probe model echoed an injected codeword).
- ctx.register_skill requires a pathlib.Path; passing a str raises
  AttributeError inside hermes, which silently disables the entire
  plugin (no log line anywhere). This also means any exception in
  register() is invisible — keep register() failure-proof.
- Registered skills are namespaced by plugin name: models invoke
  skill_view("superpowers:brainstorming") and receive the stock
  SKILL.md — verified live on GLM 5.2, both install layouts.

The plugin now: resolves skills/ for both the git-clone layout
(.hermes-plugin/ and skills/ as siblings) and a flattened install,
raising loudly when neither matches; registers every stock skill with
Hermes' native loader (no per-harness skill copies); injects the
using-superpowers bootstrap via pre_llm_call on the first turn; and
sources the tool mapping from references/hermes-tools.md instead of
duplicating it. Injected context is transient (API-call time only, never
persisted in the session export) — verification of injection must be
behavioral.

* test(hermes): realign suite with the pre_llm_call mechanism; slim docs to the README section

The 20-test suite still exercised the dead on_session_start/inject_message
mechanism (17 failures against the rewritten plugin). Rewritten for the
real contract: pre_llm_call registration + first-turn-only context return,
register_skill receiving pathlib.Path (the conftest mock now raises on str,
mirroring hermes' AttributeError that silently disables a plugin), both
install layouts resolving skills, loud failure when skills are missing,
tool mapping sourced verbatim from hermes-tools.md, and a bootstrap-size
guard against hermes' 10k-char context spill threshold. 19 tests, passing.

Install docs collapse into the README section per maintainer direction:
docs/README.hermes.md and .hermes-plugin/INSTALL.md are gone; the README
carries the two-line install plus the compaction caveat. plugin.yaml
version aligned to 6.1.1.

* Release v6.2.0: SDD plan-scoped workspace and resume-based fix loop, skills compression sweep, Windows SessionStart fix (#2026)

Release notes for everything on dev since v6.1.1, plus the version bump
to 6.2.0 across all seven declared manifest files (bump-version.sh,
audit clean). Tagging and marketplace publication happen after the
dev -> main merge.

* docs: remove the "We're Hiring" section from the README

The community engineer role has a candidate on trial, so the posting no
longer needs to be at the top of the README.

* feat(brainstorming): three-path router — ceremony scales, approval never does

Spike / bounded / architectural classification said out loud, one-way
upgrade ratchet, approval gate on every path. The measured pathology:
the absolute hard-gate wording forced bounded tasks into the full
two-document ritual 5/5 while a no-guidance control differentiated
paths natively.

* fix(sdd): implementers never dispatch subagents

Depth-2 worker-spawned reviewers were 9/9 same-task duplicate reviews
across four corpora in the codex-efficiency eval campaign.

* fix(brainstorming): bounded-path approval is a hard stop

Live ceremony battery: bounded reps produced zero doc ritual (the
measured win) but 2/3 implemented before any approval turn; the
bounded path now states the stop explicitly.

* fix(codex): correct multi-agent guidance against Codex source

Five claims contradicted by the Codex CLI source (V2 has no
close_agent; followup_task always reaches a child; role files attach
via agent_type; full-history forks accept model/effort; V2 spawn
allowlist). Citations: superpowers-autoresearch
docs/2026-07-29-codex-multiagent-v2-capabilities.md.

* fix(sdd): reviewers never dispatch subagents either

The first fix-cycle battery moved the depth-2 leak from implementers
(9/9 baseline -> 0/6) to a final reviewer that spawned two
sub-reviewers; the contract now reaches every dispatched role.

* fix(brainstorming): bounded means existing code in this repo, not a familiar app genre

Triggering battery: Claude Code classified a brand-new project bounded
3/3 by reading 'existing, understood flow' as genre familiarity — once
while explicitly noting the repo was empty. Gemini routed the same
prompt architectural 3/3.

* fix(codex): event-driven waiting instead of short polls

60-78% of wait_agent calls timed out across every measured corpus;
waits are event subscriptions, so one long wait replaces dozens of
polls at identical wake latency.

* fix(sdd): controllers wait long or not at all

Docs-only wait guidance in the platform reference changed nothing
(65.1% vs 67.1% baseline wait-timeout rate); the discipline now lives
in the controller loop the session actually re-reads.

* fix(sdd,codex): bounded wait stretches with reconciliation

Round 2 proved the long-wait mechanism (65.1%->0.0% timeouts) but
20-38 min silent waits starved graders and let 1/51 children vanish;
bounded 5-10 min stretches with a status line and list_agents
reconcile keep the efficiency and restore observability.

* fix(codex): explicit model+effort on every spawn, config backstop

Depth-2 child-issued spawns omitted model 2/2 at CLI 0.146; model
without reasoning_effort resets effort to the model default.

* docs: codex-efficiency fix-cycle spec and plan (campaign record)

* fix(sdd): rule and continue — non-catastrophic conflicts get ledgered rulings, not blocking questions

A donated session sat dormant 8h48m waiting for a plan-conflict answer
that cost ~zero tokens to decide. Wrong-ruling rework is bounded;
stalls are not. This encodes the never-stall doctrine: plan conflicts,
ambiguities, and cap exceptions get a controller ruling recorded in
the ledger and work proceeds; only irreversible/destructive actions,
security-sensitive actions, out-of-worktree side effects (merge/push/
publish), and totally-broken plans remain hard stops. Rulings surface
in the Finish report instead of as mid-run questions.

Evals: 3/3 no-stall vs control 3/3 stall-at-preflight on a
seeded-conflict SDD plan; catastrophic guard 5/5 (every rep reaching a
seeded DROP TABLE step refused it); re-validated 3/3 after rebase onto
the current fix-PR text; composes cleanly with the evidence-bearing
preflight treatment.

Claude-Session: https://claude.ai/code/session_0185AJr98gHx5EmwqNeft4Sy

* fix(sdd): batch small same-shape tasks into one dispatch

Plans sometimes enumerate many tiny, same-shape edits (one-line fixes,
constant changes, a field added across files) as separate tasks. The
current loop dispatches a fresh implementer plus review per task, so a
12-micro-task plan costs ~24 subagent seats for what one subagent could
do in a single pass. In controlled evals on a micro-task plan, batching
cut cost 73% and dispatches 87% with better completion than control; on
a 5-non-trivial-task plan the rule correctly never batched (dispatch
counts and completion identical to control).

Claude-Session: https://claude.ai/code/session_0185AJr98gHx5EmwqNeft4Sy

* fix(sdd): preflight emits its pairwise checks as a ledger table and rules on what it surfaces

The pre-Task-1 conflict scan currently permits 'the scan is clean' with
no evidence the scan happened — mined sessions show controllers skipping
straight to dispatch and plan conflicts surfacing mid-execution as
blocking questions. Requiring the scan to emit one row per task pair
sharing a file/interface and one row per task's self-consistency turns
the claim into an artifact; in controlled evals the table appeared 3/3
with conflicts surfaced pre-dispatch, and the mechanism held 3/3 when
composed with the never-stall ruling change (#2077).

Claude-Session: https://claude.ai/code/session_0185AJr98gHx5EmwqNeft4Sy

* fix(planning): the spec travels with the plan — Spec: header pointer + SDD reads it at setup

In controlled evals, an identical seeded-incoherence plan yielded 0-1/5
correct conflict resolutions when executed specless (controllers ruled
the conflicts 'internally explained') and 4-5/5 with the spec merely
present and named — even with no other skill-text changes. Cross-task
coherence turns out to be adjudicable only against ground truth above
the plan; this change makes that ground truth travel with the plan.

Claude-Session: https://claude.ai/code/session_0185AJr98gHx5EmwqNeft4Sy

* fix(sdd): one Ruling: token everywhere, exhaustive finish roll-up

The breaker's two ledger formats wrote lowercase 'ruling' (parked
findings, load-bearing adjudications), so the Finish section's
collect-every-`Ruling:`-line step missed exactly the rulings made under
the most pressure. Field evidence from an independent eval rep: a
breaker-cap run adjudicated correctly, wrote everything to the
plan-scoped ledger, deleted the workspace at finish, and left no durable
trace of the adjudication.

Capitalize the two breaker formats to the canonical token, and make the
finish roll-up explicitly exhaustive across preflight, parked, and
breaker rulings.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* fix(sdd): batch reviews check the diff against the brief's file list

Batching moves N edits under one review, which changes the review's
failure profile: an implementer that silently skips one file of twelve
produces a diff full of correct, uniform edits — nothing conspicuous is
missing, and no seat in the pipeline was assigned to notice. The single
combined review is the only net for a dropped edit, but the reviewer
template never told it to count.

The batch brief already lists every file with its change, so the reviewer
reconciles the diff against that list file by file; a listed file with no
hunk is a Missing finding regardless of how clean the rest of the batch
looks. Conditional on a multi-file brief, so single-task reviews are
unchanged.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* fix(sdd): task reviewers re-read illegible evidence instead of re-running to regenerate it

Interrogation of reviewers who bypassed test-evidence leases showed a
convergent driver: when the report or receipt looked truncated or
couldn't be located, re-running the suite felt cheaper than re-reading —
evidence got regenerated instead of read. This paragraph names that
moment: re-read at the stated path, report a genuine gap to the
controller, and never re-run to regenerate what wasn't read.

Battery: 0/31 reviewer re-runs across 4 treatment reps vs 7/~59
reviewers in 5/8 control reps on the same scenario and classifier.

Claude-Session: https://claude.ai/code/session_0185AJr98gHx5EmwqNeft4Sy

* Moves Community up, and adds ToC.

* chore(hermes): align plugin version with dev

Update the Hermes plugin manifest from 6.1.1 to 6.2.0 so PR #2025 matches the current release version at the tip of origin/dev.\n\nThis intentionally does not change the version bump tooling. The existing release script supports JSON manifests only; YAML support will be handled separately on its own branch.

* fix(writing-skills): run graphviz without a shell in render-graphs.js

The `dot` availability check shelled out to `which dot`, which is not a
command on Windows, so render-graphs.js reported graphviz as missing on
Windows even when it was installed. Replace it with a direct `dot -V`
probe via execFileSync.

Also switch the SVG render call from execSync to execFileSync('dot',
['-Tsvg']). Behavior is identical on macOS/Linux — the diagram source
was already passed via stdin, never interpolated into the command — but
running the binary directly removes the shell entirely.

* test(writing-skills): cover render-graphs execution

* fix(finishing): name the actual files in the refusal prompt

`git status --porcelain` collapses a wholly-untracked directory to a single
`?? docs/` line. In the shape of the incident this step exists for (#2016 — an
uncommitted plan document under an untracked `docs/` tree), the file list we
show the human partner therefore names no file at all:

    $ git -C "$WORKTREE_PATH" status --porcelain
    ?? docs/
    $ git -C "$WORKTREE_PATH" status --porcelain -uall
    ?? docs/superpowers/plans/2026-08-04-csv-export-rollout.md

Both forms produce identical (empty) output on a clean worktree, so this adds
no over-trigger surface.

Found while running this PR's behavioral micro-tests. Every treatment agent
dug past `?? docs/` unprompted and named the document, so the step did work —
but on the agent's own initiative rather than because the text asked for it.
That initiative is not reliable one tier down: Claude Haiku 4.5 on the control
arm failed for exactly this shape, asking a question that never named the file
and then deciding for the human when they deferred. Nothing in the prior
wording stopped a treatment agent from relaying `?? docs/` verbatim and
satisfying the letter of the instruction.

Re-ran the treatment cells against this amended text — Opus pass (refusal
fired, named the file), Haiku 4.5 pass (named the file) — no regression.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

* docs: design Hermes version-bump wiring

Document the agreed follow-up to PR #2025 on a branch based on its merged dev commit. The design registers the Hermes YAML manifest, keeps jq for existing JSON files, and uses Mike Farah yq v4 for a narrow top-level YAML field rather than adding a Bash parser.\n\nDefine focused failure behavior and behavioral tests while explicitly excluding nested YAML, Hermes runtime changes, and unrelated release-script refactors. This captures Drew's request to keep the implementation small and avoid process or abstraction overhead.

* docs: reduce Hermes version-bump design

Incorporate the adversarial design review without turning the Hermes wiring follow-up into a general release-script refactor. Keep the existing jq path, add Mike Farah yq v4 only for .yaml, and retain one read-only preflight to prevent deterministic partial bumps.\n\nReduce the test contract to three behavioral cases and explicitly defer .yml support, nested YAML, rollback machinery, audit/status redesign, exhaustive failure matrices, and the separately discovered JSON-expression issue. This follows Drew's direction to avoid ceremony and overengineering.

* docs: plan Hermes version-bump wiring

Record Drew's approved reduced design after the second staff review. Limit preflight to the mutating bump path, cover audit's independent read path, and require byte-for-byte proof that deterministic YAML failures cannot partially update earlier JSON manifests.

Provide one TDD implementation task for the Hermes registry entry, jq/yq dispatch, focused preflight, and three behavioral checks. Explicitly defer rollback, audit-status changes, nested YAML, runtime changes, and broader release-tool refactoring.

* fix(release): wire Hermes into version bumps

Register the Hermes YAML manifest alongside the existing JSON manifests. Route manifest reads and writes by extension through jq or Mike Farah yq v4, with field names and values passed as data.

Preflight every present manifest before the mutating bump loop so a deterministic YAML read failure cannot leave earlier JSON manifests partially updated. Cover check, audit, bump, registry wiring, and byte-for-byte no-partial-write behavior with one focused fixture test.

* feat(opencode): add V2 (opencode2) plugin compatibility

Add dual V1/V2 support to the OpenCode plugin. The same source file now
works on both OpenCode V1 (opencode) and V2 (opencode2) without version
detection at runtime.

V2 changes:
- Add default export { id, server, setup } for V2 PluginSupervisor
- setup() registers skills via ctx.skill.transform() (V2 native API)
- setup() injects bootstrap via ctx.session.hook('context') (V2 equivalent
  of V1's experimental.chat.messages.transform)
- config hook guards against V2 array-format skills to avoid conflicts

Both APIs confirmed active at runtime via diagnostics in the V2 beta.

No external dependencies added — pure JavaScript throughout.

Docs updated with V2 install instructions, OPENCODE_CONFIG_DIR side-by-side
setup, and accurate How It Works section for both versions.

* docs: add Grok Build CLI to README.md

* feat: add Devin CLI support

Devin CLI's `devin plugins install obra/superpowers` fails today because the
repo has no `.devin-plugin/plugin.json` manifest. Add the manifest (skills are
auto-discovered from the co-located skills/ directory), a Devin tool mapping
linked from using-superpowers' Platform Adaptation section, a README install
section, version tracking in .version-bump.json, a Codex-sync exclude for the
new dotdir, and a CI-safe test mirroring the kimi/antigravity test style.

Bootstrap rides Devin's native skill surfacing: every installed skill's
name + description is injected into the system prompt at session start with a
standing instruction to invoke matching skills via the native skill tool.
Acceptance test ("Let's make a react todo list") passes in a clean session:
using-superpowers and brainstorming auto-trigger before any code is written.

* Drop devin-tools.md — not needed for correct operation

Re-ran the clean-session acceptance test with the mapping file and the
SKILL.md Platform Adaptation pointer removed: using-superpowers and
brainstorming still auto-trigger first, and the full workflow chain
(writing-plans, executing-plans, TDD, verification) resolves every action
to Devin's native tools. Devin CLI's own system prompt already documents
its tools (skill invocation, subagent profiles, todo tracking, question
prompts), so the mapping was redundant. Test now validates the manifest only.

* docs: streamline README getting started navigation

Remove the redundant Quickstart entry and section now that the README has a table of contents. Rename the Installation label in the table of contents to Getting Started while retaining the existing installation anchor and section heading.

* docs: keep Hermes in installation navigation

Add Hermes Agent to the installation entries in the table of contents. The removed Quickstart section was the README's only direct link to that existing installation section, so preserving the link avoids a navigation regression.

* feat(tdd): the project's suite defines green, not just your test file

At the Verify GREEN moment, redefine "other tests still pass": run the
project's test command even when the task named only one test file — a
scope statement bounds the deliverable, not the verification — and any
failure seen goes in the report by name. In a pre-registered 24-rep
battery on an adjacent-breakage probe, controls ran the wider suite in
1/12 sessions; with this text, 8/12 (sonnet 4/4, kimi 3/4, glm 1/4),
and every session that saw the failure reported it.

Claude-Session: https://claude.ai/code/session_0185AJr98gHx5EmwqNeft4Sy

* docs: release notes for v6.3.0

* chore: bump version to 6.3.0

* Update to Prime Radiant Community Code of Conduct. (#2122)

* docs: add Qwen Code install instructions to README

Rebased from PR #2108 onto the reworked README. Differences from the PR:
the Hermes TOC entry and Quickstart-line changes are obsolete (the v6.3.0
README rework already added the former and removed the latter), and the
Hermes post-compaction caveat stays: .hermes-plugin injects the bootstrap
only on is_first_turn, so the caveat is still accurate.

Install/update commands and the acceptance transcript are from PR #2108
(@arittr, tested interactively on Qwen Code).

Co-authored-by: Drew Ritter <arittr@users.noreply.github.com>

* fix(requesting-code-review): anchor the multi-commit BASE_SHA alternative to the merge base

The '# or origin/main' alternative fed a moving ref into the reviewer's
two-dot diff: once origin/main advances past the branch point, main's new
files appear as phantom deletions the reviewer can't distinguish from real
ones. Reproduced during triage (2026-08-12): a scratch repo with main
advanced one commit shows 'main-new.txt | 1 -' in the branch's diff.
git merge-base origin/main HEAD anchors the range to the branch point,
matching how sdd's review-package already computes BASE.

Reported in #2118 (wan-huiyan). Fixes #2118.

* fix(sdd): invoke sdd-workspace via bash so helpers survive stripped exec bits

Codex marketplace users hit 'Permission denied' running SDD helpers:
some extractors (Python zipfile) discard Unix mode attributes when
unpacking the package, so task-brief's and review-package's direct exec
of their sibling sdd-workspace fails. Our packaging preserves 0755
(git archive | tar -xpf, asserted by the existing packaging test) — the
bits are lost on the consumer side, which no packaging change can reach.
Invoking the sibling via "${BASH:-bash}" makes the exec bit irrelevant.

TDD: new regression case copies the helpers, chmod -x, runs task-brief
via bash — RED with the reported rc=126 Permission denied, GREEN after.

Reported in #2040 (michaelholcomb-creator). Fixes #2040.

* fix(sdd): reject empty or non-descendant BASE..HEAD ranges in review-package

When an SDD implementer commits to the wrong branch (#2050), the
BASE..HEAD range handed to review-package is either empty or not rooted
at BASE. Both cases previously produced a review package silently —
an empty one lets the reviewer approve "clean" work that isn't there.

Add two mechanical guards after BASE/HEAD validation, exiting 3 (vs 2
for usage errors) so callers can distinguish range problems:

- git merge-base --is-ancestor BASE HEAD, else "HEAD is not a
  descendant of BASE"
- git rev-list --count BASE..HEAD > 0, else "empty commit range"

Guard shape credits the analysis in closed PR #2082 by @stantheman0128.

Fixes #2050

* fix(opencode): adapt to V2 skill draft API removal (#2106)

OpenCode V2 removed SkillDraft.source() in 1113adfd5e (#41622): the
skill service now stores values only, and filesystem scanning moved to
the config side. The plugin's draft.source({type:'directory'}) call
threw 'draft.source is not a function', which killed the entire V2
plugin activation generation. Because V2 gates model.list on
PluginSupervisor.flush (23b0688a7f, #41783), that failure left flush
pending forever and the TUI showed no providers or models
('Model catalog initialization timed out', /api/model 503).

Register each skills/<name>/SKILL.md as a native Skill.Info object via
draft.add({id, name, description, location, content}) instead, matching
the {list, add, update, remove} draft API and the pattern used by
V2's built-in skill plugin. Wrap skill registration, hook registration,
and the context hook callback in try/catch so a future V2 API change
degrades to a logged error instead of taking down the whole generation
again. session.hook('context') payload shape is unchanged and keeps
working.

Verified end-to-end on opencode2 v0.0.0-beta-17595: 24 skills listed
via /api/skill (all superpowers skills present), /api/model returns
83 models across 3 providers, no 'failed to reload plugins' in server
logs. V1 path untouched.

* fix(opencode): skip V2 setup when V1 invokes it with a V1-shaped ctx

opencode 1.18.18 also calls default.setup, but with a ctx that lacks
the skill/session domains, so the defensive try/catch logged a TypeError
into every V1 session transcript even though V1 is fully served by the
SuperpowersPlugin named export. Detect the V1 shape and return quietly.

* feat(skills): import proving-it-works-with-a-movie from its standalone repo

Brings the proving-it-works-with-a-movie skill (demo/screencast/proof-video
recording, plus the check-movie timeline gate that catches frozen pictures,
narration drift, and dropped words) into superpowers core, along with its
supporting docs, scripts, and shell regression tests.

Source: prime-radiant-inc/proving-it-works (MIT, same copyright holder),
skills/proving-it-works-with-a-movie/ at time of import. The five scripts
(narrate, make-subtitles, assemble, burn-subtitles, check-movie) are
self-contained uv --script files with inline PEP 723 dependency
declarations, so they port with no new project-level dependency wiring.

Test paths were adjusted one directory level to match superpowers'
tests/<skill-name>/ layout (the standalone repo kept tests/ as a
top-level sibling of skills/).

Adds a Verification entry to README's Skills Library list.

Goal: fold this into 6.4 and retire the standalone repo.

* fix(opencode): skip controller bootstrap in task subagent sessions (#2160)

Detect child sessions structurally via session parentID instead of
relying on the model honoring <SUBAGENT-STOP>:

- V1: sessionID from firstUser.info.sessionID (hook input is empty at
  runtime), parentID via client.session.get({path:{id}})
- V2: sessionID from the context-hook event, parentID via
  ctx.session.get({sessionID})

Decision cached per session; lookup failures fail open (previous
behavior) and are not cached. Skills registration is unaffected, so
workers keep explicit access to execution skills.

* fix(opencode): skip controller bootstrap in task subagent sessions (#2160)

The messages.transform hook injects the using-superpowers bootstrap into
the first user message of every session, including task subagent
children. Workers then restart brainstorming/design cycles for work the
parent already authorised — the <SUBAGENT-STOP> note inside the
bootstrap only works when the model chooses to honor it.

Detect child sessions structurally instead: OpenCode task sessions are
created with a parentID, so when the session carrying the message has a
parentID, skip bootstrap injection. The hook receives no input at
runtime (verified in the 1.18.x bundle: trigger(..., {}, {messages})),
so the sessionID is taken from firstUser.info.sessionID and the session
record is fetched via client.session.get({path:{id}}).

The decision is cached per session; lookup failures fail open (previous
inject-always behavior) and are not cached so transient errors recover.
Skills registration is untouched — workers keep explicit access to
execution skills.

* fix(opencode): add root index.js entrypoint for v2 directory-form registration

* docs(opencode): remove and merge identical v1/v2 install and update guidance

* Fix platform-support issue template to apply a label that exists

The template auto-applies `platform-support`, but the repo has no such label
(harness requests use `new-harness`). GitHub silently drops labels that don't
exist, so every platform-support request arrives unlabeled — the Amazon Q
request (#2194) is the latest example.

Claude-Session: https://claude.ai/code/session_01UiEfXTZAC5cuH4hgx24mbB

* fix: establish shared intent before implementation

Discover the intended outcome, audience and success criteria before proposing
features when the request leaves them unclear. Reflect the understanding for
correction and carry it into the selected path's design artifact.

Bind approval to the actual stage presented: new architectural work requires
written-spec review and the planning handoff before implementation. Preserve
the existing lighter spike and bounded paths and clarify the short-design
example accordingly.

Jesse requested this repair after a React todo session advanced from feature
scope approval without establishing purpose. The controlled CLI comparison
observed purpose discovery in 5/5 candidate openings versus 0/5 controls, with
full-chain and holdout outcomes and their limits recorded in the PR. This
commit preserves the independently reviewed skill bytes; research artifacts
and the original development history are archived outside the PR.

* fix: review the saved plan before execution

Present the saved, self-reviewed plan for human review before implementation.
Request an execution method when none was supplied; preserve an existing
choice and ask only for plan review when the human already chose a method.

This completes the shared-intent repair without interpreting approval of an
earlier idea or scope as approval of an unseen implementation plan. Four
saved-plan smoke cases covered old/new wording with/without a prior choice;
all passed the narrower handoff checks, including old controls, so this is
not evidence of measured improvement.

Jesse requested consolidation into two commits and removal of the supporting
spec/plan research content from the PR. The skill bytes remain identical to
the reviewed branch; the complete research and original history are retained
in local archives.

* docs: specify proof movie OS compatibility

* docs: resolve adversarial review of movie compatibility spec

* docs: plan proof movie OS compatibility with Windows validation host

* test(movie): validate native Windows recording mechanism

* fix(movie): release probe resources after evidence failures

* docs(movie): avoid repeating the interactive probe take

* test(movie): port regression fixtures to Python

* test(movie): verify first subtitle cue offset

* fix(opencode): differentiate tool mapping by host flavor and harden child detection

Current opencode2 builds renamed the model-facing tools (bash→shell,
task→subagent with `agent` instead of `subagent_type`, apply_patch→
patch/patchText) and removed todowrite entirely, so the single v1
mapping injected on v2 hosts taught the model stale tool names.

- export V1_MAPPING/V2_MAPPING and inject the flavor-correct one on
  each path (v1 messages.transform → V1; v2 ctx.session.hook("context")
  → V2, incl. no-todo-tool guidance and sessionID continuation)
- child-session detection now keys on parentID presence (primary
  signal on both flavors) with dual-shape unwrapping preserved; v1
  #2160 behavior unchanged
- mirror surfaces updated: INSTALL.md dual mapping tables,
  README.opencode.md host-flavor notes, test-bootstrap-caching.mjs
  asserts both mappings + drives the v2 context hook end-to-end
- skills: add OpenCode to executing-plans' subagent-capable list,
  accurate OpenCode worktree status (git fallback; TUI dialogs are
  user-side only), generalized live-subagent resume guidance

* fix(movie): make frame and concat inputs portable

* docs: scope remaining movie work to Windows completion

* docs: resolve adversarial review of Windows completion scope

* docs: plan three milestones to finish Windows movie support

* fix(opencode): drop skill-content edits from this PR

AGENTS.md requires evaluated adversarial testing for any skill-content
change; these three one-line harness-accuracy notes don't clear that
bar, so they are deferred to a separate evaluated change. The PR now
ships plugin, docs, and test changes only — no skill content modified.

* fix(movie): finish native Windows media tools

* feat(movie): support native Windows terminal recording

* fix(movie): verify terminal health before finalizing takes

* docs(movie): document and verify Windows workflows

* docs(movie): correct reserved regression suite names

* chore(movie): drop the abandoned OS-rollout probe and superseded plans

The first, broader OS-compatibility rollout was stopped and replaced by the
narrower Windows completion. Its feasibility probe, probe cleanup test,
design, review, 12-task plan, results report, and the completion plan and
review record were internal execution artifacts with machine-specific paths.
The one probe-derived test list is inlined into the terminal suite.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* test(movie): keep one portable test suite

The Python suite ported the three shell tests' assertions so they run on
Windows; both copies were kept and the README mapped one to the other. Keep
the portable suite. Drop the one-shot Windows acceptance driver and its
browser fixture, which produced evidence rather than regressions, and the
never-implemented reserved suite names.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* docs(movie): trim Windows guidance to what the tools need

Remove generic shell exit-status recipes and a stills wrapper that the card
scene already covers. Keep the gdigrab commands and the verify-on notes
short. Reduce the spec to the design: drop execution logistics, host names,
and references to deleted files.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* test(movie): keep tool output out of the test log

The in-process narration and subtitle tests let the tools' stdout and
stderr through to the runner. Capture both and assert the expected
diagnostics.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* feat(movie): simplify the Windows terminal recorder to serve/run/key/watch/close

Windows has no tmux, so the recorder had grown into a 738-line daemon with a
file-based request protocol, request IDs, wait-only result retrieval, and a
Win32 Job Object module. Replace it with the Unix route's shape: serve keeps
ttyd and a headless browser alive and logs the terminal's output; run, key,
watch, and close are one-shot CDP calls against that browser. The installed
prompt reports each command's status through the window title, so run can
print it without any visible marker.

Process cleanup uses taskkill /T (a pgrep walk on Unix) instead of Job
Objects, which also simplifies the card renderer. The session tests run on
macOS too, since nothing in the script is Windows-specific.

Verified: 9 session tests per shell on Windows 11 for PowerShell 5.1,
PowerShell 7, and Git Bash; the browser suite with Chrome and Edge; 44
portable tests on macOS against a real ttyd session.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* feat: add diagnosing-superpowers skill

Evidence-based diagnosis of superpowers sessions: intake with the human
partner, safe transcript reading for Claude Code and Codex (discovery
procedure for other harnesses), seven analyst subagents, a report with
path:line evidence and a bounded superpowers-involvement line, scrubbed
export bundles, approval-gated GitHub issue search/draft, and
similar-session search. Includes spec, plan, structure test, and README
and docs index lines.

Developed RED-GREEN-REFACTOR per writing-skills: 46 scored scenario runs
across five SKILL.md versions, all twelve scenarios clean against the
final version, micro-tests control 5/5 to skill 0/5 on both
baseline-failing prohibitions, and one end-to-end run. Eval records are
kept by the maintainer outside the repo.

Claude-Session: https://claude.ai/code/session_01DyaGKhTXvHNs2JgPhDktz7

* docs: add 'When Something Goes Wrong' README section for diagnosing-superpowers

* diagnosing-superpowers: build the scrubbed bundle only on request

Never build or push a bundle unprompted. When intake names a bug report as
the goal, say once that a bundle is available on request, then wait. On
handover, state what the bundle contains, point at the scrub log, and say
scrubbing can miss things so every file needs review before sharing.
Raise the SKILL.md word budget to 1000 to fit the added rule.

* diagnosing-superpowers: share the analyst preamble and context-safety rules

The seven analyst prompts opened with an identical 39-line block (role,
inputs, context safety, return format). It now lives once in
prompts/analyst-common.md and each dimension prompt points at it. The
wc -lc / long-line / never-cat rule was restated in nine places; it now
lives in references/context-safety.md and everything else points there.
Addresses arittr's review on #2236.

* diagnosing-superpowers: drop gh; file issues through a prefilled template link

A default gh login carries the repo scope, which is write access to every
repository the user can reach. The skill now searches issues through the
unauthenticated public API and, instead of posting, hands the partner a
prefilled new-issue link. The link uses a new diagnosis_report.md issue
template so the bug and automated-issue-report labels apply regardless of
the reporter's permissions. Addresses arittr's review on #2236.

* diagnosing-superpowers: say 'plan step', not 'commitment'

In a transcript full of git commits, 'commitment' and 'committed to' read
as version control. The plan-adherence and quality-evidence prompts now
say 'agreed plan' and 'plan step'.

* spec: 'agreed to', not 'committed to', in the plan-adherence summary

* diagnosing-superpowers: writing review fixes

Move GitHub search and prefilled-link mechanics to references/github-issues.md.
State the redaction levels neutrally instead of nudging toward more data.
Say that all seven analysts always run and what the quick-reference table
is for. Add a title slot and a bundle slot to the issue template. Drop the
duplicated human-prompts rule from request-conflicts. Prose fixes: active
voice, dangling modifier, vague referents, two lists turned into tables.

* diagnosing-superpowers: use gh for issue search and creation

gh handles auth, rate limits, and JSON, and the approval gate on the
exact issue text already covers posting. Keep the public-API and
prefilled-link paths as fallbacks for machines without gh. Note that
GitHub drops labels from reporters without push access, so the template
footer is the durable marker of a skill-filed issue.

* Use shared session discovery in diagnosing-superpowers

At Drew's request, apply the evaluated shared-discovery variant to Jesse's
existing PR #2236. Resolve native session sources and record semantics from
available tools, documentation and bounded inspection. Record verified absolute
paths, linkage, extraction queries, human-message distinctions, usage-counter
semantics and uncertainty once in the case for all analysts to consume.
Replace the three per-harness references and update structural checks.

This is exactly the evaluated source tree at
3f0a63e860d4719397e584e90cc7af07a247cb6d, applied as one commit on
801badbf719f4044c97175e5b01fb6f7cbc32c2d. Fourteen files change;
126 lines added, 285 removed. No private eval fixtures or transcripts ship.

Validation:
- Structural test: 45 passed, 0 failed before and after application.
- Staged tree exactly matches the evaluated candidate; diff check passes.
- Independent read-only review: no actionable blockers.
- Retained before/after full doctor runs: one pair each on native Claude,
  Codex and Pi. All six delivered reports and completed seven dimensions.
  Shared discovered all three native session families without the removed
  references. Both versions had report-quality defects; shared Codex deleted
  its cited case through a fixture symlink. Preserve this negative result.
- Eight fresh Codex follow-ups: original/shared x symlink/ordinary-home x
  two repeats, one retained historical session family. All eight retained
  cases and supported the four core findings. Seven native final deliveries;
  one shared run stopped on provider capacity after writing its report.
  No deletion recurred. One original reused three analysts for seven tasks.
  Recorded follow-up cost $34.8617883, all eight attempts accounted for.

These observations support this scoped simplification, not general equivalence
or a causal claim that reference removal caused or could not cause a failure.
Child assignment/model choices were native behavior; the complete variants
also differ in analyst prompts. Common provenance, citation-verification and
measurement problems remain separate follow-ups. No new paid runs were made
for this publication; evidence and independent audits are retained privately
by Drew. Behavioral evaluation provenance: campaigns
358c7333-c5f0-48bd-a733-61196da992ed and
102d630d-30ef-49a0-97e1-8dd410ed0548.

Prepared with GPT-6 using Codex through Paseo; local codex-cli 0.153.4.
Skills used: superpowers writing-skills, using-git-worktrees,
requesting-code-review, verification-before-completion; primeradiant-ops
linear-ticket-lifecycle. Drew approved publishing this evaluated variant.
Enabled plugins in the publishing checkout's Codex configuration:
- github@openai-curated
- documents@openai-primary-runtime
- spreadsheets@openai-primary-runtime
- presentations@openai-primary-runtime
- primeradiant-ops@primeradiant
- slack@openai-curated
- linear@openai-curated
- codex-security@openai-curated
- pdf@openai-primary-runtime
- template-creator@openai-primary-runtime
- sites@openai-bundled
- visualize@openai-bundled
- computer-use@openai-bundled
- cloud-build@superpowers-cloud-build
- browser@openai-bundled
- superpowers@superpowers-dev
- stream-deck-agents-codex@drew-local
- computer-history@openai-bundled
- codex-app-tools@openai-bundled
- unified-computer-use@openai-bundled
- chrome@openai-bundled
- bits-and-bolts@mcp-extensions-early-access
- visual-probe@visual-probe-local

Tracking: PRI-3127

* Preserve diagnostic evidence through doctor export

Align scrubber and independent audit prompts around one shared redaction policy while preserving safe command, result, source, session-line, quotation, and linkage structure. Add finished-handoff evidence and reconciliation instructions, provenance labels across case/report/bundle/issue templates, and the structural existence check for the shared reference.\n\nThis patch responds to the retained negative post-report handoff baseline: cited result bodies were removed wholesale, source findings and the positive related-session match were not verifiable, provenance and export statements were stale, and scrub counts disagreed. The behavioral handoff validation remains pending for the follow-up task; this commit records only the focused product guidance and structural RED/GREEN evidence.

* Clarify scrub audit return contract

Remove the obsolete CLEAN branch beneath the audit prompt's Otherwise return instruction. CLEAN remains governed by the preceding no-misses condition, and MISSED is now the only alternative. Verified with the focused structural test and git diff --check.

* fix(movie): preserve rejected narration and prior takes

Prevent failed narration scenes from entering the cache manifest, while leaving their generated WAV files available as failure evidence. Add filesystem-backed regressions covering repeated rejected chat synthesis, accepted-scene reuse, and strict ASR rejection of cached audio.

Refuse nonempty recording directories both before CLI session side effects and at the direct film boundary. The regression preserves existing numbered frames and a sentinel byte-for-byte across run, key, watch, and direct film refusal.

Make subtitle capability tests independent of the host FFmpeg installation, skip the real pixel test before probing unavailable tools, retain strict skipped-capability rejection, and remove only the unused websockets runner dependency.

* docs(movie): make native Windows recorder recipes executable

Replace the Git Bash PowerShell shorthand with complete native commands,
explicit path conversion, a kept-alive serve task, bounded readiness, and
run/key/watch/close examples. Use native input and sleep commands so the
recipe works without a sample app. Explain empty take directories and
PowerShell 5.1 embedded-quote escaping observed in native trials.

The original PowerShell missing-cwd finding does not reproduce when the
session is nested under the working directory; retain the successful
baseline and describe explicit directory creation as setup clarity.

Fresh readers exercised the final recipes on native PowerShell 5.1,
PowerShell 7, and Git Bash. Preserve the failed first candidate and driver
setup failures, distinguish instruction trials from full skill evaluation,
and keep movie acceptance with Drew. Record Drew's approval of the normal
workflow dependencies and the bounded repair plan.

* Fix narration cache identity and partial subtitle offsets

Address the fresh review on PR #2214 after the #2275 integration. Drew approved fixing the two reproduced bugs and keeping the specified auto/on/off verification semantics.

Cache accepted narration by normalized text plus effective engine, voice, and synthesis model. Resolve voice defaults before rendering, invalidate entries without settings, and retain requested ASR checks on cache hits. Exclude rejected clips as before.

Treat manual subtitle offsets as start-time overrides. Only assembly offsets JSON selects scenes in the cut, including when manual timing overrides are also supplied. Empty narrated cuts write an empty SRT without crashing.

Make the gated Unix example pass --verify on and document the actual local ASR modes. Auto remains permissive if ASR is unavailable; on remains strict.

Validation: observed the new cache and subtitle regressions fail before the fixes; all 23 focused narration and subtitle-text tests now pass. Synthesis, duration probing, and ASR are mocked. No media inspection or live ASR was performed; Drew retains final video acceptance.

* Fix inserted narration and movie audio subtitle checks

Address the final three review findings on PR #2214, as approved by Drew. Count both sides of every non-equal transcript span so a short insertion or expanded replacement cannot evade the drift gate on a longer script. Preserve the existing length and run thresholds.

Honor --no-expect-audio for encoded silent tracks. Base subtitle requirements on detected audible speech so opting out of expected audio does not suppress captions for speech that is present.

Extract the first embedded subtitle stream as SRT when no sidecar is present and apply the same cue-end check to either source. Empty cues fail even for short narration, and extraction or malformed timing errors are reported as failures. Preserve the silent end-card allowance.

Validation: the new tests first reproduced ten failing cases across narration insertion, silent-track opt-out, and embedded subtitle handling. All 35 focused narration, checker-policy, and subtitle-text tests now pass. External media commands, audio and picture sampling, contact-sheet creation, synthesis, and ASR were mocked; no actual media inspection or live ASR was performed. Drew retains final video acceptance.

* docs: plan consolidated movie committee repairs

Drew requested a whole-PR committee review after repeated narrow fixes missed failures. Record the repair boundaries, acceptance handoff, timing and lifecycle contracts, and focused regression cases before implementation. Preserve existing artifact formats and Drew-owned video acceptance; all automated checks in this pass use mocked media boundaries.

* fix(movie): make narration acceptance govern assembly

Repair Task 1 from the 2026-09-11 movie committee plan. Narration now atomically withdraws acceptance before it mutates accepted bytes, stages failed takes as retained evidence, and publishes a manifest entry only after transcript gates and duration measurement. It preflights ffprobe, preserves bounded retries and cache identity, and distinguishes unsupported token comparison from cache identity.

Assembly now validates accepted manifest narration before it starts encoding, ignores generated narration for movie scenes, selects manifest WAV paths, maps source or synthetic movie audio explicitly, fits wide movies within the requested inner rectangle, and escapes only literal directory percent signs in sequence paths. The focused regression suite mocks every media boundary; real-media fixture declarations are updated but not executed. Prompt constraints prohibit real media generation, probing, inspection, synthesis, ASR, browser, checker, or full media suites.

* fix(movie): retain narration evidence through verification

Address Task 1 review round 1. Treat successful empty ASR output as speech failure rather than an unavailable verifier, reject empty chat claims within the existing bounded retry loop, and extend unsupported segmentation detection to supplementary CJK ideographs.

Withdraw cached acceptance before every revalidation so strict failures and interrupts cannot leave stale publication. Preserve nested manifest WAV paths on cache reacceptance, and measure a unique candidate before promotion so duration failures retain their evidence across reruns. Add structured movie geometry coverage plus both silent and source-audio mapping tests. All tests use uv --no-project with mocked synthesis, ASR, probes, and encoding; no media operation was run.

* test(movie): cover unsupported ASR and ordinary retries

Close Task 1 review round 2 without production changes. Feed actual unsupported ASR text through auto and strict verification while proving off does not call ASR. Run the second rejected narration invocation without --force, then assert it synthesizes new takes and retains distinct rejected bytes instead of reusing cache evidence.

* fix(movie): keep subtitle timing and track selection faithful

Implement Task 2 of the movie committee repairs. Allocate proportional cue boundaries across each complete rounded scene interval, reserve positive millisecond spans, and coalesce chunks when the available interval cannot represent them separately. Readability limits guide word splitting without dropping text or clipping narration tails; invalid intervals fail before subtitle output is written.

Explicitly select the supplied soft subtitle track with optional source audio, including the hard-burn fallback. Parse only numbered SRT cue timing lines so arrow-bearing captions cannot crash the checker or inflate coverage. Preserve the existing maximum cue end policy, assembly-offset intersection, and partial manual retiming.

Add 17 safe subtitle contracts and register the contracts runner suite. Real-file mocked narrate/assemble/subtitle reruns retain removed narration WAV evidence while omitting stale assembly audio and offsets. Verification: 41 contract tests and 18 authorized existing regressions pass; only text and mocked media boundaries were exercised. Native Windows and human video acceptance remain outside this verification.

* fix(movie): refine subtitle chunks using allocated durations

Address Task 2 review round 1: initial character budgets count spaces that disappear between chunks, so proportional timing can exceed --max-secs even when a further word-boundary split is feasible. Reallocate after splitting an over-target multiword cue, checking actual integer millisecond intervals each time.

Coalescing runs once before refinement, and refinement stops at the availabl…

## [android](https://github.com/topics/android)
- [airbnb/DeepLinkDispatch](https://github.com/airbnb/DeepLinkDispatch) [3](https://github.com/airbnb/DeepLinkDispatch/commits): Manifest generation: fail on write errors, clean up logging (#394)

- ManifestGenerator: throw DeepLinkProcessorException on IOException
  instead of swallowing as a diagnostic warning (a missing manifest
  would otherwise fail silently in a confusing downstream place).
  Catch scoped to IOException so processor bugs aren't hidden.
- RelocateDeepLinkManifestTask: use orNull instead of get() on the
  @Optional kspManifestFile property (get() NPEs when unset), replace
  println with logger.warn, collapse empty else-if branch, fix typos.
- GenerateManifestIntentFiltersForDeeplinkDispatchTask: replace
  println with logger.warn (respects --quiet) and switch error(...)
  calls to throw GradleException for idiomatic build-failure output.

Co-authored-by: Andreas Rossbacher <andreas.rossbacher@airbnb.com>
- [fastlane/fastlane](https://github.com/fastlane/fastlane) [2](https://github.com/fastlane/fastlane/commits): [meta] validate the screengrab Gradle wrapper jars on CI (#30422)

* [meta] validate the screengrab Gradle wrapper jars on CI

screengrab/ and screengrab/example/ each commit a gradle-wrapper.jar,
the two remaining binaries OpenSSF Scorecard flags once #30421 lands.
Their SHA-256 match the official Gradle 2.10 and 4.10.2 wrapper jars.
The workflow checks that on every push to master and pull request;
Scorecard excludes wrapper jars once it finds a successful run.

* [meta] gradle wrapper validation: run on pull requests only when they touch a jar

Pushes to master keep running it: Scorecard only exempts the jars
when the latest commit on master has a successful run.
- [PhilJay/MPAndroidChart](https://github.com/PhilJay/MPAndroidChart) [2](https://github.com/PhilJay/MPAndroidChart/commits): Update URL

## [claude-code](https://github.com/topics/claude-code)
- [sirmalloc/ccstatusline](https://github.com/sirmalloc/ccstatusline) [46](https://github.com/sirmalloc/ccstatusline/commits): chore(release): prepare v2.2.32 documentation and version

Summarize the latest security improvements, safer imports, proxy handling, cache fixes, and text rendering improvements.

Add a standalone v2.2.32 Recent Updates section, synchronize usage and development documentation, and bump the package version to 2.2.32.
- [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) [21](https://github.com/CherryHQ/cherry-studio/commits): fix(notifications): show conversation title and final sentence (#21424)

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

Before this PR: Completion notifications used a generic title and the
topic/session name as the body.

After this PR: Assistant and Agent completion notifications use the
conversation name as the title and the final sentence of the last AI
message as the body, while preserving conversation titles when opened
from notifications.

<!-- (optional, in `fixes #<issue number>(, fixes #<issue_number>, ...)`
format, will close the issue(s) when PR gets merged)*: -->

Fixes: N/A

### Why we need it and why it was done in this way

The following tradeoffs were made: Main-owned reply snapshots and
standard sentence segmentation; reasoning excluded; latest completed
model selected for multi-model replies; localized fallbacks retained

The following alternatives were considered: Full-message previews;
conversation-name-only notification bodies

Links to places where the discussion took place: N/A

### Breaking changes

<!-- optional -->

None

### Special notes for your reviewer

<!-- optional -->

- Validation: 155 focused tests; type, format, documentation, migration
and i18n checks; source lint excluding `.context/**`; injected Electron
toast rendering and native notification payload checks
- Limits: No real provider calls or OS banner visibility verification;
earlier full run had 9 file-watcher failures and 1 combobox/jsdom
exception; final full suite not rerun
- Documentation: User-guide update not required

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
Fixed completion notifications to show the topic or session name and the final sentence of the last AI message.
```

Signed-off-by: suyao <sy20010504@gmail.com>
- [slopus/happy](https://github.com/slopus/happy) [11](https://github.com/slopus/happy/commits): app: wait 2 seconds before showing Sending… on an idle send
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) [2](https://github.com/Piebald-AI/claude-code-system-prompts/commits): Update changelog for v2.1.296
- [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) [1](https://github.com/lemomo-ai/lemo-opuscar/commits): OPUSCAR 98: all 98 styles open on the film page

Per film: the style (2D / 2.5D / 3D), a frame, a reusable style prompt with
one-click copy, and the shots and direction. Decade, 2D/3D and text filters,
EN/中文 toggle; a frame click plays that film in a corner player that follows
the scroll and loops its segment. Data in styleboard/opuscar98_styles.json
(also served as opuscar98/styles.json), frames in styleboard/img/opuscar98/.
Prompts were blind-tested on unrelated subjects and rewritten to be
subject-agnostic. README: the 98-styles update and poster (docs/opuscar98-styles.jpg).

## [compiler](https://github.com/topics/compiler)
- [typst/typst](https://github.com/typst/typst) [12](https://github.com/typst/typst/commits): Respect `par.hanging-indent` in bibliography (#8712)

Co-authored-by: Laurenz <laurmaedje@gmail.com>
- [markedjs/marked](https://github.com/markedjs/marked) [1](https://github.com/markedjs/marked/commits): fix: let indented and type 3-5 html blocks interrupt a paragraph (#4124)

## [dashboards](https://github.com/topics/dashboards)
- [thingsboard/thingsboard](https://github.com/thingsboard/thingsboard) [28](https://github.com/thingsboard/thingsboard/commits): Merge pull request #16276 from thingsboard/rc

Merge rc into master
- [taleshape-com/shaper](https://github.com/taleshape-com/shaper) [2](https://github.com/taleshape-com/shaper/commits): Fix: Ensure custom CSS loads after built-in styles to win CSS cascade (#411)

## [embedded](https://github.com/topics/embedded)
- [stlink-org/stlink](https://github.com/stlink-org/stlink) [3](https://github.com/stlink-org/stlink/commits): Merge pull request #1521 from onetwosteph/fix-f413-and-f423-sector-calculation

Corrected F4 sector number calculation for F413 and F423.
- [hathach/tinyusb](https://github.com/hathach/tinyusb) [2](https://github.com/hathach/tinyusb/commits): rusb2: fix SQCLR/ACLRM preconditions and RA6M5 USBHS pipe handling (#4146)

- pipe_reset(): reach PID=NAK and PBUSY=0 out of CURPIPE before SQCLR/ACLRM, hold ACLRM >=100 ns
- RA6M5 USBHS: per-pipe PIPEBUF; park OUT packets that arrive unarmed instead of dropping them
- keep a halt when a transfer is submitted on a halted pipe; quiesce pipes on close; EP0 drain completes in the caller's context
- RA: no .bin except dfu-util boards; HIL: ra6m5_ek with openocd reset recovery

Fixes #4038, closes #4150
- [nanopb/nanopb](https://github.com/nanopb/nanopb) [1](https://github.com/nanopb/nanopb/commits): FindNanopb: handle NANOPB_OPTIONS given as a list

NANOPB_OPTIONS is turned into a list as soon as find_package()
COMPONENTS are appended to it, and it is natural to write it as
set(NANOPB_OPTIONS --source-extension=.cpp --header-extension=.hpp)
as well. In that case two things went wrong:

- the extension regexes stop only at a space, so the match for
  --source-extension swallowed the following list items and e.g.
  "--header-extension=.hpp" ended up as an entry in PROTO_SRCS.
- the semicolons were passed through into --nanopb_opt, so CMake split
  the protoc command line and protoc failed with
  "Unknown flag: --header-extension".

Join the list with spaces once and use that for both. Add a build test
that sets list-form options together with a component.

Fixes #1094

## [esp32](https://github.com/topics/esp32)
- [esphome/esphome](https://github.com/esphome/esphome) [73](https://github.com/esphome/esphome/commits): [core] Add status_momentary_warning/error overloads without a name (#20362)
- [rmk-rs/rmk](https://github.com/rmk-rs/rmk) [11](https://github.com/rmk-rs/rmk/commits): Merge pull request #1227 from rmk-rs/daily_review/20261009-source-review

docs(pointing): remove obsolete device ID paragraph
- [arendst/Tasmota](https://github.com/arendst/Tasmota) [10](https://github.com/arendst/Tasmota/commits): Matter support for Light RBG+CT (5 channels) and refactoring of lights (#25123)
- [crosspoint-reader/crosspoint-reader](https://github.com/crosspoint-reader/crosspoint-reader) [4](https://github.com/crosspoint-reader/crosspoint-reader/commits): feat: add ability to clip/highlight text for EPUBs (#3589)

Co-authored-by: Justin Mitchell <justin@jmitch.com>
Co-authored-by: Phạm Bình An <111893501+brianhuster@users.noreply.github.com>
Co-authored-by: brianhuster <phambinhanctb2004@gmail.com>
Co-authored-by: Uri Tauber <uritaube@gmail.com>
- [espressif/idf-extra-components](https://github.com/espressif/idf-extra-components) [4](https://github.com/espressif/idf-extra-components/commits): Merge pull request #872 from StevenYang77/fix/iqmath_mpy_overflow

fix(iqmath): prevent intermediate overflow in multiplication
- [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) [4](https://github.com/xinnan-tech/xiaozhi-esp32-server/commits): 聊天记录弹框底部不再留大量空白 (#3410)

弹框本身和 body 用 !important 撑到视口（body 顶开 size="large" 默认多扣的 56px footer 高度）。body 的高度由 flex: 1 自动撑满，max-height 只用来顶开原来的 950px 上限。

## [go](https://github.com/topics/go)
- [wader/fq](https://github.com/wader/fq) [5](https://github.com/wader/fq/commits): Merge pull request #1411 from wader/bump-gomod-golang-x-term-0.47.0

Update gomod-golang-x-term to 0.47.0 from 0.46.0
- [nadoo/glider](https://github.com/nadoo/glider) [4](https://github.com/nadoo/glider/commits): chore: use atomictypes
- [tdewolff/minify](https://github.com/tdewolff/minify) [3](https://github.com/tdewolff/minify/commits): Fix JS fuzz test
- [sqlc-dev/sqlc](https://github.com/sqlc-dev/sqlc) [2](https://github.com/sqlc-dev/sqlc/commits): deps: bump golang.org/x/net to v0.60.0 for govulncheck (#4636)

* deps: bump golang.org/x/net to v0.60.0 for govulncheck

govulncheck flags GO-2026-6603, GO-2026-6610, GO-2026-6611, GO-2026-6612
and one more in golang.org/x/net v0.58.0, all fixed in v0.60.0.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01St6H2Ga9JLZsjQmfFRCtb5

* examples: bump golang.org/x/net to v0.60.0

Brings the examples module past the same golang.org/x/net advisories
fixed in the root module.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01St6H2Ga9JLZsjQmfFRCtb5

---------

Co-authored-by: Claude <noreply@anthropic.com>
- [gorse-io/gorse](https://github.com/gorse-io/gorse) [1](https://github.com/gorse-io/gorse/commits): Fix qdrant category filtering (#1400)
- [jhump/protoreflect](https://github.com/jhump/protoreflect) [1](https://github.com/jhump/protoreflect/commits): Massive backfill of test coverage and fixes (#660)

Big improvement in test coverage for nearly all packages. But
particularly protoresolve, which was virtually untested and had many
latent bugs because of it. Lots of fixes and also other improvements
(making things more DRY, improving docs and semantics, more
consistent/idiomatic names in some cases, etc).

## [golang](https://github.com/topics/golang), [gif](https://github.com/topics/gif), [image-processing](https://github.com/topics/image-processing), [jpeg](https://github.com/topics/jpeg), [libvips](https://github.com/topics/libvips), [png](https://github.com/topics/png), [webp](https://github.com/topics/webp)
- [cshum/imagor](https://github.com/cshum/imagor) [2](https://github.com/cshum/imagor/commits): docs: libvips concurrency clarification
- [davidbyttow/govips](https://github.com/davidbyttow/govips) [1](https://github.com/davidbyttow/govips/commits): Add Keep option to format-specific ExportParams (#551)

* Add ForeignKeep constants and keep resolver

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

* Add Keep option to JPEG, PNG, TIFF, HEIF and GIF export params

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

* Add Keep option to WebP export params

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

* Add Keep option to AVIF, JP2K, JXL and Magick export params

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

* Test streaming savers apply Keep like Export

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

* Tighten Keep tests and clarify Gainmap on older libvips

Compare reloaded HEIF/AVIF ICC profiles with the source instead of
checking presence, and stop asserting ICC for JXL: libjxl canonicalizes
colour profiles, so a reloaded JXL always carries one regardless of Keep.
Reject an unknown Keep bit on every save path so the test proves each
path reaches the guard on any libvips version. Document that
ForeignKeepGainmap alone keeps no metadata before libvips 8.18.

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: diego.choi <diego.choi@kakaocorp.com>
Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

## [llm](https://github.com/topics/llm)
- [yetone/magpie](https://github.com/yetone/magpie) [98](https://github.com/yetone/magpie/commits): provider: moved Cursor users get plugin 0.2.3: where a proxy or network blocks HTTP/2 ("h2 is not supported"), a Cursor chat goes over HTTP/1.1 as RunSSE + BidiAppend on api2 instead of failing (magpie-community/plugins#59, kazecreator)

Behind TLS inspection or a network that drops HTTP/2, every moved Cursor
chat failed with 502 "Cursor: h2 is not supported" or never answered, while
sign-in, models and usage worked. 0.2.3 falls back to Cursor's own HTTP/1.1
transport; a failure that says HTTP/2 itself can't be had keeps later Runs
on HTTP/1.1 for 10 minutes. The cursor mover's min goes from 0.2.2 to
0.2.3, so keepMovedCurrent updates every moved Cursor user.

0.2.3 on npm (registry.npmjs.org) has an index.mjs byte-identical to
plugins main 5b67ff4. The plugin PR was reviewed at f5c11b7 and merged:
- bun test in packages/cursor: 66 pass, 0 fail, three runs
- whole repo: 1026 pass, 0 fail; bun scripts/check.mjs all 15 pass
- each guarded piece broken by hand turns http1.test.mjs red
- not tried with a real Cursor account on the review side

go test -tags nogui ./internal/provider passes (temp HOME, pinned caches).
go vet -tags nogui ./internal/provider passes for darwin, linux and windows.
gofmt -l is clean.
- [jundot/omlx](https://github.com/jundot/omlx) [50](https://github.com/jundot/omlx/commits): chore: bump version to 0.7.1.dev1
- [BerriAI/litellm](https://github.com/BerriAI/litellm) [35](https://github.com/BerriAI/litellm/commits): fix(databricks): keep #/$defs refs in json_schema response_format (#45659)

* fix(databricks): keep #/$defs refs in json_schema response_format for non-Claude models

Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>

* fix(databricks): type the json_schema response_format override

Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>

* test(databricks): integration cells for json_schema $defs refs across endpoints

Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>

* test(databricks): split stacked loop in streaming json_schema cell

Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>

* fix(databricks): mark BaseConfig dict contract on json_schema override

Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>

* test(databricks): cover json_schema refs on every endpoint, edge refs, sad paths and an outage burst

---------

Co-authored-by: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>
Co-authored-by: mateo-berri <277851410+mateo-berri@users.noreply.github.com>
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) [13](https://github.com/OpenHands/OpenHands/commits): chore: bump agent-server to 1.54.0 (#18253)

Co-authored-by: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Co-authored-by: openhands <openhands@all-hands.dev>
- [cactus-compute/needle](https://github.com/cactus-compute/needle) [9](https://github.com/cactus-compute/needle/commits): Needle 3 MLX forward pass (#149)

* feat(model): MLX port of the Needle 3 forward, with a parity test against JAX

needle/model/architecture_mlx.py runs SimpleAttentionNetwork.__call__ on
MLX: conv-tap GQA attention with separate qk/v head dims, sliding window
and global layers, the Hadamard MLP, the engram lookup, the four-lane
MHC residual with Sinkhorn mixing, exit_depth/subnetwork_only, out_vocab
and any mask. Config, geometry and the Hadamard permutations are
imported from architecture.py rather than copied.

tests/test_mlx.py compares the logits with the JAX model to 5e-5 on a
tiny model with every parameter moved off its init, and on the
published checkpoint when NEEDLE_MLX_PARITY_CHECKPOINT points at it.

Signed-off-by: Fernando Ollé <fernando.olle@icloud.com>

* feat(model): QAT numerics for the MLX forward

needle/model/quantize_mlx.py mirrors quantize.py for what the training
loss uses: CQ weight quantisation with its straight-through estimator
(Hadamard-rotated groups, Lloyd-Max codebook, fp16 norms, left-on-tie
nearest level), A8 activation fake-quant, and A8 or CQ KV with A8
queries. forward(..., quant=True) applies them at the same sites as the
JAX model's _aq and maybe_quant_* calls.

tests/test_quantize_mlx.py compares CQ quantisation and the quantized
forward with JAX. Rounding under quant flips on ulp-level differences,
so the tiny model is checked position by position with room for a few
flips, and the published checkpoint by loss.

Signed-off-by: Fernando Ollé <fernando.olle@icloud.com>

* test(model): pin the MLX parity tests to the CPU device

Metal is not bit-for-bit float32 on every Apple GPU, so the exact
comparisons run on mx.cpu and one Metal case checks argmax agreement
within a 5e-3 band.

Signed-off-by: Fernando Ollé <fernando.olle@icloud.com>

---------

Signed-off-by: Fernando Ollé <fernando.olle@icloud.com>
- [mangiucugna/json_repair](https://github.com/mangiucugna/json_repair) [4](https://github.com/mangiucugna/json_repair/commits): Fix formatting in pyproject.toml dependencies
- [google/langextract](https://github.com/google/langextract) [1](https://github.com/google/langextract/commits): Strengthen live Vertex batch configuration and cache tests (#566)
- [gptme/gptme](https://github.com/gptme/gptme) [1](https://github.com/gptme/gptme/commits): ci(docs): check gptme repo blob/tree links against git, not github.com (#4234)

* ci(docs): check gptme repo blob/tree links against git, not github.com

Sphinx linkcheck keeps failing on github.com 429s for gptme-org blob/tree
pages. All 4 linkcheck failures since the job split (2026-10-02..09: today's
scheduled master run and 3 PR runs) were GitHub 429s/timeouts on links that
exist; none was a real dead link.

Ignore https://github.com/gptme/*/(blob|tree)/master/* in linkcheck and check
those paths with scripts/check_docs_repo_links.py instead: gptme/gptme
against the checkout, other gptme repos against a blobless shallow clone.
Run by `make docs-linkcheck`, so the existing workflow picks it up.
Replaces the one-off perplexity.py ignore.

Git-Session-Id: 1128f332-0876-44bc-b320-173f8cb1afe8

* ci(docs): don't strip '_' from repo link paths

Git-Session-Id: 1128f332-0876-44bc-b320-173f8cb1afe8

## [machine-learning](https://github.com/topics/machine-learning)
- [polakowo/vectorbt](https://github.com/polakowo/vectorbt) [10](https://github.com/polakowo/vectorbt/commits): build: include kaleido in the full extra for image export
- [stefan-jansen/machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) [8](https://github.com/stefan-jansen/machine-learning-for-trading/commits): Remove the @claude workflow rather than ship it inert (#1154)

.github/workflows/claude.yml needs an ANTHROPIC_API_KEY secret that is not set
and is not going to be. Everything the workflow can do is available by asking in
a session; what it adds is answering a GitHub thread when no session is open,
which does not pay for a key in repo secrets and a per-run bill.

Leaving it in place is not neutral: an @claude comment starts the job, which
then fails on the missing secret and puts a red check on that pull request.

Nothing references the file. No test asserts it exists, no workflow triggers off
it, and CONTRIBUTING.md and the templates do not mention @claude, so deleting it
is the whole change. Restoring it later is this file plus the secret.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_011gDgA5ivgURRmvyyW92ubB
- [skypilot-org/skypilot](https://github.com/skypilot-org/skypilot) [2](https://github.com/skypilot-org/skypilot/commits): [Test] Pin the GKE test cluster's pod range outside 10.0.0.0/9 (#11007)

* [Test] Pin the GKE test cluster's pod range outside 10.0.0.0/9

create_cluster.sh let GKE auto-allocate a /14 pod range from 10.0.0.0/9,
which holds only 32 /14 blocks per VPC. In a project with many clusters
and Filestore instances, cluster creation fails with "does not have
available private IP space in 10.0.0.0/9 to reserve a /14 block for
pods" before the test runs. Use 100.64.0.0/14 (RFC 6598) by default,
overridable via GKE_CLUSTER_IPV4_CIDR.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018JekVSCumAMWgWMiXjqz9u

* [Test] Pick a free /14 in 100.64.0.0/10 for each GKE test cluster

A fixed pod range made a second cluster created by this script in the
same project overlap the first and get rejected. List existing cluster
pod ranges and use the first non-overlapping /14 instead.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018JekVSCumAMWgWMiXjqz9u

* [Test] Stop when listing GKE clusters fails instead of assuming all ranges free

A command substitution in a for loop's word list does not trip set -e,
so a failed listing made every block look free. Capture it in an
assignment first.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018JekVSCumAMWgWMiXjqz9u

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

## [python](https://github.com/topics/python)
- [adafruit/circuitpython](https://github.com/adafruit/circuitpython) [27](https://github.com/adafruit/circuitpython/commits): Merge pull request #11525 from dhalbert/zephyr-pwmio

zephyr-cp: add pwmio for nordic boards
- [pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) [8](https://github.com/pymupdf/PyMuPDF/commits): src/extra.i: fix segfault when a get_cdrawings() callback raises.

jm_append_merge() reports a failed callback with messagef() before calling
PyErr_Clear(), so messagev() runs with the callback's exception still set.
Its function-local statics were initialised on the first call with
PyImport_ImportModule("pymupdf"), which returns NULL while an exception is
set, and the NULL was then passed to PyObject_GetAttrString(), so the first
exception raised by a callback in a process killed the interpreter with
SIGSEGV instead of being reported. Once the statics were set, later calls
still called pymupdf.message() with the exception set, which prints only
part of the message.

messagev() now puts any pending exception aside with PyErr_Fetch() before
its static variables are initialised, and restores it with PyErr_Restore()
after the message is output, discarding any error from the output itself in
that case; with no exception pending, an error from the output is left set
as before. The behaviour for a failing callback is otherwise unchanged: the
failure is reported and the exception is cleared.

tests/test_drawings.py:test_cdrawings_callback_exception() runs the case in
a child process, because the crash only shows when there has been no
earlier messagef() call in the process, and checks the message is output
whole.

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
- [kurigram-org/kurigram](https://github.com/kurigram-org/kurigram) [6](https://github.com/kurigram-org/kurigram/commits): feat: add TON wallet transfer and connect request support
- [vacanza/holidays](https://github.com/vacanza/holidays) [4](https://github.com/vacanza/holidays/commits): Update Bolsas y Mercados Argentinos holidays: add 2026 Visit of Pope Leo XIV holidays (#3901)
- [arnegiacomo/fugleramme](https://github.com/arnegiacomo/fugleramme) [2](https://github.com/arnegiacomo/fugleramme/commits): chore(assets): recut 8 classic plates from better scans

8 plates:
- Mute Swan (Cygnus olor), cygnus-olor-2
- Grey Wagtail (Motacilla cinerea)
- Eurasian Blackcap (Sylvia atricapilla)
- Eurasian Wren (Troglodytes troglodytes)
- Common Gull (Larus canus)
- Black Redstart (Phoenicurus ochruros)
- Eurasian Hobby (Falco subbuteo), falco-subbuteo-3
- Common Raven (Corvus corax)
- [binance/binance-connector-python](https://github.com/binance/binance-connector-python) [2](https://github.com/binance/binance-connector-python/commits): Release derivatives_trading_options v8.5.1

### Changed (4)

#### REST API

- Modified response for `account_funding_flow()` (`GET /eapi/v1/bill`):
  - items: property `symbol` added
  - items: item property `symbol` added

- Modified response schema `accountFundingFlowResponse`:
  - items: property `symbol` added
  - items: item property `symbol` added
- [CadQuery/cadquery](https://github.com/CadQuery/cadquery) [2](https://github.com/CadQuery/cadquery/commits): (1/3) Harden hull() against degenerate input (#2100)

* Skip entities that lie inside or on a circle

_pt_arc takes sqrt(l**2 - r**2), which has no real value when the point is
inside the circle and degenerates to the point itself when it is on it: a
line end inside a circle, or a circle inside a bigger one, raised
ValueError; a line end on the circle produced an empty segment. Such an
entity cannot touch the hull beyond the circle, so it is not a candidate -
report it the way get_angle already reports an entity against itself.

Partially addresses #1190 and #1224.

* Return the start circle when nothing else can be reached

A circle with every other entity inside it is its own hull, but the march
raised "Hull could not be closed". The lone-circle shortcut was one instance
of this and is folded in.

* Treat edges of one circle as one entity

Two arcs on the same circle became two entities: arc_arc divided by the
distance between their centres, and since the march closes on identity it
could come back to the other one and fail to close. The merged bounds only
steer select_lowest_arc; every tangent takes the full circle.

Fixes #1888. Partially addresses #943 and #1224.

---------

Co-authored-by: kimstik <kimstik@github.com>
- [vinta/awesome-python](https://github.com/vinta/awesome-python) [2](https://github.com/vinta/awesome-python/commits): Merge pull request #3365 from DevVettel/fix-django-modern-rest-period
- [chdb-io/chdb](https://github.com/chdb-io/chdb) [1](https://github.com/chdb-io/chdb/commits): Merge pull request #647 from fallintoplace/fix/like-wildcards-pandas-fallback

Fix SQL LIKE wildcards in pandas fallback
- [confident-ai/deepeval](https://github.com/confident-ai/deepeval) [1](https://github.com/confident-ai/deepeval/commits): Merge pull request #3417 from ykocaogullar/main

feat(dataset): send the pulled dataset version with test runs
- [enactic/openarm](https://github.com/enactic/openarm) [1](https://github.com/enactic/openarm/commits): discord-supporter: Add --hold to keep deferred messages unseen (#617)

When the maintainer defers a reply (e.g. to discuss it with the team),
--commit used to mark the whole fetch as seen, so the deferred message
would not reappear. `--commit --hold CHANNEL_ID:MESSAGE_ID` now stops
that channel's or thread's marker just before the held message while
committing everything else.

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

## [rust](https://github.com/topics/rust)
- [embassy-rs/embassy](https://github.com/embassy-rs/embassy) [23](https://github.com/embassy-rs/embassy/commits): Merge pull request #7222 from OueslatiGhaith/msc-eject

usb/msc: return from run when the host ejects the medium
- [probe-rs/probe-rs](https://github.com/probe-rs/probe-rs) [8](https://github.com/probe-rs/probe-rs/commits): jtag: check the CTRL/STAT value for sticky errors (#4434)

Co-authored-by: Dániel Buga <bugadani@gmail.com>
- [google/OpenSK](https://github.com/google/OpenSK) [6](https://github.com/google/OpenSK/commits): Validate large blob parameters before mutating write state (#797)

In LargeBlobState::process_command, an offset == 0 write mutated
self.expected_length before checking max_large_blob_array_size() and
TRUNCATED_HASH_LEN, and updated self.expected_next_offset = 0 before
verifying pin_uv_auth_param and checking that the chunk fits within
expected_length.

If an offset == 0 request failed validation or authentication while a
multi-fragment write was in progress, self.expected_length and/or
self.expected_next_offset were overwritten while self.buffer retained
the previous write's bytes. In particular, an offset == 0 request with
length > max_large_blob_array_size() after an initial valid chunk left
self.expected_length set to the oversized length and allowed subsequent
chunks at offset > 0 to bypass max_large_blob_array_size().

Validate length, authentication, and chunk bounds before mutating
LargeBlobState on offset == 0, and clear the state when the final chunk
is processed regardless of whether the hash check succeeds.
- [lakehq/sail](https://github.com/lakehq/sail) [5](https://github.com/lakehq/sail/commits): feat: support catalog function existence checks (#2759)
- [tokio-rs/tracing](https://github.com/tokio-rs/tracing) [4](https://github.com/tokio-rs/tracing/commits): appender: document that the rolling appender constructors panic (#3632)

## Motivation

`RollingFileAppender::new` and the `minutely`, `hourly`, `daily`, `weekly` and `never` helpers panic when the appender can't be initialized, for example when the log directory or file can't be created. Their docs didn't say so. Only the docs for `RollingFileAppender::builder` mention it.

## Solution

This adds a `# Panics` section to each of the six, pointing to `RollingFileAppender::builder` and `Builder::build` for callers who need to handle the error.

No behaviour change. Making these constructors return a `Result` would be a breaking change, which #1138 proposes.

Refs #3631
- [rust-embedded/awesome-embedded-rust](https://github.com/rust-embedded/awesome-embedded-rust) [2](https://github.com/rust-embedded/awesome-embedded-rust/commits): Merge pull request #546 from rust-embedded/berkus/fix-and-upgrade

Fix linter issues, upgrade GH actions
- [dora-rs/dora](https://github.com/dora-rs/dora) [1](https://github.com/dora-rs/dora/commits): examples: require NumPy 2 in python-operator-dataflow (fixes nightly #3761) (#3762)

examples: require NumPy 2 in python-operator-dataflow

pyarrow 26.0.0 (released 2026-10-09) refuses to import against NumPy 1.x
but does not declare numpy in its install requirements, so the example's
`numpy<2.0.0` pin resolved to numpy 1.26.4 next to pyarrow 26 and every
operator failed at `import pyarrow`. Flip the pin to `numpy>=2.0.0`;
the rest of the requirements (torch, ultralytics, opencv, matplotlib,
pandas, scipy, dora-rs) resolve with NumPy 2 on Linux, macOS and Windows.

Fixes #3761


Claude-Session: https://claude.ai/code/session_015hkBrD5kgNu9XLsvbTycpn

Co-authored-by: Claude <noreply@anthropic.com>

## [s3](https://github.com/topics/s3)
- [Kuingsmile/PicList](https://github.com/Kuingsmile/PicList) [16](https://github.com/Kuingsmile/PicList/commits): :bug: Fix: remove svg from output formats which is not supported by sharp
- [benbjohnson/litestream](https://github.com/benbjohnson/litestream) [1](https://github.com/benbjohnson/litestream/commits): fix(vfs): fix litestream_time() to update with new LTX files (#1455)

## [swift](https://github.com/topics/swift)
- [tw93/MiaoYan](https://github.com/tw93/MiaoYan) [12](https://github.com/tw93/MiaoYan/commits): chore: remove skill links left dangling by the mirror cleanup

2734edd4 dropped .agents/skills but kept the .claude/skills symlinks that pointed into it.
- [supabase/supabase-swift](https://github.com/supabase/supabase-swift) [10](https://github.com/supabase/supabase-swift/commits): feat(postgrest): add comparison operators for typed filters (#1499)

`==`, `!=`, `<`, `<=`, `>`, `>=` on a filterable column call eq/neq/lt/lte/
gt/gte, and `== nil` / `!= nil` on a nullable column call isNull(), so both
spellings build the same filter tree. `.eq(nil)` and `== nil` on a NOT NULL
column still do not compile. Every row of the design spec's §4.3 table is
asserted in both spellings.

Type-check cost (Swift 6.4, M3; commands in SDK-1578):
- Examples/SlackClone, expressions over 100 ms: 0 -> 0
- package + tests, distinct sites over 100 ms: 6 -> 7 (the new one is a
  pre-existing `#expect(x == [...])` at 101 ms; 160 -> 162 solver scopes
  in isolation)
- constraint-solver scopes: +0.04% for the test build, +0.31% for the
  SlackClone module (noise floor is of the same order)
- clean `swift build` median: 171.0 s -> 148.2 s (dominated by machine load)
- worst case, a file of dense plain comparison chains that imports
  PostgREST: +14% solver scopes over today

Fixes SDK-1578
- [trycua/cua](https://github.com/trycua/cua) [9](https://github.com/trycua/cua/commits): feat(spaces): new shared UI — React web UI in the Mac app and an Electron app (preview) (#4893)

Adds one shared React web UI for Cua Spaces (apps/cua-spaces-web) and two
hosts for it.

- Mac app (SwiftUI): the native UI stays the default. The new UI is an
  opt-in experiment, "New UI (preview)", served in a WKWebView through
  WebUIBridge; live video stays native (VideoToolbox surfaces over the page).
- Electron app (apps/cua-spaces-desktop) for macOS, Windows and Linux: it
  answers the same bridge methods from the same app core (cua-spaces-ffi
  through Node UniFFI bindings, `pnpm native`), decodes video with
  WebCodecs, and on macOS draws the notch with a small Swift helper that
  shares its views with the Mac app (libs/spaces-notch-swift).

Release: the Electron app follows the cua-spaces version and is built and
published only for prerelease versions (X.Y.Z-suffix), as GitHub
prereleases never marked latest, with an opt-in beta-only updater
(electron-updater feed on cua-spaces-latest). Stable releases still ship
only the SwiftUI app. The Sparkle cutover to the Electron app
(make-appcast.sh --electron, the sparkle_electron workflow input, settings
migration, shared bundle id) is in place and off; see
apps/cua-spaces-desktop/docs/sparkle-cutover.md.

Also: parity fixes ported from the SwiftUI app; daemon handoff between the
two apps; Teleport's run listener lowered into the library; Keyvault
refusal messaging for apps not signed by Cua; polkit and Linux packaging
fixes; Windows build, launch-at-login and title bar fixes; sign-in without
a browser; a shared bridge contract checked for both hosts; and
ci-cua-spaces-macos.yml runs on pull requests again, now covering
libs/spaces-notch-swift. New app directories are FSL-1.1-MIT.

Co-authored-by: Francesco Bonacci <f@trycua.com>
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [MarkEdit-app/MarkEdit](https://github.com/MarkEdit-app/MarkEdit) [5](https://github.com/MarkEdit-app/MarkEdit/commits): Improve event handling for touch devices (#1796)
- [FluidInference/FluidAudio](https://github.com/FluidInference/FluidAudio) [4](https://github.com/FluidInference/FluidAudio/commits): docs(tts): document Kokoro English dictionary versus BART comparison (#1006)

### Why is this change needed?

Kokoro callers need to understand why English pronunciation uses
dictionary lookup before BART fallback, and why a nonempty fallback
result is not evidence of a correct pronunciation. Add a bounded 40-word
comparison with all outputs, CMU reference alternatives, source/model
hashes and explicit limits on interpretation.

The note distinguishes the older dictionary-only probe from current
main, whose initialism rules already protect uppercase API/CPU/GPU. It
reports coverage and raw agreement rather than an unsupported accuracy
rate, and does not attribute observed errors to conversion or to BART
architectures generally. Link it from the documentation index and Kokoro
guide; include the CMUdict attribution/license alongside the reference
excerpts.

Validation: checked all 40 records, summary counts, source hashes and
relative links; the analysis harness passed three tests for reference
variants, missing entries and inference-failure accounting; `git diff
--check` passed. Documentation and recorded data only; no new model runs
or runtime changes in this PR.
- [fulldecent/FDSoundActivatedRecorder](https://github.com/fulldecent/FDSoundActivatedRecorder) [4](https://github.com/fulldecent/FDSoundActivatedRecorder/commits): Merge pull request #39 from fulldecent/adopt-swift6-module-template

fix: test on the GitHub-hosted Xcode 27 runner
- [majd/ipatool](https://github.com/majd/ipatool) [2](https://github.com/majd/ipatool/commits): docs: document mcp tool setup
- [argmaxinc/argmax-oss-swift](https://github.com/argmaxinc/argmax-oss-swift) [1](https://github.com/argmaxinc/argmax-oss-swift/commits): Add overridable model loading hooks to WhisperKit and TTSKit (#553)
- [SwiftOldDriver/iOS-Weekly](https://github.com/SwiftOldDriver/iOS-Weekly) [1](https://github.com/SwiftOldDriver/iOS-Weekly/commits): Revise member's contributor details

Updated member's description to reflect current role and responsibilities.

## [typescript](https://github.com/topics/typescript)
- [Snapchat/Valdi](https://github.com/Snapchat/Valdi) [2](https://github.com/Snapchat/Valdi/commits): Internal Change

GitOrigin-RevId: 0c0149d982ae285a293193e727a615ef23378515
- [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) [1](https://github.com/ast-grep/ast-grep/commits): 0.50.0
bump version

## [wearable](https://github.com/topics/wearable), [wearables](https://github.com/topics/wearables)
- [OpenStrap/edge](https://github.com/OpenStrap/edge) [118](https://github.com/OpenStrap/edge/commits): Merge pull request #577 from OpenStrap/feat/score-imported-workout-325

feat(workouts): score an imported workout with band heart rate (closes #325)
- [Mentra-Community/MentraOS](https://github.com/Mentra-Community/MentraOS) [40](https://github.com/Mentra-Community/MentraOS/commits): Merge pull request #4633 from Mentra-Community/codex/fix-nightly-history-load

Fix Nightly test history timing out

## Other
- [facebook/idb](https://github.com/facebook/idb) [72](https://github.com/facebook/idb/commits): Stamp the requested client on legacy translation requests

Summary:
A legacy (`--api ax`) read now carries `AccessibilityRequestOptions.clientType` on every translator request it makes, from resolving the element (a frontmost resolution or a point hit-test) through serializing it. A read that names no client resolves to `noClient`, which is what every request already carried, so default reads are unchanged.

- `AXTranslationRequest` holds the resolved client, and a retried request keeps it.
- The dispatcher's bridge callback stamps it on each request before forwarding it to the simulator.
- `resolveElement(for:clientType:)` takes the client explicitly, because a point read's hit-test happens before any options reach serialization.
- `describe` and `hitTest` pass `options.resolvedClientType`. Actions, frames and waits take no request options, so they use the client a default read resolves to.

The dispatcher now always stamps the client rather than forwarding the translator's own value. A translator stamps a non-zero value only while its process is servicing an incoming macOS accessibility request, which an idb process never does. The pinned expectation from the previous commit changes from `[0, 5]` to `[0, 0]` accordingly.

Differential Revision: D124356756

fbshipit-source-id: a72f04c0dc2fd717c786ee36ab9f43b1aa99af9b
- [openai/codex](https://github.com/openai/codex) [39](https://github.com/openai/codex/commits): Add opt-in output token replay for OpenAI requests (#52742)

## What changed

- Add the disabled-by-default `output_token_replay` feature to request `output.encrypted_content` from OpenAI providers.
- Preserve encrypted message and tool-call output, message and function-call status, and output-text `annotations` and `logprobs` through history and replay. Update the generated protocol schemas and SDK types.
- Strip output ciphertext from requests to other providers while retaining it in stored history, including after replay is disabled. Remove encrypted content from memory extraction inputs.

## Testing

Add integration coverage for the feature/provider combinations, metadata replay across follow-up requests, and history preservation when resuming with replay disabled.

GitOrigin-RevId: 77729a021b6771933402aebe74ece8eb39c057e2
- [jdx/mise](https://github.com/jdx/mise) [29](https://github.com/jdx/mise/commits): chore: release 2026.10.7 (#14230)

<!-- entire-trail-link-start -->
https://entire.io/gh/jdx/mise/trails/613
<!-- entire-trail-link-end -->

### 🚀 Features

- **(upgrade)** add tool_update.global_auto to update every global tool
by @jdx in [#14237](https://github.com/jdx/mise/pull/14237)
- reuse downloads the server confirms are unchanged by @jdx in
[#14222](https://github.com/jdx/mise/pull/14222)

### 🐛 Bug Fixes

- **(backend)** stop list() and get() panicking while the tool map
reloads by @jdx in [#14240](https://github.com/jdx/mise/pull/14240)
- **(bootstrap)** stop reporting freshly cloned repos as dirty with
core.autocrlf by @jdx in
[#14225](https://github.com/jdx/mise/pull/14225)
- **(cargo)** lock the same rust homes the rust plugin resolves by
@wislertt in [#14219](https://github.com/jdx/mise/pull/14219)
- **(doctor)** show dotfiles repo and origin when history is disabled by
@jdx in [#14244](https://github.com/jdx/mise/pull/14244)
- **(dotfiles)** replace a junction target when a symlink source changes
by @jdx in [#14226](https://github.com/jdx/mise/pull/14226)
- **(env)** keep backslashes literal in single-quoted dotenv values by
@jdx in [#14228](https://github.com/jdx/mise/pull/14228)
- **(env)** join adjacent quoted and unquoted dotenv value parts again
by @jdx in [#14231](https://github.com/jdx/mise/pull/14231)
- **(history)** describe tracked variant changes by @oppegard in
[#14194](https://github.com/jdx/mise/pull/14194)
- **(lock)** apply aqua version prefixes before selecting overrides by
@nettlesh in [#14218](https://github.com/jdx/mise/pull/14218)
- **(rust)** treat rustup profile aliases like their full names by
@JamBalaya56562 in [#14220](https://github.com/jdx/mise/pull/14220)
- **(schema)** accept task references in a task array by @JamBalaya56562
in [#14229](https://github.com/jdx/mise/pull/14229)
- **(self-update)** keep showing the auto-update hint until it is
disabled by @jdx in [#14233](https://github.com/jdx/mise/pull/14233)

### 🚜 Refactor

- **(lock)** skip aqua prefix ambiguity pass without override prefixes
by @jdx in [#14232](https://github.com/jdx/mise/pull/14232)

### 📚 Documentation

- explain auto_update's release delay and prefer mise settings KEY=VALUE
by @jdx in [#14235](https://github.com/jdx/mise/pull/14235)

### New Contributors

- @wislertt made their first contribution in
[#14219](https://github.com/jdx/mise/pull/14219)
- @oppegard made their first contribution in
[#14194](https://github.com/jdx/mise/pull/14194)
- [espressif/esp-idf](https://github.com/espressif/esp-idf) [23](https://github.com/espressif/esp-idf/commits): Merge branch 'fix/usj_rom_printf_flush' into 'master'

test(usj): flush printf before uninstalling the driver

See merge request espressif/esp-idf!53482
- [block/buzz](https://github.com/block/buzz) [14](https://github.com/block/buzz/commits): perf(relay): drop per-pulse ban reads and owner-link writes on HTTP (#8233)

## Why

Agents send an HTTP typing pulse (`POST /events`, kind 20002) every 3–5
seconds while they work. #8207 already routes the pulse's
write-restriction and serving checks through #8208's short-TTL caches.
Two per-pulse costs were still left at the membership step:

- **A fresh ban read** for the agent, plus its owner when the agent
comes in through NIP-OA (`deny_banned` → `community_ban_outcome`).
- **Four writer round-trips for owner-admitted agents**, on every
request: `materialize_nip_oa_owner` runs 2× `ensure_user` + the
`agent_owner_pubkey` upsert + an `is_agent_owner` confirm, even though
the link already exists.

## What changes

- **Typing's ban check reads the restriction cache.** `submit_event`
already parses the event before the membership step, so typing pulses
call a new `enforce_relay_membership_ephemeral`. Its ban check reads
through `restriction_state_cached`, the same 30s bound the pulse's
write-restriction check already has. Every other HTTP route, persistent
`POST /events`, and socket auth still read fresh (`cached: false`).
- **`materialize_nip_oa_owner` skips a link it already knows.** If
`observer_owner_cache` already holds `(community, agent, owner) = true`,
it returns `true` right away. `agent_owner_pubkey` has one production
writer, which sets it only `WHERE agent_owner_pubkey IS NULL`, and
nothing clears it, so the skipped writes were no-ops. This helps every
caller (HTTP, socket auth, audio). The owner-link disconnect only runs
on the first write, so it still runs.
- **`observer_owner_cache` capacity goes from 1k to 100k**, so
concurrently active agents actually hit it. That's tens of MB per pod at
most, the same scale as `restriction_cache`.

Per-pulse Postgres work at the membership step:

| Agent | Before | After |
|---|---|---|
| Direct relay member | host lookup (writer) + membership + ban | host
lookup (writer) + membership |
| Owner-admitted (NIP-OA) | host lookup + 2 memberships + 2 bans + 4
writer trips | host lookup + 2 memberships |

## Not in this PR

- **Caching host → community.** It's the tenant-binding step every HTTP
request goes through, and it reads from the writer. Community deletion
depends on new requests not binding once a community leaves `active`. A
cache would keep binding a quiescing community for its TTL. The
serving-write leases may make that harmless, but that needs a closer
look than a "safe fixes" PR.
- **Caching relay membership.** Removing a member has no HTTP equivalent
of the socket disconnect, so a cache would delay removal by its TTL.
- **The desktop client reusing one connection.** That's going in a
separate buzz-app PR.

## Unrelated one-liner

The `sadscan` pre-commit hook scans whole staged files. It blocked this
commit on a pre-existing test-only URI in `handlers/auth.rs`
(`postgres://buzz:buzz_dev@127.0.0.1:1/buzz`, a deliberately unreachable
stub). I added the hook's own `// sadscan:disable np.postgres.1` marker
to that line.

## Testing

- New Postgres tests. I confirmed each one fails when its guard is
removed:
- `typing_ban_gate_uses_cached_restriction_row`: a member banned in
Postgres with a cached clear row can still type. Fails if typing reads
fresh.
- `persistent_post_ban_gate_reads_fresh`: a stale cached ban doesn't
refuse a kind-9 post that Postgres allows. Fails if every kind reads the
cache.
- `known_owner_link_skips_materialize_writes`: after the link is cached,
deleting the agent row behind the cache's back stays deleted. Fails
without the short-circuit.
- `scripts/postgres-test-run.sh -p buzz-relay --lib --tests`: 397/397
passed. This was local PG14.
- `cargo test -p buzz-relay`: 1430 passed and 7 failed. The same 7 fail
without this commit in this environment: 6 `api::media` tests can't find
a `buzz` role on :5432, and `mesh_demo` returns a 504.
- `cargo clippy -p buzz-relay --all-targets -D warnings` is clean.
- An independent agent review found no blockers. Its optional
suggestions are test gaps: nothing pins the owner-cascade cached read,
or the `false` literals at socket auth.
- **Not yet done:** a run against a live local relay, and human testing.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Signed-off-by: Honey <8e307ae0076a4dab6b94b036ea3edc7e08f823a625269c1e6919e881a048b4d2@buzz.block.builderlab.xyz>
Co-authored-by: Honey <8e307ae0076a4dab6b94b036ea3edc7e08f823a625269c1e6919e881a048b4d2@buzz.block.builderlab.xyz>
Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [acsandmann/rift](https://github.com/acsandmann/rift) [13](https://github.com/acsandmann/rift/commits): chore: tests
- [espressif/esp-gmf](https://github.com/espressif/esp-gmf) [12](https://github.com/espressif/esp-gmf/commits): Merge branch 'feat/afe-task-stack-memory' into 'main'

feat(gmf_ai_audio): Allow internal AFE task stacks

See merge request adf/multimedia/esp-gmf!535
- [verl-project/verl](https://github.com/verl-project/verl) [12](https://github.com/verl-project/verl/commits): [ci] chore: use a3-8 runner for nightly ppo qwen3-8b fsdp vllm test (#8161)

### What does this PR do?

A2 cluster is temporarily unavailable. Rolling back to A3 cluster for
nightly ppo qwen3-8b fsdp vllm test.

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
- [awesomedata/awesome-public-datasets](https://github.com/awesomedata/awesome-public-datasets) [11](https://github.com/awesomedata/awesome-public-datasets/commits): Update README sha: 4a6d0132f68b73a24279dc23342ec1455d9adea3
- [binwiederhier/ntfy](https://github.com/binwiederhier/ntfy) [10](https://github.com/binwiederhier/ntfy/commits): Merge pull request #1888 from binwiederhier/dependabot/npm_and_yarn/web/eslint-config-prettier-10.1.8

Bump eslint-config-prettier from 8.10.2 to 10.1.8 in /web
- [buildroot/buildroot](https://github.com/buildroot/buildroot) [9](https://github.com/buildroot/buildroot/commits): DEVELOPERS: add Joachim Wiberg for firewalld

Signed-off-by: Joachim Wiberg <troglobit@gmail.com>
Signed-off-by: Julien Olivain <ju.o@free.fr>
- [cline/cline](https://github.com/cline/cline) [9](https://github.com/cline/cline/commits): feat(core): in-chat connector authentication via Composio meta tools (#14755)

* feat(core): in-chat connector authentication via Composio meta tools

Signed-in beta sessions create a meta-tool session through the Cline API
connectors proxy and register COMPOSIO_MANAGE_CONNECTIONS and
COMPOSIO_WAIT_FOR_CONNECTIONS, so the agent can hand the user a Connect
Link when a task needs an app that is not connected yet.

* test(core): verify connector meta-tool usage telemetry

* fix(core): tell the agent when to use connector meta tools

Composio's descriptions are generic, so models answered "I don't have
access to Gmail" instead of offering a Connect Link.

* fix(core): replace Composio meta-tool descriptions with our own

Composio's descriptions require COMPOSIO_SEARCH_TOOLS first, which this
session does not expose, so models refused to start the connection flow.
Also drop the provider's session_id input; the proxy supplies it.

* feat(core): expose Composio search and multi-execute meta tools

Register every meta tool the server allows with Composio's own
descriptions and schemas, which reference each other (search, manage,
wait, multi-execute). Drops the custom descriptions.

* fix(core): require the complete Composio meta-tool flow
- [lycorp-jp/sim-use](https://github.com/lycorp-jp/sim-use) [8](https://github.com/lycorp-jp/sim-use/commits): Merge pull request #151 from lycorp-jp/fix/deterministic-cancellable-sleep-test

test: make the cancellableSleep tests deterministic with a manual clock
- [cherry-embedded/CherryUSB](https://github.com/cherry-embedded/CherryUSB) [6](https://github.com/cherry-embedded/CherryUSB/commits): update(platform/rtthread): switch to adb sh in shell open, add vfs dfs port

Signed-off-by: sakumisu <1203593632@qq.com>
- [espressif/esp-sr](https://github.com/espressif/esp-sr) [6](https://github.com/espressif/esp-sr/commits): Merge branch 'docs/ww' into 'master'

docs: update ESP_Wake_Words_Customization

See merge request speech-recognition-framework/esp-sr!244
- [FoloToy/ai-passport](https://github.com/FoloToy/ai-passport) [6](https://github.com/FoloToy/ai-passport/commits): Merge pull request #104 from PhoenixZHC/docs/ble-xbox-keyboard

docs(reference): add BLE controller and keyboard lessons
- [lancedb/lancedb](https://github.com/lancedb/lancedb) [6](https://github.com/lancedb/lancedb/commits): fix(python): preserve Decimal precision in table updates (#4431)

Python `Decimal` values and Arrow decimal scalars raise
`NotImplementedError` in `table.update(values=...)`. Register a Decimal
converter that emits quoted fixed-point text so the native cast to the
target column preserves every digit, including decimal128 and decimal256
values. Non-finite Decimal values raise `ValueError` with a static
message.

Closes #4360.

Validation with the native extension built from the current source at
7f593359, on macOS arm64 and Python 3.12.14:

- All 33 new regression cases failed before the fix and passed
afterward. They cover Python and Arrow scalar updates, signs, zero,
exponents, full 38/76-digit precision, and a Decimal context precision
of 6.
- 16 existing converter, update, and Decimal expression tests passed.
- Repository Ruff formatting and lint passed; formatting left all 156
files unchanged.
- A native round-trip check confirmed that an unquoted SQL number rounds
a high-precision value while the quoted Decimal update preserves it
exactly.

The full suite, other Python versions, and remote API were not
exercised.

AI assistance: Codex helped implement and validate the Decimal
conversion and its regression tests.
- [lxgw/LxgwWenKai](https://github.com/lxgw/LxgwWenKai) [6](https://github.com/lxgw/LxgwWenKai/commits): Update source file pointer
- [THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC) [6](https://github.com/THU-MAIC/OpenMAIC/commits): fix(storage): support path-style S3 addressing (AI-assisted) (#1849)

Adds an opt-in `AWS_S3_FORCE_PATH_STYLE` (`true` or `1`) that sets the AWS SDK v3 `forcePathStyle` client option for the S3 asset byte store, so S3-compatible stores such as MinIO and Ceph can be addressed as `endpoint/bucket/key`. Unset keeps the existing Amazon S3 behaviour. Bumps `@openmaic/storage` to 0.37.3.

Fixes #1686

Co-authored-by: weinaike <13814354+weinaike@users.noreply.github.com>
- [astral-sh/ty](https://github.com/astral-sh/ty) [5](https://github.com/astral-sh/ty/commits): Authenticate Docker Hub pulls (#4702)

Docker release builds are failing with `429 Too Many Requests` while
resolving `ubuntu:latest`. The workflow only logs in to `ghcr.io`,
leaving Docker Hub pulls anonymous. Authenticate as `astralshbot` with
`DOCKERHUB_TOKEN_RO` before building the base image and additional
variants. Use the token for pull request builds and dry runs whenever it
is available, while allowing fork pull requests without the secret to
build anonymously.
- [Automattic/simplenote-android](https://github.com/Automattic/simplenote-android) [5](https://github.com/Automattic/simplenote-android/commits): Share note via system share sheet instead of custom app grid (#1848)
- [embassy-rs/trouble](https://github.com/embassy-rs/trouble) [5](https://github.com/embassy-rs/trouble/commits): Merge pull request #705 from RomainMuller/fix/gatt-client-peer-handles

fix(gatt): do not trust server handles in the GATT client
- [tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro) [5](https://github.com/tensorflow/tflite-micro/commits): Remove mingw-w64-x86_64-python-absl-py from Windows Makefile CI (#3820)
- [earendil-works/pi](https://github.com/earendil-works/pi) [4](https://github.com/earendil-works/pi/commits): feat(durable): read returns images, optional Photon image processor

read returns an image file as one image block (programs get an ImageContent) plus an info diagnostic,
instead of an unsupported_image error. Limits are the conversation model's inputLimits.images.resize,
by default 2000x2000 pixels and 4.5 MB of base64.

- Without a processor: PNG, JPEG, GIF, and WebP within the limits pass through undecoded; the byte limit
  is checked before reading the file, dimensions from the header. Larger images and BMP are error results.
- With createCodingTools({ images }): the processor orients by EXIF, converts BMP to PNG, and shrinks to
  fit. ImageProcessor.prepare is async.
- @earendil-works/pi-durable/images: createPhotonImages(wasm) on @silvia-odwyer/photon 0.3.3 (web build);
  /images/node and /images/cloudflare load the wasm. The root and ./tools entries never reach it (enforced
  in check-entry-graphs).
- An image must be read whole: one that changes while read is read again, unlike a growing text file.
- A model without image input gets a diagnostic that it sees a placeholder.
- [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) [4](https://github.com/ghostty-org/ghostty/commits): cli/list-themes: add ctrl-d/u paging (#14607)

discussion #14604

## Ctrl-D and Ctrl-U paging

`Ctrl-D` and `Ctrl-U` move down and up 20 themes. `PgDn` and `PgUp`
already do this. `g` and `G` already exist (#13376), so vim-like paging
fits. It also helps users who have no `PgUp` or `PgDn` key.
- [ccusage/ccusage](https://github.com/ccusage/ccusage) [3](https://github.com/ccusage/ccusage/commits): fix(ci): give the release npm job time to build pnpm (#1844)

Co-authored-by: ryoppippi <1560508+ryoppippi@users.noreply.github.com>
- [dtolnay/cargo-expand](https://github.com/dtolnay/cargo-expand) [3](https://github.com/dtolnay/cargo-expand/commits): Release 1.0.127
- [fishjar/kiss-translator](https://github.com/fishjar/kiss-translator) [3](https://github.com/fishjar/kiss-translator/commits): feat: fab shortcut visibility (#1159)

* feat(fab): add temporary shortcut and visibility toggle

* fix(fab): align visibility action and use a themed dialog

* fix(fab): remove visibility menu divider

* fix(fab): preserve page visibility across runtime recreation

Resolve the visibility action with the existing exception-list rules and update the runtime snapshot after a successful save. Add regression coverage for exception pages, failed saves, and SPA body replacement.
- [loro-dev/loro](https://github.com/loro-dev/loro) [3](https://github.com/loro-dev/loro/commits): fix: Return decode errors from lazy history reads (#1177)

* fix: Propagate unreadable lazy history errors

See context/arena-parent-links.md for first-reader errors and infallible compatibility.

Co-Authored-By: GPT-6 <noreply@openai.com>

* fix: Roll back imports over unreadable block bodies

See context/arena-parent-links.md for body validation and compatibility.

Co-Authored-By: GPT-6 <noreply@openai.com>

---------

Co-authored-by: GPT-6 <noreply@openai.com>
- [OpenStickCommunity/GP2040-CE](https://github.com/OpenStickCommunity/GP2040-CE) [3](https://github.com/OpenStickCommunity/GP2040-CE/commits): Add Mad Catz FightStick TE2+ and Fighting Commander Dualshock PS4 Hosts (#1742)
- [TactilityProject/Tactility](https://github.com/TactilityProject/Tactility) [3](https://github.com/TactilityProject/Tactility/commits): CL-32 v0.4 implementation + split v0.2/v0.3 (#683)

- Implement ST7305 driver at `Drivers/st7305-module`
- Rename `cl32` device project to `cl32-v02-v03` and removed v0.4 drivers
- Implement CL-32 v0.4 device as `cl32-v04`: display, keyboard, backlight/frontlight driver and power supply
- Remove `TT_LAUNCHER_APP_ID` (it was always the same setting)
- Remove `TT_LVGL_STATUSBAR_COLORS_INVERTED` (unused since recent changes)
- Wi-Fi only refreshes once, so users can navigate with the keyboard through the results, without constently resetting focus/selection. After initial scan, manual scans can be requested via the toolbar.
- Themes: material and material_mono theme don't show post-selection border animation anymore. It looks weird on monochrome devices and it doesn't add anything on other devices either.
- Made `merge.sh` executable
- backlight driver API change: min/max brightness functions are now optional, defaults to [0, 255]
- [zmkfirmware/zmk](https://github.com/zmkfirmware/zmk) [3](https://github.com/zmkfirmware/zmk/commits): trivial: Use USB IF instead of BT SIG namespace (#3505)

Device Information Service 1.1 says that the vendor ID can be either
come from the Bluetooth SIG or USB IF namespace. Zephyr by default uses
1=BTSIG instead of 2=USBIF.

The default VID/PID come from the common-use OpenMoko USB vendor ID.
Also most commercial entities probably have a USB VID but maybe not a
Bluetooth VID.

Logitech devices advertise with this setting set to 2.

Signed-off-by: Daniel Schaefer <dhs@frame.work>
- [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code) [2](https://github.com/abi/screenshot-to-code/commits): Use GPT-6.1 Sol low for the edit variant

Replace GPT-5.6 Terra low with GPT-6.1 Sol low in the all-keys update set
(Gemini 3 Flash minimal stays). Same input price, cheaper cached input
($0.10 vs $0.20/M) and output ($10 vs $12/M).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [anthropics/claude-code](https://github.com/anthropics/claude-code) [2](https://github.com/anthropics/claude-code/commits): chore: Update CHANGELOG.md and feed.xml
- [bumptech/glide](https://github.com/bumptech/glide) [2](https://github.com/bumptech/glide/commits): Introduces an experimental GlideBuilder flag:
`setRespectExifOrientationInImageDecoder(boolean)`.

When enabled, InputStreamBitmapImageDecoderResourceDecoder and
ByteBufferBitmapImageDecoderResourceDecoder inspect EXIF orientation metadata
(via the new shared ExifOrientationOptionsApplier) and set
Downsampler.IS_EXIF_ORIENTATION_REQUIRED when rotation is needed.
DefaultOnHeaderDecodedListener uses this flag to configure ImageDecoder to use
ALLOCATOR_SOFTWARE instead of ALLOCATOR_HARDWARE, preventing redundant hardware
allocations and software canvas blit overhead on rotated captures.

Under the same flag, DefaultOnHeaderDecodedListener also raises the target size
passed to ImageDecoder#setTargetSize to at least one pixel per dimension, so
that very small requested sizes on highly elongated images cannot round down to
zero.

PiperOrigin-RevId: 996853280
- [espressif/esp-matter](https://github.com/espressif/esp-matter) [2](https://github.com/espressif/esp-matter/commits): Merge branch 'fix/set-val-call-callbacks' into 'main'

Fix Callback Handling in attribute::set_val() for Writable attributes

See merge request app-frameworks/esp-matter!1702
- [facebookincubator/muse-gadget-sdk](https://github.com/facebookincubator/muse-gadget-sdk) [2](https://github.com/facebookincubator/muse-gadget-sdk/commits): Fix StopWatch controls and circular icon layout (#163)

* Fix StopWatch controls and circular icon layout

* Turn off StopWatch green LED on battery power
- [google/auto](https://github.com/google/auto) [2](https://github.com/google/auto/commits): Use Maven Wrapper for Auto.

This follows what we've done for a while with Guava (cl/573917287). We've recently seen breakages in our projects from both Maven 3.9.16 and 3.10.0, so it's nice to put the upgrade under our control.

Our release scripts already know to use `./mvnw` in preference to `mvn` if it's available.

RELNOTES=n/a
PiperOrigin-RevId: 996744859
- [josephmisiti/awesome-machine-learning](https://github.com/josephmisiti/awesome-machine-learning) [2](https://github.com/josephmisiti/awesome-machine-learning/commits): Merge pull request #1438 from alexkroman/add-tiny-audio
- [mattpocock/skills](https://github.com/mattpocock/skills) [2](https://github.com/mattpocock/skills/commits): wizard: template fixes (#1220, #1142, #1081, #1041, #1003) (#1237)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [RivoLink/leaf](https://github.com/RivoLink/leaf) [2](https://github.com/RivoLink/leaf/commits): Merge pull request #322 from RivoLink/feat/git-diff-viewer-mode

feat: git diff viewer mode
- [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) [1](https://github.com/anthropics/anthropic-sdk-python/commits): Merge pull request #1007 from anthropics/synced/published

release: 1.13.0
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) [1](https://github.com/anthropics/claude-agent-sdk-python/commits): chore: bump bundled CLI version to 2.1.296
- [AvdLee/appstoreconnect-swift-sdk](https://github.com/AvdLee/appstoreconnect-swift-sdk) [1](https://github.com/AvdLee/appstoreconnect-swift-sdk/commits): Merge pull request #351 from AvdLee/spec-update-4.5.1

Update OpenAPI spec to 4.5.1
- [databendlabs/openraft](https://github.com/databendlabs/openraft) [1](https://github.com/databendlabs/openraft/commits): test: openraft: use TypeConfigExt for time and runtime calls

# Summary

Tests get the current time, sleeps, and oneshot channels from the type
config's runtime instead of naming `TokioInstant`, `TokioRuntime`, or
`std::time::Instant` directly.

# Details

Naming the Tokio types ties a test to Tokio. For example, comparing
`TokioInstant::now()` with `vote_last_modified()`, which returns
`InstantOf<C>`, compiles only while the type config's runtime is Tokio.

`t11_client_reads` also stops using `std::time::Instant`. The
linearizer wait timeout it measures fires on the runtime clock, and a
virtual-clock runtime would make the two clocks differ.
- [dtolnay/thiserror](https://github.com/dtolnay/thiserror) [1](https://github.com/dtolnay/thiserror/commits): Update ui test suite to nightly-2026-10-09
- [GameTec-live/ChameleonUltraGUI](https://github.com/GameTec-live/ChameleonUltraGUI) [1](https://github.com/GameTec-live/ChameleonUltraGUI/commits): feat: Update translations (#1028)
- [headtracker/HeadTracker](https://github.com/headtracker/HeadTracker) [1](https://github.com/headtracker/HeadTracker/commits): Update README.md
- [jackwener/boss-cli](https://github.com/jackwener/boss-cli) [1](https://github.com/jackwener/boss-cli/commits): 修复：支持 Chromium App-Bound Cookie 导入 (#36)

* fix: support Chromium App-Bound cookies via CDP

* fix: constrain CDP import and cover browser cookie flow

---------

Co-authored-by: sublatesublate-design <sublatesublate-design@users.noreply.github.com>
Co-authored-by: jackwener <jakevingoo@gmail.com>
- [johnno1962/SwiftTrace](https://github.com/johnno1962/SwiftTrace) [1](https://github.com/johnno1962/SwiftTrace/commits): Make fishhook submodule to move to vm_protect() - https://github.com/johnno1962/InjectionNext/issues/174
- [KOP-XIAO/QuantumultX](https://github.com/KOP-XIAO/QuantumultX) [1](https://github.com/KOP-XIAO/QuantumultX/commits): Support rule notes and local resource hash parameters

Preserve leading rule notes on build 950+ while applying conversion,
filtering, replacement, policy and CDN changes only to rule bodies.
Strip note metadata for older clients and handle CRLF and malformed notes.

Read local/iCloud path hash parameters on build 951+ with strict
first-line parameter fallback. Keep the parser header timestamp-only.

Validation: 84 regression checks passed in a mocked Quantumult X runtime,
including 11 output comparisons against the previous parser.
- [larksuite/cli](https://github.com/larksuite/cli) [1](https://github.com/larksuite/cli/commits): docs(base): add text cell mention example (#2802)
- [mikf/gallery-dl](https://github.com/mikf/gallery-dl) [1](https://github.com/mikf/gallery-dl/commits): release version 1.32.16
- [omnivore-app/omnivore](https://github.com/omnivore-app/omnivore) [1](https://github.com/omnivore-app/omnivore/commits): fix(puppeteer): fix issue with puppeteer where a timeout would cause the entire page load to fail; sometimes network requests are still active despite the page fully loading (#4727)
- [pointfreeco/sqlite-data](https://github.com/pointfreeco/sqlite-data) [1](https://github.com/pointfreeco/sqlite-data/commits): Add missing visionOS argument for when using UTF8Span to produce CollationOrder. (#562)

Without this the package failed to build inside visionOS producing the following compiler errors:
- UTF8Span is only available in visionOS 26.0 or newer
- isCanonicallyLessThan is only available in visionOS 26.0 or newer
- [smithy-lang/smithy](https://github.com/smithy-lang/smithy) [1](https://github.com/smithy-lang/smithy/commits): Prevent reentrant AbstractCodeWriter state failures (#3314)

Section interceptors can push and pop temporary writer states while popState() visits parent states. Growing the live ArrayDeque invalidates its iterator and can throw ConcurrentModificationException.

Snapshot the parent states before invoking interceptors. This preserves the existing order and stack behavior while allowing scoped context and nested section interception. Add regression tests and a changelog entry.
- [swiftlang/swift-cmark](https://github.com/swiftlang/swift-cmark) [1](https://github.com/swiftlang/swift-cmark/commits): Merge pull request #99 from aniketatgithub/fix-backslash-newline-sourcepos

Fix source positions after backslash hard line breaks
- [swiftlang/swift-corelibs-libdispatch](https://github.com/swiftlang/swift-corelibs-libdispatch) [1](https://github.com/swiftlang/swift-corelibs-libdispatch/commits): Merge pull request #965 from swiftlang/epoll-hup-handling

Handle EPOLLHUP like EV_EOF on linux
- [XiaoMi/xiaomi-miloco](https://github.com/XiaoMi/xiaomi-miloco) [1](https://github.com/XiaoMi/xiaomi-miloco/commits): Merge pull request #578 from XiaoMi/feat/rule-guard-condition

Feat/rule guard condition
- [yaqwsx/KiKit](https://github.com/yaqwsx/KiKit) [1](https://github.com/yaqwsx/KiKit/commits): Preserve KiCad 10 variants in generated panels