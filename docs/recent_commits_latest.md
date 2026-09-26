# Recent Activity in Starred Repositories
_146 active repos with 2276 new commits_

## [ai](https://github.com/topics/ai)
- [openclaw/openclaw](https://github.com/openclaw/openclaw) [493](https://github.com/openclaw/openclaw/commits): fix(cli): finish help rendering after descendants exit (#158448)

Co-authored-by: Vincent Koc <vincentkoc@ieee.org>
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) [254](https://github.com/NousResearch/hermes-agent/commits): fix(stream): tidy clean-EOF diagnostics and truncation copy

- _mark_finish_seen helper on the local _diag; also set on the Anthropic
  path when message_delta carries stop_reason
- emit_stream_drop status: 'attempt N/M dropped, reconnecting'
- clean-EOF log wording: server or proxy closed the stream cleanly
- truncated_unreported copy drops the raw finish_reason placeholder
- turn_tool_validation compares against FINISH_REASON_LENGTH
- [unslothai/unsloth](https://github.com/unslothai/unsloth) [136](https://github.com/unslothai/unsloth/commits): Studio: steady pinned model drop line and pill-shaped project drop highlight (#11986)
- [BasedHardware/omi](https://github.com/BasedHardware/omi) [106](https://github.com/BasedHardware/omi/commits): feat(listen): capture-position clock for transcripts, audio and live speaker ID (#18995)

* feat(listen): pure audio-timeline v2 primitives

One capture coordinate: a per-socket integer sample cursor over decoded
PCM16 mono, with arrival-time anchors at the first accepted frame and at
measured inter-arrival hiatuses (2 s jitter guard, monotonic-confirmed so
a wall-clock step never mints an hour of audio). Provider timestamps
translate only through SendMap spans the provider actually accepted;
out-of-range or evicted ranges fail closed. segment_wall_window is the
one wall-time conversion; covered_window/coverage_outcome never guess
coverage from timestamps alone. AUDIO_TIMELINE_V2 flag helper is pure
config/, read at the call boundary, default off.

* feat(listen): capture sample timeline through receiver, STT epochs and pusher audio runs

Eligible sessions (flag on, single-channel, server STT) get a
CaptureTimeline; every decoded frame occupies an exact sample range that
is carried into the ring buffer (span ledger), the STT buffer (contiguous
start sample) and the pusher audio runs. Each selected provider socket
gets its own epoch translator created at callback-creation time (legacy
callbacks and the managed chain both rebuild per epoch); the VAD gate
tracks pre-roll/source spans and GatedSTTSocket/LiveLegSocket record
only sends the provider accepted. Mapped segments resolve their owning
conversation from the capture span; straddling segments are dropped.

listen_pusher_session buffers AudioRun(conversation_id, start_wall,
bytes) captured at acceptance, sends one 101 per contiguous
same-conversation run with the retained projected start (opcode 103
ahead of boundaries), and performs the opt-in audio_timeline=2
capability handshake: ack required before any v2 audio and on every
reconnect; capability loss mid-recording withholds audio as a coverage
gap instead of terminating or silently downgrading.

* feat(listen): pin conversation first-audio origin with fenced v2 marker

started_at is set once from the first accepted audio frame associated
with the conversation (not conversation creation, not the first
segment), so pre-roll can leave the first segment at a positive offset
and delayed callbacks cannot shift an origin already emitted to
clients. update_conversation_segments pins the typed audio_timeline
marker and the projected origin in one transaction, only while the row
has no marker; once pinned, stale started_at writes are ignored.

The conversation controller tracks per-conversation origins: fresh v2
generations pin at their first accepted frame (receiver), resumed
conversations reuse the persisted started_at and are never marked v2.
TranscriptProcessor processes epoch-translated segments per owning
conversation from the capture span: the current generation gets the
full live path with offsets projected against the pinned origin; a
late batch may still write its still-open owner, and a terminal owner
is fenced out and counted, never replayed into a newer recording.
Photo-only drains keep ordinary wall lifecycle times.

* feat(pusher): v2 continuity, span-carrying chunks and coverage-true storage

Opted-in connections (audio_timeline=2 query param) get an explicit
pusher->listen acknowledgment (opcode 202, fixed version) before any
v2 audio is accepted. v2 audio frames are checked against the last
accepted run's end with 1 ms tolerance: positive discontinuities flush
the partial private-cloud chunk and close the pending batch for upload
(never concatenating across a gap or inside a 60s batch), exact replays
are ignored, partial overlaps are trimmed after verifying the retained
bytes, and conflicting bytes for an accepted range fail closed.

v2 chunk queues carry their authoritative PCM sample count; uploads
stamp span metadata on the blob and refuse to overwrite a colliding
filename with differing bytes. Listing rehydrates spans; grouping
splits at actual uncovered ends (or overlaps) rather than start-to-start
differences; AudioFile exposes validated chunk_spans whose layout joins
the artifact fingerprint; span-aware merging trims overlaps and
silence-fills only real gaps. Legacy listings behave exactly as before.

* feat(listen): coverage-gated audio consumers

Clips, speaker-tag prompt selection and speaker-sample extraction use
the central helpers: for v2-marked conversations the actual selected
window must be covered by validated chunk_spans (clip endpoint rechecks
through the same conversation_clip_pcm); uncovered, pending-upload,
unsupported and no-audio windows are unavailable rather than a clip of
the wrong audio, with bounded coverage counters at each check. Legacy
conversations keep the timestamp-based best-effort behavior unchanged.
v2 playback parts are contiguous by construction (grouping splits at
every real gap), so one span per part keeps the released clients'
strict-seek arithmetic.

* docs(listen): audio timeline v2 wire/storage contract; dev-on prod-off flag

listen_pusher_pipeline.mdx owns the overlap env/wire contract and now
documents the v2 capture coordinate, epoch translation, the
audio_timeline=2 query-parameter handshake with the opcode-202
acknowledgment, discontinuity/overlap reconciliation, span-carrying
blobs and the coverage-gated consumers. AUDIO_TIMELINE_V2 is true in
the dev backend-listen and pusher values and explicitly false in prod;
no dev backend Cloud Run env surface exists (backend-listen and pusher
deploy through the GKE charts).

* test(listen): hermetic receiver->pusher->storage->clip v2 regression

Drives the actual receiver frame/epoch logic, ListenPusherSession run
buffering, the pusher websocket handler (ack, continuity, batch split,
span uploads), storage upload/listing/grouping/merge, the fenced
conversation persistence and the clip helper against in-memory doubles.

The same burst scenario runs with the flag off — which IS the legacy
calculation — and asserts the acceptance criterion fails there: the
chunk timestamp (last arrival minus the whole buffered run) lands ~10 s
away from the segment position (first audio + provider time), coverage
is unsupported and no correct clip exists. With v2 on: origin pinned to
the first accepted frame, an hour-long wall step mints no audio and no
anchor, a reconnect rebuilds the provider epoch with provider time
restarted, the rollover conversation pins its own origin, out-of-range
provider segments reject, and clips return the exact phrase bytes.
Capability loss withholds buffered audio and never downgrades.

Also: ownership ranges are bounded by capture time (120 s) not a tiny
frame count, batch uploads carry the span start, and the v2 branch in
process_loop reads the timeline defensively for stub hosts.

* feat(probe): opt-in audio-timeline alignment scenario for dev

--alignment-scenario paces two >8 s speech windows in real time with
delivered silence and one actual bounded inter-arrival gap, holds the
socket open through finalization, and checks the v2 marker, span
coverage of the transcript windows, /v1/sync/audio urls, and the clip
endpoint with verify_and_transcribe_sample as an auxiliary ASR check
only (deterministic PCM identity stays the hermetic gate). Enrollment
in private-cloud sync is verified/attempted first; NOT_RUN — never
PASS — when the dev identity cannot enable it. Receipts carry no
transcript, audio, token, or endpoint data; all reads stay inside the
five-minute token TTL. Not executed here: dev-only, run by the
coordinator.

* test(pusher): v2 wire matrix — ack, discontinuity flush, replay, overlap

Old listen (no query parameter) sees no ack and keeps legacy
concatenation; an opted-in connection is acknowledged with opcode 202
before anything else and an unsupported version is refused. A positive
discontinuity uploads the partial run separately (span-carrying, never
concatenated across the gap or inside a pending batch), an exact replay
is ignored, a conflicting overlap fails closed, a partial overlap is
trimmed to continue the run exactly, and a conversation switch flushes
and rebinds. The switch test caught a real bug: the extracted flush
helper skipped the buffer reset, so a switched conversation's audio
appended to the previous conversation's leftover bytes under its old
start; the reset is restored.

* refactor(storage): share v2 span helpers from the pure timeline module

Blob span metadata helpers and coverage-aware chunk grouping move to
utils/audio_timeline.py so storage.py and database/conversations.py keep
only their persistence-specific code (and their line-count growth
shrinks to what the feature genuinely adds there).

* feat(listen): capture-clock speaker ID for every server-STT session

Live speaker identification now locates audio on the capture sample clock
for every single-channel server-STT listen session, not only AUDIO_TIMELINE_V2
admissions. After a mid-session STT failover the replacement provider's
timestamps restart at zero; the legacy first_audio + raw_start window then
lands minutes before the 60s ring buffer and matching returns silently, so
the owner loses live recognition for the rest of the recording even though
the voiceprint is correct.

The sample cursor, per-provider-epoch translators (fresh on every failover
rebuild), the capture-positioned ring buffer and the speaker-ID window are
internal to one listen socket: they run always. Only the v2 persistence
stays flag-gated via state.capture_timeline_v2 (pinned once per recording):
projected segment times, started_at pin/marker and the pusher opcode-101
projection. With the flag off the translator runs in project_times=False
mode - provider-native times pass through untouched, owner fencing is
skipped, unmapped segments stay delivered (origin/main persisted them) -
so persisted fields, WebSocket segment fields and the pusher wire remain
byte-identical to the flag-off baseline; only the speaker-ID window moves.
Multi-channel and custom-STT keep no capture clock at all.

* feat(listen): attributable live speaker-ID match exits

After the 2026-09-25 incident the queued owner detections returned before
any match decision without a single log line; the affected account could
only be attributed by replaying the saved conversation's speaker ids.

Every early return in speakers._match_unmapped and its callers that drops
a queued detection now emits exactly one bounded reason as a Prometheus
counter (label = reason only) plus one log line: window_outside_buffer
(the post-failover clock bug's signature, previously disguised as an
inverted-clamp "too short"), too_short, no_pcm, stale_generation and
already_mapped. Pending evidence accumulation is not a drop - it already
logs and its speaker reaches a decision on the next clip - so it is not
counted as an exit. The existing speaker_id_evidence/speaker_id_decision
lines, the new exit line and the match-failure line all carry the
recording session id (never uid, never transcript content).

* test(listen): owner recognition acceptance across an STT failover

Hermetic acceptance test for the 2026-09-25 incident: the owner voiceprint
is enrolled, the owner's pre-failover clip accumulates evidence, the
provider dies mid-conversation, the real failover path rebuilds the socket
and the replacement stream's timestamps restart at zero, and the owner's
later segments must be is_user=true in BOTH the WebSocket output and the
persisted conversation. Drives the actual receiver (decode, capture clock,
epoch translators, the actual _failover_stt_socket rebuild), the actual
TranscriptProcessor.process_loop, the actual SpeakerMatcher and the actual
fenced persistence against in-memory doubles and a deterministic fake
embedding model (fixed-frequency bins; no model download). The replacement
provider also opens a new diarization scope, so recognition must recover
from a fresh unmapped speaker - exactly the incident's Speaker 1.

Passes with AUDIO_TIMELINE_V2 off and on; at the merge base
(771fe0175e, in a temporary worktree under .local/) the same file fails
both parameterizations on the is_user assertion - the queued detections
land before the 60s ring buffer and never decide.

Speaker-ID queueing in the legacy persistence path now queues from the
provider's raw segments (each carrying its capture window) instead of the
post-merge turns: the live merge relabels a merged turn with the absorbing
id, whose window is not in the batch's id-keyed map. The matcher's
covered-audio subtraction already dedupes overlapping re-sends.

The dev probe's alignment scenario gains the same assertion where the probe
identity has a voiceprint (persisted all-is_user plus one live-delivered
is_user segment; NOT_RUN, never PASS, without one). The probe is not run
by this change.

* feat(speaker-tag): attributable owner confirmation outcome

The 2026-09-25 incident: a client-side "That's me" answer reported
succeeded=true yet left no owner_voice_confirmation and did not update the
voiceprint - the outcome existed only as an unlabeled Prometheus counter, so
the loss could not be attributed to a conversation. store_owner_voice_sample
now logs one line per outcome naming the conversation id (never the uid);
the recording session id is not on this path because prompts are answered
after the socket closed, so the conversation id is the join key.

Clip-path proof: a hermetic test runs the real store_owner_voice_sample
through the real owner_clip_window and the real span-carrying clip path
(batch upload -> span-aware listing -> merge -> sample-accurate trim) on a
v2 conversation that experienced a failover, and asserts by byte identity
that the pooled sample is the owner's actual post-failover audio window -
not the pre-failover phrase the legacy first-audio + restarted-provider-time
formula selects.

* docs(listen): capture-clock speaker ID for all server-STT sessions; match-exit counter

Document that the capture sample clock, per-provider-epoch translators and
the capture-positioned ring buffer are internal to one listen socket and run
for every single-channel server-STT session - only the v2 persistence stays
behind AUDIO_TIMELINE_V2 - and that with the flag off only the speaker-ID
window relocates. Document the bounded omi_speaker_id_match_exits_total
reasons, the session id on the speaker-ID log lines, and the attributable
That's-me outcome line.

* fix(storage): database-layer pure span helpers; content-hash batch no-overwrite

Move the pure v2 span helpers into a stdlib-only database/audio_timeline.py
and import them relatively from database/conversations.py: hermetic tests exec
database modules against a stubbed utils package, so a new module-scope
utils.audio_timeline import there broke test collection
(ModuleNotFoundError: utils.audio_timeline). utils/audio_timeline re-exports
the shared helpers as the single source of truth.

parse_span_blob_metadata now requires a real mapping: a test double's
auto-attribute metadata previously parsed as span {start:1.0,...} (MagicMock
supports __float__), silently rerouting legacy per-chunk merges into the v2
span-trim branch and dropping the second chunk.

upload_audio_chunks_batch compares content, never plaintext size: equal
length is not identity (fixed-size 60 s PCM chunks), and enhanced-protection
objects are ciphertext whose length cannot prove a retry. A SHA-256 of the
plaintext payload is compared against the existing blob (decrypted first for
enhanced); identical retries are idempotent no-ops, unreadable or differing
content fails closed without overwriting.

* fix(listen): flag-off VAD remap, thread-safe callbacks, run-based owner ranges

P0: with the capture clock on and v2 off, the non-passthrough callback kept
make_stream_callback's semantics: the active gate's remap_segments runs on
provider timestamps before anything is buffered, and the epoch translation
only attaches the capture window without rewriting start/end, so flag-off
stored/emitted times stay byte-identical to origin/main (with v2 on the
send-map translation replaces the mapper; never both).

Deepgram SDK callbacks arrive off the event loop; receiver-built callbacks
and the managed-chain enqueue now hop onto the listen loop
(_run_on_listen_loop) before touching timeline/send-map state, and the
managed chain uses the receiver's pinned persistence mode instead of always
owner-fencing (_enqueue_epoch_segments).

conversation_sample_ranges entries coalesce into same-conversation runs, so
retention is time-based (120 s) instead of the ~10 s a 512-frame cap held;
a late final now resolves its owner instead of dropping as
late_owner_dropped. Capture origins carry a pinnable flag: only fresh v2
conversations may pin; a resumed row adopts its persisted started_at
(datetime/number/ISO string, parsed by persisted_started_seconds in
contracts) and an unparseable one locks the row legacy — never a fresh pin.
Anchor compaction now fails closed: wall_strict refuses samples in evicted
intervals and the translator rejects such segments instead of extrapolating
across dropped hiatuses.

* fix(listen): introductions run with capture windows; v2 batch parity

P0: queue_from_raw only re-homes the duplicate embedding enqueue; name
introduction detection runs on the merged segments exactly as on origin/main,
so a flag-off pendant user saying 'My name is Alice' keeps the person
creation, suggestion event and assignment updates.

_process_v2_batches: only a pinnable origin (or an already-pinned marker)
writes the v2 marker + started_at — a resumed row projects against its
adopted started_at and stays legacy for its lifetime; a legacy-locked row
(unparseable started_at) keeps its transcript on the legacy base. A
photo-only drain, or a late-owner-only drain with current photos, now runs
the current conversation's write so photos are never dropped. Late-but-open
owners are persist-only (documented); Diarization Completed accounting is
shared with the legacy loop via the same per-conversation speaker map, and
the delivery block is one shared _deliver_live_updates used by both paths.

* fix(pusher): span-walking extract, gap-split 101 frames, flushed-range conflicts

AudioRingBuffer.extract walks the per-write span ledger and copies the bytes
overlapping the window span by span, so a clip crossing a >2 s client stall
returns the audio on both sides instead of converting the whole wall delta
into one byte offset (wrong PCM or ring wraparound). The write path and
per-byte copy are unchanged from origin/main.

ListenPusherSession flushes one 101 frame per contiguous same-conversation
group, splitting when the next run's projected start is more than 1 ms past
the previous run's end, so a disconnect-length gap is never erased from the
stored audio while the header claims the first run's position. Legacy runs
without a projection keep the legacy grouping.

Pusher v2 overlap verification extends past the live buffer through a
bounded digest ledger of flushed runs ((start, end, sha256)); a range that
can be neither byte-compared nor digest-matched is a conflict — the frame is
dropped and counted in omi_audio_timeline_replay_conflicts_total instead of
appending an unverified suffix over stored bytes.

The private-cloud overflow-warning test now asserts the structural invariant
(every enqueue into private_cloud_queue sits in a function that warns) after
the three inline enqueue sites were consolidated into one guarded helper.

* test(listen): pin round-3 fixes through the real receiver/gate/pipeline

test_audio_timeline_round3: flag-off remap equality with the gate mapper,
passthrough/v2 variants, unmappable-segment survival, SDK-thread loop hop,
30 s-late owner resolution on coalesced runs, evicted-interval refusals,
resumed-row (datetime and string started_at) never marked v2, photo-only and
late-owner photo drains, fresh-row pin control.

test_listen_speaker_id_failover now drives the real initialize_stt and
_rebuild_stt_socket_locked through provider-connector doubles with a REAL
active VADStreamingGate (deterministic Silero fake) behind the receiver's own
GatedSTTSocket install — removing send_tracker=epoch from the install now
fails the wiring assertions and the recognition acceptance. Adds the >2 s
client-stall case asserting the ring buffer extracts exact bytes across the
gap, the P0 introduction regression (introduction handled identically to
origin/main with capture windows present), and Diarization Completed for
both persistence modes.

Also: span-walk stall tests for the ring buffer (including wraparound),
101-frame gap-split tests, flushed-range replay conflict/digest-match tests,
and the pipeline doc updates for all changed behavior.

* test(listen): accept epoch in the parity socket double; pin audio_timeline field

The parity runtime's _create_stt_socket double predates the epoch argument
the receiver passes (round-1/2 addition the coordinator's partial CI run
never reached), so initialize_stt failed silently and the capture-once
acceptance lost its socket. Conversation.audio_timeline is pinned in the
trust-boundary field set as server-authored provenance, not projection-family
(never client-authored, no text).

* fix(pusher): drain the retry lane when no batch is pending; fix connect double arity

A failed private-cloud upload's retry batch lives in ready_batches, but the
loop's 'if not pending: continue' skipped the ready-lane drain, leaving the
loop condition truthy forever — a busy spin once shutdown is set (the upload-
failure test hung at 100% CPU). The guard now also checks ready_batches.

The circuit-breaker connect double predates the audio_timeline parameter the
branch added to _connect_to_trigger_pusher; the signature mismatch raised at
call time before the double could set its started event, hanging the stale-
inflight test on await started.wait().

* fix(listen): managed chain keeps the legacy offset rebase in clock-only mode; rebuild-factory stubs

With the capture clock on and v2 persistence off, the managed chain's
callback translated epochs and dropped the leg's own offset/last_end clock,
so flag-off emitted times restarted at 0 per leg instead of staying
monotonic like the pre-timeline managed chain. Clock-only legs now translate
first (attaching the capture window from provider timestamps), then apply
the same gate remap and offset rebase as the epoch-less path, and enqueue
through the receiver's pinned mode. v2 legs keep the projected translation.

The _stt_rebuild tuple became a callback FACTORY in round 1 (a fresh epoch
translator per rebuild); three failover test files still stubbed the old
callbacks-tuple shape and crashed the rebuild with a TypeError.

* chore(failure-classes): FC-transcript-and-audio-on-independent-clocks

Defines the class this branch closes: transcript times and stored/buffered
audio placed by independent clocks (STT provider offset vs frame arrival),
which drifted up to 54 minutes and silently broke clip playback and live
owner recognition after a provider failover.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* fix(listen): owner fail-open only inside the retention horizon

A sample older than the oldest retained run no longer fails open to the
single surviving conversation: retention may have evicted the run — and
every boundary — that owned the sample, so the retained window cannot
prove ownership and the segment stays late_owner_dropped (re-review N1).
The single-conversation fail-open now applies only between retained runs,
inside the retention horizon, where no run covering the sample could have
been evicted yet.

* fix(storage): an exists() probe failure fails closed like an unreadable blob

A raised blob.exists() on the v2 no-overwrite path was swallowed as
'absent', so the upload opened the blob for write and replaced whatever
object actually sat at the colliding 3-decimal batch key (re-review N2).
Any exception from the probe now raises the same ValueError as an
unreadable existing blob and never opens the blob for write.

* fix(pusher): keep the new tail past last_end on an unverifiable v2 replay

An overlap that could be neither byte-compared nor digest-matched dropped
the whole 101 frame, losing the frame's genuinely new audio past the
accepted end as a coverage hole (re-review N3). The conflict branch now
trims to the bytes past audio_timeline_last_end and continues the run
there, still never storing the unverified overlap and still counting the
conflict.

The flushed-run digest ledger is now recorded only after a batch's GCS
upload succeeds (one contiguous entry per batch), so a chunk evicted by
the bounded queue or a batch dropped after exhausting its retries leaves
no entry: replays of that range are unverifiable conflicts instead of
being trusted by a digest whose bytes were never stored.

* fix(pusher): pace ready-lane upload retries one process interval

A failed upload re-queued itself at the front of the ready lane, so the
in-turn while-loop retried it immediately: one fast permanent error
burned the whole retry budget in a single tick, and one slow timeout
blocked this socket's uploader for back-to-back attempts (re-review N4).
The retry now keeps its queue time and is gated by retry_at for one
PRIVATE_CLOUD_SYNC_PROCESS_INTERVAL tick; the gate is skipped during
shutdown so the drain stays bounded.

* fix(listen): deferred STT callbacks count rejections and carry their own segments

A provider callback deferred onto the listen loop via call_soon_threadsafe
ran on the caller's segment list and, if it raised, died as a bare asyncio
callback error: the batch was gone with no counter and no log (re-review
N5). The hop now copies the segment list (a provider may reuse its buffer
once the callback returns) and wraps the deferred action so a failure
increments omi_audio_timeline_segments_total{outcome=rejected} for the
session's mode and logs one bounded line (exception type and count only).
The closed-loop drop stays.

* test(pusher): overflow warning must guard the private-cloud enqueue

The overflow check counted the 'private_cloud_queue full' string anywhere
in the enqueuing function, so a second enqueue on a path the fullness
check never runs on (before it, or in an early return above it) would
drop the oldest chunk silently (re-review N6). The AST test now also
requires the warning's fullness branch to precede each enqueue on its
statement path, and proves the checker flags a synthetic early-return
enqueue.

* docs(listen): round-4 replay, ownership, and loop-hop behavior

The digest ledger is per uploaded batch and written only after the GCS
upload succeeds; an unverifiable replay keeps its new tail past the
accepted end; upload retries are paced by the process interval; the
ownership fail-open is bounded by the retention horizon; deferred STT
callbacks count rejections on their own segment copy.

* chore(deploy): classify AUDIO_TIMELINE_V2 as non-secret config

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* fix(listen): pyright-clean audio timeline typing; regenerate API contracts

Types PrivateCloudChunk's optional v2 span, binds the pusher socket once
per flush and ack wait, drops unused imports/re-exports and the private
span-helper aliases, and registers AudioTimelineProvenance with the Dart
schema group. Regenerates the app-client OpenAPI contract and the Dart,
TypeScript and Swift client models for the new optional fields.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* chore(app): changelog fragment for the audio timeline

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

* fix(storage): store audio-timeline chunk spans as {start, end} objects

Firestore rejects an array directly inside an array, so AudioFile.chunk_spans
as [start, end] pairs would have failed every v2 audio_files write on dev
(hermetic fakes accepted it), and the generated Dart reader for the nested
list did not compile. Spans are now ChunkSpan objects, every reader goes
through database/audio_timeline.chunk_span_bounds, and a test pins that a
dumped AudioFile carries no nested arrays. Client models regenerated.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [t8y2/dbx](https://github.com/t8y2/dbx) [74](https://github.com/t8y2/dbx/commits): chore(release): prepare v0.6.24
- [kortix-ai/suna](https://github.com/kortix-ai/suna) [57](https://github.com/kortix-ai/suna/commits): fix(config-releases): serve a former archive from the store when a repository replacement outruns the mirror (CFG-7) (#7701)

## Summary

Staging release-gate run 36188978457 (attempt 2, `deployed api shard
(2)`)
failed `CFG-7` with `the project's own stored archive: 404`
(`tests/src/flows/config-releases.flow.ts:1000`), on staging SHA
`b6872877`
with `CONFIG_RELEASES_ENABLED=true` (#7691).

**Verdict: product bug**, not a test bug.

### Root cause

`apps/api/src/config-releases/serve-archive.ts` (`serveConfigArchive`)
gated
every archive request on `isTreeObject(mirror, treeId)` *before* ever
consulting the S3 store. `PUT /v1/projects/:id/git/repository` (the
route
CFG-7 exercises by writing the same columns it writes) can replace a
project's origin with a second, genuinely unrelated repository. The OLD
config tree is not reachable from the NEW origin's history — no `git
fetch`
of the current origin will ever reproduce it.

The bare git mirror lives on **per-ECS-task ephemeral disk**
(`apps/api/src/projects/git/mirror.ts`, `repoCachePath` keyed only by
`projectId`, root `/tmp/kortix/git-cache`), not shared across API
replicas.
A replica whose local mirror never warmed *before* the replacement
clones
straight from the CURRENT (already-replaced) origin and can **never**
contain
the old tree — the mirror-gate returns 404 there forever, even though
the
archive is durably stored in S3 under the project's own key
(`projects/<project_id>/trees/<tree>.tar.gz`, written by
`storeConfigArchive`
when the pre-replacement descriptor was first built).

This explains why `CFG-1/2/3/4/6/8/9/10` passed in the same run: none of
them
replace the repository with unrelated history, so every replica's mirror
still contains the tree the archive route needs, regardless of which
replica serves the request. `CFG-7` is the only flow that swaps to a
genuinely unrelated repository, so it is the only one exposed to a cold
replica.

Confirmed NOT an S3 IAM permission gap (the learnings entry on
HeadObject-403-vs-404 does not apply here): the 404 response is returned
directly from the mirror-gate, before the code ever calls `store.head()`
/
`store.downloadUrl()`.

### Fix

When the tree is absent from both the warm and the forced-refresh
mirror,
try the store directly by its project-scoped key before answering 404.
The
key alone proves the archive is this project's own former config (the
caller already passed repository-access / `PROJECT_FILE_READ` to reach
the
route), so no mirror confirmation is required. Only 404 when **neither**
the mirror **nor** the store has it.

## Test plan

- [x] `bun test --isolate --env-file=scripts/test.env --timeout=15000`
over
every `apps/api/src/config-releases/**/*.test.ts` file: **108 pass, 0
fail** (includes 2 new regression tests — store-hit/mirror-miss now
      serves 200 from the store, mirror-miss/store-miss still 404).
- [x] `tsc --noEmit` on `apps/api`: clean.
- [x] `pnpm test -- --domain config-releases` (local stack): **10/10
flows
      pass**, `CFG-7` included (2.3s). The local profile runs one API
process, so it cannot reproduce the multi-replica cache split itself —
the new unit tests are the deterministic reproduction of that exact
      condition.
- [ ] `test` label on this PR for the six CI lanes (not run yet —
requesting
      the label on open).

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/kortix-ai/codesmith/suna/pr/7701?autoLogin=true&ref=codesmith_pr_footer"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img
alt="View with [code]smith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a>
<a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1792970194&installation_model_id=434224&pr_number=7701&ref=codesmith_pr_footer&repository=kortix-ai%2Fsuna&return_to=https%3A%2F%2Fgithub.com%2Fkortix-ai%2Fsuna%2Fpull%2F7701&signature=3bd387813c3ca24a3b4ab8ed076e510a59db5b3cb86e9476264358a3c790729e"><picture><source
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
- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) [35](https://github.com/QwenLM/qwen-code/commits): test(cli): Close the fixture gaps deferred from managed-context/1 (#12712)

The audit of #12700 deferred ten fixture and wording gaps in the
managed-context/1 contract. Close them before W0c consumes the fixtures.

- Identity comparisons are exact. Attestation and installation cases
  answer 409 for identifiers that differ only in letter case, and for
  storage IDs and mount roots that only a normalizer would equate. Session
  and operation IDs that differ only in case are different IDs.
- A context change that touches only the directory, the revision or the
  configuration reference is a conflict, under a new and under a reused
  operation.
- New sequences pin that operation reuse is checked after the digest and
  the Workspace part, and that no refusal records, overwrites or forgets
  state.
- More rule cases: operationId bounds, trailing newlines, non-ASCII
  digits, numeric binding fields, non-string identifiers, signs, a
  padding-only token and loose ready records. Attestation now repeats
  every single-field boot case on an attested field, valid and invalid.
- The Java conformance test pins the schema's enums and its record and
  outcome references.
- The design document names the protocol token, drops the PATH_MAX
  analogy, and states which JSON parsers can read the fixtures. It
  records that the Broker cannot yet tell a refused boot from a crash,
  adds an open question on installation retention, and lists a W0c test
  for the Broker's JSON writer. The runtime-broker README and QWEN.md
  state the parser requirement too.

Refs #12380
- [google/magika](https://github.com/google/magika) [26](https://github.com/google/magika/commits): Merge pull request #1483 from google/pyo3

python: port Magika Python library to wrap magika-lib via PyO3
- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) [23](https://github.com/openai/openai-agents-python/commits): fix(sessions): reject blank SQLite branch names (#5179)

fix(memory): reject blank SQLite branch names
- [screenpipe/screenpipe](https://github.com/screenpipe/screenpipe) [19](https://github.com/screenpipe/screenpipe/commits): Invite teammates from Chat and Workflows with explicit seat pricing (#7303)

* Show team identity above sidebar settings

* Invite teammates from the sidebar popover

* Cover team invite popover in Workflows mode

* feat: confirm team seat pricing before quick-invite purchase

* fix: show the recurring Business seat rate beside due-now pricing

* fix: hide team invite navigation in Enterprise builds
- [google/adk-python](https://github.com/google/adk-python) [16](https://github.com/google/adk-python/commits): docs: fix to_a2a import so the task mode sample runs

Merge https://github.com/google/adk-python/pull/7179

PiperOrigin-RevId: 988542663
- [JerryZLiu/Dayflow](https://github.com/JerryZLiu/Dayflow) [10](https://github.com/JerryZLiu/Dayflow/commits): release: update appcast for v2.6.0
- [Kiln-AI/Kiln](https://github.com/Kiln-AI/Kiln) [10](https://github.com/Kiln-AI/Kiln/commits): Merge pull request #1815 from Kiln-AI/claude/gallant-cerf-2qv3eg

docs: add human-only PR template header and agent PR rules
- [langgenius/dify](https://github.com/langgenius/dify) [10](https://github.com/langgenius/dify/commits): refactor(web): refine detail sidebar states and preview (#42938)
- [pykeio/ort](https://github.com/pykeio/ort) [8](https://github.com/pykeio/ort/commits): ci(code-quality): update tarpaulin
- [github/spec-kit](https://github.com/github/spec-kit) [6](https://github.com/github/spec-kit/commits): chore: release 1.0.12, begin 1.0.13.dev0 development (#4759)

* chore: bump version to 1.0.12

* chore: begin 1.0.13.dev0 development

---------

Co-authored-by: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) [6](https://github.com/google-gemini/gemini-cli/commits): fix(core): align policy redirection gates, path validation, and workflow parsing (#29506)

Co-authored-by: Adam Weidman <65992621+adamfweidman@users.noreply.github.com>
- [lutzroeder/netron](https://github.com/lutzroeder/netron) [5](https://github.com/lutzroeder/netron/commits): Update to 9.3.0
- [docling-project/docling](https://github.com/docling-project/docling) [3](https://github.com/docling-project/docling/commits): fix(md): keep every character-reference spelling of a pipe inside its table cell (#4371)

#2904 keeps an HTML-escaped pipe in its table cell by leaving the
reference encoded until the row is split, but it matched only &#124;,
&#x7C; and &vert;. The other spellings CommonMark accepts for U+007C
(&#x7c;, &#x07C;, &#0124;, &verbar;, &VerticalLine;) were decoded first
and taken for a cell delimiter: the cell was cut at the pipe, the rest
shifted into the next column, and the row's last cell was dropped.

Keep a reference encoded whenever it decodes to a pipe. _close_table
already unescapes the whole cell, so every spelling comes out as | there.

Signed-off-by: RachelWanggg <rachelwangrq2@gmail.com>
- [herdrdev/herdr](https://github.com/herdrdev/herdr) [3](https://github.com/herdrdev/herdr/commits): fix: accept plugin install options before the repository (#4453)

refs #4446

Co-authored-by: akbash-bot <300245827+akbash-bot@users.noreply.github.com>
Co-authored-by: JJ Liebig <jonathan.liebig@gmail.com>
- [akdeb/ElatoAI](https://github.com/akdeb/ElatoAI) [1](https://github.com/akdeb/ElatoAI/commits): adding gpt-live

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- [obra/superpowers](https://github.com/obra/superpowers) [1](https://github.com/obra/superpowers/commits): Release v6.4.2: leaner plans from writing-plans (#2384)

* Harden Codex package script checks

* Default Codex portal package to zip

* Fix Codex plugin category

* chore(codex): remove orphaned session-start-codex hook + refresh hook docs

hooks/session-start-codex has had no caller since "Remove Codex hooks"
(#1845) deleted hooks-codex.json and its manifest registration; the
Codex manifest now declares an empty hooks object so Codex registers no
session-start hook at all. The script is Codex-specific dead code —
nothing executes it on Codex or any other harness.

- Delete hooks/session-start-codex.
- tests/hooks/test-session-start.sh: drop the two Codex cases that are
  redundant with the generic session-start tests (nested-format and the
  legacy-warning omission are already covered by the Claude Code cases).
  Re-point the "wrapper dispatches" case to the live `session-start`
  script so run-hook.cmd dispatch coverage — used by Claude Code and
  Cursor in production — is preserved rather than lost.
- docs/porting-to-a-new-harness.md: Codex is no longer a Shape A
  (shell-hook) harness, so re-anchor that worked example to Cursor (a
  live shell-hook harness that demonstrates the same per-harness field,
  schema, and matcher variance) and mark Codex as native skill discovery
  with no session-start hook. Clears the references to the deleted
  hooks-codex.json.
- docs/windows/polyglot-hooks.md: the "check hooks-codex.json" pointer
  referenced a file deleted in #1845; re-point to hooks-cursor.json.

RELEASE-NOTES.md keeps its historical mention of hooks-codex.json (it
accurately records what that release did). The tests/codex-plugin-sync
fixtures build their own synthetic session-start-codex and test the sync
mechanism generically, so they are intentionally left as-is.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* docs: re-anchor Shape A examples away from Codex

* Strip hooks from Codex portal package

* Preserve hooks in Codex package manifest

* Release v6.1.1: fix Codex SessionStart hook re-registration, add Codex portal packaging

* Revert "Remove Gemini CLI support"

This reverts commit 711d895ce736cbcc5fb0c219ea3f49277f17fa8c.

* refactor(skills): fold Integration skill lists into points of use

The list-style Integration sections in subagent-driven-development and
executing-plans duplicated references that already exist where the flow
uses them (process digraph, When to Use, prompt templates, Step 3), so
they added maintenance cost without carrying behavior. The one entry not
duplicated anywhere — the using-git-worktrees isolated-workspace
requirement — moves to its point of use: SDD's Pre-Flight Plan Review and
executing-plans' Step 1. Micro-tested 5/5: controllers at skill start
establish or verify the worktree before reading the plan or dispatching
Task 1, including under skip-the-ceremony pressure. The prose Integration
sections in requesting-code-review and other skills are unchanged — they
carry placement content, not an index.

* refactor(skills): fold systematic-debugging Related-skills block into Phase 4

Same treatment as subagent-driven-development and executing-plans: the
test-driven-development entry duplicated the reference already at Phase 4
Step 1, and the verification-before-completion entry was a sole carrier —
it moves to its point of use in Phase 4 Step 3 (Verify Fix). Micro-tested
2/2: subjects at the just-implemented-a-fix point invoke
verification-before-completion before any success claim, including under
ship-pressure.

* refactor(skills): stop offering to discard work in finishing-a-development-branch

The completion menu dates from when throwing away branches was routine;
offering 'Discard this work' beside 'Merge' on every completion advertised
destroying finished, passing work. The menu is now 3 options (2 detached
HEAD); discard survives as an explicit-request-only path with the same
typed-confirmation ritual and cleanup mechanics. Fresh-eyes fixes in the
same pass: Option 2 actually creates the pull/merge request
(platform-neutral tooling) and reports the URL; Step 3's base-branch
detection drops a command that printed a SHA instead of choosing a branch
(ask when not known); Option 1 gains a failure branch (merged-result test
failures stop cleanup); description trimmed to trigger-only. Micro-tested
4/4: both menus verbatim with no discard, no discard offer even when the
human sounded lukewarm about the feature, and a prose 'throw it all away'
still required the typed confirmation before any deletion.

* refactor(skills): make PR creation forge-agnostic in finishing-a-development-branch

Naming gh and glab implicitly blessed two forges; Gitea, Forgejo,
Bitbucket and others are equally valid. Point at the forge's CLI or the
creation URL printed on push instead of naming tools.

* refactor(skills): compress finishing-a-development-branch, adopt rationalization table

Red Flags and Common Mistakes fold into one Common Rationalizations table
(house Excuse/Reality form); every prior entry maps to a table row or an
inline sentence in the step it guards. Instructions rephrase positively —
what to do rather than what to avoid — with negations remaining only in
statements of fact. Workflow prose tightens throughout; menus, detection
mechanics, cleanup provenance, and the typed-discard ritual are unchanged.
Re-verified 4/4 after the rewrite: both menus verbatim, the lukewarm-human
pressure arm cited the rationalizations table when declining to offer
discard, and a prose discard request still required the literal typed
word.

* fix(skills): capture worktree path before Step 5 changes directory

Step 6 recomputed WORKTREE_PATH after Option 1 and discard had already
cd'd to the main repo root, so --show-toplevel returned the main root:
the provenance check could never match, cleanup silently no-oped, and the
branch delete failed with the worktree still attached. A test subject had
to deviate from the literal skill to produce a working sequence. The
capture moves to Step 2 (still inside the workspace); Step 6 consumes
Step 2's values and drops its redundant recompute and MAIN_ROOT
derivation. Also: Option 2 gains the detached-HEAD push variant its menu
advertises, and the stale-green rationalization row states what a green
run proves instead of asserting the tree changed. Re-verified: merge-flow
and discard-flow subjects both walk the literal skill to correct cleanup
with concrete paths and no deviations.

* refactor(skills): reframe testing-anti-patterns as writing-good-tests

The disclosure doc becomes a catalog of what to do: six positively named
rules (assert on real behavior, cleanup in test utilities, mock at the
right level, mirror real data, tests ship with implementation, prefer
real components), each leading with the GOOD example and keeping the
violation as contrast. Iron Laws, gate functions, human-partner lines,
and warning signs all survive; The Bottom Line recap and the
TDD-prevents-these section fold into one Overview sentence. SKILL.md's
pointer moves into the Good Tests section it belongs with. Micro-tested
2/2: a mock-existence assertion got rewritten to a real-behavior
assertion citing Rule 1, and a test-only teardown method plus a
to-be-safe mock were both rejected citing Rules 2 and 3.

* fix(skills): broaden writing-good-tests trigger to any test writing

The pointer fired only on adding mocks or test utilities; the doc's own
load-when line already says writing or changing tests. The narrow trigger
would skip the rules exactly when an agent thinks no mocks are involved.

* feat(skills): absorb falsifiability discipline into writing-good-tests

Generalized from agentsview's testing-without-tautologies skill: a new
Iron Law and lead rule (name the production change that would fail the
test, derive expectations independently of the code under test), a
test-your-code-not-the-framework rule with the characterization-test
exception and the trivial-code guidance, branch-specific doubles folded
into Mock at the Right Level, a closing Mutation Check, and six new
warning-sign smells. Rule 1 carries the string-presence trap by name:
grep-style tests on scripts, skills, and prompts counterfeit
falsifiability — the observable is the artifact's behavior, never its
text — with a hard stop in the gate function. Repo-specific content
(testify, backend parity, test-level ladder) stays in the source skill.
Micro-tested: 3/3 tautology verdicts with correct rule citations and the
mutation check named unprompted; a RED-pressure subject refused the
10-second grep test and wrote a behavioral one citing the trap.

* fix(skills): close the change-detector hole in writing-good-tests

Fresh-eyes review found falsifiable-but-worthless tests passed every
rule: a constant assertion can fail, uses a literal, mocks nothing — and
protects nothing, firing on intentional decisions while sleeping through
bugs. Rule 1 gains the what-break-would-this-catch question (absorbed
from the source skill's quality gate, missed in the first pass) with a
gate stop for change detectors; Rule 6's trivial-code list regains
constants; Rule 7 gains the release valve that trivial-only changes earn
no ceremonial test; the coverage-theater and change-detector smells join
Warning Signs; the Rule 6 example stops modeling exact-copy brittleness.
Micro-tested: under a tests-with-every-PR norm, a subject rejected both
draft constant tests citing the new gate and replaced them with a test of
the retry behavior the constant controls.

* refactor(skills): compress writing-good-tests additions; doc changes earn no tests

Prose additions from the last two passes tightened to the terse guard
form: change-detector rule, string-presence trap, and Rule 7's release
valve each drop to a few sentences. Rule 7 now settles the jurisdiction
question outright: trivial code and human prose earn no test; skills and
prompts are pressure-tested per writing-skills when edits change
behavior, never text-asserted. Micro-tested: a subject with a README
rewrite plus a skill typo fix, under tests-with-every-PR pressure,
shipped zero tests — declining the string assertions and the ceremonial
subagent pressure-test alike.

* experiment: ground-up two-principle rewrite of writing-good-tests

Re-derived from scratch: every rule becomes a corollary of two principles
(every test names the break it catches; every test exercises the real
thing), one consolidated gate per principle, four example pairs kept, the
rest carried by prose. Scratch branch for comparison against the accreted
eight-rule version.

* refactor(skills): drop social proof from dispatching-parallel-agents

Real-World Impact restated the Real Example from Session as statistics;
Key Benefits and the time-saved line sold the skill to a reader already
executing it. Instructions unchanged.

* refactor(skills): drop social proof from systematic-debugging

Real-World Impact was statistics; the Overview opener restated the core
principle as motivation. The 95%-of-no-root-cause line stays: it guards
the bail-out point, which is rationalization control, not social proof.
Supporting Techniques/Related skills untouched (PR #1932 owns that).

* refactor(skills): drop persuasion sections from verification-before-completion

Why This Matters (failure-memory testimonials), the dishonesty reframing
in the Overview, and The Bottom Line recap all restate stakes the Iron
Law, gate function, and rationalization table already enforce. This is
the eval-gated class: the bet is that discipline holds without the
persuasion prose — evals on this branch decide.

* refactor(skills): trim quality claim from executing-plans subagent note

The tell-your-partner directive and the prefer-SDD instruction stay; the
significantly-higher-quality sentence restated them as a claim.
Integration section untouched (PR #1932 owns it).

* refactor(skills): drop Advantages section from subagent-driven-development

Five blocks of benefits and cost/benefit selling aimed at a reader who
has already invoked the skill; the vs-Executing-Plans comparison also
duplicates the one under When to Use. Integration section untouched
(PR #1932 owns it).

* refactor(skills): trim requesting-code-review, keep review guards as a table

Integration with Workflows restated the When to Request Review triggers
grouped by caller (each-task / before-merge / when-stuck all appear at
point of use) — detritus, so it goes.

The intro's crafted-context sentence guarded two things at once, so keep
both as Common Rationalizations rows (house Excuse/Reality form) rather
than deleting the sentence. The skill's reader is the coordinator, not
the code's author:

- Don't review the diff inline — that burns the coordinator's context
  window; dispatch a subagent so the diff and evaluation live in its
  context and only findings return. ("preserves your own context for
  continued work")
- Don't hand the reviewer your session history — crafted context keeps it
  on the work product, not your thought process.

* refactor(skills): convert using-git-worktrees guard sections to rationalization table

Common Mistakes and Red Flags restated Steps 0-3 wholesale; both fold
into one Common Rationalizations table (house Excuse/Reality form) whose
five rows carry the tempting-thought version of each rule, including the
#1-mistake emphasis on bypassing native tools. Quick Reference stays as
the compact decision aid.

* refactor(skills): fold brainstorming Key Principles into points of use

Five of six principles restated the Checklist and Process sections
verbatim-in-spirit. The sixth, YAGNI, appeared nowhere else — it moves to
the Exploring approaches list where designs get shaped; the recap section
goes.

* refactor(skills): drop Remember recap from writing-plans

All four lines restate the Overview (DRY/YAGNI/TDD/frequent commits),
Task Structure (exact paths, commands with expected output), and No
Placeholders (complete code in every step).

* refactor(skills): drop The Bottom Line recap from writing-skills

Restates the Iron Law, the RED-GREEN-REFACTOR mapping, and the
TDD-for-docs framing, all stated in full earlier in the file.

* refactor(skills): drop The Bottom Line recap from receiving-code-review

Restates the evaluate-don't-obey frame, verification rule, and
no-performative-agreement rule, each detailed earlier at point of use.
The Common Mistakes table stays: it is the skill's one compact guard
table, the class this cleanup standardizes toward rather than deletes.

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
prefilled new-issue link. The link uses a new diagnosis_report.m…
- [XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) [1](https://github.com/XiaomiMiMo/MiMo-Code/commits): fix(session): close disposed event streams and stop unauthorized retries (#2540)

## [automation](https://github.com/topics/automation)
- [xlwings/xlwings](https://github.com/xlwings/xlwings) [18](https://github.com/xlwings/xlwings/commits): Merge pull request #2771 from xlwings/feat/custom-function-client-cache

Add client cache flag to Office.js function decorator
- [fastlane/fastlane](https://github.com/fastlane/fastlane) [3](https://github.com/fastlane/fastlane/commits): Render the team table from one ERB template (#30266)

The Rakefile and the docs generator each built the table by hand and had drifted apart (td ids, avatar size); both dropped the last </tr> when the member count was not a multiple of 5. Both now render fastlane/lib/assets/TeamTable.md.erb, and README marks the generated region with team:start/team:end.
- [openai/tart](https://github.com/openai/tart) [1](https://github.com/openai/tart/commits): Fix listing VMs when disk capacity is unavailable (#1349)

* Allow HumanReadableByteCount to represent an unknown byte count

Some byte counts, such as the capacity of an ASIF disk image, can't
always be determined. Accept an optional byte count and render an
unknown value as "-" in text output and as null in JSON output.

* Fix listing and getting VMs when disk capacity is unavailable

For ASIF disk images, the disk capacity is read with "diskutil image
info". The command fails with "Resource temporarily unavailable" while
a running VM holds the disk image open. As a result, "tart list" and
"tart get" fail entirely when any such VM exists.

Treat the disk capacity as unknown when it can't be determined, so
that both commands still show the remaining information.

Fixes #1344

* Remove unused VMDirectory.diskSizeGB()

The method was added together with diskSizeBytes() but has never been
used. "tart list" and "tart get" use diskSizeBytes() directly.
- [yaqwsx/KiKit](https://github.com/yaqwsx/KiKit) [1](https://github.com/yaqwsx/KiKit/commits): Work around KiCad SWIG iterator incompatibility

## [esp32](https://github.com/topics/esp32)
- [esphome/esphome](https://github.com/esphome/esphome) [100](https://github.com/esphome/esphome/commits): [emontx] Use register_apply_action for emontx.send_command (#19687)
- [crosspoint-reader/crosspoint-reader](https://github.com/crosspoint-reader/crosspoint-reader) [6](https://github.com/crosspoint-reader/crosspoint-reader/commits): fix: release SD-font caches on reader exit (#3699)

## Summary

Returning Home after reading with an SD font leaves rebuildable font
caches owned by the global font system. Those allocations can split
large free heap regions after the reader's temporary buffers have been
freed.

Release those caches from `ReaderActivity::onExit()`, preserving loaded
font metadata and glyph-miss callbacks so the font data can be rebuilt
when needed. The final diff contains only this reader-exit change;
`SdCardFont.cpp` matches the baseline. The existing 40 KiB mini-cache
retention policy between pages remains in place, and the change adds no
heap allocations.

## Scope Check

- [x] Read SCOPE.md and ROADMAP.md; this addresses the Phase 1
heap-fragmentation focus.
- [x] Changes are limited to existing reader/font-cache behavior; no new
theme, connector, app, media or PDF feature.
- Stock/fork feature comparison: not applicable to this fix for
CrossPoint's existing cache lifetime.
- SDK/HAL/bootloader/OTA/recovery coordination: not applicable; those
paths are untouched.

## Additional Context

Compared with `origin/develop` at `0f01106a` on an Xteink X3 using
`default` / LOG_LEVEL=2 builds with identical serial-control
instrumentation and SDK. Three interleaved cold baseline/candidate pairs
used `/CP-Test/scheduling-demian.epub`, Pretendard 16 pt, anti-aliasing
enabled, and **hyphenation ON**, starting at spine 4 page 1. Each boot
had six warmup and six measured turns, then post-page and Home heap
samples after 13-second waits, followed by reopening the book. These are
18 measured turns per build.

**Known cost:** median total page rendering increased from 1,507.5 to
1,514.5 ms, **+7 ms (+0.46%)**. Per-pair median increases were **+3.5 /
+11.5 / +8 ms**. This remains an unexplained cost; timing parity is not
established. No extra kerning/ligature-table reloads were observed
during reading: both builds logged zero full-table reloads during warmup
and measured turns, with matching mini-matrix rebuild and advance-table
fetch logs. The captures do not provide a complete SD-read timing
breakdown.

| Median measurement | Baseline | Candidate | Difference |
|---|---:|---:|---:|
| Free heap on Home | 82,680 B | 110,536 B | +27,856 B (+27.9 KB) |
| Largest free block on Home | 36,852 B | 94,196 B | +57,344 B (+57.3
KB) |
| Largest free block after page turns | 53,236 B | 59,380 B | +6,144 B |
| Free heap after page turns | 68,464 B | 68,468 B | +4 B |
| Since-boot Min Free at post-page sample | 20,276 B | 20,288 B | +12 B
|
| Drawing including grayscale | 358 ms | 361 ms | +3 ms |
| Total page render | 1,507.5 ms | 1,514.5 ms | +7 ms |
| Cold preparation including first render | 4,398 ms | 4,408 ms | +10 ms
|
| First render after reopening | 4,019 ms | 4,033 ms | +14 ms |
| Static RAM | 58,064 B | 58,064 B | unchanged |
| Flash | 5,610,791 B | 5,610,803 B | +12 B |

Releasing the resident caches allows adjacent free heap regions to
coalesce. The recovery includes mini buffers and persistent advance
caches as well as full kerning/ligature tables. The observed post-page
largest-block gain does not establish that during-reading kerning-table
pinning is fixed. Advance-table allocation/merge code is outside this
diff.

Hyphenation was OFF in the earlier comparison and ON in this round,
following the current reader setting. Both builds used the same settings
within this round, but the changed setting prevents a clean causal
comparison with the earlier timing result. Cold-preparation differences
also varied by pair (+14 / -9 / +1 ms). Both builds reloaded tables on
reopening because resuming a section build already releases caches, so
the full reopen difference cannot be attributed to newly required table
reads.

Validation:

- `pio run -e default` passed for the revised candidate; reused the
unchanged baseline build. Formatting and `git diff --check` passed, as
did all 12 existing SdCardFont / FontCacheManager host tests.
- All nine paired page-content captures were pixel-identical. Seven full
frames were identical; two differed only in the footer.
- Zero advance-cache bitmap retries across all six boots. No errors,
power transitions, crashes or unexpected resets during measured turns.
- Both builds logged one thumbnail-cache error per boot during
deliberate cache deletion and one CSS low-heap warning per boot outside
measured turns.
- One read-only STATE timeout before the third candidate boot's first
warmup recovered without input replay, reconnect or reset. All six
warmups and six measured turns then completed; no paired boot was
discarded.

The 150-turn heaptrace workload has not been repeated with this
revision, so the longer-run bitmap retries remain unverified. Test code,
instrumentation and local evidence are excluded from the PR.

### AI Usage

YES — AI tools assisted with implementation, analysis, device testing,
and this description.
- [shorepine/tulipcc](https://github.com/shorepine/tulipcc) [6](https://github.com/shorepine/tulipcc/commits): Merge pull request #1377 from shorepine/tulip2-web-rewrite

tulip.computer/2: point the rewrites at tulip2-web.vercel.app
- [s60sc/ESP32-CAM_MJPEG2SD](https://github.com/s60sc/ESP32-CAM_MJPEG2SD) [5](https://github.com/s60sc/ESP32-CAM_MJPEG2SD/commits): v10.9.7
- [espressif/arduino-esp32](https://github.com/espressif/arduino-esp32) [4](https://github.com/espressif/arduino-esp32/commits): boards(waveshare): Change C5 Zero LED color order to GRB (#12941)
- [arendst/Tasmota](https://github.com/arendst/Tasmota) [2](https://github.com/arendst/Tasmota/commits): Improve tooltip on touch devices and provide BSSID to Berry (#25057)

* Improve tooltip on touch devices and provide SSID to Berry

* Improve rendering of battery symbol
- [espressif/idf-extra-components](https://github.com/espressif/idf-extra-components) [2](https://github.com/espressif/idf-extra-components/commits): Merge pull request #854 from espressif/fix/update_c2_partition_table

ci: update C2 app partition size to fix the build warning
- [goat-hill/bitclock](https://github.com/goat-hill/bitclock) [2](https://github.com/goat-hill/bitclock/commits): Disable Bitclock sales

Show all three products grayed out as "Out of stock" with no Stripe
checkout on the order page, and reject new checkout sessions in the API.

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

## [github](https://github.com/topics/github)
- [dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact) [3](https://github.com/dawidd6/action-download-artifact/commits): workflows: update
- [Kuingsmile/PicList](https://github.com/Kuingsmile/PicList) [1](https://github.com/Kuingsmile/PicList/commits): :sparkles: Feature(ssh): optimize sshclient implemention

## [keyboard](https://github.com/topics/keyboard)
- [tompi/cheapino](https://github.com/tompi/cheapino) [3](https://github.com/tompi/cheapino/commits): Merge pull request #173 from bdeboer-x/encoder-gamepad-tip

Add tip: spare half as gaming pad with EC11 encoder
- [pqrs-org/Karabiner-Elements](https://github.com/pqrs-org/Karabiner-Elements) [1](https://github.com/pqrs-org/Karabiner-Elements/commits): Update vendor

## [lists](https://github.com/topics/lists), [resources](https://github.com/topics/resources)
- [public-apis/public-apis](https://github.com/public-apis/public-apis) [11](https://github.com/public-apis/public-apis/commits): Merge pull request #7462 from deepshekhardas/add-google-pagespeed-insights-api

feat: add Google PageSpeed Insights API
- [bkrem/awesome-solidity](https://github.com/bkrem/awesome-solidity) [2](https://github.com/bkrem/awesome-solidity/commits): docs: add alloy-rs/core to developer tools (#212)

## [llm](https://github.com/topics/llm)
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) [21](https://github.com/OpenHands/OpenHands/commits): fix: detect Dockerfile language from directory-qualified paths (#17152)

Signed-off-by: jabrailkhalil <jabrailkhalil@gmail.com>
- [gptme/gptme](https://github.com/gptme/gptme) [7](https://github.com/gptme/gptme/commits): test(hooks): unregister server_confirm in test_register to stop TOOL_CONFIRM leak (#3962)

test_register left the priority-100 server_confirm hook registered. On the
same xdist worker, a later test_mcp_confirm_hooks_run_once then had that hook
answer TOOL_CONFIRM before its priority-50 counting hook ran, so master Test
failed with 'TOOL_CONFIRM must fire once, got []'.

Reproduced by replaying gw12's 351-test sequence from run 36128612797
(1 failed); bisected to this test; the same sequence passes with the fix.

Git-Session-Id: 960f
- [jjang-ai/vmlx](https://github.com/jjang-ai/vmlx) [5](https://github.com/jjang-ai/vmlx/commits): Publish vMLX 1.6.67 updater manifest

## [machine-learning](https://github.com/topics/machine-learning)
- [polakowo/vectorbt](https://github.com/polakowo/vectorbt) [7](https://github.com/polakowo/vectorbt/commits): fix(generic): avoid out-of-bounds reads on empty input

expanding_min_1d_nb, expanding_max_1d_nb and get_drawdowns_nb read a[0]
before checking the length. Start from NaN instead, which the loops already
treat as "no value yet". Caught by running the tests with NUMBA_DISABLE_JIT=1.
- [skypilot-org/skypilot](https://github.com/skypilot-org/skypilot) [3](https://github.com/skypilot-org/skypilot/commits): [Jobs] Managed job dependencies (#10876)

* [Jobs] Managed job dependencies

sky.jobs.launch(depends_on=[...]) makes a managed job wait for other
managed jobs: a controller claims it only once all of them are DONE, and
it runs only if all of them succeeded; otherwise its tasks are
cancelled with the reason. Dependencies are recorded in a new
job_dependencies table and require consolidation mode.

* [Jobs] sky jobs launch --depends-on; reject depends_on without consolidation mode

The CLI takes comma-separated managed job IDs and passes them as
depends_on. The /jobs/launch route answers 400 when depends_on is set
and the server does not run managed jobs in consolidation mode.

* [Docs] Regenerate the CLI reference for --depends-on

* [Jobs] Show which dependencies a waiting job is waiting for

A WAITING job whose dependencies are not all DONE shows 'Waiting for
dependency jobs 17, 18 to succeed' in details. Such a job no longer counts
toward the highest blocking priority, and its eligible_at is written when
its last dependency ended rather than at submission, so it is not reported
as never claimed while it waits.

* [Jobs][Dashboard] Show a job's dependencies on its detail page

The managed jobs queue returns depends_on (the job IDs a job waits for,
None without any), computed from job_dependencies. The job detail page
shows them as links under 'Depends On' when there are any.

* [Jobs] Shorten the waiting-on-dependencies details to 'Dependency: 17'

* [Jobs] depends_on: forward it from the async SDK; document the launch failure

The async jobs launch takes depends_on and passes it to the SDK. The CLI
help and docstrings say that the launch fails when a dependency has
already ended without succeeding.

* [Test] Add a smoke test for sky jobs launch --depends-on

* [Test] Use fresh job records for the second queue call in test_depends_on_field

* [Test] Capture job IDs with debug logging off in the depends_on smoke test
- [Developer-Y/cs-video-courses](https://github.com/Developer-Y/cs-video-courses) [2](https://github.com/Developer-Y/cs-video-courses/commits): Add MIT 6.566 (SP26) (#526)

## [markdown](https://github.com/topics/markdown)
- [sudoskys/telegramify-markdown](https://github.com/sudoskys/telegramify-markdown) [5](https://github.com/sudoskys/telegramify-markdown/commits): chore: release 1.4.0 (#128)
- [RivoLink/leaf](https://github.com/RivoLink/leaf) [4](https://github.com/RivoLink/leaf/commits): Merge pull request #302 from RivoLink/chore/warn-unsigned-commit

chore: warn unsigned commit
- [foambubble/foam](https://github.com/foambubble/foam) [1](https://github.com/foambubble/foam/commits): Wait for notes to be indexed before renaming in refactor.spec (#1710)

## [middleware](https://github.com/topics/middleware)
- [thingsboard/thingsboard](https://github.com/thingsboard/thingsboard) [35](https://github.com/thingsboard/thingsboard/commits): Merge pull request #16203 from thingsboard/rc

Merge rc into master
- [gin-gonic/gin](https://github.com/gin-gonic/gin) [1](https://github.com/gin-gonic/gin/commits): fix(context): load Keys under the mutex in Copy (#4854)

Copy read c.Keys before RLock. Set stores that field under Lock when the
map is created. The race detector reports the unsynchronized access, and
the copy can observe a nil header and drop keys Set has already published.

maps.Clone(nil) returns nil, so the load and the clone belong in the same
critical section. Map iteration was already under the mutex.

Co-authored-by: hazyhaar <hazyhaarlabs@gmail.com>

## [python](https://github.com/topics/python)
- [adafruit/circuitpython](https://github.com/adafruit/circuitpython) [20](https://github.com/adafruit/circuitpython/commits): Merge pull request #11466 from weblate/weblate-circuitpython-main

Translations update from Hosted Weblate
- [arnegiacomo/fugleramme](https://github.com/arnegiacomo/fugleramme) [8](https://github.com/arnegiacomo/fugleramme/commits): chore(assets): #33 add Canyon Wren and Spotted Towhee (#157)
- [kurigram-org/kurigram](https://github.com/kurigram-org/kurigram) [8](https://github.com/kurigram-org/kurigram/commits): ci(workflow): run on `push` to `main` only, so a pull request branch is tested once (#519)
- [dbcli/mycli](https://github.com/dbcli/mycli) [4](https://github.com/dbcli/mycli/commits): Merge pull request #2271 from dbcli/RW/boundary-immediate-exit

Don't wait for Boundary tunnel teardown on quit
- [norvig/pytudes](https://github.com/norvig/pytudes) [3](https://github.com/norvig/pytudes/commits): Delete py/TruncatablePrimes.ipynb
- [RhetTbull/osxphotos](https://github.com/RhetTbull/osxphotos) [2](https://github.com/RhetTbull/osxphotos/commits): Warn and continue instead of aborting on an unrecognized sidecar (#2228) (#2232)

* Warn and continue instead of aborting on an unrecognized sidecar

PhotoInfoFromFile.__init__ called metadata_from_sidecar() without catching
ValueError, so an unrecognized or unreadable sidecar raised
'Unknown sidecar type' and aborted the whole import. This path is hit when
rendering --album/--title/--description/--keyword templates, reading
--favorite-rating, and stripping edited suffixes, none of which were guarded
(only set_photo_metadata_from_sidecar caught the error).

Catch ValueError at this single chokepoint, log a warning, and continue with
whatever metadata was already gathered, so a bad sidecar no longer stops the
import batch.

Adds tests covering unknown-type and malformed JSON sidecars.

Refs #2228

Signed-off-by: mishra-prince <88850888+mishra-prince@users.noreply.github.com>

* Catch IndexError and ValueError in sidecar processing

Handle both IndexError and ValueError when processing sidecar files to avoid aborting the import batch.

Co-authored-by: Copilot Autofix powered by AI <175728472+Copilot@users.noreply.github.com>

* Handle empty-list sidecar and make sidecar tests platform-independent (#2228)

Address review feedback on PR #2232:
- get_sidecar_filetype: return Unknown for an empty JSON list instead of
  raising IndexError on metadata[0]; add regression test.
- test_photoinfo_file: force EXIFTOOL_PATH=None so tests do not read real
  image metadata on machines with exiftool installed (platform-independent).

* Assert warning is logged for unreadable sidecars in PhotoInfoFromFile tests

Claude-Session: https://claude.ai/code/session_011aFqXqQnq1czhCgEgr3KRa

---------

Signed-off-by: mishra-prince <88850888+mishra-prince@users.noreply.github.com>
Co-authored-by: Rhet Turnbull <rturnbull@gmail.com>
Co-authored-by: Copilot Autofix powered by AI <175728472+Copilot@users.noreply.github.com>
Co-authored-by: mishra-prince <mishra-prince@users.noreply.github.com>
- [binance/binance-connector-python](https://github.com/binance/binance-connector-python) [1](https://github.com/binance/binance-connector-python/commits): Release derivatives_trading_portfolio_margin v13.1.1

### Changed (3)

#### REST API

- Modified response for `account_balance()` (`GET /papi/v1/balance`):
  - oneOf modified

- Modified response schema `accountBalanceResponse`:
  - oneOf modified
- [confident-ai/deepeval](https://github.com/confident-ai/deepeval) [1](https://github.com/confident-ai/deepeval/commits): Batch JEV
- [pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) [1](https://github.com/pymupdf/PyMuPDF/commits): Update pixmap.rst

Fix documentation error:
The Pixmap methods `pil_save()` and `pil_tobytes()` do not support "unmultiply" functionality.
- [vacanza/holidays](https://github.com/vacanza/holidays) [1](https://github.com/vacanza/holidays/commits): Update Australia holidays: add Labour Day start years (ACT, QLD) (#3832)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
- [vinta/awesome-python](https://github.com/vinta/awesome-python) [1](https://github.com/vinta/awesome-python/commits): Add jev-ultrafast

Maintainer override: repo is under 1 month old (created 2026-09-16) and not on PyPI.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## [queue](https://github.com/topics/queue)
- [apple/swift-collections](https://github.com/apple/swift-collections) [15](https://github.com/apple/swift-collections/commits): Merge pull request #740 from lorentey/release-prep

Version 1.7.1 release preparations
- [bloomberg/blazingmq](https://github.com/bloomberg/blazingmq) [4](https://github.com/bloomberg/blazingmq/commits): Refactor[mqbnet]: remove usage of atomic gate (#1790)

## [rust](https://github.com/topics/rust)
- [BerriAI/litellm](https://github.com/BerriAI/litellm) [15](https://github.com/BerriAI/litellm/commits): test: move tests/test_litellm core utils, routing, responses, caching and rust_bridge into tests/unit (#43199)

* ci: run the unit_selection.sh shard files on every event instead of only fork pull requests

Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>

* ci: rename fork-flag to unit-flag now that it applies on every event

* test: move tests/test_litellm root and small trees into tests/unit

Pure renames, no content changes. Follow-up commits in this PR fix
references, merge the three files that already existed in tests/unit,
keep live-provider tests in tests/test_litellm and wire CI.

* test: carry tests/test_litellm conftest isolation into tests/unit

Callback lists, routing fallbacks, cached HTTP clients, logger state, AWS,
proxy-URL and keychain env, and session-end client cleanup now reset for
unit tests too. The environment isolation owns its MonkeyPatch so a test's
own monkeypatch is undone before the model-cost teardown runs.

* test: merge, split and prune the moved root and small-tree tests

Merge batches/test_batch_utils.py and the chat_completions and messages
dispatch tests into the files that already existed in tests/unit. Keep
the live Gemini interactions tests, the async image-fetch format test and
the OpenAI embedding scorer test in tests/test_litellm since they need
real network or keys. Put test_router.py under tests/unit/test_router so
the existing package no longer shadows it. Delete eight tests the audit
found superseded by stronger ones kept in this move.

* ci: run the moved root and small-tree tests under their legacy flags

Add the misc and responses-caching-types flags to unit_selection.sh and
CircleCI, extend enterprise-routing and mcp-integration, and point the
legacy GHA shards, Makefile, redis-compat workflow, merge smoke manifest
and change classifier at the new paths.

* test: make the new tests/unit directories packages

tests/unit/test_package_layout.py requires every directory to carry an
__init__.py, and without one the moved and retained
test_litellm_responses_bridge.py modules collide on import.

* test: scope the unit socket block to tests/unit in shared sessions

The GHA shards collect the legacy test-path and the unit selection in one
pytest session. The unit conftest's loopback-only block leaked into legacy
modules that reach the network at import. The legacy conftest now lifts the
restriction at collect and setup time, and the unit conftest re-applies it
when collecting its own modules.

* test: move tests/test_litellm/llms into tests/unit/llms

Rename-only. Moves the provider tests and the fine-tuning fixtures they
load, mirroring the old paths. Follow-up commits merge, split and wire them.

* test: merge, split and prune the moved llms tests

Merges the Databricks chat transformation tests into the existing unit
file, keeps the tests that need real keys or the network in
tests/test_litellm, deletes the audited tests a stronger unit test
already covers, and points imports at tests.unit.llms.

* ci: run the moved llms tests under their legacy flags

The Vertex AI and All Other Providers shards keep their legacy test-path
for the retained files and add the llm-vertex-ai and llm-other-providers
unit selections. CircleCI gets matching unit jobs.

* test: make the tests/unit/llms directories packages

Adds __init__.py to the moved dirs and drops the legacy ones whose
directories no longer hold tests.

* test: drop script runners and path hacks the llms split left dangling

The __main__ runners in the split openai_like files and the Databricks e2e
runner called tests that now live in the other half of the split or were
deleted. The retained legacy halves also no longer need sys.path edits.

* test: give the shard-script tests their own GITHUB_OUTPUT

They only passed where the runner set it. The CircleCI unit job's env
allowlist drops it, so the script's redirect failed there.

* test: point the router and module-deletion checks at tests/unit

router_code_coverage and code_qa_check_tests only searched tests/test_litellm,
so the moved router tests no longer counted. The two silent-experiment tests
the audit deleted were the only direct callers of those methods; they are
replaced with tests that assert the forwarded shadow request and the
recursion guard.

* test: move tests/test_litellm integrations and secret_managers into tests/unit

Rename-only. Mirrors the old paths, including the directory conftests
and the prompt and JSON fixtures. Follow-up commits prune and wire them.

* test: prune and repoint the moved integrations tests

Deletes the 7 audited tests a stronger test in the same tree already
covers, imports the TLS sink helpers from their new conftest path, and
restores os.environ after each integrations test. Some presets write
OTEL_EXPORTER_OTLP_HEADERS straight into os.environ, and without the
legacy tree's test ordering that header leaked into the AgentOps tests.

* ci: run the moved integrations tests under their legacy flag

The integrations GHA shard and a new CircleCI job run the integrations
unit selection. secret_managers joins the misc selection.

* docs: point integrations and secret_managers references at tests/unit

* test: make the moved integrations directories packages

* test: keep the Databricks manual e2e runner and fix the SageMaker Nova run path

The Databricks e2e file is a manual script whose main() calls the tests
that were pruned, so pruning them broke the documented run. It is back to
its main version. The SageMaker Nova docstring now points at the file's
real location in tests/local_testing.

* test: move tests/test_litellm core utils, routing, responses, caching and rust_bridge into tests/unit

Rename-only. Mirrors the old paths, including fixtures, the stubtest config
and the native-route wheel script. Two files that collide with existing unit
files are merged in a follow-up commit.

* test: merge, prune and repoint the moved core, routing, responses, caching and rust_bridge tests

Merges the two files that collided with existing unit files, folding the
legacy extra case into test_is_chat_completion_cached_dict, and deletes the
9 audited tests a stronger test in the same file already covers.

Keeps what needs the network in tests/test_litellm: test_tokenizers pulls a
tokenizer from the Hugging Face hub, and the gpt2 and r50k_base tokenizer
cases download their BPE files. The unit core_utils conftest points
TIKTOKEN_CACHE_DIR at litellm's bundled encodings so the rest never depend on
import order to stay offline, and FakeSecretVault moves to a shared module
so both trees can build it.

* ci: run the moved core, routing, responses, caching and rust_bridge tests under their flags

core_utils gets a core-utils flag and CircleCI job, and its GHA shard keeps
the legacy path for the retained network tests. router_utils and
router_strategy join enterprise-routing, responses joins
responses-caching-types (minus responses/mcp, which mcp-integration owns),
caching joins caching-local and rust_bridge joins misc. The redis-compat,
test-rust, stubtest and merge-smoke paths follow the move.

* docs: point the Rust crate references at tests/unit

* test: make the moved core, routing and rust_bridge directories packages

* test: keep the no-loop DualCache batch_get_cache regression test

It runs the sync path outside any event loop, which the inside-loop test
cannot, so a change that picks the Redis client by loop state would only
show up there.

* test: keep the job's UNIT_FLAG out of the shard-script tests

* fix(url_utils): block 192.0.0.0/24 on every Python patch release

* test: move the new budget limiter tests into tests/unit/router_strategy

* test: move the new sentry scrubbing tests into tests/unit/litellm_core_utils

* test: move the new zerobus tests into tests/unit/integrations

* test: make tests/unit/integrations/zerobus a package

* test: load litellm's own tiktoken cache setup once instead of resetting it per test

---------

Co-authored-by: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>
- [embassy-rs/embassy](https://github.com/embassy-rs/embassy) [13](https://github.com/embassy-rs/embassy/commits): Merge pull request #7104 from xoviat/ci

ci: bump docserver version
- [valeriansaliou/sonic](https://github.com/valeriansaliou/sonic) [13](https://github.com/valeriansaliou/sonic/commits): v1.10.1
- [dora-rs/dora](https://github.com/dora-rs/dora) [12](https://github.com/dora-rs/dora/commits): fix(daemon): keep answering the zenoh link probe when the endpoint exchange is off or slow (#3611)

* fix(daemon): keep answering the zenoh link probe when the endpoint exchange is off or slow

Since #3533 a consumer daemon reads a peer's silence on the node-endpoint
query as a missing zenoh link, and after 30 s it logs an error that the
dataflow can never finish. A peer stayed silent in two cases even though
the link was up:
- it ran with `DORA_ZENOH_ENDPOINT_EXCHANGE_TIMEOUT_MS=0`, which skipped
  the declare;
- its declare missed the exchange budget and was dropped.

Declare the queryable on its own task that holds it until the handle is
dropped:
- The off switch now declares one that answers with no endpoints, so no
  peer dials this daemon's nodes directly, but the link probe still gets
  a reply.
- A declare that misses the budget keeps going in the background instead
  of being abandoned.

The link probe also no longer uses the spawn budget as its per-round
collection time. It uses at least the default 1.5 s, so lowering the
env var to speed up spawn cannot produce probe rounds shorter than a
WAN round trip.

Fixes #3603

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DkULGfqTuXWvCMAFvt2d8q

* test(daemon): cover the declare-past-budget path, make the probe-round test meaningful

Review findings on the #3603 fix:

- `the_link_probe_round_is_never_shorter_than_the_default` asserted
  `timeout().max(DEFAULT_TIMEOUT) >= DEFAULT_TIMEOUT`, which always holds.
  `link_probe_round` now takes the exchange budget, and the test checks
  that a short budget gives `DEFAULT_TIMEOUT` and a long one is kept.
- The declare-timeout path had no test. The holding task is split out as
  `spawn_holding`, so a test can hold the declare back past a budget and
  check that the queryable still answers once its waiter gave up, and
  stops answering once the handle is dropped. The test fails if the task
  abandons the declare when nobody waits for it any more.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DkULGfqTuXWvCMAFvt2d8q

---------

Co-authored-by: Claude <noreply@anthropic.com>
- [acsandmann/rift](https://github.com/acsandmann/rift) [10](https://github.com/acsandmann/rift/commits): feat: per display overrides for scrolling layout geometry (#505)
- [PolyMeilex/Neothesia](https://github.com/PolyMeilex/Neothesia) [9](https://github.com/PolyMeilex/Neothesia/commits): feat(nuon): Vertical text alignment
- [crate-ci/typos](https://github.com/crate-ci/typos) [6](https://github.com/crate-ci/typos/commits): chore: Release
- [retsimx/tlsr8266_mesh](https://github.com/retsimx/tlsr8266_mesh) [6](https://github.com/retsimx/tlsr8266_mesh/commits): Merge pull request #17 from retsimx/fix/mesh-status-surgical

fix(mesh-status): stop offline flapping for relayed mesh nodes
- [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) [1](https://github.com/ast-grep/ast-grep/commits): fix(schema): reject null relation fields (#2969)
- [denoland/rusty_v8](https://github.com/denoland/rusty_v8) [1](https://github.com/denoland/rusty_v8/commits): chore: bump bytes to 1.11.1

* bytes 1.10.1 -> 1.11.1 - fixes an integer overflow in
  BytesMut::reserve's unique-reclaim path: an unchecked
  new_cap + offset addition could overflow in release builds and
  pass the capacity check anyway, leaving self.cap larger than the
  actual allocation and letting spare_capacity_mut() hand out
  out-of-bounds slices (GHSA-434x-w66g-qw3r, medium)

bytes is only a dev-dependency here (used in tests), so it never
reaches consumers of the published v8 crate. Lockfile-only bump, no
source changes.
- [google/wasefire](https://github.com/google/wasefire) [1](https://github.com/google/wasefire/commits): Enable unreachable_pub lint in the host runner (#1153)
- [lakehq/sail](https://github.com/lakehq/sail) [1](https://github.com/lakehq/sail/commits): feat: support v3 MOR operations for Iceberg (#2655)
- [zurawiki/gptcommit](https://github.com/zurawiki/gptcommit) [1](https://github.com/zurawiki/gptcommit/commits): Upgrade tiktoken-rs to 0.12.1

## [skills](https://github.com/topics/skills)
- [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) [4](https://github.com/CherryHQ/cherry-studio/commits): fix(composer): prefer text for rich Excel clipboard pastes (#21031)

### What this PR does

Before this PR:

When Excel copies cells on Windows, the clipboard can contain plain
text, an HTML table, and an image representation. The composer preferred
any supported clipboard image, so copied tables could reach text-only
models as screenshots.

After this PR:

When non-empty plain text and HTML representations accompany a supported
image, the composer treats the clipboard as rich text and preserves the
existing textual path:

- short rich clipboard text is inserted as text;
- long rich clipboard text follows the existing pasted-text-file path;
- screenshot-only clipboard pastes remain image-first;
- image-plus-text pastes without an HTML representation remain
image-first.

Fixes #6119

### Why we need it and why it was done in this way

Excel's clipboard payload is a rich document representation, not a
screenshot intent. Preferring the image representation makes copied
tables harder for text-only models to read and forces users to route the
data through a text editor first.

The discriminator is deliberately narrow: both non-empty `text/plain`
(or the existing `text` fallback) and `text/html` must be present. This
distinguishes document-style clipboard content from Windows screenshot
clipboards that can also expose a text flavor.

The following tradeoffs were made:

- preserve screenshot-only behavior instead of globally preferring text
whenever any image is present;
- preserve the existing long-text file path instead of adding a new
attachment type;
- avoid HTML-to-Markdown conversion, dual attachments, wildcard file
semantics, or a broader paste refactor.

The following alternatives were considered:

- Prefer text whenever any `text/plain` flavor exists. Rejected because
screenshot clipboards may expose text alongside image bytes, and this
would regress screenshot handling.
- Parse HTML into Markdown. Rejected because it expands the behavior and
format contract beyond the reported regression.
- Attach both image and text. Rejected because it duplicates content and
leaves attachment selection ambiguous.

### Breaking changes

None.

### Special notes for your reviewer

The two affected paste entry points are covered because short text stays
in `ComposerSurfaceRuntime`, while long text is delegated to
`handlePaste`.

Verification:

- `pnpm exec vitest run --project renderer
src/renderer/components/composer/__tests__/ComposerSurface.test.tsx
src/renderer/components/composer/paste/__tests__/pasteHandling.test.ts`
— 2 files / 179 tests passed;
- targeted Oxlint — 0 warnings / 0 errors;
- targeted ESLint — passed;
- targeted Oxfmt check — passed;
- `git diff --check` — passed;
- commit is SSH signed and includes a DCO `Signed-off-by` trailer.

Native Windows Excel clipboard integration E2E was verified on
2026-09-25 07:42:49 (Beijing time). Microsoft Excel 15 copied short and
long worksheet ranges onto the real Windows clipboard; both exposed
`text/plain`, Excel `text/html`, `text/rtf`, and `Files/image.png`.
Electron 44.2.0 / Chromium then dispatched real paste events into this
PR's production `handlePaste`:

- short range: text was inserted normally, with no temporary file or
image attachment;
- long range (80 × 4 cells): 3,751 text characters were written to
`pasted_text.txt` with `composerFileKind: pasted_text`, and the Excel
PNG was not attached.

The probe is local Windows-only tooling and is not committed. A full
packaged Cherry Studio UI run was not completed because the local `pnpm
dev` launch stopped before startup while rebuilding `better-sqlite3`
(Visual Studio C++ tooling was unavailable); repository CI remains the
canonical full-suite signal. The repository-wide Windows suite was also
attempted, but unrelated main-process tests currently fail on POSIX path
expectations, Windows symlink privileges, and existing mock/export gaps;
the changed-scope renderer suites above are green.

This change is intentionally independent of the wildcard/file-extension
behavior discussed in #20357: it does not add `*` support or change
path-backed file acceptance.

### Checklist

- [x] Branch: This PR targets `main`
- [x] PR: The PR description is expressive enough and will help future
contributors
- [x] Code: The implementation is kept scoped to the reported
rich-clipboard regression
- [ ] Refactor: No unrelated cleanup is included
- [x] Upgrade: No persisted data, defaults, or upgrade flow changes
- [ ] Documentation: Not required for this narrow behavior fix
- [x] Self-review: The diff, tests, lint, formatting, signature, and DCO
trailer were reviewed

### Release note

```release-note
[Composer] Copied Excel cells now paste as text when the clipboard provides rich text alongside an image, while screenshot-only pastes remain image-first.
```

---------

Signed-off-by: Bruce-Yii <298228875+Bruce-Yii@users.noreply.github.com>
Signed-off-by: suyao <sy20010504@gmail.com>
Co-authored-by: Bruce-Yii <298228875+Bruce-Yii@users.noreply.github.com>
Co-authored-by: suyao <sy20010504@gmail.com>
- [android/skills](https://github.com/android/skills) [2](https://github.com/android/skills/commits): Bump plugin version to v1.0.13

## [swift](https://github.com/topics/swift)
- [trycua/cua](https://github.com/trycua/cua) [57](https://github.com/trycua/cua/commits): docs(cua-s1): document pinned weights and reproducible inference setup (#4186)

* docs(cua-s1): document pinned weights and reproducible inference setup

Add a "Get the weights and run inference" section to the Cua-S1 README
with Hugging Face repositories pinned to commit SHAs for every published
checkpoint and the Qwen3.5-4B base, base pairing, layouts, sizes,
declared licenses, hardware guidance with measured Apple silicon
latencies, the locked four-b environment, pinned hf download commands,
the S1_* chooser variables, and a fixture smoke with its expected output.

Record the verification scope in the model card: local fixture results
per adapter, the desktop counterexample, what canonical E2E and CI do
not yet cover, and known failure modes. Reconcile the cua-s1-forms
status and fix the stale Transformers note in the jev-use decision guide.

Refs #4184

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

* docs(cua-s1): reflect the mps loader fix, chooser identity, and latency

- Replace the mps float16 workaround with the sequential-loading fix
  (#4198) in the README, model card, and jev-use decision models doc.
- Document S1_MODALITY, --screenshot, S1_ADAPTER_ID/REVISION, and the
  derived model identity (#4204), and update the expected smoke output.
- Add bf16 multimodal and CPU latency rows, the 60-second capture
  lifetime, cold versus warm timings, and a keep-warm recommendation.
- Recommend loading only the cua-s1-forms safetensors pair and never
  unpickling the .pt copy.
- Update the CI coverage statement after #4201.

Refs #4184

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
- [FluidInference/FluidAudio](https://github.com/FluidInference/FluidAudio) [8](https://github.com/FluidInference/FluidAudio/commits): Update README with Trendshift badge and alignment

Added badges for Trendshift repository and improved alignment.
- [tw93/MiaoYan](https://github.com/tw93/MiaoYan) [8](https://github.com/tw93/MiaoYan/commits): release: prepare V4.5.0

Sets both version fields to 4.5.0 and writes the release notes for the
search, font, settings and iPhone work since 4.3.2.
- [iziz/libPhoneNumber-iOS](https://github.com/iziz/libPhoneNumber-iOS) [2](https://github.com/iziz/libPhoneNumber-iOS/commits): Merge pull request #456 from iziz/codex/metadata-v9-0-40

chore(release): refresh metadata for 2.1.1
- [scinfu/SwiftSoup](https://github.com/scinfu/SwiftSoup) [2](https://github.com/scinfu/SwiftSoup/commits): Merge pull request #458 from lake-of-fire/fix/xml-entry-points-20260925

Fix XML auto-detection and borrowed-buffer initialization
- [Beingpax/VoiceInk](https://github.com/Beingpax/VoiceInk) [1](https://github.com/Beingpax/VoiceInk/commits): Fix case-only word replacements being detected as cycles

## [wearable](https://github.com/topics/wearable), [wearables](https://github.com/topics/wearables)
- [Mentra-Community/MentraOS](https://github.com/Mentra-Community/MentraOS) [38](https://github.com/Mentra-Community/MentraOS/commits): Merge pull request #4221 from Mentra-Community/codex/review-project-sessions

Make configured PR reviews visible in Codex
- [OpenStrap/edge](https://github.com/OpenStrap/edge) [4](https://github.com/OpenStrap/edge/commits): Merge pull request #459 from OpenStrap/release/v0.10.0-build67

bump build number to 67

## Other
- [facebook/idb](https://github.com/facebook/idb) [84](https://github.com/facebook/idb/commits): Drop elements wholly outside the screen from --filter interactable

Summary:
`--filter interactable` no longer reports elements whose frame lies wholly outside the screen, together with everything beneath them. Rows of a table below the fold were reported as if tappable. Worse, the runtime reports an offscreen cell's descendants in the cell's own coordinates, so the label of row 20 claimed a frame over the search bar and looked on screen.

The pruning applies to both the backend verdict and the structural heuristic, and it does not hoist: an offscreen element's descendants have untrustworthy frames. An element that is only partly clipped is kept. An element with an empty frame never prunes, because the visible home screen page reports a zero frame but holds on-screen icons; the zero-size rule judges those instead. Reads with no screen (a named element's or a point's descendants) prune nothing.

Differential Revision: D121794765

fbshipit-source-id: 27e9d15916c3719124a4e65440d1403c9156ffa7
- [openai/codex](https://github.com/openai/codex) [55](https://github.com/openai/codex/commits): Prevent Windows daemon launches from retaining launcher stdio (#48272)

## Why

Detached Windows daemons can inherit the launcher's output pipes, leaving callers waiting for EOF after the launcher exits.

## What changed

Clear inheritance flags on the launcher's standard handles before spawning managed Windows processes. Leave the flags cleared to protect concurrent launches while preserving the child's configured stdio, and tolerate missing or already-closed handles.

## Testing

- Add a Windows regression test verifying that captured launcher output closes while the detached child remains alive and writes to its configured log.
- Give optional MCP startup grace tests more time to complete on slow runners while keeping the pending server's startup timeout longer than the turn timeout.

GitOrigin-RevId: 053e0417793db3c961e738476a05c7467978f339
- [jdx/mise](https://github.com/jdx/mise) [31](https://github.com/jdx/mise/commits): registry: nub serves 0.9.5+ from github:nubjs/nub and lists the nubr bin (#13643)

Puts `github:nubjs/nub` first in the `nub` registry entry for 0.9.5 and
later, keeps `npm:@nubjs/nub` for the versions before it, and lists
`nubr` as a third bin.

From [nub 0.9.5](https://github.com/nubjs/nub/releases/tag/v0.9.5) the
release archives carry `bin/nubx` and `bin/nubr` themselves: relative
symlinks to `bin/nub` in the tarballs, a small stub executable under
each name in the Windows zips
([nubjs/nub#956](https://github.com/nubjs/nub/pull/956)). A plain
extraction is a complete install, so the GitHub backend can serve it.
Earlier archives shipped only `bin/nub`, which is what kept the entry on
the npm package and its Node launcher
([#13191](https://github.com/jdx/mise/pull/13191)); `min_version` routes
those versions to npm as before.

Verified on macOS arm64 with mise 2026.9.14, a clean `MISE_DATA_DIR`,
and `MISE_MINIMUM_RELEASE_AGE=0` because 0.9.5 is younger than a day:

```
$ mise ls-remote github:nubjs/nub | tail -3
0.9.2
0.9.3
0.9.5
$ mise install github:nubjs/nub@0.9.5
mise ✓ github:nubjs/nub@0.9.5  5.0s  nub-darwin-arm64.tar.gz
$ ls -l $MISE_DATA_DIR/installs/github-nubjs-nub/0.9.5/bin
-rwxr-xr-x  nub
-rwxr-xr-x  nub-launcher-darwin-arm64
lrwxr-xr-x  nubr -> nub
lrwxr-xr-x  nubx -> nub
$ mise x github:nubjs/nub@0.9.5 -- nubr --version
0.9.5
$ mise x github:nubjs/nub@0.9.5 -- nubx --help | head -1
Run a tool from `node_modules/.bin`, fetching it on a local miss (`npx`/`pnpm
```

The release publishes no artifact attestations, so there is no
`attestations_since`. `registry/nubr.toml` stays on `npm:@nubjs/runner`,
the Node-only runner package.

`bins` is one list per tool, not per backend. `nubr` exists in the npm
package from 0.9.3, so only a pin at 0.9.2 or older gets a `nubr` shim
with nothing behind it, the same as any tool that gained a bin between
releases.


<!-- This is an auto-generated comment: release notes by coderabbit.ai
-->

## Summary by CodeRabbit

* **New Features**
* Added support for the Nub backend, with a minimum required version of
0.9.5.
* The `nubr` executable is now recognized alongside `nub` and `nubx`,
allowing the registered backend to work with setups that use any of
these Nub command-line tools. This expands the available Nub executable
options without changing support for the existing binaries.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->
- [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) [22](https://github.com/ghostty-org/ghostty/commits): gtk: don't tell systemd we're ready before we can handle SIGUSR2 (#14399)

On a dark desktop, syncing the color scheme during startup triggers a
config reload, which sent RELOADING=1 and READY=1 before the SIGUSR2
handler was installed. systemd 262 refuses to start a Type=notify-reload
service whose reload signal has no handler, so D-Bus activation fails
intermittently and no window opens.

Fixes #14398
Discussions: #11724, #14394, #14393

AI disclosure: Claude Code was used to investigate and develop the
patch, but the author has thoroughly reviewed the patch.
- [twmb/franz-go](https://github.com/twmb/franz-go) [22](https://github.com/twmb/franz-go/commits): Merge pull request #1477 from twmb/kgo-share-fixes

kgo: share consumer fixes (#1474 and an audit)
- [openclaw/acpx](https://github.com/openclaw/acpx) [18](https://github.com/openclaw/acpx/commits): test: require the filesystem containment refusal (#804)

Replace the host-dependent generic-error assertion with readable synthetic inside/outside files and the exact correlated filesystem RPC refusal. Verify the permitted read and reject forbidden-content exposure.

The original oracle accepts an injected unrelated error; the new oracle rejects both wrong-error and allowing-read controls through the real CLI/RPC route. Production behavior is unchanged. Focused proof, isolated review, the full Linux gate and exact-head CI passed.
- [cline/cline](https://github.com/cline/cline) [15](https://github.com/cline/cline/commits): refactor(ui): share desktop composer presentation (#14422)

* refactor(ui): share desktop context usage presentation

* refactor(ui): share desktop composer presentation

* fix(ui): inherit composer variants

* fix(ui): render zero context usage cost

* fix(ui): preserve context cost visibility

* test(ui): cover context cost visibility

* docs(ui): document shared context usage API

* docs(ui): document shared composer API

* docs(ui): shorten composer API reference

* docs(ui): keep composer documentation in UI package
- [earendil-works/pi](https://github.com/earendil-works/pi) [15](https://github.com/earendil-works/pi/commits): docs(durable): clarify scratch examples
- [biliup/biliup](https://github.com/biliup/biliup) [14](https://github.com/biliup/biliup/commits): feat(clip): publish queue for clips (#1751)

* test(server): give the streamer service fixture the clip exports

The clips field was added to ServiceRegister (#1747) while the streamer
service tests (#1749) were written against the old struct, so the biliup-cli
lib tests no longer compile on master.

* refactor(upload): split studio building and report upload progress

Split the template-to-Studio builder out of build_studio as
studio_from_template (cover upload stays in build_studio), share the @credit
expansion as desc_with_credits, add upload_single_file_with_progress and make
resolve_source crate-visible, so the clip publisher can reuse them.
Whole-stream uploads behave as before.

* feat(clip): publish settings and archive rendering for clips

- Clips pick an upload template (default: the streamer's) and may override
  title, description, tags, category, schedule and cover (StudioOverride,
  stored in clips.studio_override); the override is merged into the template
  and built through the same studio_from_template path as whole-stream uploads.
- New title / description variables {clip_title} and {clip_time}; % in values
  is escaped and a malformed strftime in the template is kept as text instead
  of panicking. @credit is expanded like whole-stream uploads.
- Copyright is always forced to reprint (2); the source is the template's
  reprint source, falling back to the live room URL. A self-made template is
  not followed.
- Pre-flight problems (no template, empty title, no tags, Noop uploader,
  scheduled time outside 4 hours to 15 days) are reported before queueing.
- clips gains set_publish_settings and mark_published; the latter records
  archive_bvid / published_at and releases the clip's segment pins in the same
  transaction, keeping the clip file.

* feat(clip): single-concurrency publish queue that pauses on 601

- A dedicated queue (not the recorder's UActor) handles one archive at a time:
  export when needed -> initialize_upload_context -> upload each part ->
  cover -> submit_to_bilibili, reporting the step, detail, upload ratio and
  parts already uploaded per job. Jobs live in memory only.
- B站 601 pauses the whole queue until resume() is called; nothing is retried
  automatically and there is no daily cap.
- Other failures keep the reason on the job (a rejected cover says so) and can
  be retried; parts already uploaded are not uploaded again, and a part whose
  clip range changed is dropped and re-uploaded.
- Jobs can be cancelled while exporting or uploading, not while submitting.
- On success the clips are marked published with the BV id.

* feat(clip): grab a JPEG frame from a recording for clip covers

thumb::grab uses the quick-cut plan to find the keyframe range covering t,
pipes it into FFmpeg (tools::ffmpeg_command, so the configured or bundled
ffmpeg is used) and decodes up to t. A frame on the segment still being
written waits up to 5 s; a time past the recording or in a gap says so in
cover terms.

* feat(clip): publish, cover and frame endpoints

- POST /v1/clips/{cid}/publish (optionally saving publish settings first)
  queues export -> upload -> submit and returns 202; POST /v1/publish-jobs
  publishes several clips, one archive per clip by default or one multi-part
  archive (combine: same session, up to 100 parts). Every archive is checked
  before anything is queued.
- GET /v1/publish-jobs, POST /v1/publish-jobs/preview, /resume,
  /{jid}/retry and DELETE /v1/publish-jobs/{jid} expose the queue.
- GET /v1/sessions/{id}/thumb returns a frame; GET / PUT / DELETE
  /v1/clips/{cid}/cover sets a clip cover from a frame, the recorded live
  cover or an uploaded JPEG / PNG / WebP (up to 5 MB).
- PATCH on a clip stores template_id / studio_override; clips in the queue
  cannot be re-ranged or deleted (409).
- Routes are classified in the policy table: publishing needs upload.submit,
  viewing the queue and frames file.view, changing covers clip.edit.
- [Donkie/Spoolman](https://github.com/Donkie/Spoolman) [11](https://github.com/Donkie/Spoolman/commits): Merge pull request #1186 from Donkie/worktree-armv7-build-speed

Speed up armv7 image builds when the layer cache misses
- [ChrisBuilds/terminaltexteffects](https://github.com/ChrisBuilds/terminaltexteffects) [10](https://github.com/ChrisBuilds/terminaltexteffects/commits): Optimize Matrix rain rendering
- [OpenStickCommunity/GP2040-CE](https://github.com/OpenStickCommunity/GP2040-CE) [10](https://github.com/OpenStickCommunity/GP2040-CE/commits): Update to the P5General to use Core0 (#1728)

This PR moves the P5General input mode to use Core0.  Using Core0 avoids all of the screen related issues we were seeing when it was on Core1.
- [ophub/amlogic-s9xxx-armbian](https://github.com/ophub/amlogic-s9xxx-armbian) [9](https://github.com/ophub/amlogic-s9xxx-armbian/commits): Update meson-sm1-tox1.dtb
- [espressif/esp-idf](https://github.com/espressif/esp-idf) [8](https://github.com/espressif/esp-idf/commits): Merge branch 'feat/least_recently_used' into 'master'

feat(nimble): Added LFU method for device deletion post bond count overflow

See merge request espressif/esp-idf!52014
- [Alishahryar1/free-claude-code](https://github.com/Alishahryar1/free-claude-code) [7](https://github.com/Alishahryar1/free-claude-code/commits): patch: Fix post-merge release lookup race (#1904)

## Why

Post-merge publication crashed after creating v6.2.67 because GitHub
temporarily omitted the new draft from its release list. The same stale
list could also report incomplete assets after upload.

## How

Retain the numeric release ID returned by draft creation and fetch
staging metadata directly by that ID before and after uploading assets.
Preserve generated release notes and cover delayed list responses for
both new drafts and interrupted uploads.
- [block/buzz](https://github.com/block/buzz) [7](https://github.com/block/buzz/commits): fix(ci): select runtime suites from PR changes only (#7843)

A documentation-only update to #7809 selected desktop builds and E2E
tests because path detection compared an old PR base SHA with GitHub's
newer synthetic merge commit. The [failing run's path-detection
log](https://github.com/block/buzz/actions/runs/35789957773/job/106955810630)
includes four unrelated desktop files from `main`; `VISION_MOBILE.md`
did not match a runtime filter.

Use GitHub's PR file list for pull requests so unrelated changes in the
synthetic merge commit cannot select runtime suites. The existing
directory filters are unchanged: root and docs/ Markdown do not select
runtime suites, while Markdown under runtime directories still selects
its affected suites. Mixed code/documentation changes retain normal
coverage. Always-on security, policy, and source-contract checks and
full push-to-main coverage are unchanged.

Added regression coverage runs the pinned paths-filter action against
real fixture repositories, including a synthetic merge containing
unrelated upstream desktop code. All 35 selection scenarios and 26
required-check scenarios pass; the new regressions failed before the
fix. Existing required-context isolation, file-size policy, and
security-review contract checks pass, as do script lint and workflow
syntax validation. Full workflow lint reports the same two pre-existing
shell-quoting findings in the untouched dead-token guard. A desktop E2E
build was run to diagnose the unrelated required smoke failure.

Related: #7809 (incident, unchanged) and #5756 (shared-input path
coverage, separate scope). No matching issue found.

PRs with at least 3,000 changed files now select every runtime suite,
avoiding GitHub's PR-file-list ceiling. Boundary tests cover 2,999,
3,000, and 3,001 files, including a runtime file omitted beyond the API
cap; disabling the safeguard makes the latter two regressions fail.

Required checks now run and fail when path selection fails, is
cancelled, or is skipped. Regression coverage exercises the workflow
conditions and shell checks for all 13 required wrappers, plus an
API-denial case against the pinned action. Mutating either the
scheduling guard or the result check makes all 13 failure regressions
fail.

The required mention-settings smoke test expected a pin after explicitly
disabling automatic mentions. Waiting for its old avatar to exit
reproduced the CI failure 3/3; the test now checks that subsequent
mentions remain manual and retains outgoing recipient-tag assertions.
Corrected browser regression: 20/20 repeated runs; related picker unit
tests: 18/18. No desktop production behavior changed. The always()
requirement is now pinned in required-wrapper regression tests; deleting
it fails all 26 gate cases.

---------

Signed-off-by: Tom Brow <tomb@block.xyz>
- [tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro) [6](https://github.com/tensorflow/tflite-micro/commits): fix(python): remove resource variable printout (#3785)

Stop printing the model's resource variable count each time the
Python interpreter loads a model. The print went to stdout without
being asked for, and it cluttered the output of every script and test
that loads a model. The interpreter still counts the resource
variables and passes the count to the C++ interpreter.

BUG=see description
- [anthropics/claude-code](https://github.com/anthropics/claude-code) [5](https://github.com/anthropics/claude-code/commits): chore: Update CHANGELOG.md and feed.xml
- [databendlabs/openraft](https://github.com/databendlabs/openraft) [5](https://github.com/databendlabs/openraft/commits): test: jepsen: assert exact partition script, share retry handler

# Summary

`partition-install-minimizes-the-leader-lease-critical-path` compares
the two recorded commands with the exact expected `iptables` script in
one assertion, and `recover!` calls one `retry-or-throw!` helper from
both of its `catch` forms.

# Details

The old test checked only fragments of each command, so it still passed
when `partition!` lost the `-A ... -j DROP` rule or gained a command
between `-I OUTPUT` and the final `/append-membership`. A real run fails
on the first edit at the `-C` rule check, and on the second because the
removed leader's lease expires before the final membership is submitted.
The Jepsen workflow runs the real scenarios only on pushes to `main`, so
no pull-request check catches either edit. The exact comparison fails on
both.

CLOSES #2138
- [mlfoundations/open_clip](https://github.com/mlfoundations/open_clip) [5](https://github.com/mlfoundations/open_clip/commits): Merge pull request #1216 from mlfoundations/siglip-chunk-interp-fixes

Siglip chunk + transform interp fixes
- [TactilityProject/Tactility](https://github.com/TactilityProject/Tactility) [5](https://github.com/TactilityProject/Tactility/commits): Tab5, CoreS3, StackChan and app icons (#662)
- [AcademySoftwareFoundation/OpenShadingLanguage](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage) [4](https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/commits): fix(optix): Allow LLVM to choose the PTX ISA version. (#2166)

LLVM's NVPTX backend selects the minimum PTX ISA version required by the
configured CUDA target architecture. Do not force PTX 5.0, which is invalid
for newer targets such as sm_75.

Assisted-by: OpenAI Codex / GPT-5

Signed-off-by: Tim Grant <tgrant@nvidia.com>
- [buildroot/buildroot](https://github.com/buildroot/buildroot) [4](https://github.com/buildroot/buildroot/commits): {linux, linux-headers}: bump 7.2.x, 6.18.x series

Update the latest kernel releases to:
- 7.2.7 -> 7.2.8
- 6.18.53 -> 6.18.54

Signed-off-by: Bernd Kuhls <bernd@kuhls.net>
Signed-off-by: Fiona Klute <fiona.klute@gmx.de>
- [hathach/tinyusb](https://github.com/hathach/tinyusb) [4](https://github.com/hathach/tinyusb/commits): skills: keep -rcN in usbtest's kernel tag, document HIL roster variant builds (#3980)

check_build.py --variants <hil config> builds each board's roster variants
into cmake-build-<variant>, matching the HIL CI matrix, and refuses a
malformed roster as a resolution error. hil_remote.py prints that build
line on every missing-build refusal; the hil, build and usbtest skills and
CLAUDE.md's build contract point HIL builds at it.
- [bumptech/glide](https://github.com/bumptech/glide) [3](https://github.com/bumptech/glide/commits): Merge pull request #5747 from bumptech:renovate/androidx.futures

PiperOrigin-RevId: 988486137
- [ccusage/ccusage](https://github.com/ccusage/ccusage) [3](https://github.com/ccusage/ccusage/commits): perf(claude): skip stale files for date-bounded loads and bound statusline blocks (#1794)

* perf(claude): skip usage files last written before --since

Session JSONL files are append-only, so a file whose mtime predates the
--since window cannot hold an entry inside it. Both Claude loaders now
drop such files before reading, with a 24-hour margin for timezone
bounds and late flushes. Unbounded reports, future windows, and files
with unreadable metadata keep every file.

Refs #1791

* perf(statusline): bound the active block load

The active block query loaded the whole Claude history on every cold
render. It now sets --since to one day behind the session window so the
Claude adapter only reads recently written files.

Refs #1790

* test(claude): cover bounded daily totals with pruned files

Run claude daily through the CLI with stale, in-margin and fresh session
files so the --json and table outputs guard that mtime pruning keeps
late-flushed entries and leaves the bounded totals unchanged.

* fix(claude): keep --since pruning from changing report output

Codex review found four ways mtime pruning changed bounded reports:

- A sidechain replay of a parent message in a stale file was counted twice.
  Files are now kept or skipped per session (the transcript together with
  its subagent transcripts), so replays still meet their parents.
- Unified `session --since` totals whole sessions, and blocks anchor on
  earlier entries, so both read the full history again through
  `load_entries`. Reports that drop entries dated before `--since` opt into
  pruning via the new `load_entries_since`.
- The statusline active block now widens its window until it reaches back
  past an idle gap longer than a session, which is where block boundaries
  stop depending on older history, and otherwise reads the full history.
- Unified reports lost `Detected: Claude` when every file predated the
  window; skipped files are now checked for usage when nothing else is found.

Regression tests run each case twice, with stale and freshly touched
mtimes, and require identical output.

* fix(claude): group pruned sessions across roots and flat agent files

Key sessions relative to `projects/` so a copy in another config root is
kept with the live original, and key legacy flat `agent-*.jsonl`
transcripts on the `sessionId` inside them so sidechain replays still meet
their parents.

The statusline active block also reads the full history when entries are
future-dated, since a pause before such an entry could otherwise anchor
blocks after the current one.

* fix(claude): group pruned files by the session IDs they record

Workflow subagent transcripts can live under one session directory and
record another session's ID, so path-based groups let a stale parent be
dropped while its in-window replay survived. Files now join a union-find
over their path-derived session and the first `sessionId` they record,
which is the identity the loaders deduplicate on. This also covers
legacy flat `agent-*.jsonl` files and copies in another config root, and
the probe parses JSON lines so whitespace or long leading lines no longer
hide the ID.
- [lancedb/lancedb](https://github.com/lancedb/lancedb) [3](https://github.com/lancedb/lancedb/commits): feat(python): pass batch_size and other CrossEncoder kwargs (#4328)
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) [2](https://github.com/anthropics/claude-agent-sdk-python/commits): chore: bump bundled CLI version to 2.1.283
- [bufbuild/buf](https://github.com/bufbuild/buf) [2](https://github.com/bufbuild/buf/commits): Add PyPI wheel publishing flow (#4656)
- [daijro/camoufox](https://github.com/daijro/camoufox) [2](https://github.com/daijro/camoufox/commits): Update README wording
- [embassy-rs/trouble](https://github.com/embassy-rs/trouble) [2](https://github.com/embassy-rs/trouble/commits): Merge pull request #688 from Helius-Messenger/fix/connection-handle-aliasing

fix: handle disconnection errors and prevent connection handle recycling conflicts
- [espressif/esp32-camera](https://github.com/espressif/esp32-camera) [2](https://github.com/espressif/esp32-camera/commits): Fix sensor function pointer initialization and update settings (#855)

* Update sensor settings to use set_dummy function

* Fix uninitialized set_* sensor function pointers

Several sensor drivers left set_* function pointers unassigned or set to
NULL. esp_camera_load_from_nvs() invokes these pointers without NULL
checks, so a NULL/uninitialized pointer crashes when camera settings are
restored from NVS. Wire unsupported features to set_dummy() (and
set_gainceiling_dummy() where a gainceiling_t argument is expected).

Also fix ov7670.c indentation and remove a duplicate set_special_effect
assignment in sc031gs.c that shadowed the sleep-mode implementation.

Co-Authored-By: Claude <noreply@anthropic.com>

---------

Co-authored-by: Claude <noreply@anthropic.com>
Co-authored-by: Me No Dev <me-no-dev@users.noreply.github.com>
- [huggingface/AnyLanguageModel](https://github.com/huggingface/AnyLanguageModel) [2](https://github.com/huggingface/AnyLanguageModel/commits): Decode the error object in OpenAI Responses results (#270)

The Responses API returns `error` as an object with a code and a message, or `null`. `OpenAILanguageModel` declared it as `[JSONValue]?`, so a non-streaming response with a non-null `error` failed to decode as a whole, and the caller got a decoding error instead of the response.

This PR decodes `error` as that object, the way `OpenResponsesLanguageModel` already does, and adds a test that decodes a response with an error object for both providers. The error isn't surfaced yet; that's separate from getting the response to decode.
- [huggingface/lerobot](https://github.com/huggingface/lerobot) [2](https://github.com/huggingface/lerobot/commits): Feat/rebot b601 motor family (#4535)

* test(rebot): lock in legacy DM behavior

* build(rebot): upgrade MotorBridge to 0.5

* feat(rebot): unify DM and RS motor families

* fix: prevent partial reBot actions moving wrist yaw

* fix(rebot): improve startup and bimanual failure safety

* refactor(rebot): use shared bimanual lifecycle cleanup

* fix(rebot): validate only device ID in RS startup ping

* fix(rebot): align bimanual cleanup with shared lifecycle API

* docs(rebot): simplify hardware setup guidance

* fix(rebot): use standard bimanual lifecycle behavior

* fix(rebot): remove unnecessary python-can dependency

* refactor(rebot): delegate MIT gain limits to MotorBridge

* refactor(rebot): remove duplicate torque ceiling handling

* refactor(rebot): simplify MotorBridge mode selection

* refactor(rebot): simplify motor family profiles

* docs(rebot): clarify cross-platform CAN transport

* refactor(rebot): use profiles for CAN adapter validation

* refactor(rebot): remove unused profile property

* refactor(rebot): keep motor profiles internal

* refactor(rebot): use shared MIT control mode default

* refactor(rebot): simplify profile set definitions

* refactor(rebot): remove connection cleanup wrapper

* refactor(rebot): remove unused public joint limits helper

* refactor(rebot): simplify present position reads

* refactor(rebot): remove redundant config exports

* refactor(rebot): share MIT mode constant

* refactor(rebot): use mutable internal motor profiles

* refactor(rebot): derive motor family from profile lookup

* refactor(rebot): select motor profiles directly

* refactor(rebot): inline control mode selection

* refactor(rebot): delegate transport validation to MotorBridge

* refactor(rebot): delegate port validation to MotorBridge

* refactor(rebot): delegate MIT gain validation to MotorBridge

* refactor(rebot): delegate command validation to MotorBridge

* refactor(rebot): keep follower directions internal

* refactor(rebot): internalize runtime safety tuning

* refactor(rebot): simplify mode-specific defaults

* refactor(rebot): simplify MotorBridge lifecycle

* refactor(rebot): simplify family configuration

* refactor(rebot): simplify bimanual configuration

* test(rebot): simplify motor family coverage

* docs(rebot): streamline motor family guide

* refactor(rebot): simplify per-joint configuration

* refactor(rebot): streamline follower configuration

* refactor(rebot): simplify motor family profiles

* refactor(rebot): simplify follower MotorBridge handling

* test(rebot): strengthen motor family and lifecycle coverage

* docs(rebot): clarify CAN setup and gripper behavior

* docs(rebot): expand DM and RS setup and recording guide

* docs(rebot): nit

* refactor(rebot): address review feedback

* fix(rebot): merge partial joint limit overrides

* refactor(rebot): validate control config before connecting

* fix(rebot): warn when feedback loss disables torque
- [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills) [2](https://github.com/lijigang/ljg-skills/commits): feat: sync ljg-* skills [ljg-map] (v1.17.114)
- [RfidResearchGroup/proxmark3](https://github.com/RfidResearchGroup/proxmark3) [2](https://github.com/RfidResearchGroup/proxmark3/commits): Fix bug when calling directly recovery Makefile
- [smithy-lang/smithy](https://github.com/smithy-lang/smithy) [2](https://github.com/smithy-lang/smithy/commits): Bump version to 1.74.0 (#3302)

* Bump version to 1.74.0

* Add missing PR link for #2992

* Fix bad format

* Include resrouce lifecycle traits in CHANGELOG

* Add CHANGELOG change
- [tidwall/tg](https://github.com/tidwall/tg) [2](https://github.com/tidwall/tg/commits): Update GEOS version in tests
- [a2aproject/A2A](https://github.com/a2aproject/A2A) [1](https://github.com/a2aproject/A2A/commits): docs: add x402-list to partners (#2202)

Adds x402-list to the A2A partners list.

x402-list is an agent-first directory of x402 payment endpoints: it
helps
agents discover and verify payable APIs (including the A2A x402
extension
flow) before paying. Homepage: https://x402-list.com

Entry inserted alphabetically between "Writer" and "Zenity", following
the
existing `- [Name](url)` list format.

Co-authored-by: Sampath Kumar <sam1990kumar@gmail.com>
- [alyssaxuu/screenity](https://github.com/alyssaxuu/screenity) [1](https://github.com/alyssaxuu/screenity/commits): Finish the previous upload before a new recording starts, recording into empty scenes, + clearer picker cancel and failed-upload handling
- [anthropics/buffa](https://github.com/anthropics/buffa) [1](https://github.com/anthropics/buffa/commits): codegen: escape a oneof enum name that PascalCases to Self (#465)

A oneof named `self` makes code generation fail outright. PascalCasing
the name produces `Self`, which is a reserved Rust identifier, so the
generator emits `pub enum Self`, the generated file does not parse, and
`generate` returns an error that names no oneof at all. The same escape
is already applied one function below to the oneof's *variant* names,
and to the struct field, so this applies it to the enum's own name as
well and the three finally agree.

`oneof_enum_ident` (`buffa-codegen/src/oneof.rs:932`) builds the
identifier with a bare `format_ident!`. `self`, `self_` and `_self` all
reach it, because `to_pascal_case` (`oneof.rs:972`) splits on `_` and
capitalises each part, and `Self` is the only reserved Rust identifier
with a leading capital, so it is the only reachable case. The ident is
produced once in `resolve_oneof_idents` (`oneof.rs:954`) and consumed
for both the owned enum (`oneof.rs:679`) and the view enum
(`view.rs:1105`). `format_tokens` (`buffa-codegen/src/lib.rs:4332`) runs
`syn::parse2::<syn::File>` before prettyplease sees the tokens, so the
result is `CodeGenError::InvalidSyntax("generated code failed to parse
as Rust: ...")` for a perfectly legal `.proto`.

`oneof_variant_ident` (`oneof.rs:967`) already routes through
`make_field_ident`, and its doc comment spells out this exact failure:
it "would otherwise produce `pub enum Foo { Self(...) }` and fail to
parse". `CodeGenContext::oneof_ident` (`context.rs:534`) escapes the
struct field too. Only the enum's own name was left raw, so for a oneof
named `self_` the generated field is `self_` and the type it points at
is `Self`.

No fixture puts a keyword on the oneof itself, which is why this
survived: `buffa-test/protos/keywords.proto` covers keyword package,
message, field and enum-value names, including `string self = 4;` at
line 35, but its one oneof is named `value`, and the #47 regression test
(`buffa-codegen/src/tests/naming.rs:1147`) puts the keyword on a variant
while naming the oneof `identity`.

The fix routes the enum name through `make_field_ident`
(`idents.rs:67`), exactly as the variant name already is, so `Self`
becomes `Self_` and matches the #47 convention. It is a no-op for every
other name: `make_field_ident` only rewrites when `is_rust_keyword`
matches, PascalCasing always yields a leading capital, and `Self` is the
only capitalised entry in that table (`idents.rs:181`). The checked-in
generated trees are unaffected, since the only oneof in either is
`google.protobuf.Value.kind` yielding `Kind`, so nothing needs
regenerating. `format_ident!` had no other use in `oneof.rs`, so its
import goes with it; that is the only other line in the diff.

`test_oneof_named_self_escapes_its_enum_to_self_underscore` sits beside
the #47 test it mirrors: it generates a message with a oneof named
`self_` and asserts the enum is `Self_` while the non-keyword variant is
untouched. On unpatched source it is the `generate(...).expect(...)`
that fails, because generation errors out before any assertion runs.

`cargo fmt --check -p buffa-codegen` is clean on the pinned 1.95.0
toolchain. I have not run the test suite on this machine, so CI is the
check on the new test.

The changelog fragment is
`.changes/unreleased/fixed-20260919-210200.yaml`. It does not cite a PR
number yet; happy to amend that in once this has one.

---------

Co-authored-by: Iain McGinniss <309153+iainmcgin@users.noreply.github.com>
- [aristocratos/btop](https://github.com/aristocratos/btop) [1](https://github.com/aristocratos/btop/commits): fix: implement only_physical on NetBSD (#1852)

The only_physical option was read but commented out on NetBSD, so the
menu toggle did nothing. Filtering relied on a hardcoded fstype
blocklist copied from FreeBSD that misses NetBSD's kernfs, ptyfs, mfs,
null, union and overlay mounts, and never treated network mounts as
non-physical.

Closes: https://github.com/aristocratos/btop/issues/1853
Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
- [DrKLO/Telegram](https://github.com/DrKLO/Telegram) [1](https://github.com/DrKLO/Telegram/commits): update to 12.10.5 (7105)
- [espressif/esp-matter](https://github.com/espressif/esp-matter) [1](https://github.com/espressif/esp-matter/commits): Merge branch 'fix/esp-matter-todos' into 'main'

clean up stale TODOs in esp_matter

See merge request app-frameworks/esp-matter!1691
- [facebook/mariana-trench](https://github.com/facebook/mariana-trench) [1](https://github.com/facebook/mariana-trench/commits): Migrate three target-backed configs

Summary:
Migrate three target-backed local Pyre configs in Android baseline-profile tooling and Mariana Trench to Buck-generated Pyrefly companions.

Preserve each recursive target scope with package-level typing at the same root. The three scopes contain 59 unique Buck-owned Python sources and emit 69 generated type-checking companions. Add 40 narrow coded Pyrefly suppressions across 16 files and remove 38 stale Pyre ignores. All 19 changed Python files are AST-identical to the parent, so runtime behavior is unchanged.

Reviewed By: minjang

Differential Revision: D121869140

fbshipit-source-id: 615695224da9135d061116f2fe2d1a27a192dcfa
- [GNOME/librsvg](https://github.com/GNOME/librsvg) [1](https://github.com/GNOME/librsvg/commits): security.rst: Add the 2.61.5 release for RUSTSEC-2026-0305

Part-of: <https://gitlab.gnome.org/GNOME/librsvg/-/merge_requests/1220>
- [jqlang/jq](https://github.com/jqlang/jq) [1](https://github.com/jqlang/jq/commits): Prefer getentropy() over arc4random() to seed the string hash (#3629)

glibc's arc4random() aborts with "Fatal glibc error: cannot get entropy
for arc4random" when the kernel lacks getrandom(2), so jq died on
startup on older kernels once 0c7d133 began seeding the hash on every
run.  getentropy() merely returns -1/ENOSYS there, so prefer it, and
route its failure through the existing `/dev/urandom` path - which works
on precisely those kernels -- instead of a guessable `getpid() ^ time()`.
- [librepods-org/librepods](https://github.com/librepods-org/librepods) [1](https://github.com/librepods-org/librepods/commits): add opencollective and remove personal gh sponsors from FUNDING.yml
- [libvips/libvips](https://github.com/libvips/libvips) [1](https://github.com/libvips/libvips/commits): cache: ensure entry invalidation uses mutex (#5212)

Entries removed from the cache are now freed outside the mutex
to hopefully avoid potential deadlock from other invalidation signals
- [mattt/iMCP](https://github.com/mattt/iMCP) [1](https://github.com/mattt/iMCP/commits): messages_fetch: report the conversation each message belongs to (#245)

Messages the user sends from another device are synced to chat.db
without a sender handle, so until now most of the user's own messages
came back with sender "me" and nothing to tie them to a conversation;
a client could not thread them or tell who they were sent to.

Each message now carries an "isPartOf" Conversation with the chat
identifier, its display name (group chats) and its participants.
Chats are looked up once per call and shared by their messages.

Relies on Message.chatID and ChatPredicate.id from Madrid 0.5.0
(mattt/Madrid#18), which the project already depends on.

Co-authored-by: patp <boumagent@gmail.com>
- [merbanan/rtl_433](https://github.com/merbanan/rtl_433) [1](https://github.com/merbanan/rtl_433/commits): Fix Flex symbol copy length in bytes (#3715)
- [MobSF/Mobile-Security-Framework-MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) [1](https://github.com/MobSF/Mobile-Security-Framework-MobSF/commits): chore: remove dead malwaredomainlist.com integration (#2687)

MALWARE_DB_URL pointed at malwaredomainlist.com, a service that has
been defunct for years, and nothing in the codebase ever fetched or
refreshed it - the only "data" behind malware_check() was a static
snapshot bundled in the repo whose newest entries date back to 2009.
That check ran on every scan against 16+ year old data without
anyone noticing, while maltrail_check() (which does self-update from
a live source) was the only domain check actually doing real work.

Removes malware_check(), its now-unused get_netloc() helper, the
stale bundled data file, and the unused MALWARE_DB_URL setting.
maltrail_check() is unaffected and remains the sole domain check.

Co-authored-by: alanhasn

Co-authored-by: Ajin Abraham <ajin25@gmail.com>
- [motherduckdb/grafana-duckdb-datasource](https://github.com/motherduckdb/grafana-duckdb-datasource) [1](https://github.com/motherduckdb/grafana-duckdb-datasource/commits): Fail the build when a Linux binary needs a newer glibc than supported (#107)

This should guard us from issues such as
https://github.com/motherduckdb/grafana-duckdb-datasource/issues/76.

---------

Co-authored-by: Louisa Huang <louisa@motherduck.com>
- [openclaw/gogcli](https://github.com/openclaw/gogcli) [1](https://github.com/openclaw/gogcli/commits): chore(release): prepare v0.42.0 (#1170)

Prepare 0.42.0 for 2026-09-25. Lead with batch editing across Sheets, Docs, Slides, and Forms, native Contacts batch commands, and typed Gmail MCP tools, followed by authentication, allowlist, and partial-batch failure reporting fixes. Preserve all 16 release entries and contributor thanks while ordering features before safety and lossless-output fixes; set `internal/cmd/VERSION` to `v0.42.0`.

Validation: local `nice -n 19 make docs-check agent-skills-check docker-version-check` passed, alongside exact changelog-entry/credit preservation and version consistency checks. The source base remains `f30249e9f693b88cf5afec4192f75c7a3ede8cb0`, identical to the previous successful full Crabbox `make ci` run (`run_7d75511c8d3829aa5358944aa6d84953`); its 16 targeted CLI checks and MCP permission checks also passed. Independent Codex autoreview covers this final metadata diff.

Release-owner waiver: live Workspace validation skipped: test grant expired; covered by unit/integration gates and CI. Authenticated scratch-object creation, mutation, readback, and cleanup were not performed; no Google sign-in was attempted for this release pass.
- [pqrs-org/osx-event-observer-examples](https://github.com/pqrs-org/osx-event-observer-examples) [1](https://github.com/pqrs-org/osx-event-observer-examples/commits): Update vendor
- [pqrs-org/osx-hid-inspector](https://github.com/pqrs-org/osx-hid-inspector) [1](https://github.com/pqrs-org/osx-hid-inspector/commits): Update vendor
- [swiftlang/swift-source-compat-suite](https://github.com/swiftlang/swift-source-compat-suite) [1](https://github.com/swiftlang/swift-source-compat-suite/commits): Add swiftly as compat project (#1086)

* add swiftly as compat project

* pin swiftly to 5.10
- [tbxark/mail2telegram](https://github.com/tbxark/mail2telegram) [1](https://github.com/tbxark/mail2telegram/commits): fix: Hide NavBar on desktop Telegram clients

On macOS and tdesktop, Telegram already provides its own header and back button, so rendering an empty NavBar inside the page is redundant. A new `showBar` prop on NavBar conditionally skips rendering the visual bar while keeping the Telegram-native back button handler active.