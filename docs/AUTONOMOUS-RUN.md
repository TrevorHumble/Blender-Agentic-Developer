# Autonomous Run — working state

**Loop mechanics are canonical in `agents/orchestrator.md` → "Autonomous timed run (never-stop loop)" and
"Self-review is automatic." This file is the run's WORKING STATE — the budget, the priority queue, and the
Live log. A fresh/compacted instance reads `orchestrator.md` for the rules and this file for where it is.**

## The one rule
Time-driven, not task-driven. The run ends only when real elapsed time reaches the budget (default
**120 min**) — never because a queue emptied or work "felt done." "Done early" is not a state; it triggers
the Done-Early Cascade (see `orchestrator.md`), which refills the queue.

## North Star
Trevor directs and trusts the tool without reading code, so his time goes to his animation. The loop's job
is to enforce on itself what he is tired of enforcing on the agent. Gates must be REAL and PROVEN.

## Priority order (engine before polish)
- **P1 — The engine.** This loop + the self-timing ledger + Produce→Auto-Review, baked into
  `orchestrator.md` (done; keep verifying it holds in practice). Without it, the next session needs Trevor.
- **P2 — Product gates.** Real correctness tests (geometry values, not counts; phyllotaxis has none); the
  mutation/tamper harness that proves the tests catch deliberately-broken work, in CI, logging
  `guards caught N/N`; honesty doc fixes (kill the coverage-fiction in DESIGN.md).
- **P3 — Continuous improvement** via the Cascade until the clock runs out.

## Live log (ledger — one line per increment; a fresh instance continues from the last line)
Format: the ledger line defined in `agents/orchestrator.md` → "Autonomous timed run" (canonical there).

- **2026-06-21 — Engine built and hardened.** Plan rewritten as a time-driven never-stop loop; the engine
  was baked into `orchestrator.md` and hardened after a two-reviewer FAIL→fix (impasse-halt reconciled to
  re-enter the selector, emergency stop-list added, ledger mechanism, WRAP-window forcing, cascade-cannot-
  exit-empty, write-scope contradiction removed). Status: **NOT STARTED.** START: *(record at run start)*.
  Budget: 120 min. Next: P1 verify the engine holds → P2 product gates. Non-blocking decisions for Trevor
  (answer in chat, never stalls the run): (a) should `main` hard-require CI/PRs before merge; (b) CLAUDE.md
  "out of the operational loop" contradicts the goal — should the orchestrator surface Blender-judgment
  checkpoints to Trevor (the "final eye"), or treat his absence as total?
