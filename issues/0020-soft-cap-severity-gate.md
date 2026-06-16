# Issue #0020 — Soft cap + external severity gate (replace the hard 3-round cap)

**Type:** ready. **Category:** governance / adversarial protocol (system-level change).
**Depends on:** #0006 (orchestrator), #0013 (reviewer independence).
**Blocks:** none.
**Touches:** `standards/adversarial-review-protocol.md`, `DESIGN.md`, `CLAUDE.md`,
`agents/orchestrator.md`, `agents/severity-adjudicator.md` (new).

## User story
As the review-loop orchestrator, I need a stop condition that never accepts work while a consequential
defect remains — where the 3-round mark merely *triggers* an independent severity judgment that can
release the loop only when every remaining defect is inconsequential, and a stubborn consequential defect
ends in a halt that surfaces to the operator rather than an acceptance — so that the operator stays out
of the loop and quality is never silently traded away to satisfy a round count.

## Background
Today the stop condition is a HARD cap: after 3 review rounds the loop stops and an adjudicator decides
which defects block. That lets the system effectively self-exit at a fixed round count. The operator's
directive: the 3-round mark is a *soft* trigger, not a hard cap; the system can never decide to exit by
itself; an independent severity gate may authorize an exit **only** when every remaining open defect is
inconsequential. A consequential defect means the loop continues — fix and re-review — and the severity
gate is re-invoked. If a consequential defect genuinely cannot be resolved, the segment halts and is
surfaced to the operator; it is never silently accepted.

## Definitions (encoded in the protocol)
- A defect is **consequential** if it does any of: violates an acceptance criterion; is a correctness,
  safety, or security defect; is a real internal contradiction in the artifact; or would mislead a future
  reader or agent. The severity adjudicator must cite which category.
- A defect is **inconsequential** only if it is none of those — a pure style/wording nit with no
  functional, correctness, or comprehension impact.

**Termination (the loop always ends, and never by accepting a consequential defect).** The loop ends in
exactly one of three ways: (a) a reviewer returns PASS; (b) the severity adjudicator authorizes exit
because every remaining defect is inconsequential; or (c) **impasse** — a consequential defect that
survives the severity gate plus **3 further fix-and-re-review rounds** is declared an impasse: the segment
halts and is surfaced to the operator. A halt is **not** an acceptance — the work is not merged. This
bounds the loop without ever self-exiting by accepting consequential work.

## Acceptance criteria
1. **Given** `standards/adversarial-review-protocol.md` after implementation, **When** a reader greps it,
   **Then** it contains each literal: `soft cap`, `the 3-round mark is a trigger, not a hard cap`,
   `severity adjudicator`, `consequential`, and `inconsequential`.
2. **Given** that protocol section, **When** a reader greps it, **Then** it contains the literal
   `exit is authorized only when every remaining defect is inconsequential` and the literal
   `never accepts work while a consequential defect remains`.
3. **Given** that protocol section, **When** a reader greps it, **Then** it states the independence rule
   with the literal `the author, implementer, and orchestrator never classify severity or authorize exit`,
   and lists the four consequential categories with the literals `violates an acceptance criterion`,
   `correctness, safety, or security`, `internal contradiction`, and `mislead`.
4. **Given** the new file `agents/severity-adjudicator.md`, **When** a reader greps its frontmatter,
   **Then** all of these literals are present: `name:`, `description:`, `model: opus`, `tools:`, and
   `Read`; **and** the body contains each literal: `consequential`, `inconsequential`, `authorize exit`,
   and `Spawner injected intent` (the bias gate).
5. **Given** `agents/severity-adjudicator.md`, **When** a reader greps it, **Then** it states that it
   classifies every remaining open defect and cites a basis for each (literal `cite a basis for each`),
   and that it authorizes exit only if every defect is inconsequential (literal
   `only if every defect is inconsequential`).
6. **Given** `CLAUDE.md` after implementation, **When** a reader greps the stop-condition section,
   **Then** it contains the literals `soft cap`, `severity adjudicator`, and
   `never self-exit on a consequential defect`.
7. **Given** `agents/orchestrator.md` after implementation, **When** a reader greps it, **Then** it
   contains the literal `the loop continues` (on a consequential defect) and the literal
   `halt and surface to the operator` (the impasse path), and the literal `never silently accepted`.
8. **Given** `DESIGN.md` after implementation, **When** a reader greps the stop-condition / Ralph-loop
   section, **Then** it contains the literals `soft cap`, `severity adjudicator`, and `consequential`.
9. **Given** the impasse rule, **When** a reader greps `standards/adversarial-review-protocol.md`,
   **Then** it contains the literal `survives the severity gate plus 3 further fix-and-re-review rounds`
   and the literal `a halt is not an acceptance`, defining a deterministic bound that guarantees the loop
   terminates without accepting consequential work.
10. **Given** the four governing files (`standards/adversarial-review-protocol.md`, `DESIGN.md`,
    `CLAUDE.md`, `agents/orchestrator.md`) after implementation, **When** a reader greps each for the
    literal `Cap: 3 review rounds`, **Then** zero matches are found (the hard-cap phrasing is removed), and
    each of the four contains the literal `soft cap`. (BUILDLOG.md is append-only history and is exempt.)

## Implementation plan
1. **Protocol.** In `standards/adversarial-review-protocol.md`, replace the hard-cap rule with the soft
   cap + severity gate: the 3-round mark triggers the `severity adjudicator`; define consequential vs
   inconsequential (the four categories); exit authorized only when every remaining defect is
   inconsequential; the author/implementer/orchestrator never classify severity or authorize exit; and the
   impasse bound — a consequential defect that `survives the severity gate plus 3 further fix-and-re-review rounds`
   halts and surfaces to the operator, and `a halt is not an acceptance` (ACs 1-3, 9).
2. **Agent.** Write `agents/severity-adjudicator.md` (frontmatter per AC4; `model: opus`, `tools: [Read]`):
   single responsibility — classify every remaining open defect consequential/inconsequential with a cited
   basis, authorize exit only if all are inconsequential, otherwise the loop continues; carry the bias gate
   (ACs 4-5). Mirror the structure of an existing reviewer agent.
3. **DESIGN.md.** Update the stop-condition / Ralph-loop section to the soft cap + severity gate (literals
   `soft cap`, `severity adjudicator`, `consequential` — AC8); keep the independent-adjudication and the
   periodic-audit cross-references intact.
4. **CLAUDE.md.** Rewrite the Stop condition section to the soft cap (AC6); remove the `Cap: 3 review rounds`
   hard-cap wording.
5. **orchestrator.md.** Update the loop behavior: on a consequential defect `the loop continues`; on a
   genuine impasse `halt and surface to the operator`; bad work is `never silently accepted` (AC7).
6. **Reconcile** all four governing files so a grep for `Cap: 3 review rounds` returns zero matches and
   each contains `soft cap` (AC10).

## Out of scope
- Enforcing the loop with a Claude Code stop hook (that is B3 / a separate issue).
- Changing the number 3 (the trigger interval stays 3 rounds).
- Updating #0015's prepared text (handled when #0015 is implemented).
