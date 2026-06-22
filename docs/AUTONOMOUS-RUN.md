# Autonomous Run — Plan & Working Method

**This file is the source of truth for a ~2-hour autonomous work session. A compacted/fresh instance
re-reads THIS FILE and the repo, then continues from the "Live progress log" at the bottom. No human
input is required to run it.**

---

## North Star (why any of this)

Trevor — a creator who can't read code — must be able to *direct* the building of his Blender tools and
*trust* the result without checking it, so his time goes into his animation and his master's instead of
policing AI output. (Full goal: `README.md` → "The goal".) For me, the builder of the tool, that means one
thing this session: **make a gate REAL and PROVEN.** Not documented. Not asserted. Proven, by running it.

A non-coder can only trust a gate he can't read by watching it catch work he *knows* is broken. So the
centerpiece of this run is exactly that: gates that check the actual product, and a standing harness that
*proves* they catch deliberately-broken work — the goal's "you've watched the checks catch broken work"
outcome, made real.

---

## The mandate

- ~2 hours, autonomous. Trevor set the North Star; **I decide and act. I do not wait for approval.**
- **Don't stop at roadblocks. Don't idle. Don't declare done-and-stop while time and queue remain.**
- End state: a completed, independently-reviewed, committed, pushed slice that makes a gate real and
  proven — something Trevor can open and see works — plus an updated GitHub board and a handoff note.

---

## How I work (the method — this is the point, not just the task list)

1. **Small green increments.** Each queue item is a thin slice that ends with the tree GREEN and
   COMMITTED, so progress survives any stop or compaction. Never leave the tree broken between increments.
2. **Adversarial review ALONG THE WAY, not just at the end.** Before I trust any "it works," I prove it —
   run the command, or spawn an independent agent (Opus) that doesn't share my context. System-level
   changes (standards/, agents/, CLAUDE.md, DESIGN.md, a new gate) get TWO independent reviewers; both
   must PASS. This whole session has shown fresh agents catch what I miss — so I never trust my own "done."
3. **Verify, don't assert.** "Done / works / passes / green" must be backed by command output or an
   independent check pasted into the log — never my say-so. BUILDLOG stays factual, no self-congratulation.
4. **Fix-for-good rule (the most important one).** When I find a defect — mine or the system's — I fix the
   instance AND add the permanent guard that would have caught it: a test, a gate, a standard line. Every
   mistake becomes a standing protection so the *class* can't recur. (Example this session: the tests were
   vacuous — count-only. The instance fix is real assertions; the for-good fix is the mutation harness,
   which makes it impossible to ship a vacuous test again, because a vacuous test lets a mutation survive
   and the harness goes red.)
5. **Working/not ledger.** I keep a short running note (in the log) of what's helping and what's wasting
   time, and adjust mid-run rather than after.
6. **Roadblock protocol — never stall the whole run on one rock.** Blocked → try an alternative approach →
   timebox it (~10 min) → if still stuck, capture it as a GitHub issue, route around it, and keep moving on
   other queue items. A blocked item is parked, not a reason to stop.
   - *Pre-solved known roadblock:* Blender isn't runnable locally. So everything I build targets the
     **bpy-free pure functions** (where the real geometry math lives) which run in plain Python locally;
     the bpy/headless parts run in CI. No local Blender is NOT a blocker.
   - *CI latency:* I never wait idle for CI. I start the next increment while CI runs; I'm notified when it
     finishes.
