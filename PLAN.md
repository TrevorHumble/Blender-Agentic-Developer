# Build plan — Blender Dev Orchestrator MVP (v2)

**Status:** in progress (autonomous build). **Owner:** orchestrator (the main Opus loop).
**Last updated:** 2026-06-15. **Supersedes:** v1 (failed adversarial review — 9 defects; this is the fix).

Sequences the MVP into dependency-correct segments. Authoritative design: [DESIGN.md](DESIGN.md).

## Goal
Stand up the foundational standards, agents, and skills that let the orchestrator run its own
pipeline on real Blender work later. Trevor is out of the loop; adversarial agents are the gate.

## Bootstrap (resolves the chicken-and-egg)
The system cannot use its own committed skills before they exist. So the build is **bootstrapped**:
- **Held protocol.** Until `standards/adversarial-review-protocol.md` is committed, every reviewer
  is framed by the existing `~/.claude/skills-cloud-staging/adversarial-agents` skill (assume-total-
  failure, de-bias the setup, research-first, independence, no human-in-loop resolutions). The
  committed standard is a repo-local formalization of that skill; reviewers switch to it once it lands.
- **Direct git commits.** During the build the orchestrator commits with plain `git` (no remote).
  The `github-write` skill (built late) formalizes git/issue ops for the *running* system, not the build.
- **Direct spawning.** The orchestrator spawns reviewers directly via the Agent mechanism; the
  `spawn-adversarial-review` skill (built late) formalizes this for the running system.
- No GitHub remote operations occur during the build. Commits stay local.

## Operating rules
- **Models:** orchestrator = main Opus loop. Implementation agent and non-reviewer spawned agents
  (researcher, etc.) = Sonnet. **Reviewers = Opus**, per issue #0013 (reviewer-independence,
  2026-06-16): the MVP initially ran reviewers on Sonnet (weaker gate); #0013 resolved that
  deviation — reviewers now run on Opus, a different model from the implementer, to eliminate
  correlated blind spots. DESIGN.md and agent-standards.md reflect the final policy.
- **Research-first, cheap.** Establish the standard from the best source — local prior art first,
  then the Blender RAG, then a quick (~few-minute) web check. Don't research what prior art answers.
- **Steal good standards (prior art on this PC):**
  - `skills/blender-rag` → reuse (RAG at `C:\Users\thumb\BlenderRag`, `search_blender_docs`).
  - `skills/blender-mcp` → reuse (live Blender control).
  - `skills-cloud-staging/adversarial-agents` → adversarial protocol source.
  - `skills-cloud-staging/time-bound-agents`, `rigorous-agent-harness`, `skills/rigorous-eval` → review depth/independence.
  - marketplace `skill-creator`, `plugin-dev/skill-development`, `plugin-dev/agent-development`,
    `software-design-philosophy`, `claude-md-improver` → authoring standards.
- **Conventions:** agentic → `agents/<role>.md`; orchestrator action → `skills/<verb-noun>.md`;
  some skills are agent-called (e.g. `blender-rag`). No FINAL/LAST/v2_final. Anti-AI-slop prose.

## Per-segment process (no author override)
1. Orchestrator writes a short issue (`issues/NNNN-*.md`): user story, Given/When/Then criteria
   testable by an agent, implementation plan, dependencies, prior-art to steal, and the standard the
   artifact is reviewed against.
2. Spawn an Opus adversarial **issue reviewer** (minimum context, de-biased). Fix every blocking
   defect and re-review with a fresh reviewer. **A FAIL is fixed, never overridden by the author.**
3. Spawn a Sonnet **implementation agent** (full handoff: the issue + the prior-art files to read).
4. Spawn an Opus adversarial **artifact reviewer** against the issue's criteria + the relevant
   standard. Fix and re-review until PASS.
5. Commit the segment (direct git). Append a one-line BUILDLOG.md entry.

**Stop condition (soft cap + severity gate — superseded by #0020).** The 3-round mark is a soft cap —
a trigger, not a hard cap. At 3 rounds without PASS, spawn an independent `severity adjudicator`
(Opus, clean prompt, no prior-round context). The severity adjudicator classifies every remaining
open defect as `consequential` or `inconsequential` and cites a basis for each. Exit is authorized
only when every remaining defect is inconsequential; the loop never accepts work while a consequential
defect remains. On a consequential defect, the loop continues — fix and re-review, then re-invoke
the severity adjudicator. Impasse — a consequential defect that survives the severity gate plus 3
further fix-and-re-review rounds — halts the segment; log and continue with independent segments.
The orchestrator tracks the post-gate round count and declares the impasse. The author never decides
what is a "nitpick."

## Segment order (dependency-layered)
**Layer A — cross-cutting standards (reviewed via held bootstrap protocol):**
1. `standards/adversarial-review-protocol.md` (from `adversarial-agents` + `rigorous-eval`).
2. `standards/documentation-standards.md` (the literal-anchor-criteria lesson from issue #0001;
   from `claude-md-improver` + `software-design-philosophy`). Cross-cutting so every later doc is
   reviewed against it.

**Layer B — authoring standards (reviewed against Layer A):**
3. `standards/skill-standards.md` (anti-bloat headline; from `skill-creator` + `skill-development`),
   `standards/agent-standards.md` (from `agent-development`), `standards/issue-standards.md`.

**Layer C — reviewer agents (each reviewed against agent-standards by an independent adversary):**
4. `agents/reviewer-issue.md`, `reviewer-pr.md`, `reviewer-skill.md`, `reviewer-agent.md`,
   `reviewer-documentation.md`.

**Layer D — writer skills + research (reviewed against skill-/agent-standards):**
5. `skills/skill-writer.md`, `agent-writer.md`, `write-documentation.md`, `issue-create.md`,
   `spawn-adversarial-review.md`; `agents/researcher.md` + `skills/research-prior-art.md`
   (from `time-bound-agents`).

**Layer E — execution agents (reviewed against agent-standards):**
6. `agents/orchestrator.md` (encodes the stop-condition above), `agents/implementation-agent.md`.

**Layer F — reused + ops skills (through the pipeline, not as-is):**
7. `skills/blender-rag.md`, `blender-connect.md` (wrappers whose criteria assert correct reuse of
   the existing `.claude` skills), `github-write.md`, `update-claude-md.md`.

**Finalize:** update CLAUDE.md + DESIGN.md (model deviation, stop-condition, conventions); reviewed.

## Status note (2026-06-16)
This file froze at the MVP foundation. The post-MVP build (#0012–#0026) is recorded in
`BUILDLOG.md`, which — with the `issues/` files and `DESIGN.md` "Delivered" list — is the
authoritative state, not the lists below. The GitHub issue tracker is known-stale (see backlog
B11). Items below are kept for historical context; strikethroughs mark what has since shipped.

## Out of scope (future issues)
`reviewer-architecture` (even/odd routing — superseded by #0016, which builds it with trigger-based
cadence instead); ~~CI/coverage enforcement~~ (CI shipped #0024; coverage-% gate still open, B9);
~~Ralph-loop stop hooks~~ (shipped #0021; verdict-producer wiring still open, B10); Blender add-on
dev standards (B4); resilience testing (B7); ~~GitHub remote push~~ (shipped, B8).

## Open items
- ~~GitHub repo name/URL~~ — resolved; remote is github.com/TrevorHumble/Blender-Agentic-Developer.
- ~~move spawned-agent model to Opus once proven?~~ — resolved by #0013 (reviewers on Opus; implementer
  stays Sonnet).
