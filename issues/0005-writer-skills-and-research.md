# Issue #0005 — Writer skills + research subsystem (Layer D)

**Type:** skills + agent. **Depends on:** #0003 (skill/agent standards), #0002 (protocol).
**Blocks:** the orchestrator (it pulls these to act).

## User story
As the orchestrator, I need pull-able skills for the recurring actions I perform — writing a skill,
writing an agent, writing a doc, drafting an issue, spawning an unbiased reviewer, and commissioning
a quick prior-art check — plus a research agent to run that check, so that I act consistently
instead of improvising each time.

## Deliverables
Skills (each conforms to `standards/skill-standards.md`):
- `skills/skill-writer.md` — how to author/update a skill (apply intent not words; anti-bloat; structure).
- `skills/agent-writer.md` — how to author an agent file (single responsibility; least-privilege tools).
- `skills/write-documentation.md` — how to write a doc (consumer POV; literal/structural acceptance criteria).
- `skills/issue-create.md` — how to draft an issue (user story, Given/When/Then, plan, dependencies).
- `skills/spawn-adversarial-review.md` — how to spawn a reviewer with minimum context and zero bias.
- `skills/research-prior-art.md` — how to run a quick, time-boxed prior-art + topic check.
Agent (conforms to `standards/agent-standards.md`):
- `agents/researcher.md` — the quick research agent.

## Source material (steal / conform)
- `standards/skill-standards.md`, `standards/agent-standards.md`, `standards/documentation-standards.md`,
  `standards/issue-standards.md`, `standards/adversarial-review-protocol.md`.
- `~/.claude/skills-cloud-staging/time-bound-agents/SKILL.md` for the researcher's time/depth floor.
- The skill/agent authoring marketplace skills already used in Layer B.

## Acceptance criteria
Each skill file:
1. YAML frontmatter `name` + `description`; the description contains at least two strings in double-quotes or backticks.
2. Body under 500 lines; references detail rather than inlining it where long.
3. No banned slop words; no FINAL/LAST.
The researcher agent (`agents/researcher.md`):
4. Conforms to agent-standards: `## When to invoke` with ≥2 bullets; least-privilege tools; defined I/O contract.
5. Is time-boxed (states a few-minute / bounded-depth check) and prefers local prior art + the Blender RAG before a web search.
6. Returns a short findings document: what exists already (with links/paths), whether it is adaptable, and the standard learned.
Content-specific:
7. `skills/spawn-adversarial-review.md` enumerates the de-bias rules (give the goal not the implementation; no positive hints; plant no suspicions; minimum context) and references `standards/adversarial-review-protocol.md`.
8. `skills/skill-writer.md` states the intent-not-words and anti-bloat disciplines and references `standards/skill-standards.md`.

## Constraints
Markdown (+YAML for the agent). Tight, no slop. Each file self-contained and short.
