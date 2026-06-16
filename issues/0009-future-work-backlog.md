# Issue #0009 — Future-work backlog

**Type:** backlog. **Status:** backlog — none of these are ready to implement.

## What this is
A backlog of deferred work. Each entry is a **backlog item**, not a ready-to-implement issue. A
backlog item captures intent and a testable desired outcome; it deliberately has **no Haiku-ready
implementation plan**, because the feature has not been researched or designed yet — writing one now
would be fabrication. Before any item is implemented it **graduates** to its own numbered ready-issue
that meets full `standards/issue-standards.md`, starting with a research spike via `agents/researcher.md`.
A backlog item is never implemented in place.

## The backlog bar (what `reviewer-issue` judges these against)
Each entry has: a consumer-POV user story; a testable desired outcome; a `Depends on` line; and a
`Graduate after` line naming a **deterministic** condition that must hold before implementation.
Backlog entries omit the `Blocks` and `Touches` fields that a ready-issue requires, because the
artifacts and file paths do not exist yet — those fields are populated at the graduate step when the
paths are known. This is the only relaxation from the ready bar, and it is the reason these are
backlog, not ready.

---

## B1 — reviewer-architecture agent + even/odd routing
**User story:** As an issue author whose issue will be routed to architectural review, I need that
review to exist with a clear bar, so my issue's structural fit is judged consistently.
**Desired outcome:** An architecture reviewer exists that, given an issue and `DESIGN.md`, returns
PASS/FAIL and FAILs any issue that contradicts the documented architecture or duplicates an existing
component. (Even/odd routing is a mechanism decided during graduation, not part of this outcome.)
**Depends on:** a stable `DESIGN.md`. **Graduate after:** a research spike defines which architectural-fit
checks are objectively testable.

**Superseded by #0016** (regular architectural + design-philosophy review, trigger-based cadence).

## B2 — CI/CD enforcement
**User story:** As Trevor, who cannot personally audit every change, I need quality enforced
automatically rather than by an agent remembering to check.
**Desired outcome:** ruff lint+format, pytest with a ≥80% coverage gate, and pre-commit hooks run on
every commit and block the commit on failure.
**Depends on:** the first Python code artifacts existing. **Graduate after:** a research spike on the
Python/Blender add-on toolchain, and headless harness ready (#0022).

## B3 — Ralph-loop stop-hook automation
**User story:** As Trevor, who needs the review loop to run to completion autonomously, I need it
enforced by a stop hook rather than by manual discipline.
**Desired outcome:** A stop hook intercepts any attempt to exit the loop before the reviewer returns
PASS (or the 3-round cap) and re-injects the task — verifiable by a test that forces an early exit and
asserts the loop continued. Specific anti-gaming guards are out of scope for this backlog entry.
**Depends on:** the built stop-condition, and Claude Code stop-hook support (an external capability,
not a repo artifact). **Graduate after:** a research spike on Claude Code stop-hook mechanics.

Graduated to #0021

## B4 — Blender add-on development standards
**User story:** As an implementation agent building a Blender add-on, I need a standard for what a good
add-on is so my output is idiomatic and testable.
**Desired outcome:** `standards/blender-addon-standards.md` exists with sections on add-on structure,
`bpy` registration, the `blender_manifest.toml` extension format, and headless testing.
**Depends on:** the Blender RAG (`C:\Users\thumb\BlenderRag`). **Graduate after:** a RAG + web research
spike on Blender 5.x add-on best practices.

## B5 — documentation-enforcement agent
**User story:** As Trevor, whose `DESIGN.md` drifted during this very build, I need an agent that catches
stale docs so the drift does not recur.
**Desired outcome:** A documentation-currency reviewer agent exists that, given a PR diff and
`standards/documentation-standards.md`, returns PASS/FAIL and FAILs when a file under a currency
trigger was changed without its corresponding doc updated.
**Depends on:** `standards/documentation-standards.md` (built). **Graduate after:** the currency-check
rule set is designed.

## B6 — comment-review agent
**User story:** As a reviewer, I need code comments held to the why-not-what, one-line, anti-slop standard.
**Desired outcome:** A `reviewer-comments` agent exists that FAILs a comment that describes what the code
does, exceeds one line, or contains a quotable slop word.
**Depends on:** the first code artifacts, and a written comment standard. **Graduate after:** the comment
standard is written.

## B7 — resilience & reliability testing agent
**User story:** As Trevor, I need the pipeline stress-tested so failure modes surface before they hit real work.
**Desired outcome:** An agent that produces a structured report (one finding per section: failure mode
tested, result, PASS/FAIL) covering at least three modes — a reviewer that always passes, a runaway loop,
and a biased spawn.
**Depends on:** the full pipeline (issues #0002–#0008, built). **Graduate after:** a research spike on
agentic-system reliability testing.

## B8 — GitHub remote + live github-write integration
**User story:** As Trevor, I need the local repo pushed to GitHub so the work is backed up and shareable.
**Desired outcome:** A remote is configured under TrevorHumble, commits push, and `skills/github-write.md`
creates real issues/PRs via `gh`.
**Depends on:** the repo name/URL (open item). **Graduate after:** Trevor provides the repo name/URL as a
committed file (e.g., `config/github.txt`); the existence of that file is the deterministic trigger — not
a verbal approval.

---

*(The ready-vs-backlog tier itself is not a backlog item — it is small and ready, so it lives as a
ready-issue: see `issues/0010-issue-tiers.md`.)*
