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
  exit-empty, write-scope contradiction removed). Budget: 120 min. Non-blocking decisions for Trevor
  (answer in chat, never stalls the run): (a) should `main` hard-require CI/PRs before merge; (b) CLAUDE.md
  "out of the operational loop" contradicts the goal — should the orchestrator surface Blender-judgment
  checkpoints to Trevor (the "final eye"), or treat his absence as total?

### RUN STARTED — 2026-06-21 18:15:33 (epoch 1782065733) · budget 120m · WRAP at 20:15:33 (epoch 1782072933)
- `[18:15] elapsed=0m/budget=120m | selector→DO pre-flight-arch+quality-review | next=architecture+quality review (self + 2 adversaries) then fix before P2`
- `[18:19] elapsed=4m/budget=120m | selector→DO pre-flight-review-done | next=fix-cluster: tests→harness→doc-honesty→security. Both adversaries PASS-equivalent (converged punch-list); confirmed plan P2 priority. Findings: phyllotaxis 0 tests, bevel ignores handles, no mutation harness, coverage-80% fiction, CodeQL absent, timing never real.`
- `[18:21] elapsed=5m/budget=120m | selector→DO #41-phyllotaxis-test | next=delegate phyllotaxis correctness test (golden angle + radius law + dome) to implementation-agent, then Opus review`
- `[18:26] elapsed=11m/budget=120m | selector→DO #41-phyllotaxis-test(commit) | next=commit phyllotaxis test (impl PASS + tamper-checked, Opus review PASS non-tautological), then bevel handle assertions`
