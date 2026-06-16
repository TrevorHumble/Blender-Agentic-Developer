# Issue #0004 — Reviewer agents (Layer C)

**Type:** agents. **Depends on:** #0002 (protocol), #0003 (agent-standards + the target standards).
**Blocks:** the running pipeline (these gate every artifact).

## User story
As the orchestrator about to gate an artifact, I need a defined reviewer agent per artifact type, so
that I spawn a reviewer that already knows the protocol and the standard it must apply.

## Deliverables (one agent file each)
- `agents/reviewer-issue.md` — reviews an issue against `standards/issue-standards.md`.
- `agents/reviewer-pr.md` — reviews a code/doc change against its issue's acceptance criteria.
- `agents/reviewer-skill.md` — reviews a skill against `standards/skill-standards.md` (anti-bloat first).
- `agents/reviewer-agent.md` — reviews an agent against `standards/agent-standards.md`.
- `agents/reviewer-documentation.md` — reviews a doc against `standards/documentation-standards.md`.

## Source material (steal / conform)
- `standards/adversarial-review-protocol.md` — every reviewer follows it.
- `standards/agent-standards.md` — every reviewer file must conform to it.
- Each reviewer's target standard (listed above).
- Prior art: `~/.claude/plugins/.../plugin-dev/skills/agent-development/SKILL.md` for agent.md form.

## Acceptance criteria (apply to EACH of the five files)
1. YAML frontmatter with `name` and a `description` that contains at least two strings in
   double-quotes or backticks (trigger phrases).
2. A `## When to invoke` section with at least two bullet points.
3. Single responsibility: the file reviews exactly ONE artifact type (named in its role line).
4. States least-privilege tools (it reads the artifact + its standard; it does not edit or write code).
5. Defines an input/output contract: input = the artifact (minimum context) + the standard; output =
   the literal token `PASS/FAIL` plus a numbered list of specific defects citing evidence.
6. References `standards/adversarial-review-protocol.md` and instructs the reviewer to follow it
   (assume total failure, no benefit of the doubt, de-biased, no human-in-loop resolutions).
7. Names the specific target standard it judges against.
8. No FINAL/LAST and no banned slop words.

## Constraints
Markdown with YAML frontmatter. Tight. Each file self-contained and short. Conform to agent-standards.
