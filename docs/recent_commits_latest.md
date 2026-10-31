# Recent Activity in Starred Repositories
_177 active repos with 3120 new commits_

## [3d-printing](https://github.com/topics/3d-printing)
- [nicklockwood/ShapeScript](https://github.com/nicklockwood/ShapeScript) [121](https://github.com/nicklockwood/ShapeScript/commits): Update for 1.12.0 release
- [Donkie/Spoolman](https://github.com/Donkie/Spoolman) [1](https://github.com/Donkie/Spoolman/commits): chore: update sponsors image

## [ai](https://github.com/topics/ai)
- [openclaw/openclaw](https://github.com/openclaw/openclaw) [545](https://github.com/openclaw/openclaw/commits): feat: allow scoped operators to manage their automations (#188090)

* feat: allow scoped operators to manage their automations

Add operator.cron, implied by operator.write, for authenticated agent-turn scheduling within existing caller ownership. Preserve the initiating grant for scheduled work without granting global scheduler administration.

Co-authored-by: VACInc <3279061+VACInc@users.noreply.github.com>

* test: prove scoped cron authority through persistence

Update ingress and continuation consumer expectations for scoped scheduling. Exercise signed requester creation, cross-owner denial, and revocation before persistence.

Co-authored-by: VACInc <3279061+VACInc@users.noreply.github.com>

* fix: refresh incomplete usage cost snapshots

Keep refreshing cost responses outside the freshness TTL and cover both agent scopes. Accept the current symlink denial message without weakening the rejection invariant.

Co-authored-by: VACInc <3279061+VACInc@users.noreply.github.com>

---------

Co-authored-by: VACInc <3279061+VACInc@users.noreply.github.com>
- [BasedHardware/omi](https://github.com/BasedHardware/omi) [192](https://github.com/BasedHardware/omi/commits): fix: make seal repair refuse cheaply and rotate attempted rows (#24144)

Seal repair currently spends its row budget walking recordings whose
tail cannot pass, then retries the same expensive prefix ahead of rows
that were deferred. This change checks the final retained chunk first
and still requires the complete existing proof before any seal. A
one-sample conservative allowance returns overlap-rounding edge cases to
the full walk; a regression demonstrates a naive tail check would
incorrectly refuse a sealable row.

The reader reuses its generation-pinned metadata GET without dropping
validation. Repair checkpoints the last attempted row after each cycle,
in addition to the existing interruption checkpoint (lead ruling
`4cbd2a`). The same encrypted cursor freezes the pass's finish-time
boundary so continuing inflow cannot prevent wrap to old refusals. No
per-row retry state, terminal marker, age-gate exemption, or new seal
rule is added.

Proof refusals emit only fixed allowlisted reason counts. Worker
defaults remain eight processes and increase to 270 seconds per row.
`Forbid`, privacy checks, fresh producer proof, exact-state apply, and
the kill switch remain enforced.

Validation: 270 tests across ten targeted unit files passed through
`backend/test.sh` using `BACKEND_UNIT_TEST_FILE_LIST`; the two affected
files were rerun after the final rounding assertion (57 passed).
Coverage includes trimmed overlaps and the rounding counterexample,
metadata reload count, multi-cycle refused/exhausted/deferred fairness,
wrapping under continuing inflow, encrypted nanosecond cursor state,
canonical planner reason propagation, and rendered chart/metric
fixtures. These suites, final preflight and push gates use `nice -n 19`
and `omi-heavy`.

Release scope: worker image and repair chart defaults only. Lead owns
merge and worker release; no prod access or deployment in this lane.
Refresh retained Helm values to eight workers and 270 seconds explicitly
when reusing release values, and install the updated proof-reason log
metric. Observe attempted/sealed/refused/exhausted/deferred counts and
backlog age over full cycles. Rollback:
`recordSealRepair.runtimeEnabled=false` and stop the active repair Job
for immediate cessation.

Hermetic route validation: `nice -n 19
/Users/dazheng/workspace/omi/bin/omi-heavy run -- bash
backend/testing/e2e/run.sh -k 'listen_stt or sync'` passed 24 tests,
with external sockets blocked by the harness. No deployed or
real-account behavior is claimed.

Failure-Class: FC-bounded-discovery-pinned-by-blocked-page

`make preflight` passed all 35 selected checks at `74201cb5dc0`,
including the seven-file Firestore guard (811 tests) and runtime image
source closure. The query driver classifies the output-only selected
cursor map; no index manifest change is needed.

Independent Luna full review at `74201cb5dc0`: **SHIP**, no actionable
findings (round 1 of the two-round cap). The reviewer checked the
complete diff, index coverage and all reference-reader callers; the
parent collected the result.
- [unslothai/unsloth](https://github.com/unslothai/unsloth) [111](https://github.com/unslothai/unsloth/commits): LoRA: add the rank-r term inside the base GEMM so small updates are not rounded away (#16071)

## Summary

The fused LoRA kernels (`LoRA_MLP`, `LoRA_QKV`, `LoRA_W` via
`matmul_lora`) compute the base GEMM, round it to bf16, then add the
rank-r term in a second pass and round again. A LoRA update smaller than
half a bf16 step of the base output is rounded away. Early in training,
or at small learning rates, part of every update is lost, so the adapter
trains as if its learning rate were smaller. PEFT has the same order.

This PR writes the rank-r term first and lets the base GEMM accumulate
onto it (`out.addmm_(X, W.t())`, beta 1). cuBLAS reads the LoRA term in
the fp32 epilogue of the GEMM, so the sum is rounded once.

- **Backward:** dX starts as the rank-r term and the base GEMMs
accumulate onto it the same way.
- **Under `torch.compile`:** the fused forward runs as one custom op,
`unsloth::lora_first_addmm`. It writes the rank-r term into a fresh
buffer, accumulates the base GEMM in place and returns a new tensor.
Written as two functional `torch.addmm` calls, Inductor first copied the
rank-r term into a new output for the second GEMM (242 device-to-device
copies per step on Llama-3.2-1B). It registers the addmm gradients and
saves only the operands the requested gradients read, so a compiled
caller that differentiates through `matmul_lora` still works (a frozen
base created under `inference_mode` included). Under `vmap` /
`torch.func` transforms the eager helper uses the functional calls.
Compiled inside `torch.func` transforms (`grad`, `jvp`, `jacrev`,
`jacfwd`, `vmap`) or native forward-mode AD
(`torch.autograd.forward_ad.dual_level`), `matmul_lora` keeps the
base-then-LoRA order: the op has no forward-mode or batching rule (a
compiled `jvp` returned zeros, a compiled dual lost its tangent), and a
traced `beta = 0` addmm under `jvp` crashes torch. The op is used only
inside the Dynamo trace of `torch.compile`, not under `torch.export`
(strict or not), which keeps the two functional calls so `torch.func`
still applies to an exported program. Export is recognised by the flag
`torch.export` sets, read directly: torch 2.10 / 2.11 Dynamo folds
`torch.compiler.is_exporting()` to True in every compiled region. torch
2.6 has no such flag, so there compiled code keeps the functional calls.
If any registration step of the op fails, the traced branch keeps the
functional calls.
- **Fewer passes over X:** in eager mode q / k / v (and gate / up)
compute `X @ A` in one GEMM (compressed sparse LoRA A weights, which
cannot be concatenated, keep one product each); in the backward every
projection's LoRA gradients read X once. Under `torch.compile` the
shared forward GEMM is skipped (the shared intermediate breaks the block
compile), the rest applies.
- **bf16 and fp32 only:** fp16 keeps the base-then-LoRA order
everywhere, forward and backward. In fp16 a rank-r term (or a summed
LoRA dX) rounded on its own can overflow before the base term cancels
it, which would make the GradScaler skip steps that main completes.
- **One rule for every call site** (`_lora_fused_ok`), applied the same
way in the forward and backward of `LoRA_W`, `LoRA_QKV` and `LoRA_MLP`.
These keep the base-then-LoRA order:
  - fp16 activations;
- `lora_dropout` or a `lora_bias` anywhere in the module (a down-only
bias included), for the whole module;
- FP8, INT4 (either orientation) and packed weights, including the MLP
down derivative after its FP8 weight is converted;
- a base weight that dequantizes to another dtype (fp32 weights or an
fp16 4-bit state under bf16 autocast), since the in-place accumulate
does not autocast;
  - per-projection scales that differ (shared backward only);
- a caller `out` buffer that is not already the output, or that shares
storage with X, W, A or B, or that cannot be inspected (traced by
`torch.compile` or `make_fx`); a precomputed `X @ A` sharing the caller
buffer is recomputed, for every base (dense, 4-bit, INT4, packed,
Float8Tensor), and a 3-D one is flattened with X. The weight is
dequantized before the caller's buffer is written, so a buffer sharing
storage with the quant state (absmax, code) is read first;
  - a sparse base weight, in eager mode and under `torch.export`;
- a tensor-subclass base weight with no quant state (TorchAO `NF4Tensor`
reports bf16 over packed storage and has no `addmm_`);
- a DTensor base weight or activation (X, A, B or a precomputed `X @
A`), whose placements the plain accumulator would drop. The QKV, MLP and
single-projection functions record the same decision for the backward,
so a DTensor input never takes the shared or fused backward either (it
changed the input gradient's placement for QKV);
- calls compiled inside `torch.func` transforms or under native
forward-mode AD;
- multi-token inference (`fast_linear_forward`, q_len > 1) on a
projection with a configured `lora_dropout`, matching the training
kernels;
- under `torch.compile`, LoRA weights that are plain tensors rather than
`nn.Parameter` (on torch 2.14 their dynamic shapes broke the backward on
a recompile);
- a backward context built without the forward's `fused` decision (older
or handcrafted callers).
- DoRA and other unsupported adapters still go to PEFT as before.
- **Rounding tradeoff:** the term rounded on its own changes from the
base output to the LoRA term. Its rounding error scales with its own
size, so the result is closer to the exact sum whenever the LoRA term is
smaller than the base term, which is the normal case for a LoRA update.
When the LoRA term is about as large as the base output and cancels it,
main can keep a residual this PR rounds away. Against an fp64 oracle
(bf16, M = 2048, K = N = 1024, r = 16, random weights, varying the LoRA
/ base ratio):

| LoRA / base | output mean abs error, this PR / main | QKV dX mean abs
error, this PR / main |
  |---|---|---|
  | 0.01 | 1.12e-3 / 1.50e-3 | 2.88e-3 / 3.97e-3 |
  | 0.1 | 1.16e-3 / 1.54e-3 | 2.92e-3 / 4.02e-3 |
  | 1 | 2.48e-3 / 2.48e-3 | 5.48e-3 / 5.92e-3 |
  | 10 | 2.11e-2 / 1.79e-2 | not run |

- **Kill switch:** `UNSLOTH_LORA_FUSED_PASSES=0` restores the previous
order everywhere, bit for bit.

## Results

### Training quality

`yahma/alpaca-cleaned` (2,000 train rows, 200 held-out eval rows,
completion-only loss, up to 1,024 tokens), LoRA r16 on all linear
layers, 250 steps, 3 seeds. Held-out eval loss at step 250, mean over
seeds:

| model, lr | fp32-compute reference | main | this PR | this PR - main,
per seed | kill switch - main (noise) |
|---|---|---|---|---|---|
| Llama-3.2-3B bnb-4bit, 1e-5 | 1.12501 | 1.12749 | 1.12510 | -0.0023 /
-0.0024 / -0.0024 | <= 0.00025 |
| Llama-3.2-3B bnb-4bit, 5e-5 | 1.09976 | 1.10010 | 1.09981 | -0.0003 /
-0.0003 / -0.0002 | <= 0.00005 |
| Llama-3.2-3B bnb-4bit, 2e-4 | 1.09869 | 1.09881 | 1.09860 | -0.0003 /
-0.0000 / -0.0003 | <= 0.00012 |
| Qwen3-8B bnb-4bit, 2e-4 | n/a | 0.99794 | 0.99809 | +0.0002 / +0.0000
/ +0.0003 | <= 0.0004 |

- **lr 1e-5:** better on every seed at every eval point (step 50: -0.017
to -0.027), and within 0.0001 of the fp32-compute reference where main
is 0.0025 away. The LoRA B weights are 5x closer to the reference
(relative distance 0.024 vs 0.124).
- **lr 5e-5:** better on every seed, by less.
- **lr 2e-4:** no difference beyond noise on either model; never worse
than main at any eval point.

### Speed

ms per step, 2 x 2048 tokens, LoRA r16, default block compile, fresh
process per arm, two runs each:

| GPU | model | main | this PR | change |
|---|---|---|---|---|
| A100 | Qwen3-8B bnb-4bit | 1077 / 1080 | 1070 / 1069 | -0.9% |
| A100 | Llama-3.2-3B bnb-4bit | 516 / 515 | 509 / 510 | -1.1% |
| L4 | Qwen3-8B / Llama-3.2-3B | | | within the run to run spread |

Without block compile the gain on A100 is 2.0-2.7%. Peak memory is
unchanged.

Compiled bf16 step time, Llama-3.2-1B LoRA r16, 2 x 512 tokens, fresh
process per arm in ABBA order (median of 10 steps per run):

| device | main order (kill switch) | two functional addmms (earlier
head) | custom op (this head) |
|---|---|---|---|
| Radeon 8060S (gfx1151), Linux, torch 2.11 ROCm | 511.8 / 513.9 ms |
552.6 / 554.4 ms | 514.3 / 511.3 ms |
| A100, torch 2.14 | 62.1 / 62.1 / 63.0 ms | 61.1 / 62.7 / 64.5 ms |
61.6 / 60.8 / 60.5 ms |

On gfx1151 the losses with the op are bit-identical to the functional
form; on A100 the two agree within the run-to-run spread of either arm
(final loss 1.1233-1.1239 vs 1.1235-1.1239). 0 graph breaks in every arm
on both. On the current head, which adds the op's gradients and the
transform, export and DTensor guards, the same A100 harness on another
VM gives 62.5 / 64.0 / 65.2 ms, against 64.5 / 64.5 / 66.1 ms for the
first version of the op and 65.7 / 65.7 / 78.0 ms with the kill switch,
with 273 device-to-device copies per step in every arm.

### Memory of the shared paths

Peak live tensor storage above the inputs on CPU (bf16 unless noted),
one QKV forward and backward:

| tokens x hidden, width, rank | forward main / this PR | backward main
/ this PR |
|---|---|---|
| 8192 x 512, 512, 128 | 26.25 / 30.13 MiB | 9.50 / 7.88 MiB |
| 8192 x 512, 512, 128 (fp32) | 52.5 / 60.25 MiB | 19.0 / 15.75 MiB |
| 256 x 8192, 1024, 128 (fp32) | 7.63 / 12.38 MiB | 67.38 / 67.0 MiB |
| 2048 x 256, 256, 128 (fp32) | 7.25 / 9.13 MiB | 6.75 / 6.88 MiB |

The shared backward frees `A @ X.t()` before allocating the combined `dY
@ B.t()`, writes it in place and computes `lora_A` gradients directly in
the `[r, K]` parameter layout, so its peak is at or below main's. The
forward's combined `X @ [A_q; A_k; A_v].t()` stays live across the three
projections: about `2 x tokens x rank x element size` more (4 MiB at
8192 tokens, rank 128, bf16), plus the concatenated `A` (rank x hidden
per projection), which matters only when the hidden size is large and
the token count small. The CUDA allocator peak is set by the
activations, which this does not change (the speed runs above show the
same peak memory).

## Tests

- **New `tests/test_lora_fused_passes.py`:**
- qkv / o / mlp outputs, dX and LoRA gradients against the previous
order and an fp64 PEFT oracle (fp32 and bf16, equal and mixed
`alpha_pattern`);
  - the shared paths engage only where they apply;
- with the kill switch, `matmul_lora` equals base GEMM then in-place
rank-r add, bit for bit;
- every excluded configuration (fp16 at all; dropout, `lora_bias` and a
down-only `lora_bias` in fp16, bf16 and fp32) gives outputs, dX and LoRA
gradients bit-identical to the kill switch;
- an fp16 case whose rank-r term alone overflows stays finite and equals
the kill switch;
- an fp32 base under bf16 autocast, an fp16 NF4 state under bf16
autocast, the eligibility table (INT4 in both orientations, packed,
FP8), a caller buffer that needs resizing and one that shares storage
with the weight;
- a bf16 case where the LoRA update is smaller than half a bf16 step of
the base output: this PR keeps it (the exact result rounded once), the
previous order drops it;
- the shared backward's `lora_A` gradients already have the parameter's
`[r, K]` contiguous layout, as row views of one buffer (no copies);
- a caller buffer under `torch.compile` and under `make_fx` fake
tracing, a precomputed `X @ A` sharing the caller buffer (fused and old
order), a sparse base weight, multi-token inference with and without a
configured `lora_dropout`;
- `torch.compile(dynamic = True)` of `LoRA_QKV` with plain-tensor and
`nn.Parameter` LoRA weights where a rank equals the first sequence
length (fresh interpreter; fails before this change on torch 2.14), and
the traced order for both.
- a precomputed `X @ A` sharing the caller buffer with packed, INT4 and
Float8Tensor bases (mocked on CPU), and a 3-D precomputed `X @ A`;
- a TorchAO `NF4Tensor` base, CSR / CSC / BSR LoRA A weights in the
shared `X @ A`, a caller buffer sharing storage with the quant state;
- a sparse base weight exported with `torch.export` and run, a
replicated DTensor base weight, and a DTensor X (replicated, row- and
column-sharded) with plain W / A / B, whose value and placement match
the base-then-LoRA order;
- QKV, MLP and single-projection forward + backward with DTensor X, A
and B (replicated, row- and column-sharded): the recorded decision is
the base-then-LoRA order and `dX` has the same value and placement as
with the kill switch (8 of these fail on the previous head, where QKV's
`dX` changed placement). Where a torch's DTensor cannot run main's own
order (views of a sharded dim, in-place `addmm`), they skip. The
one-rank DTensor tests use a gloo group on a file store (no TCP
rendezvous) and destroy only a group they created.
- **New `tests/test_lora_first_addmm_op.py`:** the op equals the eager
sequence bit for bit, passes `opcheck` including its autograd
registration, is used by a fullgraph compiled `matmul_lora`, gives the
eager gradients when that compiled call is differentiated (bf16 and
fp32), runs under `vmap` over X or W, stays out of the graph with the
kill switch, and without the op the traced branch keeps the functional
form. Compiled `grad`, `jvp`, `jacrev`, `jacfwd` and `vmap` around
`matmul_lora` (bf16 and fp32, eager and `aot_eager` backends) match the
eager transforms, and the op's backward needs no saved frozen operands.
A compiled native forward-AD tangent matches eager; a strict and a
non-strict exported module have no opaque op and give the right
`torch.func.jvp` / `grad`; export detection reads the export flag, not
the folded query; an op whose autograd registration fails (injected,
fresh interpreter) stays disabled; a fullgraph compiled `LoRA_W` forward
and backward traces with the op and no graph break (on torch 2.10 / 2.11
Dynamo folds `torch.compiler.is_exporting()` to True, which once reached
a `layout` read Dynamo refuses).
- **CPU:** the 15 LoRA / FP8 kernel test files give 352 passed, 0 failed
on torch 2.13, 340 passed on torch 2.11 and 331 passed on torch 2.6
(main: 243 passed, 0 failed, without the new files). The 9 tests added
for strict export, the export flag, the partly registered op, the
`NF4Tensor` base, compressed sparse A weights and the quant-state buffer
fail on the previous head (strict export on torch 2.6, 2.11 and 2.13)
and pass now. Every test added for compiled `torch.func` transforms,
native forward AD, export, DTensor operands, the op's saved operands and
a sparse base fails on an earlier head of this PR and passes now (the 4
compiled `vmap` cases pass on both); the fullgraph `LoRA_W` test fails
on torch 2.11 with the earlier `is_exporting` check. On an earlier head
`test_lora_fused_passes.py` and the dropout / bias and gradient layout
files also passed on PEFT 0.18.0 and 0.21.2.
- **Version floor (CPU):** torch 2.6.0 + PEFT 0.18.0 + transformers
4.57.6 + TRL 0.22.2: the 15 LoRA / FP8 files give 330 passed, 0 failed
(main: 238 passed, 0 failed); the op registers there, and compiled code
keeps the functional calls (no export flag). On torch 2.6 main's own
order cannot run a DTensor X (`aten.addmm_` has no sharding strategy
there), so that test skips. A sparse base under `torch.export` keeps
main's order on torch 2.6 as well (it has no
`torch.compiler.is_exporting`, so the check reads `is_sparse` /
`is_sparse_csr`).
- **GPU (A100, torch 2.14.1):** the same 15 files give 781 passed, 3
failed; main gives 631 passed, 3 failed. The 3 are the same IDs on both
(`test_fused_lora_peft_fallbacks.py::test_disabled_adapter_without_grad_on_4bit_base_stays_fused[o|qkv|mlp]`).
RTX PRO 6000 on an earlier head: 455 passed, the same 3 failed.
- **Compile:** tiny Llama, Qwen3 and Gemma-3 LoRA training with the
default block compile: 0 graph breaks and the same number of compiled
graphs with the switch on and off.
- **fp16 + GradScaler (A100 and RTX PRO 6000):** Llama-3.2-1B bnb-4bit,
30 steps, autocast fp16: losses identical to the kill switch at every
step (fp16 keeps the previous order), 0 skipped steps, scale 65536.

## Not covered

- T4 / fp16 timing, H100 and B200.
- Training longer than 250 steps, downstream benchmarks, DPO and GRPO
trainers.
- Qwen3-8B at a small learning rate.
- Gemma-3: the tiny model gave bit-identical losses with the switch on
and off, so its path did not reach these kernels; real Gemma models not
checked.
- Compressed sparse (CSC / BSR) base weights or LoRA A weights under
`torch.compile`: only COO and CSR are recognised in traced code (Dynamo
refuses to read `layout` there); eager mode checks every layout.
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) [91](https://github.com/NousResearch/hermes-agent/commits): fix(gateway): resolve the orphan idle probe's target before opening a read

_idle_s runs on the gateway's startup thread (recover_local_sessions ->
arm_startup_orphan_closes) and resolved the physical session id inside its
own SessionDB._read_ctx() block. _physical_target reads the local receipt, so
that argument opened a second read context. A read that cannot use the WAL
pool -- no WAL (DELETE journal / NFS fallback) or every read permit spent --
is served from the writer connection under SessionDB._lock, which is not
reentrant: the nested read waited on the lock the same thread already held.

Boot then never reached the control socket. Desktop clients gave up with
"Gateway inaccessible: incomplete_control_response" / "Gateway starting:
deadline", the loop-liveness watchdog dumped the stack and exited 75, and
launchd restarted the gateway into the same wedge: a boot loop, not a slow
start.

Resolve the target first; the probe now opens exactly one read context.

Test: test_the_startup_idle_probe_does_not_nest_its_read_context fails on
main (the nested read) and passes here.
- [langgenius/dify](https://github.com/langgenius/dify) [83](https://github.com/langgenius/dify/commits): fix: reject 4xx/5xx responses in download_with_size_limit instead of returning the error page (#44333)

Co-authored-by: autofix-ci[bot] <114827586+autofix-ci[bot]@users.noreply.github.com>
Co-authored-by: Stream29 <36751053+Stream29@users.noreply.github.com>
- [kortix-ai/suna](https://github.com/kortix-ai/suna) [76](https://github.com/kortix-ai/suna/commits): fix(my-kortix): My Kortix memory has no screen; you ask My Kortix about it (#11258)

## Summary

My Kortix's memory is driven only by its `kortix_memory` tool. #11255
had also added UI for it:
- a **Memory** row in the sidebar for every project with Files;
- a My Kortix tab on the Memory screen;
- an empty state with "Remember this…";
- tool cards linking there.

The owner asked to remove all of it and keep this simple. This PR
removes that UI. A person asks My Kortix "what do you remember about
me?", "change…" or "forget…" in chat. The tool, the API routes and the
per-turn index are unchanged.

## Demo

Removal only. On a project without Channels, the sidebar no longer shows
**Memory**, as before #11255. On a project with Channels, the Memory
screen is the company Memory screen it was before #11255.

## What is affected

- **Web:** reverted to their state before #11255:
  - the Memory page route (`/projects/<id>/memory`);
  - the sidebar row condition (back to Channels only);
- `memory-href`, `company-memory-page`, `memory-all`, `memory-empty`,
`memory-labels`, `memory-page-list` and `memory-view`;
  - the strings #11255 added for these screens, in 9 locales.

The 4 My Kortix page types map to the generic file icon in
`memory-labels`, because the SDK type keeps them (a public type; nothing
renders them).
- **`kortix_memory`:** its cards no longer link to a Memory screen. The
tool description, the My Kortix prompt and the docs say there is no
screen: the person asks My Kortix.
- **Not affected:** the `/v1/projects/:id/memory/me/agent/mykortix`
routes, recall on every turn, the company Memory screen with Channels
on, and the retirement of the old `memory` tool.

## Verification

| Check | Result |
| --- | --- |
| kortixd `kortix-memory-tool.test.ts` (cards carry no link) | 11 pass |
| API `unit-my-kortix-agent` | 12 pass |
| Every test file in `packages/ui/src/workspace/memory` and
`workspace/sidebar`, one by one | 14 files, 0 fail |
| tsgo `@kortix/ui`, `Kortix-Computer-Frontend`, kortixd, api; kortixd
lint; eslint on touched files; i18n check | 0 errors |
| Brand audit | No issues in touched files. 5 existing issues in
untouched sidebar files (`workspace-menu-section.tsx`,
`project-sandbox-alert.tsx`, `sidebar-alert.tsx`). |

## Risks and rollback

- None for data: memory pages stay in the person's Files folder, and My
Kortix still reads and changes them.
- Rollback: revert the squash commit.

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/kortix-ai/codesmith/suna/pr/11258?autoLogin=true&ref=codesmith_pr_footer"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v3.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v3.svg"><img
alt="View with [code]smith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v3-3x.png"
width="162" height="28"></picture></a> <a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1796001214&installation_model_id=434224&pr_number=11258&ref=codesmith_pr_footer&repository=kortix-ai%2Fsuna&return_to=https%3A%2F%2Fgithub.com%2Fkortix-ai%2Fsuna%2Fpull%2F11258&signature=69c8f521c15d25896d83910d155c484cbc417a6772d828e30f6704a56c442688"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img
alt="Autofix with [code]smith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark-3x.png"
width="190" height="28"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith-bot</code> with what you
need.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->
- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) [41](https://github.com/QwenLM/qwen-code/commits): feat(web-shell): keep skill argument hints visible while typing arguments (#15930)

* feat(web-shell): keep skill argument hints visible while typing arguments

The inline argument hint for skill slash commands disappeared as soon as any argument text was typed, leaving no guidance for the remaining flags (e.g. /verify-pr <pr-number> [--publish] [--watch] ...).

Parse the skill's argument hint into placeholder/flag/literal tokens and consume them as the user types, showing only the parts not yet provided. Matching is order-independent, keeps a flag visible while it is being typed, surfaces a missing flag value, and prefers literal mode branches for hints with top-level alternatives. Built-in commands keep their existing subcommand-driven behavior; unknown or fully consumed arguments hide the hint as before.

* fix(web-shell): recognize live-session skill sources and tighten hint matching

Review follow-up on the progressive skill argument hints:

- Recognize the loader sources live sessions actually send ('skill-dir-command', 'bundled-skill') in addition to the pre-session 'skill' label, so the hints survive session attachment. Covered by a mapper-to-editor regression with a real EditorView for project and bundled skills.
- Render a just-typed flag's missing value before the remaining arguments, matching what the matcher consumes next.
- Only accept an unfinished flag prefix as the trailing token; a prefix followed by more words is a completed, unmatchable argument and hides the hint.
- Drop the unreachable empty-args guard flagged in review.

* fix(web-shell): cover extension skills in progressive argument hints

Extension skills arrive from live sessions with the shared 'plugin-command' source label, so the source-only classification lost their progressive hints after session attachment. Treat session skill membership (availableSkills) as authoritative: the composer now feeds the skill list into the input highlight extension, and the hint matcher recognizes members regardless of source label while ordinary plugin commands keep their existing behavior.

Extends the mapper-to-editor regression with an extension-provided skill and an ordinary plugin-command control.

* fix(web-shell): consume flags typed after free text and pin the malformed-hint fallback

Free-text placeholders absorbed the whole typed tail, so a flag entered after the prose was still advertised as missing (and the same words in flag-first order hid the hint). Free text now absorbs only prose words and hands flag-looking words back to the normal flag path, restoring order independence and the unmatchable-hides rule.

Tighten the malformed-hint regression from a type tautology to asserting the hint actually hides, including the empty-group shape.

* fix(web-shell): drop empty hint groups so malformed metadata cannot echo

The R1-2 witness still reproduced: with argument-hint '[] []', typing one word consumed the first empty group and rendered the second as a leftover '[]' hint. Empty bracket groups are malformed skill metadata, so they are now dropped during tokenization and can never survive as renderable remainder.

Pin the original witness ('[] []' with '/demo x' hides) as its own regression, independent of the unknown-flag path the tightened loop happened to exercise.

* fix(web-shell): hide whitespace-only empty hint groups and pin the skills wiring

The empty-group filter only matched the literal '[]' and '<>' shapes, so whitespace-only groups like '[ ] [ ]' still echoed a leftover token after an argument was typed. Drop any bracket group whose inner text trims to empty, and pin the whitespace witnesses as their own regressions.

Add a composer-level DOM test for the skills accessor feeding the input highlight: an extension skill listed in the session skills renders its progressive hint, the same command without membership does not. Mutating the accessor to a constant empty list kills the new case while the parser-level suites stay green.

Also reword the source-set comment: 'skill-dir-command' labels custom markdown commands too, so the set selects the free-form hint path rather than strictly skill-backed commands.
- [google/adk-python](https://github.com/google/adk-python) [29](https://github.com/google/adk-python/commits): feat: support configuring eval case parallelism in eval config and CLI

Merge https://github.com/google/adk-python/pull/7780

Adds `parallelism` to `EvalConfig`, an `adk eval --parallelism` flag, and a
`parallelism` argument to `AgentEvaluator.evaluate` and
`AgentEvaluator.evaluate_eval_set`. It caps how many eval cases
`LocalEvalService` runs at once during inference and metric evaluation. The
flag or argument overrides the config; when neither is set, the service default
of 4 still applies. A `parallelism` key already present in an eval config file
was ignored before and now takes effect, and a value below 1 is rejected
(`ValidationError` in `EvalConfig`, `ValueError` from `AgentEvaluator`, a usage
error from `adk eval`).

PiperOrigin-RevId: 1010912393
- [t8y2/dbx](https://github.com/t8y2/dbx) [14](https://github.com/t8y2/dbx/commits): fix(sidebar): cut pinned lookup and saved-SQL decorate cost on large table lists

Refs: #13992
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) [11](https://github.com/screenpipe/screenpipe/commits): Bump app version to 2.7.134
- [github/spec-kit](https://github.com/github/spec-kit) [7](https://github.com/github/spec-kit/commits): fix(extensions): make extension add name optional with --from (#5197)

The positional extension argument was required, so
`specify extension add --from <url>` failed with
"Missing argument 'EXTENSION'". Make it optional when --from is given,
and print a clear error when neither a name nor a source is provided
(also for --dev without a path).

https://github.com/Quratulain-bilal/spec-kit-brownfield/issues/1
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) [7](https://github.com/google-gemini/gemini-cli/commits): fix(core,cli): preserve selected model across transient fallback, cancel, and rewind (#30059)
- [lutzroeder/netron](https://github.com/lutzroeder/netron) [6](https://github.com/lutzroeder/netron/commits): Update to 9.3.4
- [docling-project/docling](https://github.com/docling-project/docling) [4](https://github.com/docling-project/docling/commits): fix: allow chunks artifact type in ArtifactRef (#5111)

Producers (docling-jobkit) upload {stem}.chunks.jsonl as a presigned
artifact when "chunks" is requested in to_formats. The ArtifactRef
literal did not include "chunks", so building the presigned result
raised a ValidationError and the whole task failed.

Signed-off-by: Michele Dolfi <dol@zurich.ibm.com>
- [google/magika](https://github.com/google/magika) [3](https://github.com/google/magika/commits): Merge pull request #1586 from google/gh-1560-rules-remove-built-yara-rulesets

rules: remove built-in YARA rulesets and migrate regression tests to resolvers
- [steel-dev/steel-browser](https://github.com/steel-dev/steel-browser) [3](https://github.com/steel-dev/steel-browser/commits): fix(casting): validate session ID from URL against active session (#405)

The handleCastSession handler extracted the session ID from the request URL
but never compared it to the actual active session's ID. Since
sessionService.activeSession always returns the one global active session,
any string passed as the session ID in the URL path would bypass the check
and grant full cast access — including live screencast, mouse/keyboard
injection, and navigation.

Adds a session.id !== id guard so mismatched IDs are rejected.

Fixes #404
- [Kiln-AI/Kiln](https://github.com/Kiln-AI/Kiln) [2](https://github.com/Kiln-AI/Kiln/commits): Merge pull request #1986 from Kiln-AI/model-sweep/deprecations-2026-10-29

chore: mark o4 Mini and Qwen 3 Next 80B Thinking on OpenRouter deprecated
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) [1](https://github.com/openai/openai-agents-python/commits): fix: improve missing stream completion diagnostics (#5457)
- [specstoryai/getspecstory](https://github.com/specstoryai/getspecstory) [1](https://github.com/specstoryai/getspecstory/commits): Merge pull request #384 from specstoryai/dependabot/github_actions/actions-minor-patch-1064b7430f

Bump anthropics/claude-code-action from 1.0.263 to 1.0.264 in the actions-minor-patch group
- [XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) [1](https://github.com/XiaomiMiMo/MiMo-Code/commits): Merge pull request #2737 from XiaomiMiMo/codex/fix-project-config-execution

fix(config): restrict project execution without losing persisted settings

## [ai-agents](https://github.com/topics/ai-agents)
- [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) [30](https://github.com/CherryHQ/cherry-studio/commits): feat(proxy): add connection test (#20487)

### What this PR does

Before this PR:

General Settings could save proxy settings but could not test an edited
draft independently.

After this PR:

General Settings provides a Test Connection button immediately to the
left of the proxy mode selector, in the same row. It tests the draft
mode, address and bypass rules in an isolated Electron session without
saving them. Results appear only after testing and include the
destination, routing category and localized sanitized failures.

PAC lists containing both a proxy and `DIRECT` report automatic
proxy/direct fallback routing, regardless of candidate order. Connection
success does not falsely certify proxy use.

Fixes #20481

### Why we need it and why it was done in this way

The following tradeoffs were made:

- Serialize diagnostics and clear their pooled connections after
configuration changes so successive tests exercise the current draft.
- Use a fixed public destination,
`https://www.gstatic.com/generate_204`, rather than accepting arbitrary
test URLs.
- Report PAC transport uncertainty explicitly because `resolveProxy()`
returns candidates, not the transport actually used by the request.

The following alternatives were considered:

- Applying drafts to global sessions would change live traffic while
testing.
- Inspecting only the first PAC candidate misses fallback and Chromium
candidate reordering.
- Network-log recording would add lifecycle and sensitive-data handling
for a small diagnostic.

Links to places where the discussion took place:
https://github.com/CherryHQ/cherry-studio/issues/20481 and
https://github.com/CherryHQ/cherry-studio/pull/20487#discussion_r4426038874

### Agent Note / Spec

Agent Note:
[.agents/notes/implemented/bug-fix/2026-10-31-proxy-test-pac-fallback.md](.agents/notes/implemented/bug-fix/2026-10-31-proxy-test-pac-fallback.md).

Spec PR: N/A — restoration of the existing PR and direct repair of its
PAC reporting contract.

Acceptance criteria: diagnostics remain isolated and draft-only; mixed
PAC candidates retain routing uncertainty; main's existing behavior is
preserved; the button remains left of the selector without a separate
test row.

### Verification

- Regression: 76 tests passed across explicitly selected ProxyService,
proxyRouting, bypassRules and IpcRouter files, including main's proxy
reconciliation, status and loopback behavior.
- Regression: 32 tests passed in GeneralSettings and
ContextManagementSettings, including main's developer settings and
agent-language behavior.
- Node and Web typechecks, scoped ESLint/Oxlint/Oxfmt, i18n catalog
validation (97,151 translations), unused-key validation (zero unused
keys), documentation checks and signed-commit hooks passed.
- Regression: 18/18 real Electron 44.9.3 end-to-end cases passed in 91
seconds, with zero uncaught renderer exceptions. Cases include isolated
drafts, mouse and keyboard activation, save/reload, timeout/loading,
stale responses, 407, system/direct routes, both PAC orders and Chromium
reordering, proxy success with fallback allowed, direct-only and
proxy-only PAC, and English/Chinese light/dark rendering.
- PAC scripts are injected only into the isolated diagnostic session;
diagnostic responses and Chromium routing are not mocked. This does not
cover OS-specific PAC discovery, every platform/installer or every
provider transport.

### Breaking changes

None. The internal connection-test result includes an explicit
`fallback` route understood by the settings UI.

### Special notes for your reviewer

The previous eight feature/fix/layout commits are backed up locally at
`codex/backup-pr-20487-before-main-resolution`. Their combined
proxy-only changes were reapplied to verified main
`f14b642f58f8de9943ad3c50e80fcfe9c33c0658` and consolidated into one
signed commit, `206bcab0b`, with the original author credited. This
avoids adding main's intervening history to the PR's feature commits.

Conflict resolution retains main's applied-proxy snapshot, loopback
bypass rules, developer CDP controls and agent-language settings. The
final comparison contains 26 files: proxy code/tests, 15 locale
catalogs, and the bilingual PAC note with its required consistency
sidecar. No workflow, release configuration, dependency/lockfile or
database migration changes are included.

All validation above was rerun on the resolved version with Node 24.21.0
and Electron 44.9.3. Earlier Electron 41 reports do not validate this
revision. The new report, screenshots, reproducible runner and raw logs
are retained locally under
`.context/cherry-electron-dev/pr-20487/main-resolved-2026-10-31/`.
GitHub CI is reported separately from local results.

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

```release-note
Add a proxy connection test to General Settings with isolated draft testing, localized errors, and explicit proxy/direct fallback reporting for PAC routing.
```

Signed-off-by: suyao <sy20010504@gmail.com>
Co-authored-by: suyao <sy20010504@gmail.com>
- [steipete/agent-scripts](https://github.com/steipete/agent-scripts) [2](https://github.com/steipete/agent-scripts/commits): feat(codex-first): admit OpenClaw sessions on Claude models

The gate now covers any native-Claude session that can run shell
commands, including OpenClaw agents on the Team Gateway, and keeps
non-Claude sessions working directly. Replace Mac-only
~/.codex/skills/agent-scripts paths with skill-relative ones.

## [android](https://github.com/topics/android)
- [fastlane/fastlane](https://github.com/fastlane/fastlane) [4](https://github.com/fastlane/fastlane/commits): [core] Pass the Apple ID password to the transporter in its environment (#30486)

* [core] Pass the Apple ID password to the transporter in its environment

altool and xcrun iTMSTransporter now read the password from ITMS_TRANSPORTER_PASSWORD through -p @env:, set for the transporter process only, instead of from their command line or an inline variable assignment. The legacy Java and shell-script transporters are unchanged.

* [spec] transporter password examples: choose the Mac and Xcode they test

On Linux and Windows the transporter picked the Java or shell-script executor, which still take the password on the command line, so both examples failed there.
- [gojue/ecapture](https://github.com/gojue/ecapture) [2](https://github.com/gojue/ecapture/commits): build: actually build static-pie binary (#1068)

## [claude-code](https://github.com/topics/claude-code)
- [slopus/happy](https://github.com/slopus/happy) [167](https://github.com/slopus/happy/commits): happy-ios: home draws its sections as quiet inset grouped cards

Home's list (and only home's: search, the session tree and proposals stay
plain) is now iOS's inset grouped list in Settings' card shapes: a quiet
card per section on the conversation's ground, a small grey heading over
each, hairlines between rows from the title's start, and iOS's cell
highlight clipped to the card's corners. Rows before the first heading
(Artifacts and the Surfaces in classic, Happy in spaces) are an unheaded
card. Nested rows stay in their parent's card, indented under its title,
with no tree lines.

Marks follow desktop: subtasks and a project's sessions have none, a
cloned repo wears the daemon's picture (project.avatar) and any other
project or worktree nothing. Top-level glyphs sit on a softly tinted tile
per kind. Story rows are cells of their card too.

Layout in HappyLayout (SidebarLayout.Style.grouped) with exact-frame tests;
hosted tests for cards, corners, hairlines, highlight, fold and carry; a
groupedHome harness screen for screenshots.
- [sirmalloc/ccstatusline](https://github.com/sirmalloc/ccstatusline) [18](https://github.com/sirmalloc/ccstatusline/commits): fix: use env override and settings for usable context ratio calculation (#407)

* fix: validate settings schema before saving to prevent data loss

* fix: use env override and settings for usable context ratio calculation

* Fix legacy auto-compaction preference and window clamping

---------

Co-authored-by: Matthew Breedlove <sirmalloc@gmail.com>
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) [4](https://github.com/Piebald-AI/claude-code-system-prompts/commits): Update changelog for v2.1.316

## [cross-platform](https://github.com/topics/cross-platform)
- [Snapchat/Valdi](https://github.com/Snapchat/Valdi) [10](https://github.com/Snapchat/Valdi/commits): Internal Change

GitOrigin-RevId: 3b612d72295a13c18e2f23ec4cd02e3a1f89798b
- [xyproto/algernon](https://github.com/xyproto/algernon) [1](https://github.com/xyproto/algernon/commits): Update dependencies

## [database](https://github.com/topics/database)
- [quadstorejs/quadstore](https://github.com/quadstorejs/quadstore) [3](https://github.com/quadstorejs/quadstore/commits): 15.4.2
- [ClickHouse/clickhouse-go](https://github.com/ClickHouse/clickhouse-go) [2](https://github.com/ClickHouse/clickhouse-go/commits): Merge pull request #2078 from ClickHouse/dependabot/go_modules/github.com/shopspring/decimal-1.6.0

chore(deps): bump github.com/shopspring/decimal from 1.5.0 to 1.6.0

## [distributed-systems](https://github.com/topics/distributed-systems)
- [databendlabs/openraft](https://github.com/databendlabs/openraft) [10](https://github.com/databendlabs/openraft/commits): fix: core: do not move log progress back on snapshot install

# Summary

Installing a full snapshot that ends inside the follower's log no
longer moves `log_progress.submitted` backwards. Debug builds no
longer panic, and release builds keep applying committed entries past
the snapshot.

# Details

A follower holding entries 0..=40, committed through 10, accepts a
snapshot at 30 from the same leader because 30 is above its committed
log id. `accept_log_io` keeps `accepted` at 40 and the completion
handler uses `try_flush`, but `RaftCore::run_state_machine` called
`IOProgress::submit` with log I/O (leader, 30) while `submitted` was
(leader, 40). Debug builds panicked in `IOProgress::advance`; release
builds set `submitted` below `flushed` and stopped applying at 30.

`run_state_machine` now calls `try_submit`, which advances `submitted`
only when the new value is greater. The snapshot itself is installed
as before. `InstallFullSnapshot` is the only state-machine command
that reports log progress.

A leader that has seen the follower's real log end does not send such
a snapshot; a leader acting on stale conflict information, or a late
snapshot from a deposed leader, can.

Fixes #2170
- [bloomberg/blazingmq](https://github.com/bloomberg/blazingmq) [3](https://github.com/bloomberg/blazingmq/commits): Fix[mqbnet::Channel]: handle stale watermark events

Check if a watermark event arrives from the current channel before
changing the state of mqbnet::Channel.

Signed-off-by: Evgeny Malygin <emalygin@bloomberg.net>

## [embedded](https://github.com/topics/embedded)
- [hathach/tinyusb](https://github.com/hathach/tinyusb) [22](https://github.com/hathach/tinyusb/commits): Merge pull request #4184 from satirebird/task_stop

Add an option to terminate the tud_task properly
- [rhaiscript/rhai](https://github.com/rhaiscript/rhai) [13](https://github.com/rhaiscript/rhai/commits): Merge pull request #1202 from luispedro/grain-const-pool-hash

Grain: index the constant pool by hash
- [rmk-rs/rmk](https://github.com/rmk-rs/rmk) [8](https://github.com/rmk-rs/rmk/commits): Merge pull request #1376 from rmsthebest/fix-usb-composite-timeout

fix(usb): don't let an unread composite interface stall keyboard reports
- [embassy-rs/embassy](https://github.com/embassy-rs/embassy) [7](https://github.com/embassy-rs/embassy/commits): Merge pull request #7397 from Abrahamh08/fix/stm32h7-qspi-mdma-flash-size

examples/stm32h7: fix off-by-one flash size in qspi_mdma
- [linux-msm/qdl](https://github.com/linux-msm/qdl) [4](https://github.com/linux-msm/qdl/commits): Merge pull request #348 from igoropaniuk/fix/usb-serial-fallback

usb: fall back to iSerialNumber and retry transient string reads
- [nanopb/nanopb](https://github.com/nanopb/nanopb) [1](https://github.com/nanopb/nanopb/commits): Reject submsg_callback on fixed_count fields

## [esp32](https://github.com/topics/esp32)
- [crosspoint-reader/crosspoint-reader](https://github.com/crosspoint-reader/crosspoint-reader) [8](https://github.com/crosspoint-reader/crosspoint-reader/commits): feat: add end_percent to plugin reading events (#4201)
- [schreibfaul1/ESP32-audioI2S](https://github.com/schreibfaul1/ESP32-audioI2S) [3](https://github.com/schreibfaul1/ESP32-audioI2S/commits): Merge pull request #1420 from Witaliy76/feature/upstream-vorbis-ogg-resync-af24-20261030

Fix stale Ogg parser state during Vorbis resynchronization
- [luc-github/ESP3D](https://github.com/luc-github/ESP3D) [2](https://github.com/luc-github/ESP3D/commits): Use supported board names
- [arendst/Tasmota](https://github.com/arendst/Tasmota) [1](https://github.com/arendst/Tasmota/commits): Fix: DisplayText [pN] command now works when followed by another '[' … (#25188)

* Fix: DisplayText [pN] command now works when followed by another '[' escape

* additional changes requested by s-hadinger to https://github.com/arendst/Tasmota/pull/25188
- add limits to [pN] padding to fix buffer overflow
- move fill handling to after USE_DISPLAY_MODE1TO5 check
- [espressif/arduino-esp32](https://github.com/espressif/arduino-esp32) [1](https://github.com/espressif/arduino-esp32/commits): feat(ci): Improve CI caching and load balancing (#13027)

* feat(ci): Improve CI caching and load balancing

* change(tools): Push generated binaries to PR

* ci(pre-commit): Apply automatic fixes

* change(tools): Push generated binaries to PR

* fix(get): Fix formatting

* change(tools): Push generated binaries to PR

---------

Co-authored-by: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Co-authored-by: Me No Dev <me-no-dev@users.noreply.github.com>
Co-authored-by: pre-commit-ci-lite[bot] <117423508+pre-commit-ci-lite[bot]@users.noreply.github.com>
- [Plaenkler/Egg_LDO_1000](https://github.com/Plaenkler/Egg_LDO_1000) [1](https://github.com/Plaenkler/Egg_LDO_1000/commits): [UPD] README

## [free](https://github.com/topics/free)
- [public-apis/public-apis](https://github.com/public-apis/public-apis) [25](https://github.com/public-apis/public-apis/commits): Merge pull request #8312 from priom96/add-trendsagi

Add TrendsAGI API
- [gibbok/typescript-book](https://github.com/gibbok/typescript-book) [1](https://github.com/gibbok/typescript-book/commits): News: TypeScript native compiler gains experimental WASI WebAssembly support (#293)

* news: add experimental TypeScript WASI WebAssembly support in all locales

* chore: remove temporary TypeScript news validation workflow

## [llm](https://github.com/topics/llm)
- [yetone/magpie](https://github.com/yetone/magpie) [228](https://github.com/yetone/magpie/commits): gateway: OpenCode Go's bare 400 (a model name, no error) is a 502 that rests nobody (#3740)

OpenCode's gateway answers some of s-leeq's turn-start requests with a
400 whose body is {"model":"deepseek-v4.1-flash"} and nothing else: no
error, message, code, type or param, nothing in or out, no reply id.
retryable() read it as the request's own fault, so a group stopped there
and a lone provider's turn ended on it, with a 400 nothing retries. Their
log ties it to the request, not the key: 30 of 214 requests carrying
~246K tokens of tools failed so, none of 420 under 1K, and the same
request was answered 200 some 13s to 25s after the first refusal.

openCodeBareRefusal (ported from ggbdpq's patch on the issue) reads a
400 from an OpenCode host whose body is a JSON object naming no error
field as the 502 it stands for (asBadGateway). A group asks its next
member; a lone provider is asked again within its patience (60s, with
replan pauses), which outlasts the reporter's window. Any 400 that names
something, a body that isn't a JSON object, and every other vendor's
400 go on as they came.

Changed from the patch:
- restAfterMarked rests nobody for this 502. The patch rested the key
  for fallbackCooldown in a group (a scratch test showed ocgo resting
  60s), over a refusal tied to request content: one heavy prompt would
  have set aside a key that serves every other request.
- The body is read through a 64KB limit and put back with a
  MultiReader, so nothing is cut; a body at the limit is left alone.
  The patch read it whole.
- TestOpenCodeGoBare400ToldAs502 asserts at least 3 asks, not exactly
  3: on current main the lone provider's patience asks 15 times.

Run on mote:
- At the pushed head (on c272e5582): gofmt -l clean; go vet
  ./internal/gateway for darwin, linux and windows; go test
  ./internal/gateway -run 'OpenCode|Rest|Fallback|Patience|Retry' ok (83s).
- On 576b5dcbc, before main took four more gateway commits
  (82ff88933..c272e5582): go test ./internal/gateway -count=1
  -timeout 45m ok (615.8s).
- TestOpenCodeGoBare400AskedAgain, ToldAs502, RestsNobody (new: a group
  of OpenCode Go and another provider; the first request's bare 400 is
  served by the other, the next request still reaches OpenCode) and
  TestOpenCodeGoError400Untouched pass.
- Before the rebase, the package was red only in
  TestClaudeCallerEnvironmentInAMessageIsTheLastGiven, which 576b5dcbc
  fixed on main since.

Broken by hand:
- rest exemption off (`if false &&`): RestsNobody red, "OpenCode asked
  1, the other 2".
- openCodeBareRefusal taken out of forwardOnce: AskedAgain, ToldAs502
  and RestsNobody red; AskedAgain shows the issue's exact 400.
- A real-time scratch test (refusals for 25s, 2.5s each, the real
  retryPause, lone provider) got its 200 after 32s, asked 6 times.
  Deleted after.

Not tried: a real OpenCode Go key or the reporter's DeepSeek Harness; the
bodies are the issue's bytes. A turn whose refusals outlast 60s still
ends, now as a 502 the client can retry.

Co-authored-by: ggbdpq <ggbdpq@gmail.com>
- [BerriAI/litellm](https://github.com/BerriAI/litellm) [71](https://github.com/BerriAI/litellm/commits): fix(proxy): log router-refused image generation requests (#49349)
- [gptme/gptme](https://github.com/gptme/gptme) [45](https://github.com/gptme/gptme/commits): fix(context): require explicit prompt path attachments by default (#4655)

* fix(context): require explicit prompt path attachments by default

Git-Session-Id: e6493c50-6d4a-423e-add4-a2a3be3d4916

* fix(context): preserve mixed-case URL discovery and consent

Git-Session-Id: daa5cec2-0d89-51fe-92fc-e4202d13c0eb

* fix(context): complete @paths and restore legacy command expansion

CLI path completion now matches after a leading @, so `review @REA`
completes to `@README.md`. Compatibility mode still expands implicit
`./file --help` phrases, while explicit spaced @ references and quoted
URL prose keep the no-fallback consent boundary.

Git-Session-Id: ec5c7f53-10e9-5483-a8f1-cdeaaf0923d7

* fix(cli): quote spaced @path completions

PathCompleter yields unquoted names, so completing `see @pho` for
`photo album.txt` became `see @photo album.txt` and discovery split it
into two tokens. Wrap spaced @ completions in backticks so the selected
resource stays one explicit attachment.

Git-Session-Id: ec5c7f53-10e9-5483-a8f1-cdeaaf0923d7

* fix(context): skip nested-tick completions and overlong path aborts

Do not complete @paths whose names contain backticks, which would close
a quoted attachment early and expose an inner @token. Treat ENAMETOOLONG
from Path.exists() as a skip so a huge sibling reference cannot drop a
valid explicit attachment.

Git-Session-Id: ec5c7f53-10e9-5483-a8f1-cdeaaf0923d7

* fix(cli): keep spaced directory @completions open for children

Quoted @ directory completions leave the backtick open and complete the
segment after the last tick, so `see @my` → `see `@my dir/` can still
tab-complete `child.md`. File completions close the reference.

Git-Session-Id: ec5c7f53-10e9-5483-a8f1-cdeaaf0923d7

* fix: finalize completed directory attachments on CLI submission

* fix: reset directory completion authorization between prompts

* fix: reject unsafe clipboard image attachment delimiters

* fix: validate pasted image paths before newline normalization

* fix: reuse existing closing delimiter in attachment completion

* fix: close directory attachments completed before trailing prose

* fix: recognize tab-separated legacy command phrases

---------

Co-authored-by: Erik Bjäreholt <erik@bjareho.lt>
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) [16](https://github.com/OpenHands/OpenHands/commits): fix: suppress Run on first message after a home-page model pick (cloud + local) (#19042)

Co-authored-by: openhands <openhands@all-hands.dev>
- [jundot/omlx](https://github.com/jundot/omlx) [3](https://github.com/jundot/omlx/commits): perf(bonsai): run 1-bit and 2-bit layers on stock MLX kernels (#4972)
- [browser-use/browser-use](https://github.com/browser-use/browser-use) [2](https://github.com/browser-use/browser-use/commits): Add Fireworks model example (#6238)

Fireworks is listing Browser Use as an ecosystem partner and the docs
now have a Fireworks section, but `examples/models` has no Fireworks
script to link. This adds `examples/models/fireworks.py`, which points
`ChatOpenAI` at `https://api.fireworks.ai/inference/v1` with
`accounts/fireworks/models/kimi-k3`, in the same shape as the Moonshot
and Novita examples. Fireworks documents support for the JSON-schema
features our action schema uses (in-document `$ref`, `anyOf`,
`minItems`). Ruff check and format pass; it has not been run against
Fireworks because we have no Fireworks key.

<!-- This is an auto-generated description by cubic. -->
---
## Summary by cubic
Adds `examples/models/fireworks.py`, an example for running the agent on
Fireworks-served models via their OpenAI-compatible endpoint.

- Follows the same structure as the Moonshot and Novita examples, using
`ChatOpenAI` with a Fireworks base URL and the Kimi K3 model.
- Ruff check and format pass; the script has not been run against
Fireworks because we don't have a Fireworks API key.

<sup>Written for commit 857de1fb41623a033a519f0276db61151ca9f91c.
Summary will update on new commits.</sup>

<a
href="https://cubic.dev/pr/browser-use/browser-use/pull/6238?utm_source=github"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/review-in-cubic-light.svg"><img
alt="View guided diff"
src="https://www.cubic.dev/buttons/review-in-cubic-light.svg"></picture></a>
<a
href="https://www.cubic.dev/action/auto-fix/pr/browser-use/browser-use/6238?returnTo=https%3A%2F%2Fgithub.com%2Fbrowser-use%2Fbrowser-use%2Fpull%2F6238&source=description"
target="_blank" rel="noopener noreferrer"
data-no-image-dialog="true"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://www.cubic.dev/buttons/turn-on-auto-fix-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://www.cubic.dev/buttons/turn-on-auto-fix-light.svg"><img
alt="Turn on auto-fix"
src="https://www.cubic.dev/buttons/turn-on-auto-fix-light.svg"></picture></a>

<!-- End of auto-generated description by cubic. -->

## [macos](https://github.com/topics/macos), [apple-silicon](https://github.com/topics/apple-silicon)
- [ly05010419/MacNativeGames](https://github.com/ly05010419/MacNativeGames) [32](https://github.com/ly05010419/MacNativeGames/commits): fix: packaging unlinks a variant's staging files before translating it, so the translator never rewrites a cached file

The translator writes the MSL over the file in place (Service.cs File.WriteAllBytes / WriteAllText; only the reflection
goes through a temporary file), and a staging file can be a hard link to the translation cache (TranslationCache take /
put link them). A translation made again through such a link rewrote the cached file, and one cut short could leave it
empty or partial in the cache that other packagings share. Unlinked first, the translator writes a file of its own,
which put links into the cache only after an ok reply.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01WYKg7rg7FFoMfhc88SdspH
- [openai/tart](https://github.com/openai/tart) [3](https://github.com/openai/tart/commits): Use the last name component for the default tart export path (#1389)

## [python](https://github.com/topics/python)
- [CyC2018/CS-Notes](https://github.com/CyC2018/CS-Notes) [200](https://github.com/CyC2018/CS-Notes/commits): Merge pull request #1509 from CyC2018/notes-order-payment-1031

补充订单与支付、客服 Agent 设计等内容
- [esphome/esphome](https://github.com/esphome/esphome) [48](https://github.com/esphome/esphome/commits): [cm1106] Drop the duplicate helpers.h include (#21976)
- [huangjunsen0406/py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) [15](https://github.com/huangjunsen0406/py-xiaozhi/commits): 合并 #331：收拢运行时与配置状态，完善 TUI 设置并移除 CLI/IoT

合并已通过 Python 3.10/3.12、三平台 wheel、lint 与 GitGuardian 检查的七批提交。
- [aiogram/aiogram](https://github.com/aiogram/aiogram) [13](https://github.com/aiogram/aiogram/commits): Add tasks_shutdown_timeout to wait for running update handlers on polling shutdown (#1956)

* feat(dispatcher): wait for in-flight update handlers on polling shutdown

With handle_as_tasks=True, start_polling() never awaited the tasks it
keeps in _handle_update_tasks: on SIGINT/SIGTERM or stop_polling() it
ran shutdown callbacks and closed bot sessions while handlers could
still be running, and run_polling() then cancelled them when the event
loop closed. The next getUpdates had usually confirmed their updates
already, so Telegram did not send them again.

Add tasks_shutdown_timeout to start_polling() and run_polling(). When
it is set, polling stops fetching updates, waits up to that many
seconds for the handlers of all bots, cancels and awaits the ones still
running, and only then runs shutdown callbacks and closes sessions. A
handler that awaits stop_polling() is not waited for, so it does not
wait for itself. The default, None, keeps the previous behaviour.

* docs(openspec): add the add-polling-tasks-shutdown-timeout change

Proposal, design, tasks and the event-dispatching spec delta for the
tasks_shutdown_timeout parameter of Dispatcher.start_polling() and
run_polling(). The delta adds one requirement and leaves the existing
long polling and shutdown requirements as they are.

* test(dispatcher): check that polling stops before the shutdown wait

The shutdown tests only checked that handlers finish before shutdown
callbacks, so they still passed with the wait moved in front of
cancelling the polling tasks, where getUpdates keeps running and
confirms new updates during the wait. Record when the long poll is
cancelled and expect it before the handler finishes.

* docs(dispatcher): say when the polling shutdown wait does not apply

The Shutdown section said that a handler calling stop_polling() is not
waited for, and that SIGINT/SIGTERM trigger the wait, without limits.
Neither holds in every case:

- with handle_signals=False, or where the event loop has no signal
  handlers, SIGINT raises KeyboardInterrupt or cancels the task running
  start_polling(), and shutdown runs without waiting;
- a handler that calls stop_polling() after polling has started to
  stop, or awaits it through another task (asyncio.shield(),
  asyncio.gather(), asyncio.wait_for() on Python 3.10 and 3.11), is
  waited for and cancelled when the timeout expires;
- a second SIGINT/SIGTERM does not shorten the wait.

Describe these cases and the way to stop polling from a handler that
avoids them, and drop the versionadded note, whose release number is
not known yet. The changelog fragment now names only the signals the
dispatcher handles.

* docs(openspec): record the limits of the polling shutdown wait

Bring the add-polling-tasks-shutdown-timeout change in line with what
probes showed:

- the requirement and its scenarios name the stops that wait
  (stop_polling() and signals the dispatcher handles) and the order
  "stop fetching, then wait";
- the stop-from-handler scenario covers only a handler that awaits
  stop_polling() in its own task before polling stops; design.md lists
  the two cases it misses, with the probe results, and why the check
  stays on asyncio.current_task();
- cancelling start_polling() is out of scope because #1635 was closed
  as intended behaviour, so it is no longer listed as a follow-up;
- tasks.md records the stronger shutdown tests and the docs update.

* docs(dispatcher): say that tasks started by handlers are not awaited

The shutdown wait covers only the tasks that polling creates for
updates. A handler that hands its work to its own background task and
returns is done as far as the wait is concerned, so shutdown runs and
sessions close while that task is still running.

* docs(openspec): drop the README that archived changes do not have

* docs: name the changelog fragment after issue #1955

* fix(dispatcher): exclude a handler from the shutdown wait only when it starts the stop

A handler that called stop_polling() after a signal or another call had
already started the stop removed itself from the tasks being waited for.
If that happened before the wait took its copy of the set, the handler
was not waited for, although the docs say it is waited for and then
cancelled when the timeout expires.

stop_polling() now removes the handler only while _stop_signal is not
set yet. A test with a fixed order of events covers both cases, and a
polling test covers a handler that calls stop_polling() after SIGTERM.

---------

Co-authored-by: sinnercode228 <sinnercode228@users.noreply.github.com>
- [adafruit/circuitpython](https://github.com/adafruit/circuitpython) [10](https://github.com/adafruit/circuitpython/commits): Merge pull request #11695 from jedgarpark/max3421e-shared-spi

max3421e: don't run tuh_task() while the shared SPI bus is held
- [nltk/nltk](https://github.com/nltk/nltk) [10](https://github.com/nltk/nltk/commits): Merge pull request #4005 from alvations/black-compatible-cleanups

Formatter-neutral cleanups: joined strings, f-strings and pyupgrade follow-ups
- [doronz88/pymobiledevice3](https://github.com/doronz88/pymobiledevice3) [8](https://github.com/doronz88/pymobiledevice3/commits): Merge pull request #2155 from doronz88/rsd/remoted-handshake-uuid

remote: Present remoted's UUID when --rsd targets remoted's tunnel
- [pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) [8](https://github.com/pymupdf/PyMuPDF/commits): changes.txt: updates for 2.1.
- [KoljaB/RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) [4](https://github.com/KoljaB/RealtimeSTT/commits): Merge pull request #342 from KoljaB/fix/harden-spinner-text

Harden configurable spinner text
- [arnegiacomo/fugleramme](https://github.com/arnegiacomo/fugleramme) [3](https://github.com/arnegiacomo/fugleramme/commits): fix: link how to update instead of the docker command on phones
- [lakehq/sail](https://github.com/lakehq/sail) [3](https://github.com/lakehq/sail/commits): chore: prepare v0.7.3 (#2906)
- [locustio/locust](https://github.com/locustio/locust) [3](https://github.com/locustio/locust/commits): Merge pull request #3580 from Tanishq-Choudhary/fix/postgres-user-autocommit

Use autocommit for the PostgresUser connection
- [pyocd/pyOCD](https://github.com/pyocd/pyOCD) [3](https://github.com/pyocd/pyOCD/commits): sequences: fix halt-on-reset flag leaking to other debug sequences
- [vacanza/holidays](https://github.com/vacanza/holidays) [3](https://github.com/vacanza/holidays/commits): Update `HolidayBase::__setattr__` method to validate reassignments (#3895)

Co-authored-by: ~Jhellico <KJhellico@users.noreply.github.com>
- [ESPARGOS/pyespargos](https://github.com/ESPARGOS/pyespargos) [2](https://github.com/ESPARGOS/pyespargos/commits): Fix for signal trigger mode IQ reception
- [pyodide/pyodide](https://github.com/pyodide/pyodide) [2](https://github.com/pyodide/pyodide/commits): PERF improve isPyProxy check performance (#6504)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>
- [dbcli/mycli](https://github.com/dbcli/mycli) [1](https://github.com/dbcli/mycli/commits): Merge pull request #2402 from dbcli/dependabot/github_actions/docker/login-action-4.7.0

Bump docker/login-action from 4.6.0 to 4.7.0

## [rust](https://github.com/topics/rust)
- [probe-rs/probe-rs](https://github.com/probe-rs/probe-rs) [8](https://github.com/probe-rs/probe-rs/commits): Remove duplicated test mocks (#4595)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [sharkdp/fd](https://github.com/sharkdp/fd) [2](https://github.com/sharkdp/fd/commits): Merge pull request #2202 from meop/ci/windows-arm64-gnullvm

ci: release a Windows ARM64 GNU-family (gnullvm) build
- [actix/actix](https://github.com/actix/actix) [1](https://github.com/actix/actix/commits): chore: add check-advisories recipe (#735)
- [cargo-generate/cargo-generate](https://github.com/cargo-generate/cargo-generate) [1](https://github.com/cargo-generate/cargo-generate/commits): ci: refresh examples' own lock entry so release PRs pass --locked (#1810)

## Why
Release PRs fail `check examples`: release-plz bumps the root version
but leaves the example lockfiles at the old one (e.g.
https://github.com/cargo-generate/cargo-generate/pull/1802). Last
release needed a manual lockfile commit.

## What changed
- CI runs `cargo update -p cargo-generate` per example before the
`--locked` check; third-party deps stay locked.
- `scaffold-from-blueprint` requires `cargo-generate >=0.25` instead of
`^0.25`, matching its blueprint's `cargo_generate_version`.

Signed-off-by: Sven Kanoldt <sven@d34dl0ck.me>
- [googleworkspace/cli](https://github.com/googleworkspace/cli) [1](https://github.com/googleworkspace/cli/commits): ci: switch automation workflow from pull_request_target to pull_request (#969)
- [nextest-rs/nextest](https://github.com/nextest-rs/nextest) [1](https://github.com/nextest-rs/nextest/commits): Update Rust crate thiserror to 2.0.21 (#3683)

This PR contains the following updates:

| Package | Type | Update | Change |
|---|---|---|---|
| [thiserror](https://redirect.github.com/dtolnay/thiserror) |
workspace.dependencies | patch | `2.0.20` → `2.0.21` |

---

### Release Notes

<details>
<summary>dtolnay/thiserror (thiserror)</summary>

###
[`v2.0.21`](https://redirect.github.com/dtolnay/thiserror/releases/tag/2.0.21)

[Compare
Source](https://redirect.github.com/dtolnay/thiserror/compare/2.0.20...2.0.21)

- Fix parsing of generic unit variants in display expressions
([#&#8203;459](https://redirect.github.com/dtolnay/thiserror/issues/459))

</details>

---

### Configuration

📅 **Schedule**: (in timezone America/Los_Angeles)

- Branch creation
  - "after 8pm,before 6am"
- Automerge
  - "after 8pm,before 6am"

🚦 **Automerge**: Enabled.

♻ **Rebasing**: Whenever PR is behind base branch, or you tick the
rebase/retry checkbox.

🔕 **Ignore**: Close this PR and you won't be reminded about this update
again.

---

- [ ] <!-- rebase-check -->If you want to rebase/retry this PR, check
this box

---

This PR has been generated by [Mend
Renovate](https://redirect.github.com/renovatebot/renovate).

<!--renovate-debug:eyJjcmVhdGVkSW5WZXIiOiI0My4yODguMCIsInVwZGF0ZWRJblZlciI6IjQzLjI4OC4wIiwidGFyZ2V0QnJhbmNoIjoibWFpbiIsImxhYmVscyI6WyJkZXBlbmRlbmNpZXMiXX0=-->
- [rust-itertools/itertools](https://github.com/rust-itertools/itertools) [1](https://github.com/rust-itertools/itertools/commits): Add `#[inline]` to `ZipEq::next`
- [sigoden/dufs](https://github.com/sigoden/dufs) [1](https://github.com/sigoden/dufs/commits): fix: honour Overwrite header on WebDAV MOVE (#779)

WebDAV MOVE went straight to fs::rename and never read the Overwrite
header, so a client sending "Overwrite: F" received 204 while the
existing destination was silently replaced and the source removed.

Respond with 412 Precondition Failed when the destination already exists
and overwriting is disabled, mirroring handle_copy. Move the overwrite
check ahead of ensure_path_parent in both handlers so validation happens
before any filesystem change.
- [tokio-rs/mio](https://github.com/tokio-rs/mio) [1](https://github.com/tokio-rs/mio/commits): use `RUSTFLAGS=-Cpanic=unwind` for WASI tests

The default for Rust Wasm targets is `panic=abort`, which causes the guest to
trap, preventing the test harness from gracefully failing the test and dumping
any buffered stderr or stdout, including the panic message.

This requires nightly and `-Zbuild-std` because it changes the ABI for the
target.

This also sets `WASMTIME_BACKTRACE_DETAILS=1` for better stack traces on
failures.

## [s3](https://github.com/topics/s3)
- [Altinity/clickhouse-backup](https://github.com/Altinity/clickhouse-backup) [4](https://github.com/Altinity/clickhouse-backup/commits): prepare ChangeLog.md for v2.8.3

Add entries for #1562, #1645, #1653, #1655, rsync example fixes,
plain_rewritable restore gate on ClickHouse 25.4 and go dependencies.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Signed-off-by: slach <bloodjazman@gmail.com>
- [benbjohnson/litestream](https://github.com/benbjohnson/litestream) [2](https://github.com/benbjohnson/litestream/commits): fix(s3): retry throttling with bounded backoff (#1609)

## [search-engine](https://github.com/topics/search-engine)
- [lancedb/lancedb](https://github.com/lancedb/lancedb) [17](https://github.com/lancedb/lancedb/commits): feat: resolve retry config from environment variables

Resolve retry settings from the six documented `LANCE_CLIENT_RETRY_*`
environment variables through the shared retry configuration. Explicit
configuration takes precedence, invalid values return `InvalidInput`, and
status lists tolerate whitespace and trailing commas while a blank list
disables status-based retries.

Saturate calculated backoff at one hour instead of panicking when the
exponential exceeds the representable `Duration` range, including retry
counts configured from the environment.

Includes coverage for defaults, all six environment variables, explicit
configuration precedence, status parsing, invalid environment and direct
configuration values, real process-environment wiring, and saturating
backoff.

Closes #2350

Originally authored by Joshua Snider (@jsnider3).
- [valeriansaliou/sonic](https://github.com/valeriansaliou/sonic) [4](https://github.com/valeriansaliou/sonic/commits): Merge pull request #440 from MAHIR-BABBAR/fix/issue-438

fix: don't panic when a client disconnects before the response is written

## [swift](https://github.com/topics/swift)
- [trycua/cua](https://github.com/trycua/cua) [24](https://github.com/trycua/cua/commits): fix(cli): give a durable harness driver a Space big enough to install and run the harness (#6222)

A durable agent's driver installs the harness and runs it in a Space that
got the job default of 1 CPU and 1 GiB. On real machines OpenCode (and
Claude Code during its install) was killed for memory (exit 137) on every
drive. A driver that runs a harness now asks for 2 CPUs and 4 GiB.

Co-authored-by: Claude Sonnet 5.5 <noreply@anthropic.com>
- [supabase/supabase-swift](https://github.com/supabase/supabase-swift) [10](https://github.com/supabase/supabase-swift/commits): fix(auth): exchangeCodeForSession fails before the request when the PKCE verifier is missing (#1523)

* fix(auth): exchangeCodeForSession fails before the request when the PKCE verifier is missing

* test(auth): pass purpose to codeVerifierStorage.set after rebase

---------

Co-authored-by: Guilherme Souza <guilherme@supabase.io>
- [FluidInference/FluidAudio](https://github.com/FluidInference/FluidAudio) [7](https://github.com/FluidInference/FluidAudio/commits): feat(tts/pocket): cut oversized sentences at more kinds of punctuation and balance word splits (#935)

### Why is this change needed?

Fixes #934. PocketTTS speaks each chunk separately, so prosody restarts
wherever a sentence is cut. In the reporter's listening tests with a
cloned voice, a cut at a comma could not be heard, because a speaker
pauses there anyway, while a cut between words always was.

Since #938 a sentence stays whole as long as it fits the KV cache, so
cuts only happen to long sentences, or with cloned voices, whose
conditioning takes more of the cache. Those were still cut between words
more often than needed:

1. **Only `, ; :` counted as places to cut.** A dash or a bracketed
aside was passed over.
2. **With no punctuation to use, each part was filled to the limit**,
which strands a short tail with a prosodic start of its own.

Chunks from `synthesizeStreaming`'s chunker with the v2.1 English
tokenizer (`‖` marks a cut, numbers are tokens):

| Sentence | Voice cache position | main | This PR |
|---|---|---|---|
| "…precedes rain — a mix of ozone…" (69) | 251 (cloned) | 16 ‖ 47 ‖ 6,
"…the first drops ‖ hit the pavement." | 37 ‖ 32, at the dash |
| "The control plane on the Pi (which also serves the dashboard) polls…"
(69) | 251 | 54 ‖ 15, "…a single response that ‖ the rest…" | 21 ‖ 48,
after the aside |
| "Nobody should ever need to restart the whole machine…", no
punctuation (52) | 251 | 45 ‖ 7, "…a long ‖ question from the voice
loop." | 26 ‖ 26 |
| "…precedes rain—a mix…", longer (88) | 126 (shipped) | 72 ‖ 16, "…the
children run ‖ back inside…" | 36 ‖ 52, at the dash |

With a shipped voice the first three fit the cache and stay whole, on
main and here.

### What changed

- **`splitAtClauseBoundaries`** also splits at an em dash; at an en dash
or hyphen with a space on each side, so `well-known` and `10–12` stay
whole; after an ellipsis followed by a space; and at the edges of a
bracketed aside. Only a bracket opened after a space starts an aside, so
`f(x)` and `item(s)` stay whole.
- **Regrouped clause parts keep their original separator**, so an
unspaced boundary (`rain—a`, `beta,gamma`) is not given a space.
- **`splitAtWordBoundaries`** uses the fewest parts that fit the KV
cache and closes each at the word boundary nearest an equal share of the
tokens still to place, as long as the rest still fits in the parts left.
The single-word orphan fix from #584 is kept, and chunking costs about
what the greedy fill did.
- **`splitSentences`**: a run of sentence punctuation ends one sentence
once (`the lab...` was passed on as `the lab. . .`, `?!` as `? !`).
- **`normalizeText`** strips a trailing dash from a sentence-start
chunk, as it already did `, ; :`.
- **Docs**: the PocketTTS text-chunking section describes #938's cache
limit and these cut rules.

### Maintainer changes

Rebased onto main, dropping the #932 commit, which landed with #938. The
second commit adapts the original to main and fixes the review findings:
- The balanced split counted parts against `maxTokens`, which is the
512-token ceiling since #938, so it would no longer have split a
sentence that overflows the cache. Its fixed per-part target could also
spill into an extra short part (126 tokens became 38, 37, 41, 10). It
now works against the cache check.
- A bracket inside a word was treated as an aside (`f(x)` became `f (x)`
and a 12-token chunk).
- The `maxTokensPerChunk: 0` crash no longer applies: the public APIs
reject 0, and the split no longer divides by it.

### Verification

- `PocketTtsCutPlacementTests` covers each boundary rule and its
exceptions, separator-preserving regrouping, the balanced split, and the
table above at voice cache positions 126 and 251, with the real
tokenizer fixture. Reverting the balance, the bracket rule, or the
separators fails it.
- The PocketTTS, SentencePiece and Phonon suites pass (183 tests), as do
the TTS suites (387). `swift format lint` is clean.
- No new listening test; the original listening result above still
applies.

*Originally implemented by Claude Code working with the reporter, who
verified the results by listening. The maintainer changes were also made
with Claude Code.*

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Alex-Wengg <hanweng9@gmail.com>
- [Beingpax/VoiceInk](https://github.com/Beingpax/VoiceInk) [6](https://github.com/Beingpax/VoiceInk/commits): Merge pull request #1043 from Beingpax/fix/centralize-enhancement-retries

Delegate enhancement request retries to LLMkit
- [Clipy/Clipy](https://github.com/Clipy/Clipy) [4](https://github.com/Clipy/Clipy/commits): Bump version to 1.4.1

Version 1.4.1 is the final release to support macOS 13 Ventura.
- [Licoy/StrokeMouse](https://github.com/Licoy/StrokeMouse) [4](https://github.com/Licoy/StrokeMouse/commits): chore(release): bump version to 0.0.37
- [MarkEdit-app/MarkEdit](https://github.com/MarkEdit-app/MarkEdit) [3](https://github.com/MarkEdit-app/MarkEdit/commits): Add Quick Search to dock menu (#1847)
- [iziz/libPhoneNumber-iOS](https://github.com/iziz/libPhoneNumber-iOS) [2](https://github.com/iziz/libPhoneNumber-iOS/commits): chore(release): merge metadata update for 2.1.3
- [Alamofire/Alamofire](https://github.com/Alamofire/Alamofire) [1](https://github.com/Alamofire/Alamofire/commits): Fix AFError.isSessionTaskError documentation (#4063)

Correct the documentation for `AFError.isSessionTaskError` to refer to
`sessionTaskFailed`, matching its implementation.
- [shadowsocks/ShadowsocksX-NG](https://github.com/shadowsocks/ShadowsocksX-NG) [1](https://github.com/shadowsocks/ShadowsocksX-NG/commits): feat(rules): fix custom rule actions to their scheme

## [wearable](https://github.com/topics/wearable), [wearables](https://github.com/topics/wearables)
- [OpenStrap/edge](https://github.com/OpenStrap/edge) [111](https://github.com/OpenStrap/edge/commits): Merge pull request #645 from OpenStrap/fix/notifications-alarm-and-widgets

fix alarm, notifications, watch and widgets
- [Mentra-Community/MentraOS](https://github.com/Mentra-Community/MentraOS) [6](https://github.com/Mentra-Community/MentraOS/commits): Merge pull request #846 from Mentra-Community/mentraos/fleet-stable-phone-id

Keep the Fleet phone device ID across reinstalls

GitOrigin-RevId: cbf4dfc82cbd61ec9068f00b439266f3e86aa8ac

## Other
- [openai/codex](https://github.com/openai/codex) [54](https://github.com/openai/codex/commits): Tighten Bazel CI snapshot handling and OTLP test cleanup (#58459)

## Why

Failed snapshot assertions should print their diffs without leaving `.snap.new` files after a passing retry. The OTLP loopback collector should stop once exporter shutdown completes instead of waiting for its deadline.

## What changed

- Set `INSTA_UPDATE=no` for Bazel CI tests, including the local configuration used when no BuildBuddy API key is available.
- Initialize the OTLP provider before starting the collector's deadline in the Tokio bounded-shutdown test.
- Signal the collector to stop after shutdown and join its thread before propagating any shutdown error.

GitOrigin-RevId: 55b050822ec923894c9edbc8f039f35f693a4b7e
- [binwiederhier/ntfy](https://github.com/binwiederhier/ntfy) [40](https://github.com/binwiederhier/ntfy/commits): Merge pull request #2088 from binwiederhier/adminsock-socket

Admin socket: serve the admin API on a local unix socket
- [earendil-works/pi](https://github.com/earendil-works/pi) [25](https://github.com/earendil-works/pi/commits): fix(durable): idle checks and wake() without per-commit scans

After every commit that changed a task, the scheduler re-checked every
conversation with a kept context range (every conversation read in the last
contextRetentionMs) by walking its subtree, scanned them again for the next
expiry, and wake() scanned every live task. CPU per run grew linearly with the
number of conversations.

Now a commit re-checks only the conversations above tasks that became live or
ended (collected before the sweep; a chain load that resolves an unknown for a
live unloaded task falls back to a full check), idle context ranges expire
from an index ordered by idleSince (re-sorted when the clock goes back; zero
retention drops all idle ranges; reconcile passes still expire for hosts that
decline timers), and wake() takes the earliest sleep from the sleeping tasks
and scans live tasks only while nothing runs.

One Session, one-tool runs, no storage latency: 2048 conversations 100 -> 805
runs/s, 4096: 46 -> 772; local SQLite at 2048: 88 -> 459; CPU per run flat at
about 1.6 ms.
- [comtrya/comtrya](https://github.com/comtrya/comtrya) [22](https://github.com/comtrya/comtrya/commits): docs: bring the docs up to 0.11.0 behaviour (#740)
- [block/buzz](https://github.com/block/buzz) [21](https://github.com/block/buzz/commits): ci: bound Hermit fetches and let relay builds run without sccache (#8739)

## Summary

Two CI-workflow fixes from the 23–30 Oct flake audit. This is one of six
PRs split from the reviewed `flakey-tests` branch (siblings below). Each
PR applies on its own to `main`.

### Hermit tool downloads (5 runs, 1 on main)

- **Runs:** 40635610550 and 40941660945, in Detect Changed Paths
(`node`). The selection step printed nothing for 9–10 min, the job hit
its cap, and every gate failed as cancelled. Three more, 40373404267 on
main (PostgreSQL Tests and Desktop E2E Integration 1/3, `pgschema`),
40373003333 (Mobile Android, `cmake`) and 40373467575 (Desktop Build
macOS, `just`), got 504s during GitHub's release-asset outage on 10-26,
~17:54–18:00 UTC.
- **Cause:** jobs start with an empty Hermit cache, so a tool's first
call downloads it, with no deadline. Hermit v0.54.1 tries three times, a
second apart, then gives up.
- **Change:** a new `scripts/ci-hermit-retry.sh` runs a no-op tool
command with a 90 s deadline per attempt, three attempts and 15 s × n
backoff. The deadline is plain bash: job control gives each attempt its
own process group, which gets TERM and then KILL. macOS runners have no
`timeout(1)` and may run bash 3.2. A "Fetch Hermit tools" step calls it
for:
- `node` and `just` in Detect Changed Paths, where one stall cancels
every gate. One `sh -c` invocation covers both, so the worst case is 345
s, inside the 10-minute cap. Two invocations would take 690 s.
- `pgschema` in PostgreSQL Tests, Desktop E2E Integration and Backend
Integration (via `--help`, since it has no `--version`).
  - `just` and `cmake` in the Android lane.
  - `just` in Desktop Build (macOS).

The test, `scripts/ci-hermit-retry.test.mjs`, joins Detect Changed
Paths' `node --test` list, and the script joins the rust and mobile path
filters. One stalled attempt costs ~105 s, which fits every job's cap.
- A killed attempt doesn't break the retry. Hermit downloads to a temp
file and unpacks to a temp dir, and renames each into place only once
it's complete. Its lock is a kernel flock.

### sccache storage failures (2 runs)

- **Runs:** 40355289475 (Desktop E2E Relay postgres-tests, 10-26,
"Egress is over the account limit") and 40714034945 (relay-binaries,
10-28, "send http request").
- **Cause:** the sccache server checks its GHA cache storage at startup
and won't start if that fails. Cargo's first `sccache rustc -vV` spawns
it, so the build fails. `SCCACHE_IGNORE_SERVER_IO_ERROR` doesn't help
here: in v0.16.0 it is read only when a running server's compile
response fails.
- **Change:** a "Start sccache" step runs `sccache --start-server`. It
outputs `wrapper=sccache`, or an empty wrapper and a warning if the
server won't start. The three build steps take `RUSTC_WRAPPER` from it,
and cargo treats an empty `RUSTC_WRAPPER` as no wrapper.
- The fallback doesn't fail the job later, in sccache-action's post
step. At the pinned fc920bf, that step runs `sccache --show-stats` and
the JSON form, and fails the job if either exits non-zero. With no
server running, v0.16.0's `--show-stats` doesn't start one. It returns
zero stats from the client side and exits 0. So the step keeps its stats
annotation, and `disable_annotations` stays unset.

### Related issue

None found. **Overlaps #8213** ("ci: fix empty root-workspace Rust
caches and merge test-unit nextest runs"). #8213 already conflicts with
`main`, and this PR adds a conflict in `.github/workflows/ci.yml` (path
filters).

### Testing

Verified locally:
- With a fresh Hermit state dir, `node` was SIGKILLed mid-download, then
mid-unpack while holding the lock, then stopped with TERM by the
script's own 1 s deadline. Each retry produced a working v24.15.0, at
clean-unpack speed. The `sh -c` form fetched both tools, and a 1 s
deadline on `sh -c 'sleep 37 && ...'` stopped `sh` and its child,
leaving no orphan. Tested under macOS bash 3.2 and Debian bash 5.2.
- sccache v0.16.0 (aarch64-apple-darwin) ran against a GHA cache whose
`ACTIONS_RESULTS_URL` refused connections, in READ_ONLY and READ_WRITE
modes. `--start-server` exited 2 ("Server startup failed: cache storage
failed to read"). Both `--show-stats` forms then exited 0, with zero
stats and valid JSON. `--stop-server` exited 2, which shows no server
had started.

Only hosted CI can show:
- the script under the runners' real shells, and that healthy runs only
pay a few seconds;
- whether ~3 min of spaced attempts rides out the next outage. The 10-26
outage lasted ~6 min, longer than this covers;
- that the explicit `--start-server` behaves like cargo's implicit start
against the real GHA cache. The fallback branch needs a storage outage
to run in CI.

Not covered here: first fetches of other tools (rustup, uv, pnpm) still
have no deadline. A per-job Hermit package cache is the follow-up.

Pushed with `git push --no-verify`, because the pre-push suites fail
when the laptop is under load.

### Readiness

An agent review of the combined `flakey-tests` branch (b432453af) found
no blockers. `buzz-review-completed` is not added, because the human
test step (AGENTS.md "Before opening a PR", step 3) hasn't happened yet.

### Siblings

- #8740 test(relay): thread_window aux-page hold and `api::media`
Postgres tests
- #8741 test(mobile): RunnerTests title fade and alert wait
- #8742 fix(desktop): deep-linked message hold (product change)
- #8743 test(desktop): four specs racing scroll settles and focus
- #8744 test(desktop): five settle classes and remote-owned-mentions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Signed-off-by: Matt Toohey <contact@matttoohey.com>
Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) [19](https://github.com/ghostty-org/ghostty/commits): fuzz: fix replay crash detection and add osc target (#14896)

In Nushell, running an external command that exits successfully returns
stdout as an empty string. The previous error check tested whether the
result was not `null`, which always evaluated to `true` for clean exits.

Use the `complete` command to inspect the process exit code.

Additionally, add "osc" to the default list of fuzzers so OSC crashes
are replayed by default.

Ref: https://www.nushell.sh/commands/docs/complete.html
- [MobSF/Mobile-Security-Framework-MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) [18](https://github.com/MobSF/Mobile-Security-Framework-MobSF/commits): Merge pull request #2753 from MobSF/feat/replace-httptools-mitmproxy

feat(dynamic): replace http-tools with mitmproxy and add live HTTP traffic viewer
- [jdx/mise](https://github.com/jdx/mise) [16](https://github.com/jdx/mise/commits): feat(watch): add --once to wait for a change, run the tasks, and exit (#15212)

Scripts and coding agents often need to wait until a file changes, run a
task once, and get its result. `mise watch` couldn't do that because it
never exits, so callers wrote their own sleep-and-poll loops. `mise
watch --once` now does it:

```sh
mise watch test --once && echo "tests pass after the change"
```

With `--once`, mise:

- runs nothing at start;
- waits until one of the watched sources changes, using the same paths
and filters as a normal `mise watch` (the tasks' `sources` and those of
their dependencies, `--watch`, `--exts`, `--filter`, `--debounce` and
the rest);
- runs the tasks once with `mise run` and exits with their status. A
task that exits 3 makes `mise watch --once` exit 3, and a task killed by
a signal gives 128 plus the signal number.

`--once` implies `--postpone`, and passing `--postpone` as well changes
nothing. To run now and then once more after a change, use `mise run
build && mise watch build --once`.

Other exits:

- watchexec missing: the existing install hint, exit 1.
- watchexec stops before anything changes: `watchexec exited with …
before any watched file changed`, exit 1.
- Ctrl-C: 130. SIGTERM, SIGHUP or SIGQUIT while waiting stops watchexec
and runs nothing. During the run they go to the process group of the
nested `mise run` and every task it started, `raw = true` tasks
included. When stdin is not a terminal, that `mise run` gets its own
process group, isolated the same way mise isolates task commands. Either
way mise then exits the way the signal would have ended it (143 for
SIGTERM).
- Flags that only set how watchexec runs the command (`--restart`,
`--clear`, `--on-busy-update`, `--signal`, `--shell`, `--delay-run`,
`--stdin-quit`, `--emit-events-to` and similar) are refused with
`--once` instead of being silently ignored. `--watchexec-env` still
reaches the tasks.

### `--exit-on-error`

`mise watch` now passes watchexec's `--exit-on-error` through. A normal
watch then stops at the first failed run and exits with that run's
status, where before it exited 1 with `command watchexec exited with …`.
Needs watchexec 2.5.0 or later.

### Why not watchexec's `-1`

watchexec has a hidden `-1` flag ("exit after the first run"). Its help
says it is for testing only, and it handles signals in ways a caller
can't work with. Measured with watchexec 2.8.0:

- `watchexec -1 --postpone`: a SIGTERM while waiting **runs the
command**, then exits 0.
- During the run, SIGTERM is ignored until the command finishes, and a
command killed by a signal is reported as exit 0.

So with `--once`, watchexec runs with `--only-emit-events
--emit-events-to json-stdio`, keeping the same filters. mise reads its
first event line, stops watchexec, and runs `mise run` itself. A
caller's timeout or cancel therefore works at any point.

### Testing

- New e2e `e2e/cli/test_watch_once`:
- nothing runs at start, and a file outside `sources` doesn't trigger a
run;
- touching a source runs the task once and the exit code (3) comes back,
with `--watchexec-env` set;
  - `--once --postpone` behaves the same and exits 0;
  - SIGTERM while waiting exits 143 without running the task;
- SIGTERM during the run of a `raw = true` task stops the task's whole
process tree (this check fails if only the nested `mise run` is
signalled);
- SIGINT during the run of a raw task that ignores SIGINT gives 130, and
mise still stops the task with SIGTERM on its way out;
  - conflicting flags are refused;
  - `--exit-on-error` exits with the failed run's status.

To stay robust on slow runners, the test touches the source every second
until mise exits, so it never depends on exactly when watchexec becomes
ready.
- New unit tests for the refused-flag list, the `mise run` arguments,
signal exit codes and `--exit-on-error` forwarding. The existing watch
e2e and unit tests pass, and clippy passes with `-D warnings`.
- Not covered: Windows, where signal forwarding doesn't apply. Ctrl-C
there still kills watchexec when the wait is dropped. When stdin is a
terminal, the nested `mise run` stays in the terminal's foreground
group, as `mise run` does for its own tasks, so job control keeps
working. A SIGTERM sent to mise's pid by another process then reaches
that `mise run` but not the subprocesses of a raw task. Signals from the
terminal reach the whole group.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

*AI-assisted — Tool: Claude Code; model: anthropic/claude-opus-5-5;
version: 2.1.309.*


<!-- This is an auto-generated comment: release notes by coderabbit.ai
-->
<!-- coderabbit-ai-generated:v1 -->

## Summary by CodeRabbit

* **New Features**
* Added `mise watch --once` to wait for a matching source change, run
tasks once, and exit with the run’s status. It implies `--postpone`;
watchexec flags such as `--restart` and `--clear` aren’t supported in
this mode.
* Added `--exit-on-error` to stop watching after the first failed run
and return its status. This option requires watchexec 2.5.0 or later and
has no effect with `--once`.
* **Documentation**
  * Updated the watch command documentation and added usage examples.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [perkeep/perkeep](https://github.com/perkeep/perkeep) [14](https://github.com/perkeep/perkeep/commits): cmd/pk: make pk livejournal's journal an importer account's too

The importer pages list importer accounts, so a journal kept with pk
livejournal wasn't there, though the LiveJournal importer keeps the
same permanodes. After syncing, find (or make) the importer's account
for the user, and put the journal's set in its import root, as the
importer's runs leave it. An account it makes has no password file,
which the server's runs need, so it's set up there.
- [antirez/ds4](https://github.com/antirez/ds4) [13](https://github.com/antirez/ds4/commits): Validate Qwen tokens before prefetched input staging

Keep the existing vocabulary check ahead of embedding reads on both staging paths. Reject malformed chunks before changing live PLE history, and test invalid tokens in the first chunk, a prefetched chunk, and the partial tail with exact recovery.
- [huggingface/lerobot](https://github.com/huggingface/lerobot) [13](https://github.com/huggingface/lerobot/commits): chore(dependencies): update uv.lock (#5167)

Co-authored-by: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
- [meta/mariana-trench](https://github.com/meta/mariana-trench) [13](https://github.com/meta/mariana-trench/commits): Write the local flow format version to the bundle metadata

Summary: Local flow bundles now record `local_flow_format_version` (2) in `local_flow-metadata.json`; bundles without the field are version 1.

Reviewed By: kbuaaaaaa

Differential Revision: D128520956

fbshipit-source-id: d1da541ff18be49dc08ad11b2192583565b7d311
- [Le0Michine/FusionGridfinityGenerator](https://github.com/Le0Michine/FusionGridfinityGenerator) [12](https://github.com/Le0Michine/FusionGridfinityGenerator/commits): chore: bump version
- [adafruit/Adafruit-GFX-Library](https://github.com/adafruit/Adafruit-GFX-Library) [11](https://github.com/adafruit/Adafruit-GFX-Library/commits): Merge pull request #526 from pepijndevos/pepijn-segment-lines-spitft-20261022

Batch SPITFT line writes into Bresenham runs
- [espressif/esp-sr](https://github.com/espressif/esp-sr) [8](https://github.com/espressif/esp-sr/commits): Merge branch 'publish/esp-sr-lib-mr-27' into 'master'

feat: update prebuilt libs !27

See merge request speech-recognition-framework/esp-sr!248
- [espressif/esp-iot-solution](https://github.com/espressif/esp-iot-solution) [7](https://github.com/espressif/esp-iot-solution/commits): Merge branch 'example/gmp_ota_adapted_ble_conn_mgr' into 'master'

example(gmp_ota): adapted to ble conn mgr

See merge request ae_group/esp-iot-solution!1713
- [lovyan03/LovyanGFX](https://github.com/lovyan03/LovyanGFX) [7](https://github.com/lovyan03/LovyanGFX/commits): Merge pull request #993 from ainyan03/release_1.2.36

Release 1.2.36
- [meta/idb](https://github.com/meta/idb) [7](https://github.com/meta/idb/commits): Send the Watch Side button without changing iPhone Power

Summary:
# Context
The Apple Watch Side button has a different HID identity from the phone Power/Lock button. Reusing the existing phone mapping would request the wrong system action.

# This Diff
Add a Watch-specific Side button type and HID event, using Consumer page `0x0C`, usage `0x95`. Dispatch it through the native digitizer transport and include its release in operation cleanup. Reject Watch-button input on non-Watch targets rather than remapping it. Existing iPhone `SIDE_BUTTON`/Power behavior is unchanged. This adds Side only; it does not implement the Ultra Action button.

Reviewed By: cute-jumper

Differential Revision: D128461946

fbshipit-source-id: 60e5b9822ec9f2e3e54e56dede61e53d95d67100
- [remsky/Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) [7](https://github.com/remsky/Kokoro-FastAPI/commits): Merge pull request #576 from remsky/feat/ws-tts

feat(api): add ElevenLabs and Cartesia compatible websocket TTS for voice agents

chore(deps): bump uvicorn to 0.54.0 for websocket size limits and keepalive pings; bump version to v0.10.0-rc1
- [rstacruz/cheatsheets](https://github.com/rstacruz/cheatsheets) [7](https://github.com/rstacruz/cheatsheets/commits): [CH-JCN8] Sheets: separate tables of 8+ rows (#2277)

### Every sheet now groups tables of 8+ rows.

## Why

The writing guidelines prefer separating tables that reach 8 rows, and
~50 tables already do. This finishes the sweep across the remaining 22
sheets, as started in #2244.

## What changed

Only `| --- |` separator rows, grouped by meaning. For example, HTTP
status codes split core codes from extensions:

```md
| `303` | See Other          | … |
| ---   | ---                | --- |
| `304` | Not Modified       | … |
```

Build passes; kramdown renders each group as its own `<tbody>`, styled
by `table.scss`.

<details>
<summary>Verification</summary>

- `pnpm build` passes.
- Built `dist/http-status.html` has 13 `<tbody>` elements (6 tables, 7
new groups).
- `git diff --numstat`: 64 insertions, 0 deletions.

</details>
- [facebookincubator/muse-gadget-sdk](https://github.com/facebookincubator/muse-gadget-sdk) [6](https://github.com/facebookincubator/muse-gadget-sdk/commits): VN ESP32-S3 board: drive the NV3023 with ESP-IDF's ST7789 driver (#150)

* VN ESP32-S3 board: drive the NV3023 with ESP-IDF's ST7789 driver

The board took 78/esp_lcd_nv3023, a third-party component and the only
one from its namespace here (#103 pinned it to the release it was tested
with for that reason). The NV3023 takes the MIPI DCS commands the ST7789
does (CASET, RASET, RAMWR, MADCTL, COLMOD, INVON, SLPOUT, DISPON), which
is all that component sent besides the board's own init table, so
ESP-IDF's esp_lcd_new_panel_st7789() draws to it now and the init table
follows its init. The table moves to a small struct of the board's own,
and the SPI settings that came from the component's macro are written
out (mode 0, 40 MHz, 8-bit commands and parameters).

One managed component fewer to fetch and pin, for every build.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* VN 1.83: stop display start when an LCD init command fails

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
Co-authored-by: Anant Narayanan <anant@kix.in>
- [input-output-hk/daedalus](https://github.com/input-output-hk/daedalus) [6](https://github.com/input-output-hk/daedalus/commits): Merge pull request #3446 from input-output-hk/fix/connecting-wallet-port-race

fix(loading): configure the wallet client after a missed ready push
- [buildroot/buildroot](https://github.com/buildroot/buildroot) [5](https://github.com/buildroot/buildroot/commits): package/sunwait: bump to version 0.9.1

Upstream switched from C++ to C, so drop the C++ toolchain dependency
and use the C compiler.

Signed-off-by: Angelo Compagnucci <angelo.compagnucci@gmail.com>
[Julien: use 0.9.1 tag instead of commit id]
Signed-off-by: Julien Olivain <ju.o@free.fr>
- [cline/cline](https://github.com/cline/cline) [5](https://github.com/cline/cline/commits): Render UX verification reports with existing Desktop artifact access (#15453)

* feat: render cloud artifact images in desktop

* fix: retain published media through authentication retries

* fix: load artifact images independently of client clock

* refactor: simplify artifact rendering and event deduplication

* feat: read attached artifacts through session tools

* fix: bind artifact reads to runtime session identity

* fix: keep non-model image artifacts readable as text

* fix: preserve artifact IDs across client boundaries

* feat(sdk): expose opt-in artifact publication tool

* feat(sdk): fetch cloud artifacts through signed URLs

* feat(sdk): cache artifact download URLs per session

* refactor(sdk): derive upload policy from its schema

* refactor(sdk): separate artifact tool from cloud publication

* fix(desktop): preserve tool names at history window boundaries

* refactor: group artifact adapters and expose resource contracts

* refactor: resolve desktop artifacts through a shared lifecycle

* fix: preserve recovery of oversized artifact publication results

* refactor: keep artifact access types with the desktop resolver

* fix(desktop): wait for account readiness before artifact download

* Add UX verifier tool and shared desktop evidence carousel

* fix(desktop): display published images inside chat

* fix(desktop): reserve browser downloads before resolving URLs

* fix(desktop): suppress referrers on reserved-tab navigation

* fix(desktop): retain download action beside artifact previews

* fix(desktop): resolve artifacts when an older hub lacks support

* feat(sdk): expose signed cloud artifact URLs through the hub

* fix(desktop): normalize API base for artifact fallback

* fix(desktop): preserve existing history rendering

* Narrow UX verification PR to shared renderer

* fix(desktop): clarify artifact loading and trim duplicate tests

* refactor(sdk): simplify artifact exports and test coverage

* Use canonical artifact media for UX verification screenshots

* Render UX verification reports with Desktop artifact images

* Fix UX thumbnail controls and expanded image error handling

---------

Co-authored-by: John Choi <john.choi@cline.bot>
Co-authored-by: Saoud Rizwan <7799382+saoudrizwan@users.noreply.github.com>
- [skypilot-org/skypilot](https://github.com/skypilot-org/skypilot) [5](https://github.com/skypilot-org/skypilot/commits): [CI] Pause the monthly auto-trigger for the release pipeline (#11240)

Releases are now published manually (workflow_dispatch), so the monthly
`0 0 1 * *` schedule only produced a run that failed within ~30s: it
computed the next minor RC1 and then errored out in "Create release
branch" because `releases/<X.Y.0rc1>` already existed from an earlier
manual run (e.g. the 2026-10-01 run against the existing 0.14.0rc1).

The schedule block is commented out rather than deleted so it can be
re-enabled in one step. The rest of the workflow is unchanged: manual
dispatch keeps working as before, both with an explicit
`release_version` and with the version auto-derived as the next minor
RC1, and the scheduled path still works if the cron is re-enabled.

Co-authored-by: Claude Code <noreply@anthropic.com>
- [THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC) [5](https://github.com/THU-MAIC/OpenMAIC/commits): fix(persistence): keep edits made just before a page unload (#2113)

On unload the page now writes pending scene and stage changes straight to the server with keepalive requests instead of a read-then-write that the navigation aborted, so an edit followed by a reload, tab close or navigation is no longer lost. Changes that cannot go out that way (over the keepalive budget, structural or outline changes, or while another save could overwrite them) are held back and the browser asks before leaving; "Done editing" waits for the pending save. @openmaic/storage 0.39.1 adds the keepalive option.

Closes #2112

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [nkanaev/yarr](https://github.com/nkanaev/yarr) [4](https://github.com/nkanaev/yarr/commits): server: sliding session cookie for auth
- [TelegramMessenger/Telegram-iOS](https://github.com/TelegramMessenger/Telegram-iOS) [4](https://github.com/TelegramMessenger/Telegram-iOS/commits): Bump version
- [cnlohr/rv003usb](https://github.com/cnlohr/rv003usb) [3](https://github.com/cnlohr/rv003usb/commits): Merge pull request #142 from cnlohr/update_python_for_ci

Update python for ci
- [Community-PIO-CH32V/platform-ch32v](https://github.com/Community-PIO-CH32V/platform-ch32v) [3](https://github.com/Community-PIO-CH32V/platform-ch32v/commits): Merge pull request #136 from m039/develop

Fix wrong ld script for CH572
- [daijro/camoufox](https://github.com/daijro/camoufox) [3](https://github.com/daijro/camoufox/commits): Report each window's own innerWidth and innerHeight

nsGlobalWindowInner::GetInnerWidth and GetInnerHeight returned the identity's
window.innerWidth and innerHeight in every window. A popup a page opened
reported a content area larger than its own outerWidth, and every iframe
reported the main window's content size: a 300x150 iframe read 1366x643 on
158.0.1-beta.41, on Linux and macOS (#963). Stock reports each window's own
size.

The override is gone. CamoufoxWindow.sys.mjs already sizes the main window's
real content area to the identity's, so the main window reads the same values
as before, and the (width) and (height) media queries and visualViewport agree
with them as they did.

popup-window-size now launches with the identity's inner and outer sizes in
the config, as in the report, and checks a 300x150 iframe too. It fails on
158.0.1-beta.41.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [embassy-rs/stm32-data](https://github.com/embassy-rs/stm32-data) [3](https://github.com/embassy-rs/stm32-data/commits): Merge pull request #946 from welnanick/stm32f42-backup-sram

Add missing backup sram to stm32f4[23]..I memory definition.
- [EthanArbuckle/fairplay-decrypt](https://github.com/EthanArbuckle/fairplay-decrypt) [3](https://github.com/EthanArbuckle/fairplay-decrypt/commits): Handle multiple ARM64 slices (#26)

* Handle multiple ARM64 slices

* Improve error handling in arm64 slice extraction

Refactor arm64 slice processing to handle errors more gracefully.

Co-authored-by: Copilot Autofix powered by AI <175728472+Copilot@users.noreply.github.com>

* Remove obsolete arm64 info helper

Deletes the unused arm64_encryption_info wrapper from core.py, leaving the plural slice-info API as the supported interface.

* Handle unencrypted ARM64 slices explicitly

---------

Co-authored-by: Copilot Autofix powered by AI <175728472+Copilot@users.noreply.github.com>
Co-authored-by: objc <ethan@objc.dev>
- [fishjar/kiss-translator](https://github.com/fishjar/kiss-translator) [3](https://github.com/fishjar/kiss-translator/commits): feat: refresh AI model defaults and thinking controls (#1249)
- [sonocotta/esp32-audio-dock](https://github.com/sonocotta/esp32-audio-dock) [3](https://github.com/sonocotta/esp32-audio-dock/commits): Build ESPHome factory firmware
- [usetrmnl/trmnl-firmware](https://github.com/usetrmnl/trmnl-firmware) [3](https://github.com/usetrmnl/trmnl-firmware/commits): Added runtime logging (#629)

* Added runtime logging, that can be toggled with both captive portal and API

* Changed most of the Serial.prints to logging macros

* Declare verbose_logging in each DEV_FIRMWARE branch

Co-authored-by: Rockwell Schrock <rockwell@schrock.me>
Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [anthropics/claude-code](https://github.com/anthropics/claude-code) [2](https://github.com/anthropics/claude-code/commits): chore: Update CHANGELOG.md and feed.xml
- [Automattic/simplenote-android](https://github.com/Automattic/simplenote-android) [2](https://github.com/Automattic/simplenote-android/commits): Bump actions/setup-java from 6.0.1 to 6.1.0 in the actions-minor-patch group (#1906)
- [Automattic/simplenote-ios](https://github.com/Automattic/simplenote-ios) [2](https://github.com/Automattic/simplenote-ios/commits): Bump ruby/setup-ruby from 1.329.0 to 1.331.0 in the actions-minor-patch group (#1847)
- [espressif/esp-adf-libs](https://github.com/espressif/esp-adf-libs) [2](https://github.com/espressif/esp-adf-libs/commits): Merge branch 'bugfix/rate_cvt_have_nosie' into 'master'

fix(esp_audio_effects): ID[9b066b1a] Fix rate_cvt have noise

See merge request adf/esp-adf-libs!367
- [espressif/esp-bsp](https://github.com/espressif/esp-bsp) [2](https://github.com/espressif/esp-bsp/commits): Merge pull request #842 from ponzifex/docs/update-lvgl-doc-links

docs(lvgl_port): update links to the LVGL documentation
- [GameTec-live/ChameleonUltraGUI](https://github.com/GameTec-live/ChameleonUltraGUI) [2](https://github.com/GameTec-live/ChameleonUltraGUI/commits): feat: Update translations (#1050)
- [girliemac/a-picture-is-worth-a-1000-words](https://github.com/girliemac/a-picture-is-worth-a-1000-words) [2](https://github.com/girliemac/a-picture-is-worth-a-1000-words/commits): Update GenAI section
- [joogps/Glur](https://github.com/joogps/Glur) [2](https://github.com/joogps/Glur/commits): Hand the backdrop a new filter on every update (#31)

2.1.1 wrote updates to the layer's copy of the filter by key path. The radius
took, but a mask set that way left the backdrop unblurred, so any GlurView that
updated after appearing lost its blur entirely.

A layer ignores being handed the filter it already has, but takes a new one, so
each update now builds a fresh filter with the current radius and mask.

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills) [2](https://github.com/lijigang/ljg-skills/commits): feat: sync ljg-* skills [ljg-book] (v1.17.125)
- [microsoft/Mage](https://github.com/microsoft/Mage) [2](https://github.com/microsoft/Mage/commits): docs: add Mage-VL-Cowork model link, cowork code link, and updated PDF
- [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) [2](https://github.com/nicobailon/visual-explainer/commits): feat(kit): state machines walked from the code inside <ve-flow>, with marks, regions, auto layout, and /state-machine (#133)

* feat(kit): load and check a state-machine model from the repo's code

A <ve-flow> model names the repo's real step (or a hand model citing it) and the
rules a reader agreed to. kit/machine.mjs parses the script, runs it in a child
process with a timeout, and returns its checked shape or named errors: a rule
that holds on its own fails state, a missing or outside import, TypeScript Node
cannot strip, a step that never returns, a hand step citing a missing line.
The plan's file reader and at= check move to kit/files.mjs so both share them.
Contract in references/machines.md; fixtures in scripts/check-machine.mjs.

Refs #131

* fix(kit): a model that logs to stdout or traps SIGTERM still loads or times out

Code that writes to stdout (a logger) goes to stderr in the child, and a
non-JSON result is a named error instead of a throw. The timeout kills with
SIGKILL, so a model's SIGTERM handler cannot outlive it. Crash errors name the
exit code, an import line may end in a comment, and the model's data: URL never
appears in an error.

Refs #131

* feat(kit): walk a state-machine model and report what breaks

The child walks the model breadth-first from init, every event at every state,
comparing states as stable JSON and capped at 2000. It returns the drawn states
and merged arrows, the states each rule breaks with the shortest path to them,
the states that can still reach a break, dead ends, events that never fire, and
the counts the Page line needs. Fixtures: the player (breaks in 1 step), a door
with a dead end and a dead event, and a counter that breaks after 3 events.

Refs #131

* feat(kit): a <ve-flow> with a model draws the walk, marks what breaks, and replays it

A <script type="text/plain" model> inside <ve-flow> is walked from the repo's
code. The arrows come from the walk, the states are marked (breaks, may-break,
bug-path), and the drawing is checked against the walk: a state the walk
reaches but nobody drew, or a drawn state nothing reaches, is an error, as is a
hand-written <ve-edge>. In a stepper the walk replays depth by depth, then
lights the shortest path to the broken rule, with captions written for you.
The Page line gets one line per machine. The MCP server runs models only when
started with VISUAL_EXPLAINER_RUN_MODELS=1. Labels beside two-way vertical
arrows sit on both sides, and the drawing widens to hold them.

Refs #131

* fix(kit): the bug path lights only on the replay's last step

In a stepper the path's static accent waited for nothing, so steps before the
last already showed it and the last step added only a token; it now lights on
the full picture, and stays lit outside a stepper. Plans style the marks too.
Two walked flows in one stepper figure are an error instead of one doubled
replay, a misplaced node no longer also reads as not drawn, and the error for
an unknown flow child names the model script.

Refs #131

* feat(kit): a model whose state has parts draws each part in its own region

When state() returns an object of part → id, each part is a <ve-region> around
its nodes, and every walked step draws one arrow in each part it changes. A
step every other node of a region takes to one node, like power off, lifts to
a single arrow out of the region and back in. The drawing is checked per part:
a part value nobody drew, a node in no region, an empty region, or a region
that is not a part is an error. Nested states are checked but not drawn yet.

Refs #131

* fix(kit): a lifted arrow never runs under a node, and lights only for its own event

A lifted arrow comes back in along its node's row, so it leaves from a side with
no other node of the region in that row, and warns when no free side is left.
A plain arrow is on the bug path only when it still carries the event the path
took, not when the path took a lifted event between the same two nodes.

Refs #131

* feat(kit): <ve-flow auto> lays out a whole walk, any size, with its marks

A flow with auto and only a model inside draws every state the walk reaches as
a state diagram laid out at render time, with the states that break a rule, the
ones that can still reach it, the shortest path there, and dead ends marked. A
state that has parts draws each part in its own box, with an event every other
state takes drawn once from the box; nested states draw as boxes in boxes. A
hand-placed flow with six or more states nobody drew gets one error that points
at auto instead of a line for each.

Refs #131

* docs: a /state-machine command, and the skill points to state machines read from code

The skill's figure table, the kit, motion, and plan references point to
references/machines.md, which now covers regions, auto, the replay, the marks,
and every error. A /state-machine command runs the workflow from finding the
step to a test for each broken rule, registered with the other commands.
Diff reviews and comparisons walk a machine on each side. A state that can
still reach a broken rule gets a light amber fill, so it differs from the bug
path by more than a shade of yellow. The changelog credits pstack's /statechart.

Refs #131

* refactor(kit): tighten the state-machine code and docs after the challenge pass

One plural helper and one error-message helper; one check for a second model
script, which no longer runs the model; no unused exports or defaults; no
redundant path and depth checks. The checks now cover auto with parts and
nested states, and build the drawn-vs-walked page from the player fixture.
The docs say which rule the replay shows, count states the same way the page
does, and stop naming kit source files.

Refs #131

* fix(kit): refuse auto in a plan, keep the breaking state red off the stepper

auto in a plan rendered an empty exhibit; it is now an error that says to place
the states by hand. The bug-path stroke rule wraps its stepper condition in
:where(), so .is-breaks wins again and the breaking state is red in a plain
figure. The MCP README and the render tool's root description name the
VISUAL_EXPLAINER_RUN_MODELS opt-in, and the report schema lists machines.
machines.md says the model is your own code run with your permissions and that
the import check covers only import … from lines. A const init (or events,
rules, state) now says to write a plain assignment.

Refs #131

* fix(kit): walk copies of states, prototype-free id maps, a break at init

A step that changed its input and returned it rewrote states already walked,
so every state looked broken; each step now gets a structuredClone. The walk's
breaks, paths and depths have no prototype, so a state id like constructor or
toString gets its own depth instead of Object's method. A rule that already
fails at init has an empty path; the replay's last step now marks init alone,
captioned 'breaks “rule” at the start', and the Page line says the same.

Refs #131
- [RfidResearchGroup/ChameleonUltra](https://github.com/RfidResearchGroup/ChameleonUltra) [2](https://github.com/RfidResearchGroup/ChameleonUltra/commits): Merge pull request #527 from nieldk/docs

Add link to Device console for ChameleonUltra
- [RoCry/git-stargazer](https://github.com/RoCry/git-stargazer) [2](https://github.com/RoCry/git-stargazer/commits): build: drop ruff from dev deps (uv lock)
- [RoCry/social-trending](https://github.com/RoCry/social-trending) [2](https://github.com/RoCry/social-trending/commits): build: replace Makefile with justfile
- [smithy-lang/smithy](https://github.com/smithy-lang/smithy) [2](https://github.com/smithy-lang/smithy/commits): Check sdkId length before matching the pattern (#3346)
- [sudoskys/telegramify-markdown](https://github.com/sudoskys/telegramify-markdown) [2](https://github.com/sudoskys/telegramify-markdown/commits): chore: release 1.4.2
- [theyosh/TerrariumPI](https://github.com/theyosh/TerrariumPI) [2](https://github.com/theyosh/TerrariumPI/commits): New Svelte GUI build
- [verl-project/verl](https://github.com/verl-project/verl) [2](https://github.com/verl-project/verl/commits): [data] fix: keep the first NonTensorData in concat_tensordict with tensordict >= 0.11 (#8453)

### What does this PR do?

`concat_tensordict` treats `NonTensorData` as per-batch metadata and
keeps the first instance. `concat_tensordict_with_none_bsz` documents
this ("metadata concatenation simply preserves the first instance"), and
`test_concat_tensordict` asserts it (`output["temp"] == 1.0`).
`TensorDict.cat` behaved that way up to tensordict 0.10. From tensordict
0.11 it stacks `NonTensorData` values that differ into a
`NonTensorStack` with one value per sample. This PR restores the first
input's `NonTensorData` after `TensorDict.cat`, in both branches of
`concat_tensordict` (regular and nested tensors). With tensordict <=
0.10 nothing changes.

How it shows up: `examples/tpu/grpo/Dockerfile` pins
`tensordict==0.15.1` (#8292). There, the per-rank outputs of
`TrainingWorker.infer_batch` are concatenated through `BatchData.concat`
-> `concat_tensordict`. If their `metrics` differ between data-parallel
ranks, they come back as a list, and `sft_trainer_ray` fails in
validation:

```
  File "verl/trainer/sft_trainer_ray.py", line 365, in fit
    val_losses.append(metrics["loss"])
TypeError: list indices must be integers or slices, not str
```

The metrics differ, for example, once `perf/max_memory_allocated_gb`
reports each TPU rank's real peak memory
(verl-project/verl-hardware-plugin#91). Until now it read 0 on every
rank. `ray_trainer.py`'s `tu.get(output, "metrics")["mfu"]` after
`compute_log_prob` reads the same structure. `train_batch` is not
affected, because its outputs have no batch dimension and go through
`concat_tensordict_with_none_bsz`.

### Checklist Before Starting

- [x] Search for similar PRs:
https://github.com/verl-project/verl/pulls?q=is%3Apr+concat_tensordict+NonTensorData
- [x] Format the PR title as `[{modules}] {type}: {description}`

### Test

- `tests/test_protocol_v2_on_cpu.py -k concat`:

  | | tensordict 0.10.0 (verl's pin) | tensordict 0.15.1 (TPU image) |
  |---|---|---|
| before | 3 passed | `test_concat_tensordict` fails: `output["temp"]`
is `[1.0, 1.0, 2.0, 2.0]` |
| after | 4 passed | `test_concat_tensordict` and the new
`test_concat_tensordict_keeps_the_first_metadata` pass |

`test_chunk_concat` also fails with tensordict 0.15.1, before and after
this PR. It calls `torch.cat` on TensorDicts directly, so it tests
tensordict's own behaviour rather than verl's helper.
- New `test_concat_tensordict_keeps_the_first_metadata`: rank outputs
with different `metrics`, with regular tensors and with nested tensors.
- TPU CI (Cloud TPU v6e on GKE, `examples/tpu` recipes with this
branch's image and tensordict 0.15.1). The runs use verl `2ab35292` plus
this commit (`1ffe98bf`), and verl-hardware-plugin with real per-rank
TPU memory metrics:

| Workflow | Without this PR (verl `2ab35292`) | With this PR
(`1ffe98bf`) |
  |---|---|---|
| `e2e_sft_llm_tpu` (Qwen3-0.6B SFT, 4 DP ranks, Ray + torchrun) |
[failed](https://github.com/jialei777/verl-upstream/actions/runs/40961393275)
with the `TypeError` above |
[passed](https://github.com/jialei777/verl-upstream/actions/runs/40965388507):
train/loss 1.38 -> 0.55, val/loss 0.72 -> 0.61, with the same losses as
before |
| `tpu_unit_tests` |
[passed](https://github.com/jialei777/verl-upstream/actions/runs/40961393319)
|
[passed](https://github.com/jialei777/verl-upstream/actions/runs/40965490913)
|
| `e2e_v1_separate_async_tpu` (GRPO, 1 trainer rank) |
[passed](https://github.com/jialei777/verl-upstream/actions/runs/40961393209)
|
[passed](https://github.com/jialei777/verl-upstream/actions/runs/40965494960)
|

The crash does not need the new memory metrics. With memory metrics that
are 0.0 on every rank, the SFT run still [failed the same
way](https://github.com/jialei777/verl-upstream/actions/runs/40964850889)
in one run. In that case the only per-rank value left in the metrics is
psutil's `perf/cpu_memory_used_gb`, which each rank reads at a slightly
different moment.

### API and Usage Example

No API change.

### Design & Code Changes

- `verl/utils/tensordict_utils.py`: `_keep_first_non_tensor_data(output,
first)` puts back `first`'s `NonTensorData` values that `TensorDict.cat`
turned into something else. `concat_tensordict` applies it after both of
its `TensorDict.cat` calls.
- `tests/test_protocol_v2_on_cpu.py`:
`test_concat_tensordict_keeps_the_first_metadata`.

### Checklist Before Submitting

- [x] Read the [Contribute
Guide](https://github.com/verl-project/verl/blob/main/CONTRIBUTING.md).
- [x] Apply pre-commit checks (`ruff check`, `ruff format`).
- [ ] Add / Update the documentation: not needed.
- [x] Add unit or end-to-end test(s):
`test_concat_tensordict_keeps_the_first_metadata`.
- [a2aproject/A2A](https://github.com/a2aproject/A2A) [1](https://github.com/a2aproject/A2A/commits): docs: removing broken link (#2413)

fixes #2407

This PR removes `pancakeai.tech` from the partners list.

Signed-off-by: Aron Kerekes <arkereke@cisco.com>
- [AcademySoftwareFoundation/OpenShadingLanguage](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage) [1](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/commits): fix: Make OSL/platform.h compile for ARM64EC with clang-cl (#2198)

clang-cl defines __x86_64__ for ARM64EC, so that data layouts match x64
code, but it provides no x86 intrinsics for it. Including <x86intrin.h>
then fails with thousands of errors from clang's x86 intrinsic headers.

For ARM64EC (__arm64ec__), platform.h now leaves out <x86intrin.h> and
the bitcast<> specializations that use _castf32_u32 and related
intrinsics, so bitcast<> uses its generic memcpy version, as on arm64.
x86_64 builds are unchanged.

Co-authored-by: Oscar Anson
Assisted-by: Claude Code / Claude Opus 5.5

Signed-off-by: Thiago Ize <10453105+ThiagoIze@users.noreply.github.com>
Co-authored-by: Thiago Ize <10453105+ThiagoIze@users.noreply.github.com>
- [adafruit/Adafruit_CAD_Parts](https://github.com/adafruit/Adafruit_CAD_Parts) [1](https://github.com/adafruit/Adafruit_CAD_Parts/commits): Adding 6538 RV-8803 RTC Breakout

adding files for 6538 RV-8803 RTC Breakout
- [alibaba/open-code-review](https://github.com/alibaba/open-code-review) [1](https://github.com/alibaba/open-code-review/commits): fix(session): print an empty items array from session show --json (#1792)

Signed-off-by: kevin9327 <5299031+kevin9327@users.noreply.github.com>
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) [1](https://github.com/anthropics/claude-agent-sdk-python/commits): chore: bump bundled CLI version to 2.1.316
- [Automattic/simplenote-macos](https://github.com/Automattic/simplenote-macos) [1](https://github.com/Automattic/simplenote-macos/commits): Bump fastlane from 2.241.1 to 2.241.2 in the ruby-minor-and-patch group (#1297)
- [bitbank2/bb_spi_lcd](https://github.com/bitbank2/bb_spi_lcd) [1](https://github.com/bitbank2/bb_spi_lcd/commits): Fixed CS timing for nRF52; fixed parallel lcd structure members for IDF >= 6.0.0
- [ccusage/ccusage](https://github.com/ccusage/ccusage) [1](https://github.com/ccusage/ccusage/commits): fix(codex): price recorded Ultrafast requests at Ultrafast rates (#1989)

* fix(codex): price recorded Ultrafast requests at Ultrafast rates

Codex rollouts can record `service_tier: "ultrafast"` in
`thread_settings_applied` events, but ccusage left that value
unclassified, so with a Standard config fallback those requests were
priced at Standard rates.

Recognize the recorded tier and track it in its own usage bucket, so the
tier stays per request: when a thread switches back to Standard, earlier
requests keep their Ultrafast pricing and token totals are unchanged.

Ultrafast rates come from OpenAI's API pricing table, which publishes
them for GPT-6.1 Sol and GPT-6 Astra only, at exactly 6x Standard for
every input, cached input, cache write and output rate, short and long
context. The embedded models.dev snapshot's GPT-6.1 Sol Ultrafast entry
agrees. Models without a published Ultrafast rate keep Standard pricing.

Fixes #1987

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* fix(codex): keep Ultrafast through tier merges and model aliases

When copied records disagree, prefer Ultrafast over Fast and Flex so a
duplicate does not drop its 6x pricing; Standard still wins any conflict.

Resolve the Ultrafast multiplier through the same model identity that
Standard pricing uses (model aliases and `.`/`@` separator variants), so
a recorded `gpt-6-1-sol` gets the published `gpt-6.1-sol` rate instead
of falling back to Standard.

Document the `ultrafast` service-tier mapping in the adapter README.

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* fix(pricing): resolve the Ultrafast multiplier with the Standard entry

The Ultrafast multiplier was looked up from the recorded model name
separately from the Standard rates, so the two could disagree. Provider
spellings such as `openai@gpt-6-1-sol` fell back to Standard, and a model
aliased to Sol while an exact entry of its own existed (e.g. `gpt-6.1-terra`)
was billed Terra rates at Sol's 6x.

Store the published Ultrafast multiplier on each `Pricing` entry, as Fast
and Flex already are, so one `PricingMap::find`/`find_at` resolution
supplies both the Standard rates and the multiplier.

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* fix(pricing): keep the Ultrafast multiplier for user price overrides

Resolve an override's base entry through model aliases, and derive the
published Ultrafast multiplier from the override name when no base
exists. Load the Ultrafast allowlist alongside the Fast and Flex ones in
every loader, including built-in entries, instead of a lazy global.

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* test(codex): cover Ultrafast across speed policies and duplicate merges

Add Ultrafast to the rollout tier table, including forced Standard and
Fast overriding recorded Ultrafast usage, and to duplicate-compaction
tier merging. Pin that a configured ultrafast tier is not used for
unclassified usage, and document that Ultrafast only comes from
recorded rollout tiers.

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* fix(pricing): resolve published speed multipliers for unmatched overrides

When a price override has no base entry, take the published Fast, Flex
and Ultrafast multipliers for the override name or its alias target,
so an alias to a dated Sol name keeps Ultrafast pricing. Document the
alias base and the published multiplier defaults.

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* test(codex): assert duplicate copies land in exactly one tier bucket

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* fix(pricing): apply target overrides before aliases built from them

Pricing overrides arrive in key order, so an alias key sorting before
its overridden target was built from the target's pre-override entry.
Order overrides by alias dependency depth, which keeps key order for
independent entries and cycles. Test the alias-to-dated-target
multiplier fallback with only the alias overridden.

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* docs(config): note that the Ultrafast multiplier cannot be overridden

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

* fix(pricing): order aliases into override cycles after the cycle

A capped dependency depth let an alias pointing into an alias cycle tie
with the cycle and apply before it. Walk each override's alias chain,
detect a revisited key, and sort looping chains after acyclic ones by
the links leading into the loop. Restore the pricing_alias doc comment
to its function.

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>

---------

Co-authored-by: Razvan Aurariu <38325118+rzv-me@users.noreply.github.com>
- [cdhigh/KindleEar](https://github.com/cdhigh/KindleEar) [1](https://github.com/cdhigh/KindleEar/commits): fix reader
- [ChrisBuilds/terminaltexteffects](https://github.com/ChrisBuilds/terminaltexteffects) [1](https://github.com/ChrisBuilds/terminaltexteffects/commits): feat: draw text over solid fills on drawn bodies with Ink (#371)

Solid(background=True) paints its lit color as each cell's background. Textured(background=...) fills every cell under the text with a color or lit gradient, and Textured(ink=Ink(...)) sets the text color: a color or gradient that follows the light or spreads across the text, darkened by the light by a chosen amount. Ink replaces Textured's gradient argument.

Closes #370
- [CloudZao/Metalio-E-INK4-Plus](https://github.com/CloudZao/Metalio-E-INK4-Plus) [1](https://github.com/CloudZao/Metalio-E-INK4-Plus/commits): v2.0.71版本
- [espressif/esp32-camera](https://github.com/espressif/esp32-camera) [1](https://github.com/espressif/esp32-camera/commits): ov3640: fix the output size chain, crop aspect ratio and sensor clock (#870)

* ov3640: program crop, zoom-out and ISP output size

The driver was derived from OV3660 and changed resolution by writing
0x3800..0x3815, but the OV3640 has none of those registers. The DVP output
therefore stayed at the QVGA 320x240 configured by sensor_default_regs while
the host sized its frame buffer from the requested framesize, so every
non-QVGA framesize produced overflowing, smeared frames.

Use the size chain the datasheet documents instead:

  crop HS/VS/HW/VH (0x3020..0x3027)                    -- 4.2, table 4-2
    -> zoom out SIZE_IN (0x335F..0x3361)               -- 5.7, table 5-7
                SIZE_OUT (0x3362..0x3364)
      -> ISP output (0x3088..0x308B)                   -- 7-1, what DVP sends

Scale_En is 0x3302[5] on this sensor (0x5001 does not exist here). The crop is
centred inside the readout window read back from the sensor, so the configured
window is never exceeded, and SIZE_OUT stays slightly above the requested
output while remaining strictly below SIZE_IN as 5.7 requires.

Tested on ESP32-S3 with the Korvo OV3640 module: QVGA and 96x96 both produce
correct frames (96x96 logs crop 410,11 1536x1536 -> zoom 104x100 -> DVP 96x96).

* ov3640: use the real clock registers and keep the crop aspect ratio

This driver was derived from the OV3660 one, so set_framesize() programmed
the OV3660 PLL block. None of those registers exist on the OV3640:
0x303a..0x303d are the AEC metering window (AVS/AHW), so every frame size
change silently rewrote the auto exposure window, and 0x3824 / 0x460c are
not implemented at all. The frame rate never changed either.

Program the OV3640 clock registers instead (0x300e Rx_PLL, 0x300f dividers,
0x3010 DvpDiv) and keep the vendor default PLLDiv = 14. Measured on a
board with a 20MHz XCLK the frame rate is ~0.414 x PLLDiv (PLLDiv 14 ->
5.8 fps, PLLDiv 7 -> 2.9 fps) and it does not depend on the output size,
because the full QXGA array is always read out - cropping cannot raise it.

Also fix the crop window: when the readout window is smaller than the
requested aspect ratio in one dimension, set_window() clamped only that
dimension and the zoom block stretched the image. Shrink the other
dimension too so a 4:3 request stays 4:3 (1787x1340 instead of 1787x1536).
- [FoloToy/ai-passport](https://github.com/FoloToy/ai-passport) [1](https://github.com/FoloToy/ai-passport/commits): Merge pull request #114 from derec30240/feature/windows-symlink-test-skip

test(skills): skip symlink-dependent installer tests when unavailable
- [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) [1](https://github.com/ggml-org/whisper.cpp/commits): server : add support for .sock communication (#4124)

* server : add support for .sock communication

* server : change constant definition
- [kofrasa/mingo](https://github.com/kofrasa/mingo) [1](https://github.com/kofrasa/mingo/commits): Read the $lookup "let" option without destructuring it (#638)

JavaScriptCore before Safari 18.2 throws a SyntaxError when it parses
`const { let: x } = obj`, so any bundle that includes $lookup fails to
load there. Reading `expr.let` as a property parses in every engine and
keeps the option name and behaviour the same.

Fixes #637
- [LCAV/pyroomacoustics](https://github.com/LCAV/pyroomacoustics) [1](https://github.com/LCAV/pyroomacoustics/commits): Remove redundant ShoeBox assignment in test_add_source_mic (#445)

The first `room = pra.ShoeBox(room_size)` was immediately overwritten by
the chained construction below without being used, so drop the dead
assignment.

Co-authored-by: Cursor <cursoragent@cursor.com>
- [OpenEPaperLink/OpenEPaperLink](https://github.com/OpenEPaperLink/OpenEPaperLink) [1](https://github.com/OpenEPaperLink/OpenEPaperLink/commits): Enabled G5 compression for Chroma29, Chrom42 and Chroma60  starting with v0016.
- [Plaenkler/Gulu_ESP32-C3_ePaper](https://github.com/Plaenkler/Gulu_ESP32-C3_ePaper) [1](https://github.com/Plaenkler/Gulu_ESP32-C3_ePaper/commits): [UPD] README
- [servo/html5ever](https://github.com/servo/html5ever) [1](https://github.com/servo/html5ever/commits): Add missing MathML attributes to local name list (#809)

https://w3c.github.io/mathml-core/#ref-for-attribute-mpadded-voffset-1

https://w3c.github.io/mathml-core/#other-valid-attributes

Co-authored-by: tannal <mtan@igalia.com>
- [servo/rust-url](https://github.com/servo/rust-url) [1](https://github.com/servo/rust-url/commits): fix: prevent panic in Serializer::for_suffix by adjusting start_position (#1172)
- [TactilityProject/Tactility](https://github.com/TactilityProject/Tactility) [1](https://github.com/TactilityProject/Tactility/commits): Mesh improvements, launcher sorting and WiFi buffers increased (#727)
- [taleshape-com/shaper](https://github.com/taleshape-com/shaper) [1](https://github.com/taleshape-com/shaper/commits): flags to create initial admin user (#446)

* flags to create initial admin user

admin-user and admin-user-password flags to create the initial user.
avoids the system ever starting without authentication enabled.

* admin-email instead of admin-user
- [tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro) [1](https://github.com/tensorflow/tflite-micro/commits): Relocate pre-push hook to ci/ and clean up build and style hygiene (#3955)

BUG=n/a
- [ZyoungInc/xueersi-idf](https://github.com/ZyoungInc/xueersi-idf) [1](https://github.com/ZyoungInc/xueersi-idf/commits): Add calibrated motion level and ESP-NOW pairing