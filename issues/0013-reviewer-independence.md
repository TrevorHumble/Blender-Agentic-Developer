# Issue #0013 — Reviewer model independence

**Type:** standards / architecture (ready). **Status:** ready.
**Depends on:** #0003 (agent-standards), #0006 (orchestrator). **Blocks:** none.
**Touches:** `standards/agent-standards.md`, `DESIGN.md`, `CLAUDE.md`, `agents/reviewer-*.md`, `agents/orchestrator.md`, `.claude/commands/build.md`, `PLAN.md` (added during implementation — the original dependency map omitted these three files, which are where the reviewer spawn model is actually configured and documented).

## User story
As the orchestrator that configures each spawned reviewer, I need reviewers to run on a different
model from the implementation agent, so a reviewer does not inherit the implementer's correlated
blind spots.

## Background
The DESIGN.md adversarial review (2026-06-15) found the implementation agent, every reviewer, and the
adjudicator all run on the same model tier (Sonnet). Two instances of the same model share
training-induced blind spots, so the errors the author makes are the ones the reviewer misses. The
`adversarial-agents` source skill calls for a reviewer to be "ideally a different model/identity than
whoever produced the work."

## Acceptance criteria
1. `standards/agent-standards.md` contains the literal string `different model from the implementer`
   and the literal string `correlated blind spots` (the independence rule and its rationale).
2. Both `DESIGN.md` and `CLAUDE.md` contain the identical literal sentence
   `Reviewers run on a different model from the implementer.` (so the two files cannot diverge).
3. Each `agents/reviewer-*.md` file either has a `model:` value different from the `model:` value in
   `agents/implementation-agent.md`, or contains the literal string `multi-reviewer majority`.

## Implementation plan
1. Evaluate and choose one mechanism: (a) reviewers on a different family/tier than the implementer;
   (b) implementer Sonnet / reviewers Opus; (c) multi-reviewer majority with model diversity. Record the
   choice and the reasoning.
2. Update `standards/agent-standards.md` with the independence rule (criterion 1).
3. Update the model-by-role policy in `DESIGN.md` and `CLAUDE.md` (criterion 2).
4. Update the `agents/reviewer-*.md` `model:` fields (criterion 3); verify against all criteria.

## Out of scope
Implementing CI; changing the implementer's model; the cost tradeoff of a more expensive reviewer
(note it, decide separately).
