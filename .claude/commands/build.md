---
description: Run the full issue-to-commit pipeline on a goal. Usage: /build <goal>
---

You are the orchestrator defined in `agents/orchestrator.md`. Follow all rules in `CLAUDE.md` and `standards/`.

This pipeline assumes the session runs on Opus. If it does not, switch with `/model` before continuing — running the orchestrator below Opus degrades decision quality. (Reviewers and the adjudicator run on Opus; the implementation agent and other spawned agents run on Sonnet — see the Model policy below.)

Run goal: $ARGUMENTS

Execute the pipeline in order: `issue → review → implement → PR → review → commit`

Steps:
1. Delegate prior-art research to `agents/researcher.md` via `skills/research-prior-art.md`. Local sources first; web search only if they do not answer. If the goal touches Blender APIs, also run `skills/blender-rag.md` against the relevant symbols.
2. Draft the issue in `issues/NNNN-*.md` using `skills/issue-create.md`, incorporating prior-art findings.
3. Spawn `agents/reviewer-issue.md` (Opus) via `skills/spawn-adversarial-review.md`. A FAIL is fixed, never overridden. Re-review with a fresh instance. If the issue is a system-level change or adds a new component, also spawn `agents/reviewer-architecture.md` (Opus) — both gates must pass before implementation begins.
4. Spawn `agents/implementation-agent.md` (Sonnet) with the passing issue and all prior-art paths.
5. Spawn the appropriate `agents/reviewer-*.md` (Opus) against the artifact. Reviewer receives only the artifact and the relevant standard — no framing, no hints. For every implementation artifact (code, agent spec, skill, or standard — not a doc-only or typo-only change), after `reviewer-pr` returns PASS, also spawn `agents/reviewer-design-philosophy.md` (Opus) — both gates must pass before merge.
6. On PASS, commit with a short message and append one line to `BUILDLOG.md`.

Stop condition — no author override: cap at 3 review rounds per artifact. After 3 rounds without PASS, spawn one independent adjudicator (Opus, clean prompt, no prior-round context). The adjudicator must cite the exact acceptance criterion or `standards/adversarial-review-protocol.md` clause for each retained blocking defect. Stylistic items are logged to `BUILDLOG.md` as follow-up issues. If still unresolved after adjudication, halt the segment, log it, and continue with independent segments.

Model policy: orchestrator = Opus; implementation agent and non-reviewer spawned agents = Sonnet; all reviewers (including adjudicator) = Opus. Set `model:` explicitly on every spawn call — never rely on defaults.
