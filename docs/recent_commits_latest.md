# Recent Activity in Starred Repositories
_162 active repos with 3410 new commits_

## [ai](https://github.com/topics/ai)
- [openclaw/openclaw](https://github.com/openclaw/openclaw) [612](https://github.com/openclaw/openclaw/commits): chore(diagnostics-otel): revert unapproved duration-bucket merge (#152292)

Reverts a21ca3cebb5ff878ec3f62c2cd4f9a84c167a170 at the task requester’s explicit direction. The upstream merge exceeded the intended fleet-observability scope.
- [BasedHardware/omi](https://github.com/BasedHardware/omi) [98](https://github.com/BasedHardware/omi/commits): C8 slice 1: route the action-items list onto typed ApiResult (clean ancestry) (#14615)

* feat(app): migrate the action-items list onto typed ApiResult

Rehomes the C3.5 action-items migration onto a clean ancestry: real
CaptureSessionOwner-aware action items provider factory, typed list/
load-more/retry wiring in the production Home path, boundary-baseline
adoption, API_RESULTS.md documentation, and the C3 action-items spine
oracle with its registry entry. Ancestry rebuilt from origin/main so the
squash-era blobs that predate the merged C3 oracle revisions do not ride
along.

* fix(app): analyzer-ratchet cleanups for the typed action-items surface

const the two ApiFailure authTransient/decode returns; lift the
@visibleForTesting annotation off sendUncaughtApiCall (executeApi is a
production entry, not test-only); key the action-items retry TextButton
with OmiKeys.actionItemsRetry and register it in the addressability
catalog.

* fix(app): dedupe action-items provider imports in main.dart

The merge-forward left both the retired ActionItemsProvider() registration and a duplicate device_provider import; keep the factory-based registration only.

* test(app): make the c3 action-items wiring test timezone-independent

The fixture pinned a UTC due_at and a UTC now; the provider's Home-today
window is local-midnight based, so UTC+14 runners excluded the fixture.
Drive the fixture and both assertions from the runtime clock instead,
matching how the app itself computes the window.

* Merge remote-tracking branch 'origin/main' into task/msd-core-c3-action-items

Restores backend files that a concurrent main merge touched; unowned drift restored to origin/main bytes.
- [t8y2/dbx](https://github.com/t8y2/dbx) [57](https://github.com/t8y2/dbx/commits): ci(rust): add sccache to packages and agent jobs, drop gha fallback

The packages job compiled dbx-cli/dbx-mcp cargo targets with no cache at
all. agent-rust only had rust-cache, so every lock change recompiled the
bundled duckdb C++ library. The GHA sccache fallback for fork PRs wrote
nothing (0% hits, all writes erroring under the v2 cache service) while
main only populates S3, so forks now build without a wrapper and lean on
the rust-cache restore from main.
- [github/spec-kit](https://github.com/github/spec-kit) [8](https://github.com/github/spec-kit/commits): fix(workflows): exempt bug-fix from PR-count confirmation (#4636)

* chore: upgrade community workflows to gh-aw v0.88.7 (#18)

Regenerate the three community submission locks with Copilot CLI 1.0.80 and the compiler defaults. Preserve submission instructions and file allowlists, and cover runtime compatibility and output guards.

Assisted-by: GitHub Copilot (model: GPT-6 Astra, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix(workflows): exempt bug-fix from PR-count confirmation

Apply the community maintenance-workflow exemption to bug-fix while preserving assessment gates and harness-managed draft publication. Add static exemption and runtime-import coverage.

Assisted-by: GitHub Copilot (model: GPT-6 Astra, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* chore(workflows): refresh maintenance workflow body hashes

Regenerate bug-fix and the three community workflow lockfiles with gh-aw v0.88.7 after the PR-count exemption changes. Only body_hash metadata changes; executable YAML is unchanged.

Assisted-by: GitHub Copilot (model: GPT-6 Astra, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

---------

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
- [herdrdev/herdr](https://github.com/herdrdev/herdr) [8](https://github.com/herdrdev/herdr/commits): test: isolate integration assets from inherited omp environment (#4351)

refs #4346

Co-authored-by: akbash-bot <300245827+akbash-bot@users.noreply.github.com>
Co-authored-by: Can Celik <ogulcancelik@gmail.com>
- [docling-project/docling](https://github.com/docling-project/docling) [7](https://github.com/docling-project/docling/commits): fix: More improvements for chandra ocr parsing (#4277)

* fix: improve Chandra OCR parsing and preserve document structure

Signed-off-by: Christoph Auer <cau@zurich.ibm.com>

* fix: support Chandra OCR reasoning responses

Signed-off-by: Christoph Auer <cau@zurich.ibm.com>

* fix: avoid duplicate Chandra checkbox markers

Signed-off-by: Christoph Auer <cau@zurich.ibm.com>

* Fix double location tags

Signed-off-by: Christoph Auer <cau@zurich.ibm.com>

* More hardening for chandra OCR to docling parsing

Signed-off-by: Christoph Auer <cau@zurich.ibm.com>

---------

Signed-off-by: Christoph Auer <cau@zurich.ibm.com>
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) [6](https://github.com/google-gemini/gemini-cli/commits): fix(core): update auth error documentation link to valid anchor and add fallback (#26140) (#29377)

Co-authored-by: David Pierce <davidapierce@google.com>
- [oraios/serena](https://github.com/oraios/serena) [5](https://github.com/oraios/serena/commits): Merge pull request #2073 from oraios/change-session-handling

Make session IDs explicit tool parameters instead of auto-injecting them
- [XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) [3](https://github.com/XiaomiMiMo/MiMo-Code/commits): feat(session): cascade subagent resume and honest failure terminals (#2430)

* feat(session): cascade subagent resume and honest failure terminals

Main Resume now best-effort restores same-session non-main actors that are
registry-idle with recovery candidates. Lifecycle uses ActorExecution +
runTurn + parent notify; cancel epoch binds at acceptance; admission timeout
interrupts pending work. Missing ForkContext fails at the source (resume/send
share one terminal). running/pending rows are never auto-takeover.

Send continue relies on drain + classify (no abandon-before-drain). Tests
cover POST resume, dual-child delivery, stop/admission barriers, and real
sweep recoverability text.

* fix(session): drop session Resume from model-facing recoverability copy

Main agent does not know the Desktop concept "session Resume". Settle
error and actor.txt only tell it to send continue / re-spawn.

* fix(session): recoverability copy uses actor send, not literal continue

Any follow-up inbox send wakes the subagent; "continue" was only an
example. Settle error and actor.txt no longer prescribe that word.

* test(session): lengthen missing-fork waits for CI runners

Shard 2/4 failed when notification/registry settle exceeded ~4s.
Poll up to 10s for failed notify + missing fork lastError.

* test(session): make missing-fork negatives CI-stable

Join the wake path (wake:false + prompt.loop/inboxWake) instead of
racing forked inbox.wake. Cascade test now asserts admission then polls
the background settle.

* test(session): seed main slice for missing-fork notify drain

inbox.drain cannot seed a parent notification without a prior
model-bearing main message, so the failed-notify assertion never saw
the row. Mirror the route/multi-child fixtures.
- [s2b-dev/smart-second-brain](https://github.com/s2b-dev/smart-second-brain) [2](https://github.com/s2b-dev/smart-second-brain/commits): docs(readme): mention widgets in the Agents bullet (#509)

Co-authored-by: Claude <noreply@anthropic.com>

## [ai-agent](https://github.com/topics/ai-agent)
- [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) [28](https://github.com/CherryHQ/cherry-studio/commits): feat(provider-registry): add Moonshot AI global endpoint (#18835)

Add a built-in moonshot-global provider serving the international
endpoint (https://api.moonshot.ai, plus the /anthropic mirror) with the
international console links. It folds under the existing moonshot
preset, mirroring the minimax/minimax-global pair: shared reasoning
format, web-search server-tool declaration, and K2.6/K3 reasoning
overrides are extracted in moonshot.ts so the two endpoints cannot drift
apart. The English label of the CN entry is disambiguated to "Moonshot
CN" (same pattern as "MiniMax CN" / "MiniMax").

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

Before this PR:
The built-in Moonshot provider only ships the China endpoint
(https://api.moonshot.cn) with links to the CN console
([platform.moonshot.cn](http://platform.moonshot.cn/)). Users who signed
up on the international console (platform.moonshot.ai) hold API keys
that only work against https://api.moonshot.ai, so they have to
hand-create a custom OpenAI-compatible provider and copy the base URL
from the docs.

After this PR:
A new built-in moonshot-global provider serves the international
endpoint (https://api.moonshot.ai, plus the /anthropic mirror) with the
international console links. It folds under the existing moonshot preset
(same sidebar group, same icon, same runtime extension), mirroring the
existing minimax / minimax-global pair. The English label of the CN
entry is disambiguated to “Moonshot CN” (same pattern as “MiniMax CN” /
“MiniMax”).

<!-- (optional, in `fixes #<issue number>(, fixes #<issue_number>, ...)`
format, will close the issue(s) when PR gets merged)*: -->

Fixes #

### Why we need it and why it was done in this way
Moonshot operates two separate consoles and key pools:
[platform.moonshot.cn](http://platform.moonshot.cn/) (CN) and
[platform.moonshot.ai](http://platform.moonshot.ai/) (global). Keys are
not interchangeable across hosts; the global host is the one documented
to overseas users.

The following tradeoffs were made:
- `moonshot-global` reuses the exact connection behavior of the CN
preset — the reasoning format (`thinking.type` wire), the Kimi
`$web_search` server-tool declaration, and the K2.6/K3 reasoning
overrides are extracted to shared exports in `moonshot.ts` and
referenced by both, so the two endpoints cannot drift apart.
- `presetProviderId: 'moonshot'` routes runtime config through the
existing Moonshot extension (`matchesPreset`), so no new adapter code
was needed; the extension declares `aliases: ['moonshot-global']` like
`MinimaxExtension` does.
- The provider icon reuses the existing `moonshot` mark via
`PROVIDER_ID_ALIASES`.

The following alternatives were considered:
- Changing the existing provider's default host to `.ai`: rejected, it
would break every existing CN user.
- A host dropdown inside one provider entry: larger UI change; the
registry already has the dual-entry precedent (`minimax-global`, also
`zai`→`zhipu` folding), so this PR follows it.

Links to places where the discussion took place: <!-- optional: slack,
other GH issue, mailinglist, ... -->

### Breaking changes

None for functionality. One user-visible label change: the English
display name of the existing CN entry changes from "Moonshot" to
"Moonshot CN" (zh and other locales unchanged). Happy to drop that hunk
if you prefer keeping the old label.

<!-- optional -->

If this PR introduces breaking changes, please describe the changes and
the impact on users.

### Special notes for your reviewer

- `data/providers.json` / `data/provider-models.json` /
`src/patterns/server-tool-models.gen.ts` contain only the
`moonshot-global` rows: the catalog was regenerated with `pnpm --filter
@cherrystudio/provider-registry generate`, then unrelated daily model
drift was reverted (the daily auto-update workflow owns that churn).
- `src/shared/utils/systemProviderId.ts` regenerated with `pnpm
gen:system-provider-ids`.
- Verified: `pnpm lint` (oxlint + eslint + typecheck + i18n check +
biome), `vitest --project provider-registry` (315 tests), `vitest
--project main` for `config.test.ts` incl. the new routing cases
asserting `moonshot-global` → providerId `moonshot` with baseURL
`https://api.moonshot.ai/v1` (112 tests).

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
Added a built-in "Moonshot AI" (global, api.moonshot.ai) provider entry alongside the existing CN endpoint, so users of the international Moonshot console can connect without a custom provider.
```

---------

Signed-off-by: Tony Yu <49832190+ysntony@users.noreply.github.com>
Signed-off-by: suyao <sy20010504@gmail.com>
Co-authored-by: suyao <sy20010504@gmail.com>
- [trycua/cua](https://github.com/trycua/cua) [6](https://github.com/trycua/cua/commits): docs(cua-driver): propose optional perception extension boundary (#3934)

* docs(cua-driver): add perception extension RFC

* docs(cua-driver): link perception RFC pull request

* docs(cua-driver): link perception draft workstreams

* docs(rfc): link capture registry draft

* docs(rfc): link worker restriction spike

* docs(rfc): link topology and extension drafts

* docs(rfc): link snapshot transform draft

* docs(rfc): record perception delivery decisions

* docs(cua-driver): accept perception extension RFC

## [ai-agents](https://github.com/topics/ai-agents)
- [lycorp-jp/sim-use](https://github.com/lycorp-jp/sim-use) [1](https://github.com/lycorp-jp/sim-use/commits): Merge pull request #129 from lycorp-jp/dependabot/npm_and_yarn/Tools/Viewer/browserslist-4.28.9

build(deps-dev): bump browserslist from 4.28.6 to 4.28.9 in /Tools/Viewer
- [steipete/agent-scripts](https://github.com/steipete/agent-scripts) [1](https://github.com/steipete/agent-scripts/commits): fix(xcode-sync): guard selected toolchains with bounded smoke checks

## [claude-code](https://github.com/topics/claude-code)
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) [4](https://github.com/Piebald-AI/claude-code-system-prompts/commits): Update changelog for v2.1.277
- [slopus/happy](https://github.com/slopus/happy) [4](https://github.com/slopus/happy/commits): fix(cli): explain expired Claude provider login

Report host-side Claude authentication failures through existing session events and failed turn status. Preserve manual retry without automatic replay.

Fixes #1791
Reported by @f-liva.
- [sirmalloc/ccstatusline](https://github.com/sirmalloc/ccstatusline) [1](https://github.com/sirmalloc/ccstatusline/commits): perf: keep the TUI off the status line render path (#575)

Claude Code re-runs this binary every couple of seconds for as long as a
session is open, so module load time is paid continuously rather than once.

src/ccstatusline.ts imports runTUI statically, which pulls ink, React and
yoga-layout into the render path even though rendering never touches them.
Making that import dynamic is not enough on its own: --outfile cannot split,
so the whole graph still gets parsed. Building with --splitting moves the TUI
into its own chunk and shrinks the entry from 3.34 MB to 21 KB.

Measured on an M-series Mac, 20 runs per data point, real payload piped in:

  before  238, 237, 238 ms/render
  after   226, 222, 220 ms/render

That is roughly 7%, and the rendered output is byte-identical. The
interactive TUI was smoke-tested under a pty and behaves the same.

scripts/replace-version.ts had to change too: with splitting the
__PACKAGE_VERSION__ placeholder lands in a chunk rather than in
dist/ccstatusline.js, so patching only the entry would have silently
shipped an unreplaced placeholder. It now patches every emitted script and
fails loudly when it finds none.

Packaging is unaffected: files is already dist/, and bin/main/exports keep
pointing at dist/ccstatusline.js. Verified the built output runs under node
as well as bun.

Assisted-by: claude:claude-opus-5

Co-authored-by: Matthew Breedlove <sirmalloc@gmail.com>

## [cross-platform](https://github.com/topics/cross-platform)
- [cjpais/Handy](https://github.com/cjpais/Handy) [5](https://github.com/cjpais/Handy/commits): release 0.9.7
- [xyproto/algernon](https://github.com/xyproto/algernon) [1](https://github.com/xyproto/algernon/commits): Update dependencies

## [esp32](https://github.com/topics/esp32)
- [arendst/Tasmota](https://github.com/arendst/Tasmota) [5](https://github.com/arendst/Tasmota/commits): Change default behaviour to hashCeck = disabled (#25037)

* Add support for LoRaWAN sensor discovery for Home Assistant

See https://github.com/arendst/Tasmota/discussions/24398#discussioncomment-15649631

* Introduce hashCheck to LwDecoDrgD20

Add hashCheck variable to LwDecoDrgD20 class.
- [schreibfaul1/ESP32-audioI2S](https://github.com/schreibfaul1/ESP32-audioI2S) [4](https://github.com/schreibfaul1/ESP32-audioI2S/commits): If the http-request was unsuccessful; use a different User-Agent
- [crosspoint-reader/crosspoint-reader](https://github.com/crosspoint-reader/crosspoint-reader) [3](https://github.com/crosspoint-reader/crosspoint-reader/commits): fix: tear down WiFi when leaving the Settings network screen (#3613)

## Summary

* **What is the goal of this PR?**
* Ensure Wi-Fi resources are released when leaving `Settings → Network`,
even if the user only scans for networks.

* **What changes are included?**
* Disconnect Wi-Fi when leaving the Settings network screen and perform
a silent restart when Wi-Fi was activated.
* Add a Settings restart target so the device returns to Settings after
cleanup instead of Home.

## Additional Context

* This route did not use the normal Wi-Fi shutdown path.
`WifiSelectionActivity` is opened as a child of `SettingsActivity`; when
it closes, only the child’s `onExit()` runs. That cleanup removes scan
results but intentionally leaves Wi-Fi management to the parent. In the
other Wi-Fi flows, the parent activity exits and its `onExit()`
disconnects Wi-Fi before calling the normal silent restart. From
Settings, that parent exit never occurs, so the previous callback only
saved settings and left Wi-Fi active.
* If Wi-Fi was never enabled, no restart is requested. When it was
enabled, the cleanup restart returns the user to Settings.
* Fixes #3343
- [espressif/idf-extra-components](https://github.com/espressif/idf-extra-components) [2](https://github.com/espressif/idf-extra-components/commits): Merge pull request #839 from StevenYang77/feat/led_strip_spi_dataout_invert

fix(led_strip): use official SPI data-out inversion when available
- [espressif/arduino-esp32](https://github.com/espressif/arduino-esp32) [1](https://github.com/espressif/arduino-esp32/commits): fix(periman): correct ETHERNET_MCD typo to ETHERNET_MDC (Management Data Clock) (#12908)

* fix(periman): add ESP32_BUS_TYPE_ETHERNET_MDC with backward-compatible MCD alias

* fix(periman): update perimanGetTypeName to return ETHERNET_MDC

* fix(eth): rename private member _pin_mcd to _pin_mdc in ETHClass

* fix(eth): update MDC pin member and peripheral bus registration

* ci(pre-commit): Apply automatic fixes

---------

Co-authored-by: pre-commit-ci-lite[bot] <117423508+pre-commit-ci-lite[bot]@users.noreply.github.com>
- [RavenSystem/esp-homekit-devices](https://github.com/RavenSystem/esp-homekit-devices) [1](https://github.com/RavenSystem/esp-homekit-devices/commits): Home Accessory Architect v12.19.0 Merlin

## [ethereum](https://github.com/topics/ethereum), [solidity](https://github.com/topics/solidity)
- [ethereumbook/ethereumbook](https://github.com/ethereumbook/ethereumbook) [2](https://github.com/ethereumbook/ethereumbook/commits): fix(ch. 6): gas payment (#1323)
- [foundry-rs/forge-std](https://github.com/foundry-rs/forge-std) [1](https://github.com/foundry-rs/forge-std/commits): chore(ci): add secure runner across workflows (#914)

Add the pinned secure-runner action before checkout in build, test,
formatting, typo, CodeQL, and release-branch sync jobs, with job-scoped
OIDC permissions. The matrix generator and final result aggregation do
not install dependencies and are unchanged.

Foundry/solc binaries and Git dependencies are not covered by registry
package checks.

Validation: actionlint passed (with existing Depot labels configured
where needed), git diff --check passed, and a YAML coverage audit
confirmed the first-step ordering, OIDC permissions, preserved
triggers/matrices, and intended exclusions. Offline zizmor introduced no
new findings relative to the base branch; existing findings remain.
GitHub CI and workflows triggered only by schedules/releases/Dependabot
still require runtime validation.

The action's documented fork-PR fallback skips package-policy
enforcement when GitHub withholds OIDC. Existing caches are retained and
are not rescanned.

Prepared with AI assistance.

Prompted by: @grandizzy

Co-authored-by: grandizzy <38490174+grandizzy@users.noreply.github.com>
- [foundry-rs/foundry-toolchain](https://github.com/foundry-rs/foundry-toolchain) [1](https://github.com/foundry-rs/foundry-toolchain/commits): chore(ci): add secure runner across workflows (#177)

Add the pinned secure-runner action before checkout in the
cross-platform tests, dist verification, CodeQL, and Dependabot dist
rebuild. Grant job-scoped OIDC permissions and preserve frozen pnpm
installs and the existing same-repository Dependabot guard. Pass the bot
branch name through a quoted environment variable when pushing dist
changes.

The final result aggregation is unchanged. Foundry/solc binaries and Git
dependencies are not covered by registry package checks.

Validation: actionlint passed (with existing Depot labels configured
where needed), git diff --check passed, and a YAML coverage audit
confirmed the first-step ordering, OIDC permissions, preserved
triggers/matrices, and intended exclusions. Offline zizmor introduced no
new findings relative to the base branch; existing findings remain.
GitHub CI and workflows triggered only by schedules/releases/Dependabot
still require runtime validation.

The action's documented fork-PR fallback skips package-policy
enforcement when GitHub withholds OIDC. Existing caches are retained and
are not rescanned.

Prepared with AI assistance.

Prompted by: @grandizzy

Co-authored-by: grandizzy <38490174+grandizzy@users.noreply.github.com>

## [free](https://github.com/topics/free)
- [public-apis/public-apis](https://github.com/public-apis/public-apis) [26](https://github.com/public-apis/public-apis/commits): Merge pull request #7364 from finalburner/add-rankfabrik-jobs

Add RankFabrik Jobs API
- [gibbok/typescript-book](https://github.com/gibbok/typescript-book) [2](https://github.com/gibbok/typescript-book/commits): Grant pull request write permission to website E2E (#257)

## [golang](https://github.com/topics/golang)
- [twmb/franz-go](https://github.com/twmb/franz-go) [18](https://github.com/twmb/franz-go/commits): Merge pull request #1469 from twmb/record-reader-no-progress

kgo: error when a record consumes no input
- [cshum/imagor](https://github.com/cshum/imagor) [2](https://github.com/cshum/imagor/commits): chore: docs title update

## [ios](https://github.com/topics/ios)
- [Snapchat/Valdi](https://github.com/Snapchat/Valdi) [7](https://github.com/Snapchat/Valdi/commits): Internal Change

GitOrigin-RevId: 9f8e2e9dbba1d92067d64ff68234353ad6ee7816
- [doronz88/pymobiledevice3](https://github.com/doronz88/pymobiledevice3) [2](https://github.com/doronz88/pymobiledevice3/commits): Merge pull request #1967 from doronz88/bugfix/rsd-handshake-stable-uuid

remotexpc: Share one host-wide UUID across RSD handshakes (iOS 27.2)
- [supabase/supabase-swift](https://github.com/supabase/supabase-swift) [2](https://github.com/supabase/supabase-swift/commits): chore: declare the passkey capabilities the SDK implements (#1373)

listPasskeys, renamePasskey and deletePasskey on AuthClient, and
listPasskeys and deletePasskey on AuthAdmin, have been there since the
passkey support landed, but the matrix still reported five capabilities
as missing. They are `@_spi(Experimental)` like the two already declared
implemented, so the symbol graph never carries them and only the status
can record them.
- [fastlane/fastlane](https://github.com/fastlane/fastlane) [1](https://github.com/fastlane/fastlane/commits): [spaceship] Add support for domain association with Apple Pay merchant IDs, domain verify method(s) (#30230)

* feat: expose api surface for apple pay merchants' associated domains

* add get method for downloadDomainVerificationFile

* feat: add verify domain for apple pay merchants

* fix: properly guard string delete and base64 methods

* merchant wrappers for verification file, verify methods

* specs for new merchant and portal client methods

* refactor: ctor override for merchant domain

* test: update merchant domain e2e for fixed platform check
- [majd/ipatool](https://github.com/majd/ipatool) [1](https://github.com/majd/ipatool/commits): fix: fall back to consumer catalogs for ios version lookup

## [llm](https://github.com/topics/llm)
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) [826](https://github.com/NousResearch/hermes-agent/commits): fix(bedrock): resolve application-inference-profile ARNs before the prompt-cache allowlist match

build_converse_kwargs gated cachePoint markers on the raw model id, so a profile ARN wrapping
Claude matched nothing in _CACHE_POINT_PATTERNS and silently lost Bedrock prompt caching.
_model_supports_prompt_cache now resolves the profile through the per-process-cached
_resolve_inference_profile_model_id first; the request still targets the profile ARN.

Part of #114476
- [BerriAI/litellm](https://github.com/BerriAI/litellm) [347](https://github.com/BerriAI/litellm/commits): Merge pull request #41878 from BerriAI/litellm_requeue_daily_spend_without_redis_buffer

fix(proxy): requeue daily spend rows when the commit fails without the Redis buffer
- [kortix-ai/suna](https://github.com/kortix-ai/suna) [216](https://github.com/kortix-ai/suna/commits): Merge pull request #7417 from kortix-ai/manifest-imports

feat(manifest): `imports:` — split kortix.yaml across files
- [unslothai/unsloth](https://github.com/unslothai/unsloth) [60](https://github.com/unslothai/unsloth/commits): Stop one test's app settings answering another test's read (#11309)

* Stop one test's app settings answering another test's read

test_chat_absent_model_with_only_resolver_withheld_checkpoints fails as
`assert 500 == 404` in the (Python 3.13, l-r) shard and nowhere else. This is the
half of #11241 that stayed open all session because nothing reproduced it.

The CI traceback named it:

    Error loading model: '_B' object has no attribute 'load_model'
      File "studio/backend/routes/inference.py", line 16213, in _load_model_impl

`_B` is the withheld tests' own backend double, reached through _load_model_impl --
a LOAD path those tests must never take.

_wire_unloaded_chat pins every input for determinism (local catalog, resolver,
auto-switch, both backends) and misses auto-download. get_openai_auto_download_enabled
is `stored AND auto_switch`, and auto_switch IS pinned to True there, so the answer is
whatever `stored` says. `stored` comes from _cached_setting, a module-level memo with
_CACHE_TTL_S = 2.0 and no test isolation, so a neighbouring test that read that setting
hands this one its value and the refusal becomes a fetch-and-load.

Reproduced by seeding the memo the way a neighbour would:

    seeded True  -> not 404, takes the auto-download path
    seeded False -> 404, as the test expects

That is why no amount of reordering found it. It is not an ordering bug, it is a clock:
only tests landing inside a two second window are affected, which is why it shows up in
the full shard and never in a single-file run, and why CPU contention, a leaked managed
account and a stranded waiter all came back clean.

Two independent layers:

- _wire_unloaded_chat pins auto-download off, which is what line 6190 of this same file
  already does for the one test that thought to.
- an autouse fixture clears the memo around every test, so no process-wide settings cache
  can carry across tests at all.

Sabotage, each hitting its own test: remove the wiring pin and the new regression test
fails; drop the fixture's entry clear or its exit clear and the fixture test fails, each
with its own message. The fixture test drives the fixture directly rather than relying on
two tests running in order, since under --dist loadgroup that pair can land on different
workers and pass by luck.

test_openai_auto_switch.py: 695 passed, 1 skipped.
Full studio/backend/tests vs a clean-main baseline: nothing fails only on this branch.

* [pre-commit.ci] auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

---------

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>
- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) [44](https://github.com/QwenLM/qwen-code/commits): feat(web-shell): show a Goal's turn and active-time ceilings on the status strip (#12201)

The strip above the composer showed spend against the token budget but
active time with no ceiling and no turn figure at all, so a Goal armed
with model.goalMaxTurns or model.goalMaxActiveMinutes showed how far it
had run and not how much room was left; only the workspace Goals dialog
did. The strip now reads 12m 3s / 30m 0s and 3 / 20 turns when those
ceilings are set, and is unchanged for a Goal without them. The dialog
takes its active-time label from the same helper.
- [langgenius/dify](https://github.com/langgenius/dify) [35](https://github.com/langgenius/dify/commits): refactor(models): pass session into App.tenant (#42518)

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
- [google/adk-python](https://github.com/google/adk-python) [24](https://github.com/google/adk-python/commits): refactor: extract tool-resolution steps into tool_request_processors

Extract the three hard-coded tool-resolution calls in
`BaseLlmFlow._preprocess_async` (`_resolve_toolsets_and_auth`,
`_attach_agent_tools`, and `_finalize_dynamic_instructions`) into standalone
request processors (`_toolset_auth.request_processor`,
`_agent_tools.request_processor`, and `_dynamic_instructions.request_processor`)
held in `BaseLlmFlow.tool_request_processors`, and unify `_preprocess_async`
into a single loop over `self._iter_request_processors()`.

Keeping `request_processors` and `tool_request_processors` as two lists that run
back-to-back preserves the invariant that subclasses appending custom processors
to `self.request_processors` always run before toolset authentication and tool
resolution populate `llm_request.tools_dict`.

Co-authored-by: Shangjie Chen <deanchen@google.com>
PiperOrigin-RevId: 984130302
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) [21](https://github.com/screenpipe/screenpipe/commits): perf(activity): bound representative text lookup by frame range (#7111)
- [gptme/gptme](https://github.com/gptme/gptme) [16](https://github.com/gptme/gptme/commits): test(shell): make SIGTERM regression independent of inherited SIG_IGN (#3877)

* test(shell): make SIGTERM regression independent of inherited SIG_IGN

SIG_IGN is inherited across exec. When a pytest worker had SIGTERM ignored
(observed on master CI runs 35382892924 and 35340263104), the CLI child kept
that disposition, so main() never installed its handler: the 'terminate' case
timed out and 'default-return' hit an empty AssertionError caught by main()'s
'Fatal error' path. Reset the child to SIG_DFL before the per-mode setup.

Reproduced locally by running the test under a parent with SIGTERM ignored
(2 failed -> 4 passed).

Git-Session-Id: 111b5e86-9348-5d06-b789-031ba1866358

* test(shell): also unblock SIGTERM in the child, since the signal mask survives exec

An adversarial merge-gate pass on this PR noted the same inheritance hazard
for the signal mask: a worker with SIGTERM blocked makes the terminate case
hang exactly like SIG_IGN does. Reproduced: with SIGTERM blocked in the parent
and no unblock, test_cli_sigterm_cleans_background_job[terminate] fails; with
it, all four modes pass.

Git-Session-Id: eec7bbed-b0b9-5efe-88e3-959b7088dbf4
- [jundot/omlx](https://github.com/jundot/omlx) [16](https://github.com/jundot/omlx/commits): chore: bump version to 0.7.0.dev4
- [jjang-ai/vmlx](https://github.com/jjang-ai/vmlx) [9](https://github.com/jjang-ai/vmlx/commits): Publish vMLX 1.6.63 updater manifest
- [JerryZLiu/Dayflow](https://github.com/JerryZLiu/Dayflow) [5](https://github.com/JerryZLiu/Dayflow/commits): release: update appcast for v2.5.4
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) [4](https://github.com/OpenHands/OpenHands/commits): test: cover MCP config utilities (#17344)

Co-authored-by: openhands <openhands@all-hands.dev>
Co-authored-by: Engel Nyst <engel.nyst@gmail.com>
Co-authored-by: enyst <enyst@users.noreply.github.com>
- [cactus-compute/needle](https://github.com/cactus-compute/needle) [1](https://github.com/cactus-compute/needle/commits): Document telemetry settings in README

Added information about telemetry settings in README.
- [google/langextract](https://github.com/google/langextract) [1](https://github.com/google/langextract/commits): Surface blocked Gemini batch items instead of returning empty output (#537)
- [winfunc/opcode](https://github.com/winfunc/opcode) [1](https://github.com/winfunc/opcode/commits): Remove image from README.md

## [machine-learning](https://github.com/topics/machine-learning)
- [stefan-jansen/machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) [7](https://github.com/stefan-jansen/machine-learning-for-trading/commits): The skip-blocker guard measured whatever data root the machine had (#1113)

* The skip-blocker guard measured whatever data root the machine had

`tests/skip_blockers.py` says a skip condition has to be a property of the CI
fixture, and rejects `ML4T_ARTIFACT_ROOT` as an instrument for exactly that
reason. Its own file half then took `_resolve_data_path()`, which returns
whatever this machine holds: on a workstation with the full dataset that is
`/home/stefan/Dropbox/ml4t/data`, which carries the raw ITCH and IEX captures
and the futures contract definitions that three declarations say the fixture
lacks. The guard called all three expired and told the reader to un-skip
notebooks that red CI, and the evaluator's own negative control asserted a real
fixture path was absent while the file was there.

`_fixture_root` now returns a root only when it is a checkout of
`ml4t/third-edition-test-data`, which is what every site mounting the fixture
checks out, and raises `NotTheFixture` otherwise. That is a subclass of
`UndecidableHere`, so a notebook run honours the skip - an unmeasurable
condition is not evidence the blocker has gone - while the guard test reports it
as a skip rather than erroring. The rest of `UndecidableHere` stays uncaught:
"the fixture is here and the seeding produced no registry" is still loud.

Nothing silently disables the guard in CI. `test-unit-data` checks out the
fixture and fails the job on any skipped test, so a discriminator that stopped
recognising it turns the whole file red there instead of passing quietly.

Local run goes from 4 failed, 74 passed to 76 passed, 7 skipped, each skip
naming the root it refused to measure.

* Test the refusal itself, not only the discriminator it calls

The two tests added with the previous commit exercise `is_ci_fixture` against
synthetic checkouts, and nothing reached `_fixture_root`: deleting the
`raise NotTheFixture` left the whole file green while restoring the failure the
commit fixes. Four tests now cover the wiring, all independent of which machine
runs them - `_fixture_root` refuses a non-fixture root and still returns None
when no root resolved at all, `honoured_skip_reason` keeps an
`absent_fixture_path` skip standing on a root that holds the named file but is
not the fixture, and reports the expiry when the same file appears inside a
fixture checkout. Replacing the refusal with a no-op now fails six tests, two of
them machine-independent.

Also: `test_holdout_selection_is_single_sourced.py` pointed at
`tests/skip_blockers.py:158` for the deliberate `NoSelectableCandidates` catch,
which the previous commit pushed to line 223. It names the function now, so the
next insertion does not stale it again.
- [skypilot-org/skypilot](https://github.com/skypilot-org/skypilot) [4](https://github.com/skypilot-org/skypilot/commits): [Slurm] Support reduced sudo permissions without container snapshots (#10820)

* [Slurm] Support reduced sudo permissions without container snapshots

* [Slurm] Resolve submit-user environment variables best effort

* [Slurm] Isolate snapshots across same-name cluster lifecycles
- [akuity/awesome-argo](https://github.com/akuity/awesome-argo) [1](https://github.com/akuity/awesome-argo/commits): Add ArgoCon 2026 links

## [macos](https://github.com/topics/macos)
- [pqrs-org/Karabiner-Elements](https://github.com/pqrs-org/Karabiner-Elements) [10](https://github.com/pqrs-org/Karabiner-Elements/commits): Update localizations
- [dwarvesf/hidden](https://github.com/dwarvesf/hidden) [7](https://github.com/dwarvesf/hidden/commits): chore: make Hidden Bar the direct-build scheme (#408)

Keep the familiar scheme name for the GitHub build: "Hidden Bar" now runs
Debug-Direct and archives Release-Direct, and the sandboxed App Store lane
moves to a new "Hidden Bar App Store" scheme. Drop "Hidden Bar Direct" and
update the runbook.

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
- [acsandmann/rift](https://github.com/acsandmann/rift) [4](https://github.com/acsandmann/rift/commits): chore: bump ver
- [mattt/iMCP](https://github.com/mattt/iMCP) [4](https://github.com/mattt/iMCP/commits): Connect over loopback after Bonjour discovery (#229)
- [ViennaRSS/vienna-rss](https://github.com/ViennaRSS/vienna-rss) [2](https://github.com/ViennaRSS/vienna-rss/commits): Merge pull request #2168 from barijaona/mainBranchGoldenGate

Workaround for working on Xcode 27 (master branch)
- [MarkEdit-app/MarkEdit](https://github.com/MarkEdit-app/MarkEdit) [1](https://github.com/MarkEdit-app/MarkEdit/commits): Style table delimiters (#1754)

## [markdown](https://github.com/topics/markdown)
- [foambubble/foam](https://github.com/foambubble/foam) [12](https://github.com/foambubble/foam/commits): Refuse to build a fork's branch

An issue_comment workflow runs in the base repo's context, so this job holds
the subscription token and a write-capable App token — and it now installs,
builds and runs the checked-out branch. On a fork's PR that hands both to
code we don't control, through lifecycle scripts before a test ever runs.

A maintainer commenting @claude is the trigger, but the branch is what
executes, so the actor check is not the control that matters here. The job
now refuses outright when the PR is cross-repository.

Also drops Bash(node:*): running the suite already implies running repo code,
so the extra grant bought nothing.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
- [RivoLink/leaf](https://github.com/RivoLink/leaf) [4](https://github.com/RivoLink/leaf/commits): Merge pull request #289 from RivoLink/chore/support-editor-env-var

chore: support editor env var

## [middleware](https://github.com/topics/middleware)
- [thingsboard/thingsboard](https://github.com/thingsboard/thingsboard) [5](https://github.com/thingsboard/thingsboard/commits): Merge pull request #16164 from thingsboard/rc

Merge rc into master
- [bloomberg/blazingmq](https://github.com/bloomberg/blazingmq) [3](https://github.com/bloomberg/blazingmq/commits): Feat(bmqt): add constants for `SessionOptions` defaults

This patch exposes constants whose values are the `SessionOptions`s
defaults.

Signed-off-by: Patrick M. Niedzielski <pniedzielski@bloomberg.net>

## [python](https://github.com/topics/python)
- [adafruit/circuitpython](https://github.com/adafruit/circuitpython) [16](https://github.com/adafruit/circuitpython/commits): Merge pull request #11418 from weblate/weblate-circuitpython-main

Translations update from Hosted Weblate
- [xlwings/xlwings](https://github.com/xlwings/xlwings) [15](https://github.com/xlwings/xlwings/commits): Merge pull request #2757 from xlwings/codex/conditional-formats-followup

Strengthen conditional format snapshots
- [arnegiacomo/fugleramme](https://github.com/arnegiacomo/fugleramme) [13](https://github.com/arnegiacomo/fugleramme/commits): chore(assets): add baeolophus bicolor (#120)

refs #33
- [nltk/nltk](https://github.com/nltk/nltk) [7](https://github.com/nltk/nltk/commits): Merge pull request #3899 from alvations/robust-dos-timing-bounds

Make DoS/ReDoS timing regression tests load-invariant (fix CI flakiness)
- [dbcli/mycli](https://github.com/dbcli/mycli) [6](https://github.com/dbcli/mycli/commits): Merge pull request #2257 from dbcli/RW/tweak-uv-tool-run

Tweak `uv tool run` suggestion
- [rushter/selectolax](https://github.com/rushter/selectolax) [6](https://github.com/rushter/selectolax/commits): Make ruff happy
- [miguelgrinberg/microdot](https://github.com/miguelgrinberg/microdot) [4](https://github.com/miguelgrinberg/microdot/commits): Release 2.7.0
- [pavdmyt/yaspin](https://github.com/pavdmyt/yaspin) [4](https://github.com/pavdmyt/yaspin/commits): Merge pull request #276 from pavdmyt/version_3.5.1

release: bump version, update history

Version 3.5.1
- [esphome/esphome](https://github.com/esphome/esphome) [3](https://github.com/esphome/esphome/commits): [socket] Fix set_sockaddr() accepting malformed IPv4 addresses (#19394)

Co-authored-by: Claude Sonnet 5 <noreply@anthropic.com>
- [pyodide/pyodide](https://github.com/pyodide/pyodide) [3](https://github.com/pyodide/pyodide/commits): Add .DS_Store to gitignore [skip ci] (#6469)
- [lakehq/sail](https://github.com/lakehq/sail) [2](https://github.com/lakehq/sail/commits): fix: correct Delta statistics for dotted columns and all-null files (#2604)
- [lemon24/reader](https://github.com/lemon24/reader) [2](https://github.com/lemon24/reader/commits): EntryCounts and EntrySearchCounts inherit from a common base.
- [microsoft/FLAML](https://github.com/microsoft/FLAML) [2](https://github.com/microsoft/FLAML/commits): fix: qrandint/qlograndint never sample the documented inclusive upper bound (#1606)

* fix: qrandint/qlograndint never sample the documented inclusive upper bound

Quantized.sample()'s q=1 fast path skips quantization and calls the wrapped
Integer sampler directly, which draws exclusive of domain.upper, same as
plain randint. Since qrandint defaults to q=1, its own "upper is also
inclusive (!)" docstring was never true. For q>1 the general branch rounds
a raw exclusive-upper draw, so reaching the nominal upper depends on the
rounding fraction.

Fixed by extending the sampled range by one quantization step for Integer
domains before drawing, then clamping back to the true upper bound. Plain
randint/lograndint never go through Quantized, so they are untouched.

Fixes #1605

* fix: sample quantization grid indices directly, not rounded draws

The q=1 fast path for Integer domains routed through float division,
turning integer samples into np.float64 and losing precision above
2**53. For q>1, extending the raw draw's range by a full q and
clamping the overshoot into the top bin gave that bin roughly 1.4x
the width of an interior bin (measured with a fixed seed: 40164 vs
~39800 draws per bin over 200000 samples on a 5-bin grid, expected
40000 each).

Draw the grid point's index directly instead: every point, including
the top one, is reachable through exactly one raw index, so no bin
is over- or under-represented and the result stays a plain int with
no rounding.

Added scalar/batched dtype tests, a large-bound precision test past
2**53, and a fixed-seed bin distribution test that would have caught
the top-bin bias.

* fix: sample real grid indices, not ones rebased to 1, and use exact integer arithmetic

Addresses thinkall's second review round on #1606: qlograndint drew log-
uniformly over an index range rebased to start at 1, which is a different,
shifted distribution from the actual value grid whenever lower > q (log-
uniform is scale-invariant under multiplication, not under an additive
shift). Switched to the grid's own index (value // q). Also replaced the
remaining float division for computing grid bounds with integer ceiling/
floor division, and the batched Integer path now returns an int64 ndarray
instead of a Python list, matching the historical container and dtype.

* fix: preserve list return for batched q>1 quantized integer sampling

Quantized.sample()'s Integer branch unconditionally returned an ndarray
for size > 1, but only q == 1 historically did; q > 1 returned a plain
Python list (matching the float quantization path's list(quantized)).
Return a list for q > 1 and keep the ndarray only for q == 1.

Updated the two tests that asserted ndarray for a q > 1 domain so they
check the correct historical container instead.

* fix: preserve batched q=1 sampler dtype in Quantized.sample

* fix: avoid int64 overflow multiplying quantized batch indices by q

Grid points above 2**63 - 1 wrapped silently through numpy int64
multiplication in the batched q > 1 Integer path; multiply each index
as a Python int instead.

* fix: restore CRLF line endings in flaml/tune/sample.py

The prior merge from main flattened this file's CRLF line endings to
LF, so the PR diff showed the whole file as removed and re-added
instead of the actual ~30-line change.

* fix: restrict Quantized's integer grid-index transform to the two built-in samplers

A custom sampler on an Integer domain got the grid-index domain (and,
for q > 1, its output multiplied by q) unconditionally, which breaks
any sampler that reads domain.lower/domain.upper or returns actual
values rather than an index. Only Integer._Uniform and
Integer._LogUniform use the grid transform now; every other sampler
keeps the historical actual-value contract, q == 1 calling it directly
and q > 1 falling through to the existing float-based quantization.

* fix: restore float unit quantization at q == 1

The custom-sampler-contract fix (6320d970) widened the q == 1 direct
passthrough from Integer-only to isinstance(domain, Integer) == False
domains too, so a Float domain (quniform/qloguniform/qrandn) at q == 1
skipped the round-to-nearest-unit step entirely and returned the raw
unrounded sample. Scope the passthrough back to Integer domains, which
is what it was gating before this round's change.

test/tune/test_unit_quantization.py::test_unit_quantization_rounds_float_samples
covers this; it fails on the current head (6 of 18 parametrizations,
all q=1) and passes with this fix.

---------

Co-authored-by: Li Jiang <bnujli@gmail.com>
- [coleifer/peewee](https://github.com/coleifer/peewee) [1](https://github.com/coleifer/peewee/commits): Ensure we don't scrap non-ascii but valid identiifers.

Fixes #3078
- [confident-ai/deepeval](https://github.com/confident-ai/deepeval) [1](https://github.com/confident-ai/deepeval/commits): Merge pull request #3289 from tony-confidentai/feat/docs-site-path

feat(docs): carry the docs pages read to app signup links

## [rust](https://github.com/topics/rust)
- [embassy-rs/embassy](https://github.com/embassy-rs/embassy) [26](https://github.com/embassy-rs/embassy/commits): Merge pull request #7031 from embassy-rs/ptp-global-queue-2

net: await stack-wide TX timestamps
- [rmk-rs/rmk](https://github.com/rmk-rs/rmk) [15](https://github.com/rmk-rs/rmk/commits): Merge pull request #1154 from rmk-rs/feat/pmw3610-force-awake-on-active

feat(pmw3610): follow the keyboard's sleep state with force_awake
- [crate-ci/typos](https://github.com/crate-ci/typos) [4](https://github.com/crate-ci/typos/commits): chore: Rename master to main
- [dora-rs/dora](https://github.com/dora-rs/dora) [3](https://github.com/dora-rs/dora/commits): fix(node-api): clamp pattern-wait timeout to avoid Instant+Duration overflow panic (#3538)

`EventStream::wait_for_correlation` — the shared engine behind the public
`recv_service_response` and `recv_action_result` pattern helpers — computed
an absolute deadline as `Instant::now() + timeout` from the caller-supplied
`Duration`. A very large value, e.g. `Duration::MAX` used to mean "wait
effectively forever", overflows the monotonic clock and panics with
`overflow when adding duration to instant`, aborting the whole process.

The C++ binding already guards the identical computation on the FFI side
(`clamp_pattern_timeout` in `apis/c++/node`), noting that "the pattern
helpers compute `Instant::now() + timeout` internally"; the Rust-native
callers were left unguarded.

Add a `representable_wait_deadline` helper that reads the clock once and
halves the timeout until `now + timeout` is representable, returning the
`Instant` deadline directly. A caller asking for an enormous wait now gets
the longest representable deadline instead of a crash. (`futures_timer::Delay`
already saturates a huge duration to a ~30-year deadline, so the loop body is
safe once the deadline is guarded.)

Adds a unit test asserting a normal timeout yields a near-future deadline and
`Duration::MAX` yields a future deadline rather than panicking.

Machine-generated by an automated Claude Code review agent; no human has
reviewed this change. Please review carefully before merging.


Claude-Session: https://claude.ai/code/session_01MUMG4MrFiPKiwjC8xvtH3d

Co-authored-by: Claude <noreply@anthropic.com>
- [nextest-rs/nextest](https://github.com/nextest-rs/nextest) [2](https://github.com/nextest-rs/nextest/commits): Update Rust crate indexmap to 2.14.2 (#3603)
- [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) [1](https://github.com/ast-grep/ast-grep/commits): feat(outline): add Java record_declaration rule (#2945)

* feat(outline): add Java record_declaration rule

The bundled Java outline rules had no rule for `record_declaration`, so a
file whose only type is a `record` produced no outline elements at all, even
though both the grammar and `schemas/java_rule.json` already know the kind.

Add a `java-record` item rule mapping `record_declaration` to
`symbolType: struct`, mirroring the existing `csharp-record` rule, and list it
as a parent for the Java member rules so a record's methods, constructors and
fields are attributed to the record instead of an enclosing type.

Closes #2944

* feat(outline): recognize Java compact record constructors

Add a java-member-compact-constructor member rule targeting the
compact_constructor_declaration grammar node, alongside the existing
java-member-constructor, and snapshot a record with a compact constructor.
- [crate-ci/cargo-release](https://github.com/crate-ci/cargo-release) [1](https://github.com/crate-ci/cargo-release/commits): chore: Rename master to main
- [notify-rs/notify](https://github.com/notify-rs/notify) [1](https://github.com/notify-rs/notify/commits): fix(poll): detect subsecond symlink mtime changes (#1004)

## [s3](https://github.com/topics/s3)
- [Altinity/clickhouse-backup](https://github.com/Altinity/clickhouse-backup) [3](https://github.com/Altinity/clickhouse-backup/commits): Merge pull request #1570 from Altinity/issue-1568

Keep mapped object disk restores from sharing keys with the source table
- [Kuingsmile/PicList](https://github.com/Kuingsmile/PicList) [2](https://github.com/Kuingsmile/PicList/commits): :package: Chore: update eslint,prettier,node-bump-version config

## [usb](https://github.com/topics/usb), [usb-host](https://github.com/topics/usb-host)
- [hathach/tinyusb](https://github.com/hathach/tinyusb) [4](https://github.com/hathach/tinyusb/commits): Use agentrc defaults for chief and pr-babysit, document config-free bench locks (#3936)

- Drop TinyUSB's pr-babysit reviewer overrides in favour of agentrc's defaults
- Document the human's yes that authorizes a headless chief to drive a PR
- Allow HIL remote selection and lock forcing only when the task scope names them
- Document that a named-board lock needs no config, while hil_test.py and
  hil_pool_check.py still need the host's config
- [cherry-embedded/CherryUSB](https://github.com/cherry-embedded/CherryUSB) [1](https://github.com/cherry-embedded/CherryUSB/commits): update(port/wch): add device port speed parameter handle

## [wearable](https://github.com/topics/wearable), [wearables](https://github.com/topics/wearables)
- [OpenStrap/edge](https://github.com/OpenStrap/edge) [43](https://github.com/OpenStrap/edge/commits): fix: serialize widget push() so concurrent calls can't interleave (#416)

resume, post-derive, and bg-wake all fire WidgetService.refresh->push()
unawaited with no lock. push() writes ~20 keys with an await between
each, so two overlapping calls could interleave their writes and land
a snapshot mixing fields from two different days. chain push() through
a static future so overlapping calls run strictly one after another.
- [Mentra-Community/MentraOS](https://github.com/Mentra-Community/MentraOS) [37](https://github.com/Mentra-Community/MentraOS/commits): Merge pull request #4106 from Mentra-Community/secure-gallery-http-server

Add persistent gallery HTTP server control to Bluetooth SDK

## Other
- [Ephemeral-AI-Lab/layerfs](https://github.com/Ephemeral-AI-Lab/layerfs) [111](https://github.com/Ephemeral-AI-Lab/layerfs/commits): docs(#184): record the three round-5 rulings in the prompt, the plan and the issue

Owner rulings, 2026-09-19, replacing the open questions the prompt carried:

  * the golden number **reports and does not gate**, and does not drive the budget.
    `operation_ns` is the report's primary axis and the number tracked round to round;
    counters, heap and disk keep deciding, because D1's +17.6% same-binary spread cannot
    separate O(n) from O(log n). Making `elapsed_ns` gate-decide stays a CONTRACT.md
    change and is not this round's.
  * `FilesystemRead::inode` is **in scope with its own confirmation**: it is scoped into
    #184 as its own item, and both sides of the classification must be pinned by a test
    before any product source changes, with a blocker reported rather than guessed.
  * the **digest key is the product identity plus a declared fixture-recipe version**,
    with the producer binary recorded in the manifest as provenance and validated on
    load rather than keyed. Keying on it would invalidate every master on every harness
    edit and leave the round permanently cold.

The prompt's section is retitled from "Open questions to resolve" to "Rulings — do not
re-open these", so the round-5 agent does not spend a ruling on them again.

Documentation only. No harness behaviour changed.

Production LOC: 84936 -> 84936 (delta 0)
- [facebook/idb](https://github.com/facebook/idb) [66](https://github.com/facebook/idb/commits): Detect a crashed dtuhidd instead of discarding HID events

Summary:
On a macOS 26 host with an iOS 27 runtime, `dtuhidd` aborts during boot and every HID event sent afterwards is discarded without an error.

The daemon's own start-up races the guest's. CoreSimulator demand-launches `dtuhidd` early in boot; it asks CoreAnimation for the display list and `query_displays()` calls `abort()` when no display is up yet. A crash report from an affected boot:

```
dtuhidd  EXC_CRASH (SIGABRT)
  abort()
  QuartzCore  query_displays() + 1752
  QuartzCore  ensure_displays()
  QuartzCore  +[CADisplay displays]
  CoreDeviceUtilities ...
```

Whether it loses is a function of how slow the boot is, so it is intermittent on an idle host and reliable on a loaded one. On one captured boot the daemon launched 0.4s in, aborted at 14:00:08.9 while the device was still `WaitingOnBackboard`, and the transport connected at 14:00:09.6 -- 0.6s after its peer had died.

Nothing on the client side could observe that. `SimDevice.lookup:error:` vends a port for a demand-launched job whether or not it can run, the connection builds against a daemon launchd has crashed and throttled, `xpc_connection_set_event_handler` discarded every event including the errors, and the barrier timeout in `performColdDrain` was swallowed into a fixed sleep.

`SimulatorDTUHIDTransport.dtuhid(for:)` now round-trips a barrier before handing the transport out, and retries with backoff when nothing answers. The crash window closes once the boot settles, so a retry recovers the full transport rather than losing the keyboard: D117706226 established that Indigo keeps buttons but not keyboard on Xcode 27+, which makes falling back a partial mitigation and worth exhausting the retries first. `livenessAttempts` is sized from a measured recovery of roughly 19s after boot completion, which is launchd's exponential respawn throttle rather than the daemon's own start-up.

The lookup is inside the retried attempt rather than ahead of it. It fails while the job is being torn down to respawn, which is the state the retry exists to ride out, so hoisting it turns the most recoverable moment into a terminal one. `isTransientDTUHIDFailure` keeps that distinct from absent `_4sim` symbols, which no amount of waiting changes.

This is a probe of the connection, not of process residency: D115593130 removed residency as a signal because `dtuhidd` is demand-launched and pressured-exit, so a daemon that is merely not resident is healthy. It also holds here that an explicitly requested `.dtuhid` never silently degrades -- only the auto-negotiated path falls back, and only through the existing `isDTUHIDUnreachable` seam.

A successful probe also means the peer activated, which is what `performColdDrain` otherwise waits for on the first gesture, so its tail is paid at connect and kept out of the user's first touch.

The underlying abort is an Apple defect; this makes the transport survive it rather than removing it.

## Scope, and a separate finding

Investigating "simulator input is dead" turned up two independent causes, and this diff addresses only the first. The second is a caller-side bug, fixed separately in the consuming project: `lifecycle.connectToHID()` vends the simulator's *cached* HID, and `SimulatorNotificationUpdateStrategy` closes that cache via `terminateConnections()` on any CoreSimulator device state-change notification. Those arrive asynchronously, so the notification for a boot that has just finished can land a second or two after a caller has already connected, and the holder of the returned `SimulatorHID` gets no signal at all. `dtuhidd` then cancels all six of its virtual HID services in response to the peer leaving, so the only trace is `No active service, dropping event` in the guest log. That caller now owns its connection instead.

That is worth raising here rather than only in the caller: any consumer holding a `connectToHID()` result across a device state change has the same silent failure, and the API gives it nothing to detect it with.

## Follow-ups

Left to a refactor diff on top of this one, per review: `DTUHIDDrainClock` has grown into a bundle of injected closures and should become a protocol with a live implementation and a test implementation. That also removes the no-op default on `awaitLivenessReply`, which today lets a call site that omits the argument get a probe that always succeeds, and it is the natural place to stop `DispatchTimeInterval` rendering as `seconds(4)` inside the liveness diagnostic.

Reviewed By: lawrencelomax

Differential Revision: D120445384

fbshipit-source-id: 8a0a497e15fdde200bc3e0f8f2cee1c50386f08d
- [openai/codex](https://github.com/openai/codex) [43](https://github.com/openai/codex/commits): Remove `com.apple.runningboard` from Seatbelt platform defaults (#46532)

GitOrigin-RevId: 746bc891b26813edfff339637400d519198708d9
- [buildroot/buildroot](https://github.com/buildroot/buildroot) [39](https://github.com/buildroot/buildroot/commits): support/testing: test_squid: new runtime test

Signed-off-by: Julien Olivain <ju.o@free.fr>
Signed-off-by: Thomas Petazzoni <thomas.petazzoni@bootlin.com>
- [earendil-works/pi](https://github.com/earendil-works/pi) [24](https://github.com/earendil-works/pi/commits): fix: clean up delta test lint diagnostics
- [awesomedata/awesome-public-datasets](https://github.com/awesomedata/awesome-public-datasets) [20](https://github.com/awesomedata/awesome-public-datasets/commits): Update README sha: 3e094907e483ea305f23dd87e47c0147ee8cfb42
- [tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro) [18](https://github.com/tensorflow/tflite-micro/commits): [CI] Bump Docker container version to 0.6.10 (#3756)
- [cline/cline](https://github.com/cline/cline) [13](https://github.com/cline/cline/commits): feat(desktop): add Check for Updates menu item to app and tray menus (#14276)

Users could only wait for the 2h background updater cycle and its toast.
Add a "Check for Updates..." item to the macOS application menu (under
About) and the tray menu on every platform. The label follows the updater
state (checking/downloading disabled, "Restart to Update to vX" once an
update is staged). Clicking it restarts into a staged update directly;
otherwise the webview runs the on-demand check and toasts the outcome
(update ready / up to date / failed).

Co-authored-by: Saoud Rizwan <saoudrizwan@users.noreply.github.com>
- [signalapp/libsignal](https://github.com/signalapp/libsignal) [13](https://github.com/signalapp/libsignal/commits): AuthAccountsService.startMfaVerification and finishMfaVerification
- [alibaba/open-code-review](https://github.com/alibaba/open-code-review) [12](https://github.com/alibaba/open-code-review/commits): chore(idea): rename the Marketplace listing and set version 0.1.0 (#1438)

The bare "Open Code Review" name is already taken on JetBrains
Marketplace, so the upload was rejected under it.
- [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) [10](https://github.com/ghostty-org/ghostty/commits): terminal: add option to disable scrollback pull on resize (#14296)

#14294

This adds a boolean flag throughout the Zig API and C API to control
whether resizing can pull scrollback back into the active area. The
default is true, which is the existing behavior.

Ptys that keep their own screen buffer without scrollback (namely
Windows ConPTY) can't pull rows back, so after a resize that pulls we
disagree with the pty about what is on screen and subsequent output
lands in the wrong place.

Row growth always appends blank rows at the bottom when pulling is
disabled.

Refs:

https://github.com/microsoft/terminal/blob/7c92ecd037476f957809d0813b14d8bc44bb071a/src/cascadia/TerminalCore/Terminal.cpp#L380-L406
https://github.com/xtermjs/xterm.js/blob/c58ea3637f3968e0e6e79cd92cf9aace7ef89ee2/src/common/buffer/Buffer.ts#L194-L197
https://github.com/wezterm/wezterm/blob/b09b56c29c1e367e598b60ca266e2cc9038751e0/term/src/screen.rs#L268-L288
- [typst/typst](https://github.com/typst/typst) [10](https://github.com/typst/typst/commits): Load SVG image linked from an SVG image (#8391)

Co-authored-by: Laurenz <laurmaedje@gmail.com>
- [GNOME/librsvg](https://github.com/GNOME/librsvg) [9](https://github.com/GNOME/librsvg/commits): Update NEWS

Part-of: <https://gitlab.gnome.org/GNOME/librsvg/-/merge_requests/1213>
- [THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC) [9](https://github.com/THU-MAIC/OpenMAIC/commits): fix(audio): rebuild platform FormData bodies for the undici transport (#1580)

#1514 moved every lib/audio provider call to the npm undici package's
fetch so the pinned dispatcher is guaranteed to be honored. But the
adapters kept building multipart bodies with the platform-global
FormData — a class of Node's bundled undici — and undici's serializer
brand-checks a FormData body against its own class. A foreign FormData
fell through to the string branch and left the process as
`content-type: text/plain;charset=UTF-8` with the 17-byte literal
`[object FormData]` as the whole body: the audio bytes and every field
(including `model`) were dropped, downstream gateways fell back to
whisper-1 and answered 503, and every multipart audio request (ASR,
TTS FormData paths, voice registration/cloning) failed with a generic
internal error.

Bare Blob/File, string/JSON/Buffer and stream bodies were never
affected: undici 7.29.0 exports no File/Blob classes of its own and
its bare-body brand checks (and multipart part handling) bind the
platform classes.

Normalize the body in the transport, once, before either transport
path serializes it, so the adapters can keep the platform globals as
their public API boundary: a foreign FormData is re-created as
undici's own with every entry carried over verbatim — `append` (not
`set`) so repeated field names survive, and no filename argument so a
platform File part keeps its own name/type/lastModified. Everything
else passes through untouched.

Also drive real loopback regression tests with a platform-global
FormData (direct, with repeated field names, empty, and across a 307
redirect hop whose per-hop loop re-issues the normalized body) and a
bare Blob, asserting multipart on the wire instead of
`[object FormData]`, and update the voxcpm unit test that asserted
the buggy contract (a platform FormData at the undici boundary).

Fixes #1579

Co-authored-by: Claude Code <noreply@anthropic.com>
Co-authored-by: wyuc <wang-yc24@mails.tsinghua.edu.cn>
- [ChrisBuilds/terminaltexteffects](https://github.com/ChrisBuilds/terminaltexteffects) [8](https://github.com/ChrisBuilds/terminaltexteffects/commits): Remove unused ANSI utility APIs
- [jdx/mise](https://github.com/jdx/mise) [8](https://github.com/jdx/mise/commits): feat(daemons): set a fixed namespace and run daemons from another project (#13339)

Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
- [anthropics/claude-code](https://github.com/anthropics/claude-code) [7](https://github.com/anthropics/claude-code/commits): diff: the first edit opens the pane only from the main loop with checkpointing on, and an open the engine leaves waiting is withdrawn (#95476)
- [espressif/esp-nn](https://github.com/espressif/esp-nn) [7](https://github.com/espressif/esp-nn/commits): Merge branch 'perf/fc-batched-s8' into 'master'

perf(fc/s3): batched per-channel FC (weight-stationary over rows)

See merge request espressif/esp-nn!54
- [jqlang/jq](https://github.com/jqlang/jq) [7](https://github.com/jqlang/jq/commits): perf: avoid the intermediate array in from_entries (#3626)

Define `from_entries` as `add(.[] | f) // {}` instead of
`map(f) | add // {}`. Since `add(f)` is `reduce f as $x (null; . + $x)`,
both fold the same values in the same order from the same seed, so the
only difference is that the array of single-key objects built by `map`
is never materialized.

Measured with both the generator and the result suppressed, so that only
the `from_entries` work differs: 6-15% less user time across input shapes,
which is 10-24% of what `from_entries` itself costs. For inputs above
roughly a thousand entries, peak RSS drops by 37%, around 80% of the
memory `from_entries` adds on top of its input; a 1,000,000 entry array
goes from 1064 MiB to 672 MiB.
- [ratsark/oepl-cc2630-firmware](https://github.com/ratsark/oepl-cc2630-firmware) [7](https://github.com/ratsark/oepl-cc2630-firmware/commits): DEVELOPMENT: queueing an OTA tells the tag to sleep for an hour

contentmode 5 sets nextupdate = 3216153600 on the AP, so the nextCheckIn it
hands out is enormous and the tag sleeps its 3600 s cap. A tag that was
mid-cycle when the OTA was queued therefore goes quiet for a full hour, which
is indistinguishable from a dead tag -- Weather6 did exactly this today,
13:33 to 14:35, and was fine.

Both tags are now on v0.26 (reported version 38): bench tag displaying a
pushed test card, Weather6 displaying weather again after a clean apply
(OTA-APPLIED sectors=6 retries=0 unverified=0).

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EgYBSh93LDt8zjKAArdzTz
- [verl-project/verl](https://github.com/verl-project/verl) [7](https://github.com/verl-project/verl/commits): [vllm, rollout] feat: support W4A8 MXFP rollout refit on Ascend (#7868)

Enables W4A8 MXFP rollout refit in veRL on Ascend 950 npu devices.

### What does this PR do?

We bring W4A8 MXFP quantization refit to verl through vllm-ascend
rollout. Working in tandem with the PR
<[vllm-ascend#16568](https://github.com/vllm-project/vllm-ascend/pull/16568)>,
one can specify `quantization="ascend"` to refit W4A8 MXFP weights on
ascend 950 devices.

### Checklist Before Starting

- [x] Search for similar PRs. Paste at least one query link here:
[verl#5756](https://github.com/verl-project/verl/pull/5756)
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

Tested end-to-end with the veRL RL rollout weight refit on Ascend 950.

Model: Qwen3-30B

### API and Usage Example

adding the following arugment in the starting script



```python
actor_rollout_ref.rollout.quantization="ascend" \
```

### Design & Code Changes

> Demonstrate the high-level design if this PR is complex, and list the
specific changes.

### Checklist Before Submitting

> [!IMPORTANT]
> Please check all the following items before requesting a review,
otherwise the reviewer might deprioritize this PR for review.

- [x] Read the [Contribute
Guide](https://github.com/verl-project/verl/blob/main/CONTRIBUTING.md).
- [x] Apply [pre-commit
checks](https://github.com/verl-project/verl/blob/main/CONTRIBUTING.md#code-linting-and-formatting):
`pre-commit install && pre-commit run --all-files --show-diff-on-failure
--color=always`
- [x] Add / Update [the
documentation](https://github.com/verl-project/verl/tree/main/docs).
- [x] Add unit or end-to-end test(s) to [the CI
workflow](https://github.com/verl-project/verl/tree/main/.github/workflows)
to cover all the code. If not feasible, explain why: ...
- [x] Once your PR is ready for CI, send a message in [the `ci-request`
channel](https://verl-project.slack.com/archives/C091TCESWB1) in [the
`verl` Slack
workspace](https://join.slack.com/t/verl-project/shared_invite/zt-3855yhg8g-CTkqXu~hKojPCmo7k_yXTQ).
(If not accessible, please try [the Feishu group
(飞书群)](https://applink.larkoffice.com/client/chat/chatter/add_by_link?link_token=772jd4f1-cd91-441e-a820-498c6614126a).)
- [x] If your PR is related to the `recipe` submodule, please also
update the reference to the submodule commit via `git submodule update
--remote` or `cd recipe && git pull origin main`.

Signed-off-by: zaney9880 <zaney121122@gmail.com>
Co-authored-by: yyyy2000 <yezhibei@huawei.com>
- [block/buzz](https://github.com/block/buzz) [6](https://github.com/block/buzz/commits): release: push gateway chart 0.3.1 (#7749)

Publishes chart 0.3.1 for `buzz-push-gateway`, containing #7717.

Signed-off-by: Tom Brow <tomb@block.xyz>
- [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) [6](https://github.com/ggml-org/whisper.cpp/commits): fix(yt-wsp): Resolve script path without GNU realpath (#4072)

macOS ships BSD realpath, which rejects -e and is missing on older
releases. Use plain realpath when present, otherwise cd and pwd -P.

Fixes #530

Co-authored-by: Aurora-NICExq <Aurora-NICExq@users.noreply.github.com>
- [mkuthan/homelab-public](https://github.com/mkuthan/homelab-public) [5](https://github.com/mkuthan/homelab-public/commits): Add tags for pi playbook
- [openshwprojects/OpenBK7231T_App](https://github.com/openshwprojects/OpenBK7231T_App) [5](https://github.com/openshwprojects/OpenBK7231T_App/commits): ota: bounds check on /api/flash only covers the first chunk, and runs after init_ota (#2189)

* ota: check the whole upload against maxaddr, and check it before init_ota

Two things went wrong here, both reachable from one POST to /api/flash/<addr>.

The bounds check tested writelen, which is only the part of the body that
arrived with the headers, usually well under a kilobyte. The loop underneath
then writes towrite bytes, which comes from Content-Length, advancing startaddr
as it goes and never checking again. A large Content-Length with a small first
chunk therefore walks straight past maxaddr. Check towrite, since that is what
actually gets written.

The check also ran after init_ota, which clears flash write protection and
mallocs the sector buffer. Bailing out at that point returns without
close_ota(), so the buffer is never freed and protection is never restored.
init_ota refuses to start while sector is non-null, so one rejected upload
leaves OTA broken until the next reboot. Validate first, then init.

* ota: make the range check overflow safe and reject empty writes

startaddr + towrite is signed arithmetic, so a large content length can
wrap it negative and the sum then compares below maxaddr, passing the
check it was meant to fail. Compare with a subtraction instead, with the
operands guarded first so maxaddr - startaddr cannot go negative, and
reject a zero length in the same condition so an empty post no longer
reaches init_ota.
- [witnessmenow/ESP32-Cheap-Yellow-Display](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display) [5](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/commits): Add GymSession example (#417)
- [ccusage/ccusage](https://github.com/ccusage/ccusage) [4](https://github.com/ccusage/ccusage/commits): chore: consolidate agent instructions on AGENTS.md (#1769)

AGENTS.md is the cross-agent convention and Claude Code reads it too, so a
separate CLAUDE.md is redundant.

The removed CLAUDE.md files were symlinks to the AGENTS.md in the same
directory, so no content is lost. .claude/CLAUDE.md was a regular file and is
renamed to .claude/AGENTS.md.
- [databendlabs/openraft](https://github.com/databendlabs/openraft) [4](https://github.com/databendlabs/openraft/commits): change: openraft: gate heartbeats after quorum loss

# Summary

Add an opt-in heartbeat gate that alternates quiet and send periods after a
Leader's quorum evidence expires, giving the reachable quorum time to elect a
replacement.

# Details

`Config::quorum_loss_probe_interval` sets each phase length. The phase is
derived from the latest quorum-acknowledged timestamp, or
`RaftState::vote_last_modified()` before the first quorum acknowledgement, so
the policy needs no activity state, commands, or coordination channel.

Only heartbeat emission is gated. Replication and snapshots continue, and a
fresh quorum acknowledgement immediately restores normal heartbeat behavior.
`None` preserves existing behavior. The interval must be at least
`leader_lease + election_timeout_max`.

Upgrade tip: Add `quorum_loss_probe_interval` to exhaustive `Config` literals
and handle `ConfigError::QuorumLossProbeIntervalTooSmall` in exhaustive
matches. Existing named-field configurations default the new field to `None`.

- Fix: #2080
- [RfidResearchGroup/proxmark3](https://github.com/RfidResearchGroup/proxmark3) [4](https://github.com/RfidResearchGroup/proxmark3/commits): Fixed bug on the PM5 platform where changing PM3_CMD_DATA_SIZE to a larger value broke compatibility for certain commands.
- [adafruit/Adafruit_CAD_Parts](https://github.com/adafruit/Adafruit_CAD_Parts) [3](https://github.com/adafruit/Adafruit_CAD_Parts/commits): Rename s.jpg to 292 LCD Backpack I2C SPI.jpg

yes
- [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) [3](https://github.com/anthropics/anthropic-sdk-python/commits): Merge pull request #1939 from anthropics/release-please--branches--main--changes--next

release: 1.7.0
- [git-up/GitUp](https://github.com/git-up/GitUp) [3](https://github.com/git-up/GitUp/commits): Bump continuous appcast to b1059
- [kenjihiranabe/The-Art-of-Linear-Algebra](https://github.com/kenjihiranabe/The-Art-of-Linear-Algebra) [3](https://github.com/kenjihiranabe/The-Art-of-Linear-Algebra/commits): MatrixWorld-ja to j.
- [lancedb/lancedb](https://github.com/lancedb/lancedb) [3](https://github.com/lancedb/lancedb/commits): chore: update lance dependency to v13.0.0-beta.6 (#4224)

Updates the Rust workspace Lance dependencies, Cargo lockfile, and Java
lance-core from 13.0.0-beta.4 to
[v13.0.0-beta.6](https://github.com/lance-format/lance/releases/tag/v13.0.0-beta.6).
Fixes the redundant visibility qualifier on the internal identifier
delimiter constant reported by Clippy.

Validation: `cargo clippy --quiet --workspace --tests --all-features --
-D warnings`, `cargo fmt --all --quiet`, and `git diff --check`.
- [ophub/amlogic-s9xxx-armbian](https://github.com/ophub/amlogic-s9xxx-armbian) [3](https://github.com/ophub/amlogic-s9xxx-armbian/commits): Update dtb for rk3528-xingyicloud
- [rhaiscript/rhai](https://github.com/rhaiscript/rhai) [3](https://github.com/rhaiscript/rhai/commits): Use atomic counter to enable updating operations count after scripted function callback from native function.
- [sushi-labs/sushiswap](https://github.com/sushi-labs/sushiswap) [3](https://github.com/sushi-labs/sushiswap/commits): Fix/perps input (#2304)

* fix: use logical or

* fix: use logical or
- [andrewyng/aisuite](https://github.com/andrewyng/aisuite) [2](https://github.com/andrewyng/aisuite/commits): Merge pull request #414 from andrewyng/rp/release-0.2.0

Release 0.2.0
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) [2](https://github.com/anthropics/claude-agent-sdk-python/commits): chore: bump bundled CLI version to 2.1.277
- [astral-sh/ty](https://github.com/astral-sh/ty) [2](https://github.com/astral-sh/ty/commits): Sync the ty security mirror (#4549)

`ty-security` needs to follow public `main` while its default branch
remains locked. Add an STS-backed workflow and a policy rule granting it
`contents: write` and `workflows: write` only for the pinned
`ty-security` repository ID. The sync fast-forwards to a verified public
commit, refuses private or divergent history, and keeps private objects
and remote diagnostics out of the public workflow. After this lands,
`ty-security/main` needs a one-time fast-forward to receive the policy
before automated sync can authorize itself.

---------

Co-authored-by: zaniebot <242828183+zaniebot@users.noreply.github.com>
- [espressif/esp-adf-libs](https://github.com/espressif/esp-adf-libs) [2](https://github.com/espressif/esp-adf-libs/commits): Merge branch 'feature/add_dual_h264_encode_support' into 'master'

esp_video_codec: Added dual H264 encode support

See merge request adf/esp-adf-libs!355
- [espressif/esp-dl](https://github.com/espressif/esp-dl) [2](https://github.com/espressif/esp-dl/commits): Merge branch 'feat/mobilenet' into 'master'

feat: update mobilenet benchmark

See merge request ai/esp-dl!349
- [espressif/esp-gmf](https://github.com/espressif/esp-gmf) [2](https://github.com/espressif/esp-gmf/commits): Merge branch 'bugfix/fix_treat_status_200_as_success_range_seek' into 'main'

fix(gmf_io): Fix treat status 200 as success range seek

See merge request adf/multimedia/esp-gmf!517
- [espressif/esp-sr](https://github.com/espressif/esp-sr) [2](https://github.com/espressif/esp-sr/commits): Merge branch 'add_ja_model' into 'master'

feat: add アイリス wn10 model

See merge request speech-recognition-framework/esp-sr!235
- [input-output-hk/daedalus](https://github.com/input-output-hk/daedalus) [2](https://github.com/input-output-hk/daedalus/commits): Merge pull request #3410 from input-output-hk/sl/fix-snapshot-converter

fix(watchdog): fix snapshot-converter command and capture stderr
- [larksuite/cli](https://github.com/larksuite/cli) [2](https://github.com/larksuite/cli/commits): fix(apps): stop the db/file commands from misdirecting the caller on failure (#2719)

* fix(apps): classify the db publish-approval rejection instead of hinting at multi-env

When an app's release goes through publish approval, the server refuses
+db-env-migrate with subcode k_dl_4000052. That subcode was unmapped, so the
failure surfaced as subtype "unknown" carrying the per-command fallback hint
("ensure the app is multi-env and has pending dev changes"), which points at two
things that are both already correct and sends the caller to +db-env-create — an
irreversible no-op here. No flag, environment or app id makes the CLI path
succeed while the approval is configured, so the failure has to read as "not via
this channel" rather than "fix the request".

- Map k_dl_4000052 in dbSubcodeTable as api/feature_not_available; the hint
  states that the app requires release approval, names the two ways to release
  it (+release-create or the web console), and notes that +db-env-diff still
  previews the pending changes
- Keep exit 1: exit 2 would tell an agent to change the request and retry, exit 3
  would send it to re-authenticate, and neither can succeed
- Document the rejection under +db-env-migrate in the apps db reference so agents
  move to the release flow instead of retrying

* fix(apps): point the file commands' --jq examples at the envelope

--jq runs against the whole response envelope, but three file commands
advertised bare payload paths: +file-quota-get suggested -q '.usage_percent',
+file-get suggested -q '.size_bytes' / -q '.download_url', and +file-upload
suggested -q '.path'. Every one of them resolves to null and still exits 0 —
the worst shape for an agent, which reads a successful exit with an empty value
as "the server returned nothing" rather than "the example is wrong". The other
eight --jq examples in this domain already carry the .data prefix, so these
three were the outliers.

- Prefix the four expressions with .data, matching the rest of the domain
- Note on +file-quota-get that usage_percent only appears once a quota is
  provisioned; the command omits it (with storage_quota_bytes) when the backend
  reports quota 0, so the example would otherwise look broken against an app
  that has no quota yet
- Add TestTips_JQExpressionsAddressTheEnvelope, which rejects any tip whose --jq
  path starts outside the envelope's top-level keys. The check is structural, so
  it needs no live response and covers commands whose payload shape is
  server-dependent
- Split the root extraction into jqRootField and cover it directly: expressions
  that name no field (".", ".?", ". | .", ".[]") are all valid jq, and indexing
  the split result would have panicked on two of them and misread ".[]" as the
  field "]"

* fix(apps): report usage_percent at one decimal in both quota commands

+db-quota-get and +file-quota-get passed the server's raw percentage straight
through, so a 2 GB quota produced readings like 5.40924072265625 and
0.4398345947265625. The tail is float64 representation noise, not measurement —
it resolves to roughly a megabyte on that quota, while the companion
storage_used_bytes already carries the exact figure. It reads as false precision
and costs an agent context on digits that carry nothing.

- Round usage_percent to one decimal in both projections via a shared
  roundUsagePercent, so the two commands cannot drift apart
- Keep it a JSON number rather than a formatted string: callers compare it
  (-q '.data.usage_percent > 80'), and whole values encode as "2" not "2.0"
- Do not clamp above 100 — the server deliberately reports over-quota as-is, and
  folding 180% to 100% would hide the one reading that must stay visible
- Leave the field out entirely when it is absent or non-numeric, rather than
  writing a 0 that would read as "nothing used"
- Cover the wire-observed values, the whole-number and over-quota cases, and a
  json.Marshal assertion so a rounded float cannot serialise a tail back

pretty output is unchanged: it already formatted with %.1f.

* test(apps): cover the download_url round trip in the file commands

A download_url the platform hands out was rejected by the very commands that
take a --path: +file-get, +file-sign and +file-download all answered 400000034
"File not found or no access". An agent cannot tell that apart from a genuinely
missing file, so it reads the platform's own output as invalid and stops. The
resolution is server-side — the CLI forwards --path verbatim — so a unit test
cannot see a regression here and only a live call can.

- Upload a file, read its download_url back rather than constructing one (a
  hand-built URL would test this test's idea of the format, not the format
  callers are actually handed), then feed it to all three commands
- Assert each resolves to the real path, and compare the downloaded bytes: a
  response that wrote an error body would still exit 0
- Add a negative case so the compatibility cannot degrade into "accept
  anything" — an absent file must still fail not_found in both the plain-path
  and download_url shapes, which is also what stops the positive cases from
  passing against a server that skipped the lookup entirely
- Fixture-gated like the sibling upload workflow, and deletes what it uploads

Verified to discriminate: green against a backend carrying the fix, and red on
exactly the three round-trip cases (negative case still green) against one
without it.

* fix(apps): stop reporting a wrong app id as a missing permission

The storage permission chain answered three unrelated states with one code and
one sentence — "user need admin or developer permission": the caller genuinely
lacked a role, the app could not be found, or the argument was never an app id
at all. Only the first is a permission problem. The other two sent people off to
request access they already had, and sent agents to exit 3, which says
"re-authenticate" and cannot resolve either.

The backend now separates them. This is the client half.

- Reject a non-app_ --app-id in the file commands' Validate via requireFileAppID,
  so a meta token or a page token fails locally with exit 2 and a hint carrying
  the +get invocation that converts it into an app_id. The prefix rule stays out
  of requireAppID: +export and +get accept an app id or a meta token in the same
  argument, so a blanket check would break them
- Classify the two new backend codes: 400000008 (app not found) as api/not_found,
  matching the neighbouring file-not-found arm, and 400000009 (malformed app id)
  as validation/invalid_argument. Neither may stay under authorization
- Cover the gate per command rather than only through the helper: a helper wired
  into some of the seven commands would pass a helper-level test and still ship
  the defect
- Add e2e for both halves. The malformed case is a dry-run — the rejection
  happens before a request is built — while app-not-found can only be judged
  live, and asserts negatively (must not be authorization / exit 3) so a
  regression cannot hide behind a renamed code

* test(apps): pin that a real permission failure stays a permission failure

Splitting "app not found" out of the shared permission error is only half a
contract. The other half is that the state which genuinely is a permission
problem keeps reporting as one: an over-correction that swept it into not_found
would tell a caller the app does not exist when it does, and would hide the fact
that access can actually be requested.

- Add TestAppsFileNoPermissionLive on its own fixture, since it needs something
  the other cases do not — an app that exists in the tenant and that the caller
  has no role on
- Assert both directions: authorization / permission_denied, and explicitly not
  not_found, so the two cases cannot converge again

Verified to discriminate: against a backend carrying the split, the not-found
case passes and this one passes; against one without it, the not-found case
fails while this one still passes, which is exactly the asymmetry that tells the
two states apart.

* test(apps): configure the app-id dry-run case instead of inheriting a config

The case asserted the --app-id gate but never set up a config dir, so on a
machine that has never been configured the run stopped at the config gate and
the envelope under assertion was "not configured" rather than the validation
error. It passed locally only because an ambient config happened to exist, and
failed in CI — which is exactly the environment the case is meant to represent.

- Call setAppsDryRunEnv, the convention the other dry-run cases already use, so
  the run reaches Validate on a clean machine
- Read the envelope stdout-first then stderr, matching validateErrorMessage:
  domains differ on which stream carries it, and pinning one couples the
  assertions to runner-internal routing rather than to the contract

Verified by re-running with an empty environment and a throwaway HOME, which is
what the CI failure was.

* fix(apps): drop the classification for a code storage no longer returns

Storage briefly answered a malformed app id with its own code, and this branch
mapped it. It now reports that shape as "app not found" like any other id that
does not resolve, so the separate mapping classifies something that never
arrives.

- Remove the entry and its test row. Keeping a classification for an unobserved
  code is the mirror of guessing one: it reads as a handled case, and the next
  person has no way to tell it apart from a live mapping
- Correct the two comments that claimed storage names this shape. It does not,
  and that is precisely why requireFileAppID matters — "app not found" is true
  but points at verifying an id the caller never had, while the local check names
  the argument and carries the command that converts the token into an app id

Re-verified against the current backend: no role stays authorization / exit 3,
an absent app is not_found / exit 1, and a non-app_ argument is rejected locally
as validation / exit 2 before a request is built.
- [OpenEPaperLink/Tag_FW_EFR32xG22](https://github.com/OpenEPaperLink/Tag_FW_EFR32xG22) [2](https://github.com/OpenEPaperLink/Tag_FW_EFR32xG22/commits): Merge pull request #30 from skiphansen/EL035F5C4C

Add support for 3.5" BWRY EL035F5C4C.
- [PrintersForAnts/Micron](https://github.com/PrintersForAnts/Micron) [2](https://github.com/PrintersForAnts/Micron/commits): fixed minor issue with panel clips

Old stls were no effected , cad had the issue now both stls and cad match
Also adjusted panelclip to work with square cut panels now as well
- [scenee/FloatingPanel](https://github.com/scenee/FloatingPanel) [2](https://github.com/scenee/FloatingPanel/commits): ci: support Xcode 27 builds
- [tidwall/tg](https://github.com/tidwall/tg) [2](https://github.com/tidwall/tg/commits): Invert conditions and increase coverage
- [AcademySoftwareFoundation/OpenShadingLanguage](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage) [1](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/commits): docs: Add renderer integration example to README (#2164)

Adds a link to Path-Tracer, a personal open-source renderer that extends
the "Ray Tracing in One Weekend" path tracer with OSL shading. It serves
as a small reference example for people learning how to embed OSL in a
renderer.

Also add table of contents to README.

Signed-off-by: Jinnie Kim <jinhgkim@gmail.com>
- [android/skills](https://github.com/android/skills) [1](https://github.com/android/skills/commits): Enhance README with skill update instructions

Added instructions for updating skills in README.
- [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) [1](https://github.com/anthropics/claude-cookbooks/commits): feat(misc): add Admin API organization management cookbook (#881)

A notebook that manages a Claude Console organization from Python with client.beta.organization: invites and roles, workspaces and members, an API key audit, service accounts, and rate limits, followed by cleanup. Adds the registry entry.
- [fluidd-core/fluidd](https://github.com/fluidd-core/fluidd) [1](https://github.com/fluidd-core/fluidd/commits): fix: resolve missing jobs in batches (#1956)

Signed-off-by: Ruslan Sayfutdinov <ruslan@sayfutdinov.com>
Co-authored-by: Pedro Lamas <pedrolamas@gmail.com>
- [FoloToy/ai-passport](https://github.com/FoloToy/ai-passport) [1](https://github.com/FoloToy/ai-passport/commits): docs(readme): highlight open creative platform
- [github/gemoji](https://github.com/github/gemoji) [1](https://github.com/github/gemoji/commits): Pin GitHub Actions to commit SHAs (#347)
- [google/auto](https://github.com/google/auto) [1](https://github.com/google/auto/commits): Format some Markdown.

RELNOTES=n/a
PiperOrigin-RevId: 984055579
- [KOP-XIAO/QuantumultX](https://github.com/KOP-XIAO/QuantumultX) [1](https://github.com/KOP-XIAO/QuantumultX/commits): Fix Hysteria2 URI detection and unsupported-node notices

Recognize hysteria2:// and hy2:// at subscription detection and classify the hy2 alias as unsupported. Sync tested parser version 2026-09-18 14:27.
- [langchain-ai/local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) [1](https://github.com/langchain-ai/local-deep-researcher/commits): Merge pull request #137 from langchain-ai/dependabot/pip/python-dotenv-1.2.3

Bump python-dotenv from 1.2.2 to 1.2.3
- [mattpocock/skills](https://github.com/mattpocock/skills) [1](https://github.com/mattpocock/skills/commits): Modified the PR body template to make it easier to scan
- [omnivore-app/omnivore](https://github.com/omnivore-app/omnivore) [1](https://github.com/omnivore-app/omnivore/commits): feat: add longreads handler (#4694)

Longreads is an aggregator of longer articles. Because of this they often have a summary of the article, rather than the actual article itself.

They contain a read story link in the page itself. So we use this in order to redirect directly there when adding from an RSS feed.
- [openclaw/acpx](https://github.com/openclaw/acpx) [1](https://github.com/openclaw/acpx/commits): feat: add official Antigravity ACP support (#618)

Add the platform-specific official runtime shortcut and cancel Antigravity fixed-choice questions before permission policies or host callbacks can invent an answer. Preserve ordinary tool approvals and document the accepted behavior for existing custom launchers and embedding hosts.

Includes synchronized agent/permission guidance and Unreleased upgrade notes. Related: #362. Thanks @superbiche.

Co-authored-by: Michel Tomas <michel@superbiche.me>
- [sekai-soft/rss-lambda](https://github.com/sekai-soft/rss-lambda) [1](https://github.com/sekai-soft/rss-lambda/commits): move deployment to host
- [sonocotta/esp32-audio-dock](https://github.com/sonocotta/esp32-audio-dock) [1](https://github.com/sonocotta/esp32-audio-dock/commits): Removed wifi-credentials from squeezelite settings binary (#184)

* Removed wifi-credentials from squeezelite settings binary

* Add built squeezelite binaries, latest templates and NVS settings binaries

* Add built squeezelite binaries, latest templates and NVS settings binaries

---------

Co-authored-by: andriy.malyshenko <andriy@sonocotta.com>
Co-authored-by: anabolyc <anabolyc@users.noreply.github.com>
Co-authored-by: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
- [Squirrel/Squirrel.Mac](https://github.com/Squirrel/Squirrel.Mac) [1](https://github.com/Squirrel/Squirrel.Mac/commits): fix: don't leave a broken app behind when an install is interrupted (#335)
- [usetrmnl/trmnl-firmware](https://github.com/usetrmnl/trmnl-firmware) [1](https://github.com/usetrmnl/trmnl-firmware/commits): Read panel ID, and add Panel-Rev header (#649)

Added function to read the EPD panel revision as a 32-bit value (panel id) to be used to identify the correct temperature profile.

Also reported via /api/setup and /api/display in the new Panel-Rev header.

---------

Co-authored-by: Larry Bank <bitbank@pobox.com>
- [yutiansut/QUANTAXIS](https://github.com/yutiansut/QUANTAXIS) [1](https://github.com/yutiansut/QUANTAXIS/commits): Update README.md