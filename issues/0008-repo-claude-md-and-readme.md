# Issue #0008 — Repo CLAUDE.md + README (Finalize)

**Type:** documentation. **Depends on:** #0001–#0007 (it indexes the built system).
**Blocks:** nothing (front door).

## User story
As a newcomer (human or agent) opening this repo, I need a README that orients me and a CLAUDE.md
that tells an agent how to operate here, so that I can engage the system without reading every file.

## Deliverables
- `CLAUDE.md` (repo root) — the orchestrator's operating rules, loaded every session.
- `README.md` (repo root) — the human-facing front door.

## Source material (conform / index)
- `standards/documentation-standards.md` (both files conform).
- `DESIGN.md`, `PLAN.md`, and the built `standards/`, `skills/`, `agents/` directories — index them.

## Acceptance criteria
CLAUDE.md:
1. States the system in one line and that the product owner (Trevor) is out of the operational loop;
   the adversarial agents are the gate.
2. Describes the pipeline as an ordered list (issue → review → implement → PR → review → commit).
3. States the model policy: spawned agents are `sonnet` now; `opus` is the upgrade path; orchestrator is Opus.
4. States the stop condition (FAIL fixed not overridden; cap 3 rounds; independent adjudicator must cite a basis).
5. Maps where things live: `standards/`, `skills/`, `agents/` (names the key files).
6. Lists the conventions: no FINAL/LAST, anti-slop, PowerShell, gh at `C:\Program Files\GitHub CLI\gh.exe`.
README.md:
7. One-paragraph statement of what the project is and links to `DESIGN.md`, `PLAN.md`, and `CLAUDE.md`.
8. A repo-layout section listing the top-level directories.
9. States build status: MVP foundation committed locally; no GitHub remote configured yet.

## Constraints
Markdown. Tight, no slop, no FINAL/LAST. Both conform to documentation-standards (consumer-POV user story line).
