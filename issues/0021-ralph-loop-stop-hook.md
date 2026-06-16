# Issue #0021 — Ralph-loop enforcement via a Claude Code Stop hook (graduates B3)

**Type:** ready. **Category:** execution / enforcement.
**Depends on:** #0006 (orchestrator), #0020 (soft cap + severity gate — the legitimate-exit conditions).
**Blocks:** none.
**Touches:** `.claude/hooks/review-gate.ps1` (new), `.claude/settings.json` (new),
`issues/0009-future-work-backlog.md`, `DESIGN.md`.

## User story
As the operator who needs the review loop to run to completion without me watching, I need a Stop hook
that refuses to let a `/build` run end before the loop reaches a legitimate exit and re-injects the task
when it tries to quit early, so that the Ralph loop is enforced by tooling rather than by an agent
remembering to keep going.

## Background
Research (Claude Code hooks reference) confirms the Stop hook can block a turn from ending by emitting
`{"decision":"block","reason":"..."}` on stdout (exit 0); the `reason` is fed back to the model as its
next instruction. The hook reads stdin JSON including `stop_hook_active` (the infinite-loop guard). The
legitimate exits are defined by #0020: a reviewer `PASS`, or the severity adjudicator writing
`EXIT_AUTHORIZED` because all remaining defects are inconsequential. The hook stays a pure LOCAL check —
it only reads a verdict artifact the loop writes — so no model call happens inside the hook and the
in-license constraint holds. A counter-file iteration cap is the backstop against a model that never
writes a verdict.

## Acceptance criteria
1. **Given** the new file `.claude/hooks/review-gate.ps1`, **When** a reader greps it, **Then** it
   contains the literal `stop_hook_active`.
2. **Given** the script, **When** a reader greps it, **Then** it contains each literal: `PASS`,
   `EXIT_AUTHORIZED`, `"decision"`, `"block"`, and `reason`.
3. **Given** the script, **When** a reader greps it, **Then** it contains each literal: `MAX_ITERS` and
   `CAP_HIT`.
4. **Given** the new file `.claude/settings.json`, **When** a reader greps it, **Then** it contains each
   literal: `"Stop"`, `"type": "command"`, `review-gate.ps1`, and `"shell": "powershell"`.
5. **Given** the script, **When** a reader greps it, **Then** it contains, in source order (verifiable by
   line number), the four marker comments `# CHECK 1: stop_hook_active`, `# CHECK 2: MAX_ITERS`,
   `# CHECK 3: verdict`, and `# CHECK 4: block` — so the guard and cap precede the block emission.
6. **Given** `issues/0009-future-work-backlog.md` after implementation, **When** a reader greps the B3
   entry, **Then** it contains the literal `Graduated to #0021`.
7. **Given** `DESIGN.md` after implementation, **When** a reader greps it, **Then** it documents the
   stop-hook enforcement with the literals `review-gate.ps1`, `EXIT_AUTHORIZED`, and `stop_hook_active`.

## Orchestrator verification (recorded, not a formal acceptance criterion)
After implementation the orchestrator runs the script against three simulated Stop-hook stdin payloads
and records the outcome in `BUILDLOG.md`: (a) no verdict file + `stop_hook_active:false` → prints a
block-decision JSON; (b) a verdict file containing `EXIT_AUTHORIZED` → no block, exit 0; (c)
`stop_hook_active:true` → no block, exit 0. (This is a runtime behavioral check; the formal ACs above are
all structural reads of the produced artifact, per issue-standards.)

## Implementation plan
1. Write `.claude/hooks/review-gate.ps1` with four marker comments in source order — `# CHECK 1:
   stop_hook_active`, `# CHECK 2: MAX_ITERS`, `# CHECK 3: verdict`, `# CHECK 4: block`: read stdin JSON;
   (CHECK 1) if `stop_hook_active` is true → exit 0; (CHECK 2) read the iteration counter, increment it,
   and if it exceeds `MAX_ITERS` → allow stop (exit 0) and write the token `CAP_HIT`; (CHECK 3) read the
   verdict artifact (e.g. `.review_state/verdict.txt` under `cwd`); if it contains `PASS` or
   `EXIT_AUTHORIZED` → exit 0; (CHECK 4) otherwise emit `{"decision":"block","reason":"<imperative
   instruction naming the exit conditions and the verdict path>"}` and exit 0. PowerShell syntax.
2. Write `.claude/settings.json` registering the `Stop` command hook (`"shell": "powershell"`,
   `${CLAUDE_PROJECT_DIR}/.claude/hooks/review-gate.ps1`).
3. Document the enforcement in `DESIGN.md` (ties the hook's legitimate-exit tokens to #0020's PASS /
   EXIT_AUTHORIZED), and graduate B3 in `issues/0009-future-work-backlog.md` with `Graduated to #0021`.
4. Run the **Orchestrator verification** below: pipe the three simulated stdin payloads to the script and
   record the outputs in `BUILDLOG.md`. The verdict file used in payload (b) is a hand-authored test
   fixture, decoupled from the deferred orchestrator-writes-the-verdict wiring (Out of scope).

## Out of scope
- Wiring the orchestrator to actually WRITE the verdict artifact at each step (a follow-up; this issue
  delivers the enforcement hook and its contract, testable in isolation).
- Anti-gaming hardening beyond the iteration cap (the backlog B3 deferred this).
