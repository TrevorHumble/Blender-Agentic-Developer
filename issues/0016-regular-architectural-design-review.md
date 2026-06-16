# Issue #0016 — Regular adversarial architectural + design-philosophy review

**Type:** ready. **Category:** architecture / standards.
**Depends on:** #0001 (DESIGN.md), #0003 (agent-standards), #0004 (reviewer agents), #0006 (orchestrator).
**Blocks:** none.
**Touches:** `standards/design-philosophy.md` (new), `agents/reviewer-architecture.md` (new),
`agents/reviewer-design-philosophy.md` (new), `agents/orchestrator.md`, `DESIGN.md`, `CLAUDE.md`,
`.claude/commands/build.md`, `issues/0009-future-work-backlog.md`.

## User story
As the operator who is out of the operational loop, I need the pipeline to run an adversarial
architectural review and an adversarial design-philosophy review regularly — not occasionally — so that
structural drift and poor design get caught by an independent gate on the work as it happens, rather than
relying on me to notice.

## Background
Two review lenses were intended but never built. `software-design-philosophy` is referenced in `PLAN.md`
only as source material for the documentation standard, and architectural review sits unbuilt as backlog
B1 in `issues/0009-future-work-backlog.md`. The originally-suggested "every even / every odd issue"
cadence is rejected: an issue's parity is unrelated to whether it needs architectural scrutiny. This
issue replaces parity with **trigger-based standing gates plus a periodic full-system audit**, and adds
the two adversarial reviewers and the standard the design-philosophy reviewer judges against.

The design-philosophy principles are drawn from Ousterhout, *A Philosophy of Software Design* (deep
modules, information hiding, pulling complexity downward, defining errors out of existence, distinct
abstractions per layer, design it twice, consistency, obvious code).

## Acceptance criteria
Every criterion resolves to a literal-string or structural grep verifiable by reading only the produced
artifact. Intent is encoded as required literal strings.

### The design-philosophy standard
1. **Given** the new file `standards/design-philosophy.md`, **When** a reader greps it, **Then** it
   contains each of these literal principle names: `Deep modules`, `Information hiding`,
   `Pull complexity downward`, `Define errors out of existence`, `Different layers, different abstractions`,
   `Design it twice`, `Consistency`, `Obvious code`.
2. **Given** the same file, **When** a reader greps it, **Then** it contains a red-flags section
   containing each of these literal strings: `shallow module`, `information leakage`,
   `temporal decomposition`, `pass-through`, `vague name`, and the example `` `tmp` ``.
3. **Given** the same file, **When** a reader greps it, **Then** it contains the literal string
   `Source: Ousterhout` (attribution of the principles).

### The two adversarial reviewer agents
4. **Given** the new file `agents/reviewer-architecture.md`, **When** a reader greps its YAML
   frontmatter, **Then** all of these literal strings are present: `name:`, `description:`, `model: opus`,
   `tools:`, and `Read`. (The criterion passes only if every listed string is present.)
5. **Given** `agents/reviewer-architecture.md`, **When** a reader greps the body, **Then** all of these
   literal strings are present: `DESIGN.md`, `duplicates an existing component` (the no-duplication
   check), `standards/adversarial-review-protocol.md` (it is an adversarial reviewer), and
   `Spawner injected intent` (the bias gate, mirroring the other reviewers).
6. **Given** the new file `agents/reviewer-design-philosophy.md`, **When** a reader greps its YAML
   frontmatter, **Then** all of these literal strings are present: `name:`, `description:`, `model: opus`,
   `tools:`, and `Read`. (The criterion passes only if every listed string is present.)
7. **Given** `agents/reviewer-design-philosophy.md`, **When** a reader greps the body, **Then** all of
   these literal strings are present: `standards/design-philosophy.md` (its governing standard),
   `standards/adversarial-review-protocol.md`, and `Spawner injected intent` (the bias gate).

### The cadence (wired into the orchestrator)
8. **Given** `agents/orchestrator.md` after implementation, **When** a reader greps it, **Then** both
   literal strings are present: `reviewer-architecture` and `system-level change or adds a new component`
   (the latter is the trigger phrase; architectural review fires at issue-review time for those issues).
9. **Given** `agents/orchestrator.md`, **When** a reader greps it, **Then** both literal strings are
   present: `reviewer-design-philosophy` and `every implementation artifact` (the latter is the trigger
   phrase; design-philosophy review fires at PR-review time).
10. **Given** `agents/orchestrator.md`, **When** a reader greps it, **Then** all three literal strings
    are present: `every 5th`, `BUILDLOG`, and `full-system architectural audit` (the audit is triggered
    by counting BUILDLOG entries).

### Documentation and supersession
11. **Given** `DESIGN.md` after implementation, **When** a reader greps it, **Then** it contains the
    literal strings `reviewer-architecture`, `reviewer-design-philosophy`, and `full-system architectural audit`.
12. **Given** `CLAUDE.md` after implementation, **When** a reader greps it, **Then** it contains the
    literal strings `reviewer-architecture` and `reviewer-design-philosophy`.
13. **Given** `.claude/commands/build.md` after implementation, **When** a reader greps it, **Then** it
    contains the literal strings `reviewer-architecture` and `reviewer-design-philosophy`.
14. **Given** `issues/0009-future-work-backlog.md` after implementation, **When** a reader greps it,
    **Then** both literal strings are present: `B1` and `Superseded by #0016` (the supersession note is
    appended to the B1 entry).

## Implementation plan
1. **Write `standards/design-philosophy.md`** — the eight principles (AC1), a red-flags section naming
   `vague name` with the `` `tmp` `` example (AC2), review questions, and the `Source: Ousterhout`
   attribution (AC3). Plain markdown, tight, no slop.
2. **Write `agents/reviewer-architecture.md`** — adversarial reviewer (frontmatter per AC4) that judges
   an issue or the system against `DESIGN.md`: structural fit, no duplication of an existing component,
   no contradiction of documented architecture. Follows the protocol and carries the bias gate (AC5).
   Reuse the structure of an existing `agents/reviewer-*.md`; do not reinvent.
3. **Write `agents/reviewer-design-philosophy.md`** — adversarial reviewer (frontmatter per AC6) that
   judges an implementation artifact against `standards/design-philosophy.md`, with the bias gate (AC7).
4. **Wire the cadence into `agents/orchestrator.md`** — a section stating: architectural review fires at
   issue-review time when the issue is a `system-level change or adds a new component`; design-philosophy
   review fires at PR-review time for `every implementation artifact`; and `every 5th` BUILDLOG entry
   triggers a `full-system architectural audit` (ACs 8-10).
5. **Document in `DESIGN.md`** (AC11) and **list the new reviewers in `CLAUDE.md`** (AC12) and
   **`.claude/commands/build.md`** (AC13).
6. **Supersede B1** — append `Superseded by #0016` to the B1 entry in
   `issues/0009-future-work-backlog.md` (AC14), append-only, do not rewrite the entry.

## Out of scope
- Automating when the audit runs (the orchestrator counts BUILDLOG entries; no scheduler).
- The two-independent-reviewer bar for system-level changes (that is issue #0015).
- Changing the existing `reviewer-issue` / `reviewer-pr` gates; these two reviewers are additive.
