# Issue #0023 — Eval harness: deterministic geometry evals + Claude-as-judge

**Type:** ready. **Category:** evaluation infrastructure.
**Depends on:** #0018 (the add-on under eval), #0022 (the headless harness), #0019 (in-license stack).
**Blocks:** none.
**Touches:** `evals/cases.py` (new), `evals/run_evals.py` (new), `evals/judge.md` (new),
`evals/README.md` (new), `DESIGN.md`.

## User story
As the operator who needs to know an add-on actually works before trusting it, I need an eval harness
that scores an add-on against a suite of cases — deterministic geometric properties checked headless,
plus a Claude-as-judge pass for the subjective "does it look right" question — so that quality is
measured and regressions are caught, all within my GitHub Pro + Anthropic Max license.

## Background
The repo now has a working headless harness (#0022) and a real add-on (#0018). Evals are the next layer:
move from "a test passes" to "the add-on scores N/M on a graded suite." Two complementary eval modes,
both in-license (no external eval SaaS, no non-Anthropic model):
- **Deterministic geometry eval** — run the add-on headless over a suite of input cases and assert
  measurable geometric properties (point counts, fillet setback, closedness preserved, colinear corners
  skipped, large-radius clamping). Machine-scored, exit-code gated.
- **Claude-as-judge eval** — for the subjective axis (does the rounded curve look clean), capture a
  viewport screenshot and have an Opus agent judge it against a written rubric. This is the MCP-side eval
  (the agent drove Blender; Claude judges the result).

## Acceptance criteria
1. **Given** the new file `evals/cases.py`, **When** a reader greps it, **Then** it defines a list named
   `EVAL_CASES` where each case has the literal keys `name`, `build`, and `checks` (a case names its
   input-construction and a list of property checks), and includes at least these case names as literals:
   `square_r04`, `triangle`, `open_polyline`, `colinear_skipped`, and `large_radius_clamped`.
2. **Given** the new file `evals/run_evals.py`, **When** a reader greps it, **Then** it `import bpy`,
   imports `EVAL_CASES` from `cases`, runs each case's `build` + the add-on operator headless, evaluates
   each case's `checks`, prints a per-case PASS/FAIL line and a final `EVAL SCORE: <passed>/<total>` line
   (contains the literals `EVAL_CASES`, `curve.bevel_bezier_corners`, and `EVAL SCORE:`), and calls
   `sys.exit(1)` if any case fails.
3. **Given** the new file `evals/judge.md`, **When** a reader greps it, **Then** it documents the
   Claude-as-judge eval with the literals `get_viewport_screenshot`, `rubric`, and `Opus`, and states the
   judge returns a `PASS`/`FAIL` against the rubric (no external model — `Claude-as-judge`).
4. **Given** the new file `evals/README.md`, **When** a reader greps it, **Then** it explains both eval
   modes and contains the literals `deterministic`, `Claude-as-judge`, and `in-license`, and the command
   to run the deterministic suite (`blender --background --python evals/run_evals.py`).
5. **Given** `DESIGN.md` after implementation, **When** a reader greps it, **Then** it documents the eval
   layer with the literals `EVAL SCORE:`, `Claude-as-judge`, and `evals/run_evals.py`.
6. **Given** the eval suite, **When** the orchestrator runs `blender --background --python evals/run_evals.py`,
   **Then** it prints an `EVAL SCORE:` line and exits 0 only if every case passes. (Orchestrator
   verification, recorded in BUILDLOG — runtime behavioral check, not a formal AC.)

## Implementation plan
1. `evals/cases.py`: define `EVAL_CASES`, each a dict `{name, build, checks}`. `build` is a callable that
   constructs an input curve object (square, triangle, open polyline, colinear, large-radius) and returns
   it; `checks` is a list of callables `(obj) -> (bool, str)` asserting a geometric property. Cases:
   `square_r04` (→ 8 cyclic BEZIER points), `triangle` (→ 6 points), `open_polyline` (endpoints kept,
   interior filleted), `colinear_skipped` (a near-straight vertex is not split into two), `large_radius_clamped`
   (radius bigger than the edges still yields a valid non-self-overlapping result). Pure-ish: only the
   `build` step touches bpy.
2. `evals/run_evals.py`: `import bpy`, register the add-on (`runpy.run_path` the add-on file), import
   `EVAL_CASES`, run each case (build → `bpy.ops.curve.bevel_bezier_corners` → checks), print per-case
   results and `EVAL SCORE: P/T`, `sys.exit(1)` if any check fails.
3. `evals/judge.md`: document the Claude-as-judge eval — capture `get_viewport_screenshot`, hand it to an
   `Opus` agent with a `rubric` (smooth tangent continuity, no kinks, fillet radius visually consistent),
   judge returns `PASS`/`FAIL`. Note it is `Claude-as-judge`, in-license.
4. `evals/README.md`: explain `deterministic` + `Claude-as-judge` modes, the run command, and that it is
   `in-license`.
5. Document the eval layer in `DESIGN.md`; run the deterministic suite and record the score in BUILDLOG.

## Out of scope
- Wiring evals into CI (that is the CI issue).
- Auto-running the Claude-as-judge pass in headless CI (judging needs the Anthropic subscription in the
  loop; documented as an orchestrator/agent step, not a headless script).
- Evals for add-ons that do not exist yet.
