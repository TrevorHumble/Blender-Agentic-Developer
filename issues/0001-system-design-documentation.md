# Issue #0001 — System design documentation

**Type:** documentation
**Status:** draft — pending adversarial review
**Authored by:** orchestrator (emulated)

## User story
As a newcomer to this project who needs to get oriented by reading one document, I need `DESIGN.md`
to be the single source that explains what the system is, how it works, and the rules it follows,
so that I can understand the project from one place instead of reconstructing it from scattered context.

## Acceptance criteria
Given / When / Then. Each criterion is a literal, mechanically checkable property of the **produced
`DESIGN.md`** — a separate agent reading only that file answers each yes/no by string/structure
match, with no semantic interpretation. (Detecting internal contradictions is the doc reviewer's
job, not an acceptance criterion.)

1. Given `DESIGN.md`, when an agent lists its level-2 (`##`) headings, then exactly these twelve
   appear, in this order, and there are no other level-2 headings: `Prime directive`,
   `What the system is`, `Core principles`, `Repo structure`, `MVP scope`,
   `Adversarial review protocol`, `Lifecycles`, `Standards`, `Skill-bloat problem`,
   `Deferred items`, `Open items`, `Where the documentation lives`.
2. The "What the system is" section contains the literal substring `issue → review → implement → PR → review → commit`.
3. The document contains the literal sentence `Trevor is out of the operational loop.` and the
   literal clause `Trevor is never a required approver`.
4. The "MVP scope" section contains a Markdown table with one row per role. The row whose first cell
   is the literal `orchestrator` has tier cell `Opus`; `implementation agent` → `Sonnet`;
   `reviewer-issue` → `Opus`; `reviewer-pr` → `Opus`; `reviewer-skill` → `Opus`;
   `reviewer-agent` → `Opus`.
5. The "Lifecycles" section contains a `### Issue lifecycle` subheading immediately followed by a
   numbered list of at least six steps.
6. The "Lifecycles" section contains a `### PR lifecycle` subheading immediately followed by a
   numbered list of at least five steps.
7. The "Adversarial review protocol" section contains the literal substring `only the artifact under review`.
8. The "Adversarial review protocol" section contains a bulleted list that includes these three
   literal items: `never state what the artifact is trying to accomplish`;
   `never express any expectation about the outcome`; `never pre-answer anticipated objections`.
9. The "Adversarial review protocol" section contains the literal substring `PASS/FAIL`.
10. The "Standards" section contains the literal clause `applies the author's intent rather than transcribing the user's words`.
11. The document contains the literal substring `clarity heuristic`.
12. The document contains the literal sentence `The implementer is a Sonnet agent; Opus is used only when called for.`
13. The "Standards" section contains all three literal substrings: `end-consumer user story`;
    `Given/When/Then criteria testable by an agent`; `implementation plan that meets the Haiku bar`.
14. The "Open items" section contains at least four lines that each begin with the literal prefix
    `Open:`. Among them, one line contains the substring `repo name`, one contains `Blender RAG`,
    one contains `license`, and one contains `trigger`.
15. The "Deferred items" section contains a bulleted or numbered list of at least three items, one of
    which contains the literal token `reviewer-architecture`.

