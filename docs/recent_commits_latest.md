# Recent Activity in Starred Repositories
_114 active repos with 1969 new commits_

## [3d-printing](https://github.com/topics/3d-printing)
- [nicklockwood/ShapeScript](https://github.com/nicklockwood/ShapeScript) [8](https://github.com/nicklockwood/ShapeScript/commits): Update for 1.11.5 release
- [Frix-x/klippain](https://github.com/Frix-x/klippain) [1](https://github.com/Frix-x/klippain/commits): fix(mcu): Fix several ebb36 gen2 configuration defaults (#816)

* fix: correct EBB36 Gen2 lis2dw pin definitions

I noticed the pins for the resonance compensation LIS2DW chip were listed differently than the btt documentation and from my known working config that was used in a previous commit to add the toolhead board's config. This commit corrects those pins in the mcu_definitions folder.

* fix: add add serial line to BTT_EBB36_GEN2_v1.0.cfg for USB connection vice canbus

EBB36 Gen 2 can be connected via USB or canbus. This commit adds a commented line for easy configuration adjustment in template.

* fix: add missing EBB36 Gen2 lis2dw pins in user_templates

Some users may need to use software SPI, but the template does not include the pin names. This normally is not a problem as the accelerometer is defined using the SPI bus syntax in the lis2dw config file. This is a minor nicety to have the SPI pins defined to match the rest of the pins in case needed. The pins were already named in the mcu_definitions folder, just needed to be added to the user_templates.

* fix: lis2dw axes_map for EBB36 Gen 2 correction

The majority of users will mount the EBB36 Gen 2 board behind the hotend/extruder, resulting in a map configuration of x,-z,y rather than the current default of x,y,z. This results in an unnecessary addition to the overrides.cfg to correct the orientation. Adjusting the config to match the majority of use cases will eliminate the need for an override.

* fix: correct EBB42 Gen2 lis2dw pin definitions

While fixing the EBB36 pins, it was noted the same resonance compensation LIS2DW chip pins were listed differently than the btt documentation. This commit corrects those pins in the mcu_definitions folder.

* fix: add missing EBB42 Gen2 lis2dw pins and commented serial line in user_templates

Some users may need to use software SPI, but the template does not include the pin names. This normally is not a problem as the accelerometer is defined using the SPI bus syntax in the lis2dw config file. This is a minor nicety to have the SPI pins defined to match the rest of the pins in case needed. The pins were already named in the mcu_definitions folder, just needed to be added to the user_templates. Additionally, added a commented serial line to the file for those connecting over USB.

## [ai](https://github.com/topics/ai)
- [openclaw/openclaw](https://github.com/openclaw/openclaw) [674](https://github.com/openclaw/openclaw/commits): fix(exec): complex commands trigger human approval fallback due to reviewer token truncation (#144587)

Under tools.exec.mode: auto, give the existing command reviewer a bounded
1,024-token completion budget, clamped to smaller positive model limits.
This reduces human approval fallback when routine complex command reviews
run out of completion budget. Non-stop completions still fail closed.

Proof: both budget regressions fail against pre-fix production; all 85
reviewer/resource tests pass after the repair. Exact-head CI run 34725087843
is green. Mechanical rebase and empty CI refreshes preserve the reviewed fix.

Closes #144476

Co-authored-by: MasterSwords1 <abderrahmaneriyad15@gmail.com>
Co-authored-by: Peter Steinberger <steipete@gmail.com>
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) [293](https://github.com/NousResearch/hermes-agent/commits): fix(config): a fresh process recovers the last good config.yaml instead of running on defaults

The in-process last-known-good (the codex#31188 port) only protects a
long-running gateway. A CLI restart or `hermes config get` against broken
YAML fell through to DEFAULT_CONFIG and silently dropped every override,
including approvals.deny (#102945).

Every successful parse now leaves a `good` copy in backups/config/ through
the existing bounded, byte-deduped backup_config(); the fallback reads the
newest one, runs it through the normal canonicalize/expand/managed-overlay
pipeline, and says so on stderr. The broken config.yaml is never modified.
The backup is the raw file, so ${VAR} templates stay templates on disk.

Redo of #61796 (which added a config.validated.yaml sibling and
re-validated the whole config on every load) on top of the backups/config/
ruling from bf53ff00a736.
- [BasedHardware/omi](https://github.com/BasedHardware/omi) [47](https://github.com/BasedHardware/omi/commits): fix(backend): round-trip Vertex functionCall through the gateway (#13671)

## What changed and why

Gateway Vertex `generateContent` already forwarded OpenAI `tools` to
Gemini, but `_vertex_to_openai_response` /
`_vertex_to_openai_stream_chunk` copied **text only**. Company-paid
desktop Insight/Task (`sendImageToolLoop`) only act on `functionCall`,
so after #12337 hopped them through the gateway they got HTTP 200s with
billed tokens and emitted **zero** `Advice Generated` / `Task Extracted`
(#13666). JSON-schema Memory/Suggestion still worked because they parse
text.

This round-trips Vertex `functionCall` parts to OpenAI `tool_calls` (and
`finish_reason: tool_calls`), including functionCall-only candidates.
Desktop BFF translation already maps that back to Gemini. No client
change. Do not flip `OMI_LLM_GATEWAY_FEATURE_MODE`.

Closes #13666

## Product invariants affected

none

## How it was verified

```
backend/.venv/bin/python -m pytest \
  backend/tests/unit/test_llm_gateway_vertex_provider.py \
  backend/tests/unit/test_desktop_gemini_gateway.py -q
```

36 passed, including the new functionCall-only generateContent and SSE
regressions.

Could not exercise live prod desktop Insight/Task in this PR; that path
is the GKE LLM gateway. After merge, ship **llm-gateway** (not Cloud
Run-only) so desktop-backend's existing hop sees the translator.

## Tests

`test_vertex_function_call_only_response_emits_openai_tool_calls` and
`test_vertex_function_call_sse_emits_openai_tool_call_delta` in
`backend/tests/unit/test_llm_gateway_vertex_provider.py`. A Vertex
candidate with only `functionCall` (no text) must emit OpenAI
`tool_calls`. That is the test that would have stayed red on #12337.

## Failure class (fixes)

Failure-Class: new

## Failure-class transition narrative (only when needed)

Violated contract: an OpenAI-compatible Vertex adapter that advertises
function tools must return those tool calls, not a 200 with
empty/text-only content. Canonical guard: response + SSE normalizers
emit `tool_calls` from Gemini `functionCall` parts; the two new hermetic
tests are the prevention artifact. Registry file:
`.github/failure-classes/FC-gateway-vertex-drops-function-calls.json`.


<!-- This is an auto-generated description by cubic. -->
<a
href="https://cubic.dev/pr/BasedHardware/omi/pull/13671?utm_source=github"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-light.svg"><img
alt="Review in cubic"
src="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"></picture></a>
<!-- End of auto-generated description by cubic. -->
- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) [34](https://github.com/QwenLM/qwen-code/commits): fix(core): run web terminal PTYs on the bundled ConPTY backend (#11643)

* fix(core): run web terminal PTYs on the bundled ConPTY backend

The web terminal spawned its PTYs with node-pty's default inbox ConPTY
backend, where a natural shell exit orphans the conhost.exe --headless
the backend spawned: the native exit watcher erases the pty baton before
delivering onExit, pty_baton has no destructor, and the erased HPCON is
unreachable from JS (microsoft/node-pty#965). Every exited web terminal
leaked ~8 MB for the life of the CLI, and a pin bump does not fix it.

Mirror the #11497 shell path: spawn with useConptyDll on Windows so the
bundled backend releases its host reference right after spawn and the
host exits with its last client. The bundled backend adds one
synchronous throw point — a missing or unloadable conpty.dll — and a
web terminal has no child_process fallback, so a failed bundled spawn
retries once on the inbox backend: the pre-fix leaking behavior beats a
terminal that cannot start at all. A failed spawn produced no child, so
the retry cannot double-spawn. The 4001 non-retryable close path is
unchanged.

Also switch the agent-view PTY host to the bundled backend (same leak,
lower rate), refresh the conpty-host release docs, and add a
VERIFIED_NODE_PTY pin test so a node-pty bump forces re-verification of
the native teardown semantics the release path depends on.

Refs #11352

* fix(core): derive node-pty pins and widen the conpty-host pin guard

The six `@lydell/node-pty*` pins live in three unsynchronized places — the
root manifest, packages/core's manifest, and a hardcoded map in
scripts/prepare-package.js — but the conpty-host tripwire asserted only
one key of one manifest, so bumping the win32 prebuild keys or the root
manifest left it green and skipped the human re-check it exists to force.

Derive the six pins in writeDistPackageJson from packages/core's manifest
(deleting the third hardcoded table), and widen the tripwire to assert all
six core keys plus an equality against the root manifest's six — the
declaration packages/cli's agent-view actually resolves in a dev tree.

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
Patrol-Run: qwen-pr-closeout/jmtxennouyn

* fix(core): answer and scrub bundled-backend terminal queries in the web terminal

Switching the web-terminal registry to the bundled ConPTY backend let a
probing shell's DA / DSR query bytes into the recorded scrollback; a
reconnect that replays the buffer made the client's xterm.js re-answer
each query and write the fresh reply back into the still-live shell's
stdin. The bundled backend answers no queries itself, and the browser is
not guaranteed to be attached when the startup probe fires.

Mirror the other half of the shell path (#11497): on win32, feed a
headless terminal the PTY stream so it answers the probe server-side, and
strip the query bytes from both the scrollback and the live stream so a
replay cannot re-emit them. Also bring the releasePtyResources docstring
in line with the bundled backend (R1-8).

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
Patrol-Run: qwen-pr-closeout/jmtxennouyn

* fix(core): close query-strip gaps and a race in the web terminal

Three review findings on the bundled-ConPTY web terminal path:

- The scrollback scrub was a stateless per-chunk regex over only the `c`/`n`
  finals, so the query families xterm.js answers beyond those (tertiary DA,
  DECRQM, DECRQSS, XTVERSION, DECREQTPARM, OSC colour queries) still reached
  the scrollback and were re-answered into the live shell on reconnect. Replace
  it with a stateful stripper covering every family and carrying a probe split
  across two chunks.

- resize() resized only session.pty, leaving the headless query responder on
  its 80x24 spawn grid, so geometry-dependent replies were computed against
  the wrong size. Forward the resize to session.queryTerminal.

- loadXtermHeadless() was a second suspension point whose cancelledCreations/
  disposed guards were not re-checked, so a release()/releaseWorkspace()/
  dispose() landing during the import leaked a PTY the caller had cancelled.
  Re-check both after the import.

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
Patrol-Run: qwen-pr-closeout/jmtxrimarz8

* fix(core): strip DCS DECRQSS queries in the terminal query filter

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

Patrol-Run: qwen-pr-closeout/jmty6iqs0zv

* fix(core): bound the terminal query stripper and tie it to its responder

The stateful stripper held any unterminated OSC (a title SET included) with no cap, so one stray ESC ] swallowed every later chunk and grew pending unbounded; the DCS alternative also required the full introducer, leaking its halves that reassemble into a re-answered DECRQSS. Hold only viable query prefixes, cap the hold, end an OSC partial at a bare ESC (accepting the C1 ST terminator), hold the DCS introducer, and gate the stripper on the responder so a failed headless load no longer strips with nobody left to answer. Correct the query-set doc comment.

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
Patrol-Run: qwen-pr-closeout/jmtyf3dx109

* style(core): format web-terminal-registry.ts with prettier

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
Patrol-Run: qwen-pr-conflict/jmtyhy9mj0e

* fix(web-terminal): stop scrubbing the OSC colour family the server cannot answer

The stateful stripper added here removed the OSC 10/11/12/4 colour queries from
both the scrollback and the live listener, but the pinned @xterm/headless 5.5.0
responder answers none of them: `onData` carries DA/DSR/DECRQM/DECRQSS only,
while `_setOrReportSpecialColor` reports on the internal `_onColor` emitter that
the headless Terminal does not expose (`term.onColor` is undefined) and that
nothing in this file subscribes to. Deleting the family from the browser's
stream as well left a probing program unanswered, where the browser's own
xterm.js 6.0.0 `_handleColorEvent` is the answerer and answered it at the merge
base.

Narrow both regexes to the families the responder actually answers (plus the
never-display-content DA3 / XTVERSION / DECREQTPARM trio that no build answers),
drop the half-covered colour arm from the partial matcher — so the strip set and
the doc block no longer disagree about what the colour family is — and correct
the doc block to state the split. Covered by a new test asserting the whole
family reaches both the live listener and the snapshot untouched, and that
nothing is written back; it fails if the colour arm is restored.

The colour queries that a reconnect replay re-answers are part of the
replay-suppression redesign tracked in #11734.

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
Patrol-Run: qwen-pr-closeout/jmtyno0zh0n

* fix(web-terminal): separate live replies from reconnect history

Preserve raw PTY bytes and limit the Windows server responder to primary DA. Mark snapshots explicitly and restore history into a detached browser terminal while the old terminal continues forwarding user input. Activate live replies at the snapshot write callback, reject incompatible peers, and preserve the parallel color-query regression fix. Refs #11734.

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>

---------

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>
- [t8y2/dbx](https://github.com/t8y2/dbx) [33](https://github.com/t8y2/dbx/commits): feat(sqlite): support autoincrement primary key in structure editor
- [steipete/oracle](https://github.com/steipete/oracle) [14](https://github.com/steipete/oracle/commits): fix(browser): centralize provider routing across session entrypoints (#492)
- [herdrdev/herdr](https://github.com/herdrdev/herdr) [10](https://github.com/herdrdev/herdr/commits): fix: update grok session after new (#2683)

* fix: update grok session after new

refs #2681

* fix: avoid powershell args shadowing

refs #2681

---------

Co-authored-by: akbash-bot <300245827+akbash-bot@users.noreply.github.com>
- [XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) [10](https://github.com/XiaomiMiMo/MiMo-Code/commits): fix(server): treat port 0 as OS ephemeral; stop preferring 4096 (#2385)

* fix(server): port 0 binds OS ephemeral port, stop preferring 4096

Conventional listen port 4096 collides with MiMo Desktop embeds and other
local tools. Align port 0 with the OS (start(0)); fixed ports must be passed
explicitly. Remove runtime 4096 hardcodes from plugin client placeholders and
CLI help; docs/examples keep explicit --port when a known URL is required.

* docs(compose): deliver default-port-ephemeral feature report

* docs(compose): refresh delivered range after rebase onto main
- [google/adk-python](https://github.com/google/adk-python) [7](https://github.com/google/adk-python/commits): fix(agents): trigger after_agent_callback on cancellation

When agent execution was cancelled via asyncio.CancelledError (e.g. client
disconnect or RPC timeout), _handle_after_agent_callback was bypassed,
causing execution metrics and timers in plugins to leak. This adds an explicit
exception handler for CancelledError to ensure after_agent_callback runs for
side-effects during cancellation, while preserving the invariant that
end_invocation short-circuits and unhandled errors do not trigger
after_agent_callback.

Co-authored-by: Shangjie Chen <deanchen@google.com>
PiperOrigin-RevId: 980466771
- [kortix-ai/suna](https://github.com/kortix-ai/suna) [3](https://github.com/kortix-ai/suna/commits): fix(tests): a forced exit must raise an annotation, not a line nobody reads (#7218)

The CONN-27 incident's rule is explicit: "Do not hide a leaked connection by
forcing the test process to exit." #7203 bounds the consequence of a leak — the
run leaves once its verdict is in rather than hanging for 40 minutes — but it
announced that on stdout, and a warning in a 40,000-line CI log is close enough
to hidden that the rule has a point.

Under GitHub Actions the notice is now a `::error::` workflow command, so it
lands in the job's annotations and on the run summary page. Nobody has to go
looking. The run still reports its real verdict, and the leak is still on the
record where someone will trip over it.

Off CI it stays a plain warning, because an Actions command there is noise.

The message is flattened to one line first: Actions truncates an annotation at
the first newline, which would have dropped the part naming what leaked.

For the record, the leak that motivated all of this is now actually fixed:
404655d736 has CONN-27 mint its token through the public API and acquire its
database connection inside the cleanup scope. That flow was mine, so the leak
was mine. This change is the backstop, not the fix.

Verified:
  - tests typecheck clean; 45 files / 451 unit tests pass
  - two new cases spawn real processes: with GITHUB_ACTIONS=true the output
    carries `::error title=ke2e leaked a handle::` on a single line; with it
    unset the same run emits no `::error` and still says what happened

Claude-Session: https://claude.ai/code/session_01ECsZyxXpTLhyQxGsz3QtX2
- [langgenius/dify](https://github.com/langgenius/dify) [2](https://github.com/langgenius/dify/commits): fix(api): preserve literal NA in annotation CSV imports (#42221)

Co-authored-by: autofix-ci[bot] <114827586+autofix-ci[bot]@users.noreply.github.com>
- [oraios/serena](https://github.com/oraios/serena) [2](https://github.com/oraios/serena/commits): Merge pull request #1988 from oraios/ls-registry

SolidLSP: Add language server registry, supporting externally provided implementations
- [unslothai/unsloth](https://github.com/unslothai/unsloth) [2](https://github.com/unslothai/unsloth/commits): Unbreak main, and fix the five causes reddening the PR backlog (#10832)

* Unbreak main: read the sidebar hold-out contract as a condition, not as source text

#10706 hoisted `hasPinMode && !pinned && collapseToZero` into a named const and gave it a
peek exception. That changed nothing the contract protects, but the test pinned the inlined
spelling, so Backend CI has failed on every main commit since 22bbff627 and on roughly 25
open PRs that touch none of this.

Read the condition instead, with the helpers that already exist for exactly this in
tests/studio/_js_source.py, and assert the thing the literal form never did: that
aria-hidden and inert stay the same expression, since hidden-but-focusable is the bug.

_js_source gains two pieces:

- attribute_expressions(), to read what a JSX attribute is wired to.
- an ASI-aware declaration scan. binding_joining() only looked for `const NAME = ...;` and
  sidebar.tsx has one semicolon in 500 lines, so it found no declarations there at all and
  answered None for a binding plainly present.

* Restore linear DeepSeek R1 tool-call parsing, and measure linearity rather than speed

#10507 added a wrapper sweep that seeks the next `{` once per opener. A DeepSeek R1 body is
repeated `<|tool_sep|>` markers, so that is once per marker, each scanning the rest of the
buffer: quadratic. Measured over doubling input, the R1 path went 2.00x per doubling before
#10507 and 2.21x, 2.40x, 2.66x, 4.82x after, reaching 2.9s on 80k markers.

The sweep now carries the next `{` forward instead of re-seeking it, since both indices only
move forward, and stops when there is none left. It also no longer copies the gap between a
marker and a far-away object: a fence or blank space is short, so a long gap is not a body.
Rejecting it is the conservative direction, because an untrusted span is masked rather than
exempted. All five adversarial shapes are back to 2.00x per doubling.

test_pr5624_regressions caught this and was reported as a flake, because an absolute
`elapsed < 1.0` at one size cannot tell a slow runner from a slow parser: it read 0.20s on a
quiet runner and 1.41s on a busy one, and the real regression only tipped it over sometimes.
The three tests now compare the cost of 4x the input against the cost of 1x. Linear is ~4x,
quadratic is ~16x. Healthy measures 3.94-4.09 across all four shapes; with #10507's sweep
restored it measures 6.7x and 12.2x, so the bar at 6.0 has margin on both sides.

Adds the distant-object shape as a fourth case. It is the one that stayed quadratic after
the obvious fix, because a `{` anywhere in the buffer means the per-marker seek always
finds one.

* Do not score a PowerShell host crash as an installer-watcher failure

#10825 went red on test_the_watcher_scores_the_image_that_ran_not_the_words_in_the_message
with pwsh aborting on SIGABRT out of AssemblyName.ParseAsAssemblySpec: the .NET host tearing
itself down, on a probe that loads no assembly of its own and passes everywhere else.

Both pwsh probes now go through one runner that retries once and then skips, and only for an
abnormal termination carrying a host fault banner. A clean non-zero exit, or the wrong HITS
count, is the watcher being wrong and still fails: verified by breaking Watch-ForCompiler.ps1
and confirming the test goes red, and by driving all four shapes (crash-then-ok, crash-twice,
clean non-zero, abnormal without a banner) through the runner directly.

* Re-triage the 7 dependency-scan findings an upstream release reopened

pip scan-packages fails on every PR that touches deps (#10819 is the current one) with 5
CRITICAL and 2 HIGH that no PR introduced. The baseline binds each entry to a hash of the
flagged code, so an upstream release that edits those lines reopens the entry by design.
scikit-learn 1.9.1 did exactly that; unsloth-zoo reopens on its own PyPI releases.

Reviewed all 7 against the source, not the check name:

- sklearn/datasets/_openml.py, 'C2 polling/beaconing loop': the `while True` inside
  _retry_on_network_error. It decrements retry_counter, re-raises at zero and re-raises 412
  immediately. A bounded retry, not a beacon.
- sklearn/externals/array_api_compat/{cupy,dask,numpy,torch}/__init__.py, 'Downloads and
  executes remote code': `__import__(__spec__.parent + '.linalg')`, four copies of a
  vendored shim importing its OWN submodule, with the upstream comment explaining that the
  name is built dynamically so the library can be vendored. No network, no remote code.
- unsloth_zoo/compiler.py, 'obfuscation + exec/eval': our own compiler exec'ing the patched
  forward methods it generates. That is the module's entire purpose.
- unsloth_zoo/mlx/loader.py, same check: the Exec evidence is almost all `mx.eval(...)`,
  MLX's lazy-array evaluation, which is not Python eval at all.

Entries are appended, not regenerated, so the other 228 keep their existing review.

Known follow-up: unsloth-zoo is first-party and releases often, so these two entries will
reopen again. Worth deciding separately whether a package we publish belongs in a
third-party supply-chain scan at all; not changing the gate's design here.

* Read the media status guard as a guard, not as one exact line

#10788 rewrote setStatusIfNewest's ticket check from

    if (ticket === statusTicket.current) setStatus(next);

to

    if (ticket !== statusTicket.current) return;
    setStatus(next);

which admits exactly the same reads, and Frontend build + bundle sanity went red on the
substring. Same failure class as the sidebar contract in the previous commit.

Both spellings now count, checked against setStatusIfNewest's own callback body so a guard
elsewhere in the file cannot stand in for it. Verified against #10788's source (passes) and
against three mutations (guard deleted, guard inverted, guard moved out of the callback),
each of which fails.

* Bound the fence, not the gap, when trusting a wrapper body

The previous commit refused any gap over 4096 chars between a wrapper marker and its object,
to avoid copying it once per marker. Differential testing against the old sweep over long
gaps showed that is too blunt in the one direction that matters: _only_a_code_fence strips
before it matches, so a genuine fence trailed by blank space, or an object preceded by a long
blank run, was accepted before and refused after. Refusing wrongly is not free. An untrusted
wrapper body gets masked, and end to end that turns a tool argument of

    {"q": "<think>rehearsed</think>"}

into a run of U+E000, which is the defect #10507 added _inference_wrapper_spans to avoid.

The gap's blank ends are now found as indices and never copied, and the cap applies to what is
left, which is the only part the fence test decides on. Blank is unbounded again, as it is in
real output.

Differential against main's sweep: 60000 random short inputs, 0 mismatches. 2520 long-gap
inputs across blank, fence, text and brace fillers at 1 to 20000 chars: the only remaining
divergence is a fence whose stripped form exceeds 4096 characters, that is a 4000-plus backtick
run or language tag, which is what the cap is for and is documented as such.

Still 2.00x per doubling on all six adversarial shapes, including the two the cap exists for
(one distant object, and a long blank run before it).

* Record the new tool_call_parser constant in the refactor guard inventories

The guard pins the parsing stack's module surface, so the added _MAX_FENCE_CHARS reads as an
unrecorded top-level name and fails test_ast_inventory_matches_the_baseline and
test_runtime_surface_matches_the_baseline.

Added by hand rather than with 'refactor_guard.py snapshot'. A full snapshot on this tree also
rewrites 111 unrelated ast entries, 63 patch targets and two idempotence inputs, none of which
this branch touches, and folding someone else's unrecorded drift into a CI fix would hide it.

test_guarded_functions_produce_the_same_bytes, the digest over the 1833-input corpus, passes
unchanged, which is the check that would have caught a behaviour change in the sweep.

* Attribute a temporary DLL to a compiler, so Windows No Compiler CI can pass

This job has never once been green: 0 successes against 70 failures and 28 cancelled runs
in its last 100, red on main continuously. It fails on its own artefact detector, which
scored every *.dll created anywhere under TEMP while the installer ran. The installer
unpacks llama.cpp's checksum-verified prebuilt release into a staging directory there, so
~25 DLLs land under TEMP with no compiler within reach, and the job reported them as
'the artefact half of the same shape'.

They are not that shape. What was blocked in the field, and what this job's own prose says
it measures, is

    powershell.exe -> csc.exe -> %TEMP%\<random>.dll

An extracted archive is a different thing, so the gate was wrong and the installer was
right. A DLL now counts only when a compile is evidenced in ITS OWN directory. CodeDom,
which is what Add-Type uses and what was flagged, writes the response file, the generated
source and the captured streams into the per-invocation directory it puts the assembly in,
so the pairing holds for the shape this exists to catch. A .cmdline or .rsp still counts on
its own, wherever it lands.

The narrowing is self-checking: the positive control compiles a real type with Add-Type and
REQUIRES both detectors to fire before any measurement is believed, so cutting too far fails
there rather than passing quietly.

Also fixes the message that reported this. Both throws read '{0}' literally on every firing,
because -f binds tighter than the string concatenation it was applied to and formatted only
the last fragment.

Tests: test_the_watcher_still_reports_intermediates_that_were_left_behind asserted a bare
leftover.dll, which is the over-broad rule itself; it now leaves a response file beside the
assembly, which is what a compile that was not cleaned up looks like. Two new cases pin the
change: an unpacked release archive is not a compile, and a real compile in a sibling
directory is still caught while the archive beside it is not. 49 passed.

* Require the media status guard to precede the write, not merely exist

The early-return spelling this test started accepting is only equivalent when the guard runs
FIRST. Checking presence alone let

    setStatus(next);
    if (ticket !== statusTicket.current) return;

pass, which publishes the superseded status before returning and is the exact bug the test
exists to catch. Confirmed by building that page and watching all four tests pass.

The guard's match index must now come before the first setStatus(. The inline
'if (a === b) setStatus(next);' form satisfies it by construction. Verified against main,
against #10788's early-return form, and against both regressions (write-then-guard, and the
guard deleted outright), which now fail.

* Unblock the desktop leg, require a bare stale return, pin the MLX loader entry

Windows No Compiler CI: with the artefact detector fixed, the positive control and the shell
leg both pass for the first time, and the desktop leg then failed on something that had been
hidden behind them. Under $ErrorActionPreference = 'Stop', a native command writing ANY line
to stderr raises NativeCommandError, and install.ps1 --tauri reported

    [TAURI:ERROR_CLEAR] create virtual environment recovered

which is the installer saying it recovered. That killed the step before either detector was
read. Both legs now drop to 'Continue' around the child only; the exit code stays the gate,
which for the desktop leg is deliberately not checked at all, so a stderr line failing it was
never the intent.

media-status-sequencing: requiring the guard to precede the write still accepted
'if (ticket !== statusTicket.current) return setStatus(next);' ahead of the normal write,
which publishes the superseded status out of the return expression. Confirmed by building
that page and watching all four tests pass. The stale branch's return must now be bare.
Verified against main, against #10788's form, against a braced early return, and against
three regressions (return-with-write, write-then-guard, guard deleted), which all fail.

scan_packages baseline: the appended unsloth_zoo/mlx/loader.py entry is pinned to its
reviewed file, matching the compiler.py entry beside it. The obfuscation check's evidence is
the __import__/eval lines and the import TARGET is a variable, so it sits outside the
evidence: a changed target would leave evidence_hash intact and keep the finding suppressed.
Scan still exits 0 with 17 suppressed and no active CRITICAL or HIGH.

* Do not score the positive control's own compile against the installer

With the desktop leg unblocked, the shell leg failed reporting

    the installer spawned 1 compiler process(es)

on a cvtres.exe created by csc.exe at 12:49:23, about a second before the step began. That is
the positive control from the step above: it compiles a type on purpose, and the 4688 window
starts a second early, so its compile fell inside the installer's lookback.

The hits already present when the action has not yet started are recorded and subtracted by
identity. Moving the floor to 'now' instead would have given up what that second is for,
which is keeping a process created in the same tick as the floor from being dropped.

Also closes the last hole in the media sequencing guard: guarding the first setStatus while a
second sits unguarded after it leaves every stale response overwriting the status. The
callback must now write exactly once. All three pages have exactly one write today, #10788
included, and an added second one fails.

* State WHEN the collapsed sidebar leaves the accessibility tree, not that it does

Asking only that the held-out condition still appears in the expression accepts dropping
the peek exception along with it, and a peeked sidebar is on screen: aria-hidden and inert
on a visible, focusable panel is the same defect the assertion guards, pointing the other
way.

So expand the attribute expression down to its four inputs and compare the whole truth
table against the one this contract wants: removed exactly when pin mode is on, the sidebar
is unpinned, it collapses to zero, and it is not being peeked at. Any spelling admitting
exactly those states passes, so the rename, the rewrap and the hoisted const that broke the
old exact-string form are all invisible; dropping the peek exception, dropping inert,
dropping collapseToZero and inverting the exception all fail.

expand_bindings stops at the four inputs rather than walking to the bottom. hasPinMode is
itself a const further up, and expanding it too drags in the prop plumbing that decides
whether pin mode exists at all, which belongs to a different component. boolean_table
refuses anything that is not names, && || ! and parentheses, so a comparison cannot be
quietly mistranslated on the way to Python.

Also pins the OpenML suppression to the file it was reviewed against. The hashed evidence
is the bare 'while True:'; what makes the loop benign is the retry counter, the decrement
and the two re-raises around it, all outside that line. Removing the bound would have left
the entry suppressing. Verified against scikit-learn 1.9.1: it still suppresses, and one
flipped digit reopens the CRITICAL.

* [pre-commit.ci] auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

* Wait for the find bar to settle instead of sleeping 200ms at it

Frontend build + bundle sanity went red on a commit that touched a PowerShell script and a
node test, on 'chromium/Linux: the chord re-focuses the field instead of closing', 177/178.
The check presses the chord, sleeps a flat 200ms and reads the state; open_bar right above
it already waits on a condition, with a comment about the first open crossing a lazy
boundary. The same boundary is in front of this press, so on a loaded runner the sleep
expires first and the check reports a defect that is not there.

It now waits for open && focused, and Escape waits for the bar to be gone rather than
sleeping 250ms. Neither wait asserts anything: a bar that never settles spends the timeout
and then fails on the same check with the same message, so a real break is still reported
and only the speed of the machine stops being part of the contract.

Verified both directions: 178/178 unchanged, and with requestFocus mutated into a toggle
(setOpen(was => !was), which is literally 'closes instead of re-focusing') the check fails
in all four engine modes.

* Require the status write to survive the stale branch, not just follow it

Ordering says the write comes after the early return. It does not say the write is still
reached: `if (ticket !== statusTicket.current) { return; setStatus(next); }` returns first
and satisfies the guard regex, the ordering rule and the exactly-one-write rule while
publishing nothing at all.

When the stale branch carries a block, the write now has to live past the end of it. The
`ticket === current` spelling needs no such rule, since its pattern already ties the write
to the guard.

Mutations: the stranded write fails, a braced early return with the write after the block
passes, the braceless #10788 form passes, and dropping the guard outright still fails.

* [pre-commit.ci] auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

* Score a compile once, at its root, not at every process in the chain

The timestamp baseline did not hold. The shell leg failed again on the same cvtres.exe, and
the reason it survived the subtraction is that the Security log is written with latency:
the positive control's csc.exe started before the installer's window opened, its cvtres.exe
child landed just inside, and NEITHER was in the log yet when the baseline was read. There
was nothing to subtract. No arrangement of timestamps wins that race.

So attribute by the chain instead. A compiler started by a compiler is a step of a compile
that is already being scored, not a new one: csc.exe shells out to cvtres.exe to build its
resource blob, and counting that as a second hit says the action compiled twice. Reading
ParentProcessName off the record settles the cross-step bleed for good, because the child
is the only part of the control's chain that was ever in range.

Detection is unchanged for a compile the action really starts. Its root compiler is spawned
by the installer's shell, not by another compiler, and the window opens before the action
does, so the root is in range and is reported. What this drops is only ever the second
process of a chain whose first was already seen or was never in range at all. An orphaned
cvtres.exe with a non-compiler parent still counts, and a record from a schema with no
ParentProcessName at all still counts, so an empty field is not read as a compiler parent.

Four tests, covering each of those: the shell's compile, the orphaned resource step, the
compiler's own resource step, and the pre-ParentProcessName schema. 53 pass.

---------

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>
- [github/spec-kit](https://github.com/github/spec-kit) [1](https://github.com/github/spec-kit/commits): feat: add artifact-owned contribution lookup (#4550)

* feat: expose resolver lookup IDs

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* refactor: keep contribution lookup artifact-owned

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix: preserve canonical hook event in lookup

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix: continue duplicate hook provider lookup

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* test: cover encoded hook contribution lookup

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix: identify artifact lookups by installation

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix: reject non-json artifact contributions

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix: enforce strict artifact json

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix: align lookup with manifest semantics

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix: preserve lexical artifact source paths

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

* fix: validate artifact lookup output encoding

Assisted-by: GitHub Copilot (model: GPT-5.6 Sol, autonomous)

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>

---------

Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
- [Lightning-AI/pytorch-lightning](https://github.com/Lightning-AI/pytorch-lightning) [1](https://github.com/Lightning-AI/pytorch-lightning/commits): Fix FSDPPrecision rejecting a scaler for 16-mixed precision (#21831)

The scaler guard read self.precision before it was assigned, so it saw the base
class default 32-true and raised for a 16-mixed scaler; the else branch also
dropped a user-provided scaler. Use the local precision argument in the guard and
keep the scaler.
- [lutzroeder/netron](https://github.com/lutzroeder/netron) [1](https://github.com/lutzroeder/netron/commits): Update gguf.js
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) [1](https://github.com/openai/openai-agents-python/commits): ci: add Python and Actions CodeQL security scanning (#4974)
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) [1](https://github.com/screenpipe/screenpipe/commits): feat: auto-connect AI apps and attribute API/MCP usage (#6997)

* feat: connect AI apps installed after Screenpipe starts

* feat: attribute API and MCP retrievals to AI apps

## [c](https://github.com/topics/c)
- [shadowsocks/shadowsocks-c](https://github.com/shadowsocks/shadowsocks-c) [15](https://github.com/shadowsocks/shadowsocks-c/commits): Merge pull request #3062 from shadowsocks/feature/server-endpoints

Combine server host and port with strict IPv6 endpoint parsing
- [patriciogonzalezvivo/glslViewer](https://github.com/patriciogonzalezvivo/glslViewer) [3](https://github.com/patriciogonzalezvivo/glslViewer/commits): camera constrains and back to animation

## [claude-code](https://github.com/topics/claude-code)
- [slopus/happy](https://github.com/slopus/happy) [9](https://github.com/slopus/happy/commits): fix(app): stabilize plain headers and highlight terminal details
- [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) [8](https://github.com/CherryHQ/cherry-studio/commits): fix(api-gateway): report truncated Responses output as incomplete (#20375)

Signed-off-by: Konv Suu <hi@kovsu.com>
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) [4](https://github.com/Piebald-AI/claude-code-system-prompts/commits): Update changelog for v2.1.270

## [data-science](https://github.com/topics/data-science)
- [dbcli/mycli](https://github.com/dbcli/mycli) [30](https://github.com/dbcli/mycli/commits): Merge pull request #2243 from dbcli/RW/readme-features-list-edit

Edit list of features in `README.md`
- [stefan-jansen/machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) [18](https://github.com/stefan-jansen/machine-learning-for-trading/commits): us_equities_panel: stages 06 to 08, and latent factors on the primary label (#998)

Stages 06, 07 and 08 of us_equities_panel executed and rendered, with the supersedes
declarations each run needed.

06_linear and 07_gbm fit all three declared labels; 08_tabular_dl fits the primary label
only, which is what the notebook has always done - its population guard tests configs, not
labels. Registry: 128 training runs across the three families.

The supersedes literals in 06 and 07 named generations the registry had already replaced.
They are now "live" where the lineage is what matters, because a hash is a quotation of a
value the registry moves on every publish.

latent_factors is declared on the primary label only. 13a_pca and 13b_ipca read the
declaration to decide which labels they fit, so removing it from fwd_ret_5d.yaml and
fwd_ret_21d.yaml is what narrows them; they raise if no label declares the family.
15_model_analysis and 16_backtest stop naming the twelve sets those notebooks no longer
publish, and the named-set test checks each consumer list against what its producer fits
rather than their union, which is the defect the module docstring names.

## [esp32](https://github.com/topics/esp32)
- [1technophile/OpenMQTTGateway](https://github.com/1technophile/OpenMQTTGateway) [3](https://github.com/1technophile/OpenMQTTGateway/commits): [SYS] Fix erase command leaving MQTT credentials in SPIFFS (#2372)

eraseConfig() passed SPIFFS.format() as an argument to THEENGS_LOG_TRACE,
which expands to ((void)0) below LOG_LEVEL_TRACE and discards its arguments
along with the call. On every build using the default LOG_LEVEL_NOTICE the
format therefore never ran, so {"cmd":"erase"} only performed
nvs_flash_erase(): the WiFi credentials were cleared but /config.json
survived and restored the MQTT server, port, user, password, broker and
client certificates, connection index, topic, gateway name, OTA password
and BLE AES keys on the next boot.

Call SPIFFS.format() on its own statement and report a failed format at
ERROR level, so the failure is visible at the default log level.

This was introduced in #2232, which converted the original runtime-checked
Log.trace() call to the compile-time macro. It affects the SYS erase
command, the WebUI erase button and the GPIO factory-reset hold alike,
since all three go through eraseConfig().

Reproduced on a Theengs Plug built at the default log level: after
{"cmd":"erase"} the NVS namespaces are gone ("SYS config not found",
"ONOFF config not found") and the saved APs are empty, yet the same boot
still logs "Config loaded from flash" and restores the OTA server cert.

Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
- [arendst/Tasmota](https://github.com/arendst/Tasmota) [3](https://github.com/arendst/Tasmota/commits): Fix regression from PR #25024 and enhance WiFi status line (#25026)

- Fix regression from PR #25024, which accidentally broke the layout and rendering of the WiFi configuration page,
- The WiFi status line now includes richer tooltip text with SSID, RSSI, and AP details.
- [esphome/esphome](https://github.com/esphome/esphome) [2](https://github.com/esphome/esphome/commits): [lvgl] Fix crash when using lvgl.list.add (#19177)
- [rmk-rs/rmk](https://github.com/rmk-rs/rmk) [2](https://github.com/rmk-rs/rmk/commits): Merge pull request #1141 from rmk-rs/codex/daily-review-20260912

fix(debounce): isolate fast debounce windows per key
- [shorepine/tulipcc](https://github.com/shorepine/tulipcc) [2](https://github.com/shorepine/tulipcc/commits): Merge pull request #1355 from shorepine/amyboard-bus-distortion

AMYboard Web: add bus Distortion section (type / drive / mix)

## [gemini](https://github.com/topics/gemini)
- [cactus-compute/needle](https://github.com/cactus-compute/needle) [3](https://github.com/cactus-compute/needle/commits): fix(grounding): stop rejecting thousands-separated numbers (#123)

* fix(grounding): clear separator-formatted numbers the engine flags as ungrounded

The engine parses a thousands-separated number correctly but its literal
substring grounding check reports the emitted value as fabricated, because
"1200.0" is not a substring of "$1,200.00". The Python package propagated
that verdict: extract() raised on a correct value and run() refused a
correct call, including the README's own extraction example.

A flagged numeric path is now cleared when the emitted value matches a
whole number token in the source under numeric comparison rather than
substring comparison. Only engine flags are removed, so the check cannot
reject a value the engine itself accepted.

Fixes #120

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
Signed-off-by: Som Samantray <som.samantray@gmail.com>

* fix(review): apply review findings

Anchoring the optional sign in the number-token pattern stops a hyphen
between digits from being read as a minus sign. Without it, a source
containing an ISO date such as 2026-09-01 yielded -9 and -1 tokens, so a
fabricated negative argument whose magnitude matched the date was treated
as grounded and the engine's ungrounded flag was cleared.

Adds regression coverage for the date and range hyphen cases, and for a
genuinely written negative still clearing.

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
Signed-off-by: Som Samantray <som.samantray@gmail.com>

---------

Signed-off-by: Som Samantray <som.samantray@gmail.com>
Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
- [brianpetro/obsidian-smart-connections](https://github.com/brianpetro/obsidian-smart-connections) [1](https://github.com/brianpetro/obsidian-smart-connections/commits): Refactor Connections tool to use 'key' instead of 'to' for improved consistency and update related tests
- [google/langextract](https://github.com/google/langextract) [1](https://github.com/google/langextract/commits): Route OpenAI reasoning and GPT-3.5 models (#494)

## [golang](https://github.com/topics/golang)
- [d2lang/d2](https://github.com/d2lang/d2) [52](https://github.com/d2lang/d2/commits): Merge pull request #2923 from d2lang/security/substitution-expansion-limits

security: bound variable substitution expansion
- [cshum/imagor](https://github.com/cshum/imagor) [1](https://github.com/cshum/imagor/commits): docs: links update and cleanup

## [ios](https://github.com/topics/ios)
- [iziz/libPhoneNumber-iOS](https://github.com/iziz/libPhoneNumber-iOS) [15](https://github.com/iziz/libPhoneNumber-iOS/commits): Merge pull request #454 from iziz/revert-breaking-changes

Remove the breaking changes so the next release can be 2.1.0
- [fastlane/fastlane](https://github.com/fastlane/fastlane) [10](https://github.com/fastlane/fastlane/commits): [ci] run full workflows on master as they stack (#30218)

* chore: run full workflows on main as they stack

* chore: queue master for all builds
- [sparrowcode/PermissionsKit](https://github.com/sparrowcode/PermissionsKit) [7](https://github.com/sparrowcode/PermissionsKit/commits): refactor: drop dead branches and unused imports across the permissions

EKAuthorizationStatusAuthorized is declared as an alias of fullAccess and
kCLAuthorizationStatusAuthorized as an alias of authorizedAlways, so in
Calendar, Reminders and Location the branch listed first swallowed the one
below it. Location now says plainly what it always did: always covers either
access level, when-in-use covers only its own.

Calendar and Location kept a Permission.Kind and unpacked it with switches
ending in fatalError, although each type only ever holds its own kind. They
store the access level instead and build the kind from it, which also lets
Calendar request the level directly rather than through two intermediate
closures.

The location handlers no longer implement locationManager(_:didChangeAuthorization:),
deprecated since iOS 14 and never called at the current deployment target.
Location imported EventKit instead of CoreLocation and Bluetooth imported
CloudKit without using it. The German strings file still carried nine keys
from an interface the package no longer ships.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
- [SwiftOldDriver/iOS-Weekly](https://github.com/SwiftOldDriver/iOS-Weekly) [3](https://github.com/SwiftOldDriver/iOS-Weekly/commits): Merge pull request #5433 from SwiftOldDriver/fix/issues-5432

fix: 5432

## [lists](https://github.com/topics/lists), [resources](https://github.com/topics/resources)
- [public-apis/public-apis](https://github.com/public-apis/public-apis) [8](https://github.com/public-apis/public-apis/commits): Merge pull request #7341 from mbilalawan926-sys/mbilalawan926-sys-patch-1

Add Best Temp Mail API
- [bkrem/awesome-solidity](https://github.com/bkrem/awesome-solidity) [5](https://github.com/bkrem/awesome-solidity/commits): docs: remove obsolete contribution link

## [macos](https://github.com/topics/macos)
- [Beingpax/VoiceInk](https://github.com/Beingpax/VoiceInk) [10](https://github.com/Beingpax/VoiceInk/commits): Merge pull request #930 from Beingpax/quick-history-panel

Quick history panel
- [pqrs-org/Karabiner-Elements](https://github.com/pqrs-org/Karabiner-Elements) [9](https://github.com/pqrs-org/Karabiner-Elements/commits): Update NEWS
- [jundot/omlx](https://github.com/jundot/omlx) [5](https://github.com/jundot/omlx/commits): docs: add security reporting policy
- [trycua/cua](https://github.com/trycua/cua) [5](https://github.com/trycua/cua/commits): docs(fleets): restructure cloud and local paths (#3766)

* docs: refresh Fleet package version facts

(cherry picked from commit 7c8b1afd13743efccb469055483f26fb10cc451b)

* docs(sandbox): add Fleet Driver control guide

(cherry picked from commit d6210362f58f8185595b556ec3d3b9ee95ae1ce2)

* docs(fleet): consolidate capacity and claim guides

(cherry picked from commit 659865c7ce40242cdb1c6f305b5c34b7c66958c6)

* docs(fleets): rewrite first cloud tutorial

(cherry picked from commit 58d90e556a0c1375ae212a259361f6fc465c3fb9)

* docs(fleets): correct TypeScript cleanup contract

* docs(fleet): separate cloud and local navigation

(cherry picked from commit e927433f88438ec50e62ac40ba3e01644a3df3ea)

* docs(sandbox): generate image and package facts

(cherry picked from commit bb4b21ac27cbb31416550399ba149f594ddf79c6)

* docs(fleets): align tutorial cleanup and entry copy

* ci(docs): use resolvable setup-node revision

* docs: remove redundant Start here nav link
- [milanvarady/Applite](https://github.com/milanvarady/Applite) [3](https://github.com/milanvarady/Applite/commits): Give the README screenshots a visible edge

The light capture's window chrome is #ffffff and so is GitHub's light
background, so the window had no discernible edge -- it bled straight
into the page. Add a macOS-style drop shadow.

A black shadow does nothing on GitHub's #0d1117 dark background, so the
dark capture gets a subtle light hairline instead, which is what macOS
dark-mode windows have anyway. Both effects are derived from each PNG's
own alpha channel, so they follow the window's rounded corners.

Done in ImageMagick rather than by re-capturing with screencapture's
built-in shadow: the light/dark pair stays pixel-identical in content and
window position, and screencapture's shadow varies with window focus and
is tuned for a desktop wallpaper rather than a README. The applite-site
copies stay unframed, since the site applies its own shadow in CSS.

Scripts/Screenshots/frame-for-readme.sh makes it repeatable for future
screenshot refreshes.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LtkqHQdHSbQDiRdydqmZvd
- [steipete/RepoBar](https://github.com/steipete/RepoBar) [1](https://github.com/steipete/RepoBar/commits): chore(deps): update SwiftLog and Zod

Update SwiftLog to 1.15.1 and Zod to 4.6.2, and record the maintenance changes under Unreleased.

Regenerate the stale SwiftPM origin hash left by the localization manifest change.

Validated with 683 tests across 111 suites, signed macOS app launch and About/Settings interaction, signed CLI execution, and live GraphQL helper HTTP checks. Dependency audit, independent branch review, and CI passed.

## [markdown](https://github.com/topics/markdown)
- [markedjs/marked](https://github.com/markedjs/marked) [4](https://github.com/markedjs/marked/commits): chore(release): 18.0.13 [skip ci]

## [18.0.13](https://github.com/markedjs/marked/compare/v18.0.12...v18.0.13) (2026-09-12)

### Bug Fixes

* allow tabs in the thematic break that ends a list item ([#4087](https://github.com/markedjs/marked/issues/4087)) ([afbb27c](https://github.com/markedjs/marked/commit/afbb27c7ee753af07fb1a5c18031fc3068261b31))
* avoid O(n^2) scanning in reflinkSearch ([#4090](https://github.com/markedjs/marked/issues/4090)) ([c6a25bb](https://github.com/markedjs/marked/commit/c6a25bb2a9d14f839cf2fd9abe4e4c7c3eece25b))
* case fold reference link labels ([#4077](https://github.com/markedjs/marked/issues/4077)) ([aed9336](https://github.com/markedjs/marked/commit/aed933680dc146d868cb4573f393367abde04aae))
* drop the leading whitespace after a hard line break ([#4075](https://github.com/markedjs/marked/issues/4075)) ([123ce04](https://github.com/markedjs/marked/commit/123ce04b813e0cd87a6dcb2326112ffb54022069))
* match html block start conditions when ending a list item ([#4072](https://github.com/markedjs/marked/issues/4072)) ([c2facac](https://github.com/markedjs/marked/commit/c2facac8d455c87034f82639c900242de288aca0))
* respect raw tokens when closing link labels ([#4066](https://github.com/markedjs/marked/issues/4066)) ([ef394f7](https://github.com/markedjs/marked/commit/ef394f71df54ab9d4057821881e866366eaacf11))
* strip a tab that follows spaces in an indented code block ([#4080](https://github.com/markedjs/marked/issues/4080)) ([dbb393d](https://github.com/markedjs/marked/commit/dbb393deebc5b6982cb29d7415e8a8ba5555b83a))
- [MarkEdit-app/MarkEdit](https://github.com/MarkEdit-app/MarkEdit) [3](https://github.com/MarkEdit-app/MarkEdit/commits): Add color pattern to theme picker (#1739)

## [openai](https://github.com/topics/openai)
- [BerriAI/litellm](https://github.com/BerriAI/litellm) [116](https://github.com/BerriAI/litellm/commits): Merge pull request #40907 from BerriAI/litellm_key_alias_substring_non_admin

fix(proxy): allow key_alias substring matching on /key/list for non-admins
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) [4](https://github.com/OpenHands/OpenHands/commits): fix(static-server): HTML-escape injected runtime config and set Cache-Control: no-store on credential injection (#17175)
- [gptme/gptme](https://github.com/gptme/gptme) [2](https://github.com/gptme/gptme/commits): fix(subagent): deliver subprocess control and capture stderr (#3819)

* fix(subagent): deliver subprocess control and capture stderr

Git-Session-Id: 8407

* fix(subagent): bound stderr tail reads

Git-Session-Id: 8407

* fix(subagent): cap stderr diagnostic reads

Git-Session-Id: 8407

* fix(subagent): preserve explicit hook allowlists

Git-Session-Id: 8407

* fix(subagent): honor explicit hook restrictions

Git-Session-Id: 8407

* fix(subagent): preserve control under configured hooks

Git-Session-Id: 70dd65ca-b3c2-52e0-be03-3a4fdaf72180
- [microsoft/markitdown](https://github.com/microsoft/markitdown) [2](https://github.com/microsoft/markitdown/commits): Preserve whitepace underlines (#2477)

* Preserve whitespace underlines

## [python](https://github.com/topics/python)
- [xlwings/xlwings](https://github.com/xlwings/xlwings) [3](https://github.com/xlwings/xlwings/commits): Merge pull request #2750 from xlwings/chunksize-default

default chunksize
- [lakehq/sail](https://github.com/lakehq/sail) [2](https://github.com/lakehq/sail/commits): test: migrate local object storage from MinIO to Silo (#2574)
- [aceinnolab/Inkycal](https://github.com/aceinnolab/Inkycal) [1](https://github.com/aceinnolab/Inkycal/commits): Merge pull request #434 from kfezer/fix/network-timeouts-hang-shutdown

Add timeouts to network/subprocess calls that can hang shutdown_after_run
- [kurigram-org/kurigram](https://github.com/kurigram-org/kurigram) [1](https://github.com/kurigram-org/kurigram/commits): Update Kurigram to v2.2.26
- [nltk/nltk](https://github.com/nltk/nltk) [1](https://github.com/nltk/nltk/commits): Isolate default WordNet reference relations (#3872)

## [rest](https://github.com/topics/rest)
- [FlareSolverr/FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) [3](https://github.com/FlareSolverr/FlareSolverr/commits): Update CHANGELOG.md
- [warmuuh/milkman](https://github.com/warmuuh/milkman) [1](https://github.com/warmuuh/milkman/commits): Merge pull request #224 from warmuuh/fix/jetty-client-issues-221

fix(rest): honor cert-validation toggle and strip newlines in Jetty client

## [rust](https://github.com/topics/rust)
- [crate-ci/typos](https://github.com/crate-ci/typos) [3](https://github.com/crate-ci/typos/commits): Merge pull request #1617 from nightah/fix-1444-walk-canonicalize-panic

fix(cli): Don't panic when canonicalize fails mid-walk
- [acsandmann/rift](https://github.com/acsandmann/rift) [2](https://github.com/acsandmann/rift/commits): chore: fmt
- [embassy-rs/embassy](https://github.com/embassy-rs/embassy) [2](https://github.com/embassy-rs/embassy/commits): Merge pull request #6997 from embassy-rs/stm32-adc-clean

stm32/adc: single unified driver, add HIL test for all chips.
- [probe-rs/probe-rs](https://github.com/probe-rs/probe-rs) [2](https://github.com/probe-rs/probe-rs/commits): fix(chip erase): running once per flash algorithm instead of once per chip (#4333)

Co-authored-by: Nikitina Nataliia (ES ICW SW MTP DSPT PRGT) <Liraelle@users.noreply.github.com>
- [nextest-rs/nextest](https://github.com/nextest-rs/nextest) [1](https://github.com/nextest-rs/nextest/commits): update LLM policy
- [sunng87/handlebars-rust](https://github.com/sunng87/handlebars-rust) [1](https://github.com/sunng87/handlebars-rust/commits): Add the Auric SPA MVC framework to the related projects section (#787)

## [speech-to-text](https://github.com/topics/speech-to-text)
- [ricky0123/vad](https://github.com/ricky0123/vad) [4](https://github.com/ricky0123/vad/commits): Update examples and docs
- [cjpais/Handy](https://github.com/cjpais/Handy) [2](https://github.com/cjpais/Handy/commits): feat: add Indonesian translation (#2073)

## [swift](https://github.com/topics/swift)
- [scinfu/SwiftSoup](https://github.com/scinfu/SwiftSoup) [16](https://github.com/scinfu/SwiftSoup/commits): Merge pull request #419 from scinfu/fix/upstream-08-benchmark-evidence-20260912

Add reproducible optimization benchmarks and qualification reports
- [weichsel/ZIPFoundation](https://github.com/weichsel/ZIPFoundation) [3](https://github.com/weichsel/ZIPFoundation/commits): Merge pull request #390 from weichsel/chore/test-runners

Modernize Test Matrix

## Other
- [Ephemeral-AI-Lab/layerfs](https://github.com/Ephemeral-AI-Lab/layerfs) [156](https://github.com/Ephemeral-AI-Lab/layerfs/commits): Add the v0.1.6 completion handoff

Records the exact terminal state, the runnable commands, and the four traps
that dominated the previous attempt: any source change invalidates every
collected receipt through the compilation seal, the workload helper cannot see
the SDK crates, the generic verifier assumes the initial fixture and one inode
class per declared path, and the one retained alias failure must be fixed by
root cause rather than by loosening the check.

The prompt states the stop condition explicitly: all 33 regular cases with
passing performance and independent verification on one final source and image,
all three extended cases terminal, seeds 1/2/3 qualified, no required row
FAIL/TIMEOUT/NOT_READY/NOT_RUN, and root cause for every failure. It also
states what is out of scope: no release or tag, no weakened workload, no
shortened K100, no relocation of a failed regular case into extended mode.
- [RfidResearchGroup/proxmark3](https://github.com/RfidResearchGroup/proxmark3) [59](https://github.com/RfidResearchGroup/proxmark3/commits): pm3_online_tests: make desfire_value gate the communication mode

The six plain/mac assertion pairs differed only by -m, and the file they ran
against was created with no --amode and no --rawrights - so plain mode, free
access. Free access is served in plain whatever the file says, and the client
derives the mode from the file settings rather than from -m, so both halves of
every pair sent the same bytes:

  --op credit -m mac    ->  90 0C 00 00 05 02 0A 00 00 00 00
  --op credit -m plain  ->  90 0C 00 00 05 02 0A 00 00 00 00

They passed on a client that could not do MAC mode at all, which is how
e1598cd62 shipped: it had removed CREDIT/DEBIT/LIMITED_CREDIT from
EV1D40TransmitMAC, and this suite stayed green.

Build a fixture that makes the client answer a different question per file
instead, and drop the -m flags, since deriving the mode is the thing under
test:

  data  00  mac      EEEE   free access, MACed file
  data  01  mac      0000   key protected
  data  02  encrypt  EEEE   free access, enciphered file
  data  03  encrypt  0000   key protected
  value 10  mac      00E0   credit plain, debit MAC, same file
  value 11  mac      0000   key protected
  value 12  plain    EEEE   the original case
  value 13  encrypt  0000   plus FreeValue, so GetValue is plain

File 10 is the one worth having: credit is granted by read & write only, which
is free there, while debit is also granted by the write right, which is key 0.
A single communication mode for the whole file cannot satisfy both.

Also dump the application. It has no ISO file ids, so the client's
GetISOFileIDs probe is refused and the PICC ends the session on it; a dump
that does not notice reads the first file's plain content as a response CMAC
and reports it as no data.

Checked against a client built at 08e389c0b, before the three fixes: the free
access data writes fail -20, the MACed value credit fails -20, and the dump
loses file 00. The 00E0 and FreeValue cases pass there too - they guard the
derivation against future regressions rather than reproducing an old bug.

Co-Authored-By: Claude Opus 5 (1M context)
- [Mentra-Community/MentraOS](https://github.com/Mentra-Community/MentraOS) [25](https://github.com/Mentra-Community/MentraOS/commits): Merge pull request #4026 from Mentra-Community/codex/pause-dev-google-play

Pause dev uploads to Google Play internal testing
- [buildroot/buildroot](https://github.com/buildroot/buildroot) [22](https://github.com/buildroot/buildroot/commits): package/ibm-sw-tpm2: bump version to rev183-2026-08-26

Rebased patch 0001 and added Upstream: tag.

Removed patches which are included in this release.

Signed-off-by: Bernd Kuhls <bernd@kuhls.net>
Signed-off-by: Julien Olivain <ju.o@free.fr>
- [openai/codex](https://github.com/openai/codex) [18](https://github.com/openai/codex/commits): Remove Astra sparkle animation from the TUI composer (#45137)

## What changed

Remove the animated stars shown when selecting Astra, along with their input, terminal-focus, and model-selection hooks.

## Testing

Retain draft text and live voice control snapshots in a standalone composer snapshot test, and remove sparkle-specific tests and snapshots.

GitOrigin-RevId: cbe4396e8700cabfb1e0db9fbe8f997b94316c0f
- [anthropics/claude-code](https://github.com/anthropics/claude-code) [16](https://github.com/anthropics/claude-code/commits): Merge pull request #93912 from anthropics/poteat/mod-tests-seat

mods: unit tests for diff, sec-default and telemetry, typed against the plugin declarations
- [jdx/mise](https://github.com/jdx/mise) [16](https://github.com/jdx/mise/commits): fix(release): publish mise-agent-env before mise (#13122)
- [openclaw/gogcli](https://github.com/openclaw/gogcli) [10](https://github.com/openclaw/gogcli/commits): feat(slides): derive missing image dimensions (#1132)

* feat(slides): derive missing image dimensions

* test(slides): avoid shadowing redirect test errors
- [ChrisBuilds/terminaltexteffects](https://github.com/ChrisBuilds/terminaltexteffects) [9](https://github.com/ChrisBuilds/terminaltexteffects/commits): Handle empty canvas text bounds
- [openclaw/acpx](https://github.com/openclaw/acpx) [9](https://github.com/openclaw/acpx/commits): feat: surface normalized ACP plan entries on runtime status events (#562)

Preserve normalized ACP plan snapshots on runtime status events so embedding hosts retain task content, status and valid priority. Explicit empty snapshots now clear stale plans while legacy text summaries and CLI wire output remain compatible.

Retain the contributor's parser and manager regressions, narrow enum validation, and document replacement semantics. Built runtime proof with upstream Codex ACP observed initial, completed and empty snapshots. Full validation passed with 1,054 tests plus 152 coverage tests and two existing platform skips.

Co-authored-by: Gadzan Mak <gadzan@qq.com>
- [Alishahryar1/free-claude-code](https://github.com/Alishahryar1/free-claude-code) [8](https://github.com/Alishahryar1/free-claude-code/commits): Preserve Artifact regex restrictions in shared Claude conversions (#1772)

## Why

Claude Code's Artifact tool can make an entire request fail before
inference because OpenAI rejects the Unicode property escapes in its
parameter schema. This was reproduced on the OpenAI subscription
provider with GPT-5.6 Luna; changing only the pattern to an ordinary
regex succeeded.

Fixes #1730.

## How

Translate the four reported Unicode categories into explicit character
ranges in the shared Claude-to-Chat-Completions and Claude-to-Responses
tool converters. Keep the original pattern's filename, length,
reserved-name, and Unicode exclusions instead of removing its
validation.

Accepted design choices:
- Share the conversion across providers using these Claude request
paths. Native Codex/Responses ingress is outside this issue's scope.
- Support `\p{Cc}`, `\p{Cf}`, `\p{Zl}`, and `\p{Zp}` as standalone atoms
in ordinary negated classes. Leave unsupported whole patterns unchanged.
- Derive the ranges lazily from Python's Unicode database, including
supplementary characters, without a new dependency. Equivalence is
verified against the tested Unicode runtimes; this is not a general
regex compiler.
- Copy only changed schema paths and preserve literal schema data,
unrelated fields, and the original request.

Regression tests cover both converters, SDK serialization, every Unicode
scalar against category membership and JavaScript's original pattern,
and nested-schema/escaping cases. Actual translated requests completed
Artifact calls on Luna and OpenRouter's free Nemotron 3.5 Lightning
model. Bump 6.2.15 to 6.2.16.

Full local CI passed on rerun: 5,594 Python tests and 117 browser tests.
The first run encountered an intermittent unclosed-file warning in the
unchanged concurrent retired-chat cleanup test; that test file passed
independently and the full rerun passed.
- [darlal/obsidian-switcher-plus](https://github.com/darlal/obsidian-switcher-plus) [5](https://github.com/darlal/obsidian-switcher-plus/commits): build: version bump 6.2.0
- [steipete/agent-scripts](https://github.com/steipete/agent-scripts) [5](https://github.com/steipete/agent-scripts/commits): feat(browser-use): add Chrome remote-debugging auto-approve watcher
- [ccusage/ccusage](https://github.com/ccusage/ccusage) [4](https://github.com/ccusage/ccusage/commits): fix(issue-gate): avoid parsing status suffix (#1716)
- [eternnoir/pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) [3](https://github.com/eternnoir/pyTelegramBotAPI/commits): Merge pull request #2626 from Badiboy/chatgpt

Bot API 10.3 update
- [jamesbowman/cuflow](https://github.com/jamesbowman/cuflow) [3](https://github.com/jamesbowman/cuflow/commits): wordclock2 ready to order
- [openclaw/imsg](https://github.com/openclaw/imsg) [3](https://github.com/openclaw/imsg/commits): chore: prepare 0.15.4 release

Prepare patch 0.15.4 for native inline voice playback and refreshed phone metadata. Date the ordered Highlights section and synchronize the environment, generated Swift constant, and bundle metadata.
- [OpenStickCommunity/GP2040-CE](https://github.com/OpenStickCommunity/GP2040-CE) [3](https://github.com/OpenStickCommunity/GP2040-CE/commits): Removing a double translation in chinese (#1712)
- [alibaba/open-code-review](https://github.com/alibaba/open-code-review) [2](https://github.com/alibaba/open-code-review/commits): perf(grouping): return file indices instead of paths (#1209)

The grouping LLM call asked the model to echo full file paths back in its
JSON response, making the output size proportional to the sum of all path
lengths. On large change sets this overflowed the completion token limit;
the truncated JSON then failed to parse and the whole change set degraded to
per-file dispatch, multiplying downstream review calls.

Switch the grouping contract to integer indices:

- buildFileList prefixes each file with a zero-based index, e.g.
  "[0] MODIFIED path (+12/-3)".
- groupingResponse.Files is now []int; the model returns those indices.
- parseGroupingResponse maps indices back to diffs by position, skipping
  out-of-range indices (the index equivalent of the previous unknown-path
  skip) and duplicates. A parse failure still returns an error and the
  caller falls back to per-file dispatch, exactly as before.
- Prompts updated to ask for integer indices.

The response is now an order of magnitude smaller, so truncation on large
change sets becomes rare instead of common.

Because the grouping response is now indices, the session viewer resolves
them back to paths for display:

- buildGroupingIndex scans the request's numbered file list (user message
  only) to build an index->path map.
- parseGroupingGroups unmarshals the response into indices; a legacy
  path-string response reports not-ok so the viewer keeps showing the raw
  text (already readable for those older sessions).
- groupingView maps indices to paths and falls back to the raw response
  when nothing resolves (format drift), avoiding a wall of "#idx".
- The grouping card renders label + resolved paths with a collapsible raw
  response for audit. No on-disk format changes; existing sessions render
  retroactively.
- [block/buzz](https://github.com/block/buzz) [2](https://github.com/block/buzz/commits): fix(acp): improve hints in pi agent setup guide (#7594)

## Summary

Handle missing Pi adapter setup and update its install guidance.

### Related issue

None found.

### Testing

No manual testing.

Generated with Amp

---------

Signed-off-by: Salman Mohammed <smohammed@squareup.com>
Co-authored-by: Amp <amp@ampcode.com>
- [cpldcpu/BitNetMCU](https://github.com/cpldcpu/BitNetMCU) [2](https://github.com/cpldcpu/BitNetMCU/commits): Fix spelling and grammar errors in documentation_2026.md
- [databendlabs/openraft](https://github.com/databendlabs/openraft) [2](https://github.com/databendlabs/openraft/commits): test: turmoil: bump rand to 0.10 and move to upstream turmoil 0.7.2

# Summary

`tests-turmoil` now depends on rand 0.10 and on turmoil 0.7.2 from
crates.io instead of the `v0.6.6-openraft.1` fork. The fuzzer uses the
rand 0.10 names (`RngExt`, `random_range`, `random_bool`, `random`).

# Details

The fork existed only to seed each host runtime's tokio RNG through
`tokio::runtime::Builder::rng_seed`. turmoil 0.7.0 merged the same fix
upstream (tokio-rs/turmoil#245): `Rt::init` now seeds every host runtime
from the world RNG under `tokio_unstable`, so the fork patch would be
dead code on 0.7.x. `--cfg tokio_unstable` stays mandatory for the same
reason as before.

The 0.6 fork's `Builder::build_with_rng` took a rand 0.8 `RngCore`, so a
rand 0.10 `SmallRng` could not seed the simulation. 0.7's
`Builder::rng_seed(u64)` takes a plain seed, which removes the rand
coupling entirely.

The requirement is `0.7.2`, the version verified here; 0.7.0 and 0.7.1
lack the TCP flow control (tokio-rs/turmoil#265) and RST-on-drop
(tokio-rs/turmoil#269) behaviour that the fuzzer now runs under.

Seeds recorded before this commit no longer reproduce the same runs:
rand 0.10 changed range sampling, and turmoil 0.7 changes both world-RNG
consumption and network fault behaviour (tokio-rs/turmoil#252, #265,
#269). Reproducibility itself is intact: two `fuzz --reproduce 12345`
runs produce byte-identical output.
- [facebook/idb](https://github.com/facebook/idb) [2](https://github.com/facebook/idb/commits): Select accessibility reads for read-only clients

Summary:
Teach the accessibility test module to select only read assertions when the harness marks its client read-only. The full suite still loads every method; no assertion is weakened or skipped there.

The selected set excludes exactly the two tap tests and the scroll test, which require interaction support rather than accessibility reads.

Differential Revision: D119428932

fbshipit-source-id: 887de446d217ee7f1e5d6a3ec657abc9ee9d3fad
- [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) [2](https://github.com/ghostty-org/ghostty/commits): build: refactoring our use of translate-c (#14203)

This commit refactors our use of translate-c, in preparation for larger
removal of `cImport` and better co-ordination between building of C
dependencies and translation of headers.

The major update is the creation of an internal helper package that
wraps our use of the external translate-c library. This allows us to not
only have better shorthand and a data-driven, declarative approach to C
translation (versus the otherwise more imperative approach), it also
funnels the external dependency into a single package instead of
spreading it out among what will be an increasingly larger amount of
places as dependencies in `pkg/` get updated.

It also includes some refactors, namely to the harfbuzz package, which
has had its individual settings refactored into helpers to allow for the
settings to be better shared between translation and the build of the
c-based static library.

Wuffs has also had a bit of a refactor too so that we don't generate a
file with all of the macro defines in it - we just send these in as `-D`
flags now.
- [OpenBMB/MiniCPM](https://github.com/OpenBMB/MiniCPM) [2](https://github.com/OpenBMB/MiniCPM/commits): Merge pull request #377 from OpenBMB/minicpm5-2b

docs: update sampling parameters in README and related files to preve…
- [TactilityProject/Tactility](https://github.com/TactilityProject/Tactility) [2](https://github.com/TactilityProject/Tactility/commits): ESP-IDF v6.1 (#649)

Migrate all drivers and devices to ESP-IDF v6.1
- [theyosh/TerrariumPI](https://github.com/theyosh/TerrariumPI) [2](https://github.com/theyosh/TerrariumPI/commits): New Svelte GUI build
- [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) [1](https://github.com/abetlen/llama-cpp-python/commits): feat: update llama.cpp to v0.4.0 (#2367)
- [anthropics/buffa](https://github.com/anthropics/buffa) [1](https://github.com/anthropics/buffa/commits): examples: pin bsr-quickstart to one buffa release and check it in CI (#436)

`examples/bsr-quickstart` pinned the BSR plugin at v0.5.2 but compiled
against the in-tree runtime through path dependencies, and the
checked-in `src/gen/example.v1.rs` matched neither. Four errors on
`18476fa`, as reported.

That file had been hand-patched four times since it was generated (#184,
#284, #409, #381) rather than regenerated, so it tracked the in-tree API
by hand while still being described as published-plugin output. The
directory sits in the workspace `exclude` list, so nothing compiled it
and each round of drift stayed invisible.

**Neither half of the fix works alone.**

Pinning the runtime back to crates.io `=0.5.2` to match the plugin fails
with a different three errors, because the file is no longer v0.5.2
output:

```
error[E0433]: cannot find `unsafe_impl_view_lifetime_parametric` in `buffa`
error[E0433]: cannot find `DecodeContext` in `buffa`
error[E0407]: method `decode_view_with_ctx` is not a member of trait `::buffa::MessageView`
```

Bumping only the plugin pin fails too. v0.9.2 is published, but #381
requires the `ViewLifetimeParametric` marker and no published plugin
emits it yet, so published v0.9.2 output against `main` gives four of

```
error[E0277]: `GreetingView<'_>` does not implement `ViewLifetimeParametric`
```

which is the situation #381's own description calls out as needing a
0.10 BSR plugin.

So the plugin pin moves to v0.9.2, `src/gen/` is regenerated from it,
and `buffa` / `buffa-types` move to the matching crates.io release. Both
halves come from one buffa version, which is also what a downstream BSR
user has, and the example stops depending on `main`. That is what clears
the "cannot be regenerated until a 0.10 BSR plugin is published"
blocker: the example no longer needs to track `main`, so a 0.10 plugin
is only wanted when the example should start demonstrating 0.10.

The `unsafe_impl_view_lifetime_parametric!` line added by hand in #381
goes away with the regen, which is correct here: `buffa` 0.9.2 has no
such macro, and the example no longer compiles against the runtime that
requires it.

The cost is the forward-compat canary the old `Cargo.toml` comment
described, and it was not working. The published plugin lags `main` by
design, so between releases the canary's only outcome was a red example,
and it was being silenced by hand-patching rather than acted on. In-tree
codegen against the in-tree runtime is already covered by `buffa-test`
and the two codegen compile matrices in `lint-and-test`.

A `cargo check` step in `lint-and-test` now covers the example. With
both pins naming one release it can only go red if one pin moves without
the other, which is what the release bump has to get right anyway.

## Verified

Regenerated with `buf generate` against the pinned v0.9.2 plugin, then
in `examples/bsr-quickstart`:

```
cargo check                                clean
cargo run                                  encodes 47 bytes, prints the views and the JSON
cargo clippy --all-targets -- -D warnings  clean
```

Cross-check on the regen: published v0.9.2 plugin output and the in-tree
`protoc-gen-buffa` differ by exactly the one
`unsafe_impl_view_lifetime_parametric!(GreetingView);` line, so the
published plugin is otherwise current with in-tree codegen.

Not run: the workspace test suite, since nothing here touches a
workspace crate. The `ci.yml` step is the only change outside
`examples/bsr-quickstart` and `.changes/`.

This is option 2 from the issue. If you would rather have option 1, the
regenerated `src/gen/` is the same file either way and only the two
`Cargo.toml` lines change, but it does not compile against `main` today
for the #381 reason above.

Fixes #427.

---------

Co-authored-by: Iain McGinniss <309153+iainmcgin@users.noreply.github.com>
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) [1](https://github.com/anthropics/claude-agent-sdk-python/commits): chore: bump bundled CLI version to 2.1.270
- [antirez/ds4](https://github.com/antirez/ds4) [1](https://github.com/antirez/ds4/commits): DeepSeek v4.1 Flash support for Metal
- [biliup/biliup](https://github.com/biliup/biliup) [1](https://github.com/biliup/biliup/commits): fix(docker): FFmpeg 固定到 BtbN 月末 autobuild (#1691)

autobuild-2026-08-29 已被上游删除，Docker 构建 404。BtbN 只长期保留每月最后一天的构建，改为固定 autobuild-2026-08-31-13-27 并更新 SHA-256。
- [daijro/camoufox](https://github.com/daijro/camoufox) [1](https://github.com/daijro/camoufox/commits): Update README

September updates
- [hathach/tinyusb](https://github.com/hathach/tinyusb) [1](https://github.com/hathach/tinyusb/commits): Merge pull request #3869 from Duet3D/master

dcd/samx7x: fix ZLP being dropped on DMA-capable IN endpoints
- [josephmisiti/awesome-machine-learning](https://github.com/josephmisiti/awesome-machine-learning) [1](https://github.com/josephmisiti/awesome-machine-learning/commits): Add Glyph library to Javascript NLP resources list (#1404)
- [Julow/Unexpected-Keyboard](https://github.com/Julow/Unexpected-Keyboard) [1](https://github.com/Julow/Unexpected-Keyboard/commits): Fix key opacity settings not working (#1422)

setAlpha() is overriden by setColor().
- [mikf/gallery-dl](https://github.com/mikf/gallery-dl) [1](https://github.com/mikf/gallery-dl/commits): release version 1.32.12
- [moonlight-stream/moonlight-android](https://github.com/moonlight-stream/moonlight-android) [1](https://github.com/moonlight-stream/moonlight-android/commits): Version 12.2
- [mozilla/sccache](https://github.com/mozilla/sccache) [1](https://github.com/mozilla/sccache/commits): ci: dump sccache logs on integration failures
- [rs/xid](https://github.com/rs/xid) [1](https://github.com/rs/xid/commits): Reject non-string JSON values when decoding IDs (#125)
- [sonocotta/esp32-audio-dock](https://github.com/sonocotta/esp32-audio-dock) [1](https://github.com/sonocotta/esp32-audio-dock/commits): Added husb238a component config for louder-esp32-mini (#179)

* Added husb238a component config for louder-esp32-mini

* Added 55-mm configs

* rename files

* restored main branch before merge

---------

Co-authored-by: andriy.malyshenko <andriy@sonocotta.com>
- [typst/typst](https://github.com/typst/typst) [1](https://github.com/typst/typst/commits): Improve type safety in flow layout (#8761)

Co-authored-by: Laurenz <laurmaedje@gmail.com>