# Issue #0006 — Execution agents (Layer E)

**Type:** agents. **Depends on:** #0002–#0005 (it references the standards, skills, and reviewers).
**Blocks:** running the pipeline on real work.

## User story
As Trevor, who is out of the operational loop, I need an orchestrator agent that runs the whole
pipeline by the rules and an implementation agent that builds a passing issue, so that work proceeds
autonomously and to standard without me in the loop.

## Deliverables
- `agents/orchestrator.md` — drives issue → review → implement → PR → review → commit.
- `agents/implementation-agent.md` — builds the artifact for a passing issue.

## Source material (conform)
- `standards/agent-standards.md` (both files conform to it).
- `standards/adversarial-review-protocol.md`, `standards/issue-standards.md`.
- The Layer D skills (`issue-create`, `spawn-adversarial-review`, `research-prior-art`, the writers)
  and the Layer C reviewer agents — the orchestrator references these by path.
- `skills/blender-rag.md` and `skills/blender-connect.md` will exist after Layer F; reference by name.

## Acceptance criteria
orchestrator.md:
1. Conforms to agent-standards (frontmatter `name`+`description` with ≥2 quoted trigger strings;
   `## When to invoke` with ≥2 bullets; defined I/O contract).
2. Describes the pipeline as an ordered list of stages from issue creation through commit.
3. States that it spawns reviewers with minimum context and never frames or biases them (references
   `skills/spawn-adversarial-review.md` and the protocol).
4. Encodes the stop condition: a FAIL is fixed not overridden; cap 3 review rounds; after 3 an
   INDEPENDENT second reviewer adjudicates which defects truly block; the author never decides "nitpick".
5. States the model policy: spawned agents are `sonnet` now, `opus` is the upgrade path.
6. States research-first: prefer local prior art and the Blender RAG before web (references
   `skills/research-prior-art.md` / `agents/researcher.md`).
implementation-agent.md:
7. Conforms to agent-standards; states it builds only a PASSING issue and gets full handoff context.
8. States it must consult the Blender RAG (`search_blender_docs`) before writing any `bpy` Blender code,
   and follows the repo standards (naming, comments, anti-slop).
9. Defined I/O contract: input = the issue + handoff; output = the artifact + a confirmation, no self-approval.

## Constraints
Markdown + YAML. Tight, no slop, no FINAL/LAST. Each file self-contained and short.

---

**Superseded (2026-06-16) — model policy.** Criterion 5 records the model policy as it stood when this issue was built (reviewers on Sonnet, "opus is the upgrade path"). That upgrade happened: the live policy is reviewers-on-Opus, a different model from the implementer, per #0013; see `DESIGN.md` model-by-role. Appended, not a rewrite.