7. **No-approval rule.** I act on judgment inside the North Star and the out-of-scope fences. Genuinely
   irreversible, out-of-scope, or direction-changing decisions I write as a one-line note in the handoff
   and keep working — I do not block the run on them. (E.g., "should main require PRs" is a direction
   decision: I note it, I don't stop.)
8. **Pacing so I don't stop.** Timeboxed phases with checkpoints (below). Finish an item early → pull the
   next. Reserve the last ~15 min for wrap-up: final independent review of the whole slice, board update,
   BUILDLOG line, and updating this file's log + handoff. If behind, drop the stretch items, never the
   proof or the review.

---

## This session's work queue (ordered; every item builds the TOOL, serves the North Star)

Each item: **build → prove (run it / independent review) → fix-for-good → commit green → update board → next.**

### Q1 — Real correctness tests (serves Goal 1 "checked automatically", Goal 2 "nothing quietly breaks"; GH#41)
The tests today check point *counts*, not whether the geometry is *correct* — a visibly-wrong fillet
passes. Phyllotaxis has zero tests.
- Add coordinate + handle assertions for `rounded_corner` at several angles (30/90/150°) and the
  overlap-clamp/colinear guards, against an independently-derived expected value.
- Add `phyllotaxis_points` assertions: golden-angle spacing (137.5078°), count→vertex count, `dome=0`→flat.
- All target the bpy-free pure functions → runs locally via `python tests/run_pure.py`.
- **Done when:** the new assertions run green locally. **Proof:** paste the run output in the log.

### Q2 — Mutation/tamper harness: the smoke detector (serves Goal 1 "watched it catch broken work" — the trust-by-evidence outcome; GH#42). CENTERPIECE.
A standing harness that programmatically mutates the geometry in a catalog of known-bad ways (sign flip,
drop the overlap clamp, change the `4.0/3.0` arc constant, break the golden angle), runs the test+eval
suite against each mutant, and asserts **every** mutant is CAUGHT (suite goes red). Logs `guards caught
N/N`. If any mutant survives → the harness FAILS (that's a vacuous test exposed). Wire it into CI.
- This is a NEW GATE = system-level → TWO independent reviewers before commit.
- **Done when:** harness runs, catches N/N, logs it, and is in CI. **Proof:** paste `N/N` output; show the
  CI step. Tamper-test the harness itself once (make a test weak, confirm a mutant survives and the harness
  goes red, then restore) — proving the harness has teeth.

### Q3 — Honesty fix: docs tell the truth (serves trust; GH#44)
We are deliberately NOT doing coverage-% (vanity metric) and ARE doing mutation testing. So the docs must
stop claiming a coverage gate that doesn't exist.
- Remove/correct the "≥80% coverage" fiction in `DESIGN.md`; state the real gate (mutation harness +
  correctness tests). Reconcile the eval-stack self-contradiction. Light de-slop of any
  self-congratulatory BUILDLOG tone I touch.
- System-level (DESIGN.md) → independent review.
- **Done when:** `grep` shows the coverage-fiction gone and the real gate named. **Proof:** the greps.

### Q4 — STRETCH: make CI an actual gate (branch protection requiring the CI checks)
Enable required status checks on `main` so broken geometry can't land. NOTE: this changes the
straight-to-main workflow and touches the open PR-flow direction decision — so I enable it at the END,
and if it would block the run I instead file it and note it. Don't let it stall anything.

### Q5 — STRETCH: context-isolate the PR reviewer (serves Goal 1 "confirm it's what you meant")
Edit `agents/reviewer-pr.md` so the reviewer receives code + acceptance criteria + standards but NOT the
implementation plan — the independence improvement we designed. System-level → two reviewers. Only if Q1–Q3
are done and green with time left.

---

## Timeline (~120 min) — checkpoints, never skip proof/review

- **0:00–0:10 — Orient.** Re-read this file + the North Star; read the current `tests/`, `evals/`,
  `addons/*.py`; confirm the queue still fits. Update log.
- **0:10–0:40 — Q1** (real correctness tests): build → run → independent review → fix → commit → board. Checkpoint.
- **0:40–1:25 — Q2** (mutation harness, centerpiece): build → run (N/N) → wire CI → TWO reviewers →
  fix-for-good → commit → board. Checkpoint.
- **1:25–1:45 — Q3** (honesty fixes): edit → review → commit → board. Checkpoint.
- **1:45–2:00 — Wrap.** Stretch (Q4/Q5) only if green + time. Then: final independent review of the whole
  slice; close GH#41/#42, update GH#44; one factual BUILDLOG line; update this file's Live log + write the
  handoff; `git push`. Leave the tree green and a completed thing.

At each checkpoint: update the log; if behind, drop a stretch item, never the proof or the review; if an
independent reviewer FAILs something, fix-and-re-review (never override).

---

## Definition of "a completed thing, ready to go" (end of run)
The test/eval gates now **check the actual product** (not counts), and a **standing mutation harness proves
they catch deliberately-broken work**, running in CI, with a `guards caught N/N` line Trevor can read — and
the docs tell the truth about it. That is the goal's "trust by evidence" outcome, made real and provable by
a non-coder. Board updated; BUILDLOG line added; this file's handoff written.

---

## Live progress log (update after every increment — a fresh instance continues from here)

- **2026-06-21 — Plan written.** Status: NOT STARTED. Next action: Orient phase (0:00–0:10), then Q1.
  Queue: Q1 correctness tests → Q2 mutation harness (centerpiece) → Q3 honesty fixes → (stretch Q4 CI gate,
  Q5 reviewer context-isolation). Known roadblock pre-solved: no local Blender → target bpy-free functions;
  headless runs in CI. Decisions surfaced for Trevor (do NOT block on these): (a) whether `main` should
  require PRs/CI as a hard gate; (b) the CLAUDE.md "out of the operational loop" line contradicts the new
  goal (Trevor is the director/final eye) — needs his reconciliation.
