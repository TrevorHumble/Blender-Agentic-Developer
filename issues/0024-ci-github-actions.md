# Issue #0024 — CI on GitHub Actions (graduates B2)

**Type:** ready. **Category:** CI / automation.
**Depends on:** #0018 (add-on code), #0022 (headless harness), #0023 (eval harness), #0019 (in-license).
**Blocks:** none.
**Touches:** `.github/workflows/ci.yml` (new), `DESIGN.md`, `issues/0009-future-work-backlog.md`.

## User story
As Trevor, who cannot personally audit every change, I need the test harness and eval suite to run
automatically on every push and pull request and fail the build on any failure, so that a regression in
an add-on is caught by the repo itself rather than by me remembering to run the tests — all on GitHub
Actions under my GitHub Pro license (public repo, unlimited minutes), with no external service.

## Background
Graduates B2. The repo has a dependency-free headless test harness (#0022) and an eval suite (#0023),
both runnable via `blender --background`. CI installs free/open-source Blender into a GitHub-hosted runner
and runs: the bpy-free pure test (plain Python), the headless operator test, and the deterministic eval
suite — each gating on exit code. In-license: GitHub Actions on the public repo + the free Blender
download; NO Codecov or any hosted coverage/eval SaaS, NO non-Anthropic model.

## Acceptance criteria
1. **Given** the new file `.github/workflows/ci.yml`, **When** a reader greps it, **Then** it triggers on
   both `push` and `pull_request` (contains the literals `on:`, `push:`, and `pull_request:`).
2. **Given** the workflow, **When** a reader greps it, **Then** it downloads/installs Blender (a step that
   fetches a Blender release — contains the literal `blender` in a download/run step) and runs the headless
   operator test with the exit-code guard (contains the literals `--background`, `--python-exit-code 1`,
   and `tests/run_headless.py`).
3. **Given** the workflow, **When** a reader greps it, **Then** it runs the pure-logic test
   (`tests/run_pure.py`) and the eval suite (`evals/run_evals.py`), so all three gates run in CI.
4. **Given** the workflow, **When** a reader greps it, **Then** it contains NO reference to an external
   coverage/eval SaaS — it does NOT contain any of the literals `codecov`, `coveralls`, `braintrust`, or
   `langsmith` (the in-license guard).
5. **Given** `DESIGN.md` after implementation, **When** a reader greps it, **Then** it documents CI with
   the literals `.github/workflows/ci.yml`, `GitHub Actions`, and `public repo`.
6. **Given** `issues/0009-future-work-backlog.md` after implementation, **When** a reader greps the B2
   entry, **Then** it contains the literal `Graduated to #0024`.
7. **Given** the pushed workflow, **When** it runs on GitHub Actions, **Then** the job completes (green or
   red is a real signal, not a config error) — the orchestrator confirms the run was created and reports
   its conclusion. (Orchestrator verification, recorded in BUILDLOG — runtime check, not a formal AC.)

## Implementation plan
1. Write `.github/workflows/ci.yml`: `on: [push, pull_request]`; a single `ubuntu-latest` job that
   (a) checks out, (b) sets up Python, (c) runs `python tests/run_pure.py`, (d) downloads a Blender 5.x
   Linux build to a cached/temp dir and extracts it, (e) runs
   `<blender> --background --python-exit-code 1 --python tests/run_headless.py`, (f) runs
   `<blender> --background --python-exit-code 1 --python evals/run_evals.py`. Each step fails the job on a
   non-zero exit (default shell behaviour). Pin a concrete Blender download URL from the official
   `download.blender.org` mirror (free/open-source).
2. Do NOT add Codecov/Coveralls or any hosted service. Keep it dependency-free (no pip installs needed for
   the harness; `ruff`/coverage are a documented future option, not required here).
3. Document CI in `DESIGN.md`; graduate B2 in `issues/0009-future-work-backlog.md` (`Graduated to #0024`).
4. Push and confirm the Actions run was created; record its conclusion in BUILDLOG.

## Out of scope
- A coverage-percentage gate (needs `coverage.py` under Blender's Python; a follow-up).
- Caching the Blender download across runs (a speed optimization; first version may re-download).
- `ruff` lint/format enforcement (a clean follow-up; optional and in-license via pip, but not required).
