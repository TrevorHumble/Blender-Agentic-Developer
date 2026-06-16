# Issue #0022 — Headless Blender test harness (graduates #0017)

**Type:** ready. **Category:** testing infrastructure.
**Depends on:** #0007 (Blender skills), #0018 (the first add-on with `bpy` code).
**Blocks:** none.
**Touches:** `tests/run_pure.py` (new), `tests/run_headless.py` (new), `tests/run_tests.ps1` (new),
`DESIGN.md`, `issues/0017-headless-blender-test-harness.md`, `issues/0009-future-work-backlog.md`.

## User story
As the operator relying on the pipeline's quality gates, I need a one-command way to run an add-on's
tests — both the bpy-free geometry logic and the bpy-dependent operator — without opening the Blender
GUI, so that `reviewer-pr`'s "tests must pass" check is real for the Blender domain and the same command
can run in CI.

## Background
Graduates #0017. Headless Blender 5.1 is installed at
`C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`, and `blender --background --python <script>`
runs bpy code and exits non-zero on an unhandled error — verified live (a bpy test of the bevel add-on
produced 8 bezier points headlessly, exit 0). The harness uses a dependency-free assertion runner (no
`pytest`/`pip` install, keeping it in-license and reproducible): pure-logic tests run in plain Python,
bpy tests run under `blender --background --python`. The split (bpy-free geometry vs bpy operator) is the
one #0017 requires; the bevel add-on already isolates `rounded_corner` as bpy-free.

## Acceptance criteria
1. **Given** the new file `tests/run_pure.py`, **When** a reader greps it, **Then** it imports the
   add-on's bpy-free `rounded_corner` function WITHOUT importing `bpy`, asserts on a known corner (the
   90° case → tangent points `(0.6, -1.0, 0.0)` and `(1.0, -0.6, 0.0)`), and calls `sys.exit(1)` on any
   failure (contains the literals `rounded_corner`, `sys.exit(1)`, and does NOT contain the literal
   `import bpy`).
2. **Given** the new file `tests/run_headless.py`, **When** a reader greps it, **Then** it `import bpy`,
   registers the add-on, builds a cyclic POLY square, runs `curve.bevel_bezier_corners`, asserts the
   result is a cyclic `BEZIER` spline with `8` bezier points, and calls `sys.exit(1)` on any failure
   (contains the literals `import bpy`, `curve.bevel_bezier_corners`, `BEZIER`, and `sys.exit(1)`).
3. **Given** the new file `tests/run_tests.ps1`, **When** a reader greps it, **Then** it runs
   `tests/run_pure.py` with plain Python and `tests/run_headless.py` with
   `blender --background --python` (contains the literals `run_pure.py`, `run_headless.py`,
   `--background`, and `--python`), and it exits non-zero if EITHER test process exits non-zero (contains
   the literal `exit 1`).
4. **Given** the harness, **When** the orchestrator runs `tests/run_tests.ps1`, **Then** both test
   processes exit 0 and the runner prints a pass marker and exits 0. (Orchestrator verification, recorded
   in BUILDLOG — a runtime behavioral check, not a formal AC.)
5. **Given** `DESIGN.md` after implementation, **When** a reader greps it, **Then** it documents the
   harness with the literals `run_tests.ps1`, `--background`, and `dependency-free` (the no-pip design).
6. **Given** `issues/0017-headless-blender-test-harness.md` after implementation, **When** a reader greps
   it, **Then** it contains the literal `Graduated to #0022`.
7. **Given** `issues/0009-future-work-backlog.md` after implementation, **When** a reader greps the B2
   entry, **Then** it contains the literal `headless harness ready (#0022)` (so the CI item knows its
   dependency is met).

## Implementation plan
1. `tests/run_pure.py`: import the add-on's `rounded_corner` from `addons/bevel_bezier_corners.py` via a
   bpy-free path (load only that function, e.g. exec the module text up to the bpy import, or import the
   symbol without triggering `import bpy` — simplest: read the file and `exec` the `rounded_corner` def in
   an isolated namespace). Assert the 90° corner case. `sys.exit(1)` on failure, print a marker and
   `sys.exit(0)` on success. No `import bpy`.
2. `tests/run_headless.py`: `import bpy`, load + `register()` the add-on, build a cyclic POLY square,
   run the operator at radius 0.4, assert cyclic BEZIER with 8 points. `sys.exit(1)` on failure.
3. `tests/run_tests.ps1`: run `python tests/run_pure.py`; run
   `& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --background --python tests/run_headless.py`;
   capture both exit codes; if either is non-zero, write a failure line and `exit 1`; else print a pass
   marker and `exit 0`. (Resolve the Blender path robustly; allow a `$env:BLENDER_EXE` override.)
4. Document in `DESIGN.md`; graduate #0017 (`Graduated to #0022`) and annotate B2 in #0009.
5. Run `tests/run_tests.ps1` and record the result in BUILDLOG (AC4).

## Out of scope
- A coverage-percentage gate (the dependency-free runner reports pass/fail; a coverage number needs
  `coverage.py` under Blender's Python — a follow-up for the CI issue).
- Wiring this into GitHub Actions (that is B2 / a separate CI issue).
