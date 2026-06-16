# Issue #0003 — Authoring standards (Layer B)

**Type:** standards. **Depends on:** #0002 (reviewed against documentation-standards + protocol).
**Blocks:** reviewer agents (Layer C) and writer skills (Layer D).

## User story
As a reviewer or author of a skill, an agent, or an issue, I need written standards that define
what "good" is for each, so that I can produce or judge one without guessing.

## Deliverables
- `standards/skill-standards.md`
- `standards/agent-standards.md`
- `standards/issue-standards.md`

## Source material (steal)
- `C:\Users\thumb\.claude\plugins\marketplaces\claude-plugins-official\plugins\skill-creator\skills\skill-creator\SKILL.md`
- `C:\Users\thumb\.claude\plugins\marketplaces\claude-plugins-official\plugins\plugin-dev\skills\skill-development\SKILL.md`
- `C:\Users\thumb\.claude\plugins\marketplaces\claude-plugins-official\plugins\plugin-dev\skills\agent-development\SKILL.md`
- This repo's issue #0001 and #0002 (the Haiku-bar and literal-anchor lessons) and `DESIGN.md` §Standards.
- Conform to `standards/documentation-standards.md`.

## Acceptance criteria (checkable by an agent reading the produced files)
skill-standards.md:
1. The literal phrase `anti-bloat` appears, and the file states that updating a skill applies the
   author's intent rather than transcribing the user's words.
2. Names the role of a skill's description/trigger metadata (when the skill fires).
3. States a progressive-disclosure rule (keep the main file short; push detail to references).
4. Provides a checkable PASS/FAIL checklist a skill reviewer can apply (at least four objective items).

agent-standards.md:
5. States single-responsibility scoping for an agent.
6. States least-privilege tool access (an agent gets only the tools it needs).
7. Requires a defined input/output contract for each agent.
8. States the model-tier guidance (which tier for which job) and that a reviewer's prompt must carry
   no task-specific bias.
9. Provides a checkable PASS/FAIL checklist an agent reviewer can apply (at least four objective items).

issue-standards.md:
10. Requires a user story from an `end-consumer` POV.
11. Requires acceptance criteria as `Given/When/Then` testable by another agent.
12. Defines the Haiku bar as a `clarity heuristic` and states the implementer is a Sonnet agent.
13. Requires a dependency map with `Depends on`, `Blocks`, and `Touches`.
14. States that for a documentation issue, acceptance criteria must reduce to `literal` string or
    structural checks (the issue #0001 lesson).

## Constraints
Markdown only, tight, no slop. Each file self-contained and conforms to documentation-standards
(including its own consumer-POV user-story line). No FINAL/LAST/v2_final.