## Source material
The authoritative content for every section is provided to the implementing agent by the orchestrator
at handoff. (In the real system this source is the repository, prior issues, and the Blender RAG; in
this emulation it is the orchestrator's handoff briefing.) The implementer **synthesizes** the
document from that source following the structure below — it does not invent facts, and it is not
expected to already know them.

## Implementation plan
Produce one Markdown file, `DESIGN.md`, at the repo root, whose twelve level-2 (`##`) headings are
exactly those in criterion 1, in that order, with no other level-2 headings. Each section below
states what it must establish and the literal anchor strings it must contain verbatim (so the
acceptance criteria pass). The implementer writes the prose from the provided source material.

1. **Prime directive** — Trevor is a product manager, not a developer. Include the sentence
   `Trevor is out of the operational loop.` The adversarial agents are the gate.
2. **What the system is** — it builds Blender add-ons and maintains itself. Include the pipeline
   string `issue → review → implement → PR → review → commit`.
3. **Core principles** — human-out-of-loop (include the clause `Trevor is never a required approver`);
   unbiased reviewers; adversarial-by-design; model-by-role; the skill-bloat guard;
   living-repo-same-pipeline.
4. **Repo structure** — the target tree (`skills/`, `agents/`, `standards/`, `README.md`,
   `CLAUDE.md`, `DESIGN.md`). Names only; do not create or edit those files.
5. **MVP scope** — the skills list; the agent roster as a Markdown table with one row per role and an
   explicit tier, using the exact role tokens and tiers in criterion 4; the process flows. Note that
   the implementation agent may escalate (see the Standards sentence in §8); do not add
   `reviewer-architecture` here — it is deferred (§10).
6. **Adversarial review protocol** — define minimum context with the literal phrase
   `only the artifact under review` (plus the single relevant standard); include a bulleted list of
   actions the spawner must never take that contains verbatim the three items in criterion 8;
   the canonical reviewer framing; the anchoring and position-bias mitigations; and the output
   contract, including the literal token `PASS/FAIL`.
7. **Lifecycles** — a `### Issue lifecycle` subheading followed by a numbered list of at least six
   steps; a `### PR lifecycle` subheading followed by a numbered list of at least five steps; the
   skill/agent-update lifecycle (this is where `reviewer-skill` and `reviewer-agent` run); the Ralph
   loop (external verification; manual now, hooks later).
8. **Standards** — user story (include `end-consumer user story`); acceptance criteria (include
   `Given/When/Then criteria testable by an agent`); implementation plan (include
   `implementation plan that meets the Haiku bar`, the phrase `clarity heuristic`, and the exact
   sentence `The implementer is a Sonnet agent; Opus is used only when called for.`); skills (include
   `applies the author's intent rather than transcribing the user's words`); agents; comments
   (why-not-what, one line, anti-slop); naming (no FINAL); 80% coverage (code artifacts only);
   CLAUDE.md update triggers; documentation currency.
9. **Skill-bloat problem** — the failure mode (over-indexing on the user's words) and the
   intent-over-words discipline.
10. **Deferred items** — a list of at least three out-of-MVP items that become future issues,
    including one item naming `reviewer-architecture`, plus e.g. CI/coverage enforcement and
    Ralph-loop hooks.
11. **Open items** — at least four lines, each beginning with the literal prefix `Open:`. Ensure one
    line contains `repo name`, one contains `Blender RAG`, one contains `license`, and one contains
    `trigger`. Do not guess values.
12. **Where the documentation lives** — describe the DESIGN.md vs CLAUDE.md vs README split
    conceptually; do not reproduce README or CLAUDE.md contents verbatim.

Boundary between MVP scope (§5) and Deferred items (§10): §5 lists only what exists now — the skills
and the six roster agents in criterion 4; §10 lists everything not yet built (e.g.,
`reviewer-architecture`, CI/coverage enforcement, Ralph-loop hooks).

### The Haiku bar (the standard this plan is held to)
The plan must be clear and unambiguous enough that following it would not send a weak model off the
rails. It is a *thought experiment* about plan clarity — it does **not** require every fact to be
inlined. The implementer is a Sonnet agent that receives the source material above and synthesizes from it.

Constraints:
- Markdown only. No code, no tests.
- Apply the naming standard (no FINAL/LAST/v2_final) and the anti-slop standard to the document itself.

## Dependencies
- **Depends on:** none. This is the first issue.
- **Blocks:** the known downstream documentation issues — `README.md`, `CLAUDE.md`, and the
  `standards/` files — each of which will reference this document.
- **Touches:** `DESIGN.md` only.

## Out of scope
Creating or editing `README.md`, `CLAUDE.md`, individual skill or agent files, any Python or Blender
code. Sections 4 and 12 *name and describe* README/CLAUDE.md conceptually but must not create,
modify, or reproduce their contents.
