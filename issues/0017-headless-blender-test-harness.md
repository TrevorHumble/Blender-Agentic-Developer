# Issue #0017 — Headless Blender test harness

**Type:** backlog. **Status:** backlog.
**Depends on:** #0007 (Blender skills). (The arrival of the first `bpy` add-on is the graduation
trigger below, not a dependency.)

## User story
As the operator relying on the pipeline's quality gates, I need add-on `bpy` code to be testable without
a human opening Blender, so that `reviewer-pr`'s "tests trace to acceptance criteria, coverage ≥ 80%"
check is real for the Blender domain instead of unenforceable.

## Background
`reviewer-pr` is supposed to check that an implementation's tests trace to its acceptance criteria and
meet a coverage bar. For `bpy` code that check is currently fiction: `bpy` cannot be imported or executed
outside Blender, so there is no way to run or measure tests on add-on logic. Until a headless harness
exists, every Blender add-on ships with its coverage gate unenforced. This also blocks CI (#0009 B2),
which assumes a runnable test+coverage toolchain.

## Acceptance criteria
1. (Deterministic gate criterion) A documented command runs an add-on's tests in headless Blender —
   `blender --background --python` driving `pytest` — and exits non-zero on any test failure, so the
   pipeline can gate on the exit code.

Graduation-spike goals (resolved when this graduates to a ready-issue; not deterministic as written):
2. The pattern separates `bpy`-dependent code (needs Blender) from pure logic (the geometry/math that
   can be unit-tested without Blender), and coverage is reported as a number the `reviewer-pr` coverage
   check can read.
3. The harness runs from the repo with no human opening the Blender GUI.

## Graduate after
The first add-on containing `bpy` code is committed to the repo (at that point there is real code to
test, the headless pattern can be pinned to a concrete example, and a research spike can resolve the open
unknowns below). Graduation opens a numbered ready-issue.

## Open unknowns for the graduation spike
- How `pytest` and a coverage tool (e.g. `coverage.py`) run under `blender --background --python` and
  where the Blender Python interpreter's site-packages live.
- The exact split boundary between `bpy`-dependent and pure-logic modules for a real add-on.
- Whether coverage under background mode counts the `bpy`-touching lines or only the pure-logic lines,
  and what coverage denominator the ≥80% bar should apply to.
