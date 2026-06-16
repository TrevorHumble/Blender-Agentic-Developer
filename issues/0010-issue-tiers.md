# Issue #0010 — Issue tiers: ready vs backlog

**Type:** standards (ready-issue). **Status:** ready.
**Depends on:** #0003 (issue-standards). **Blocks:** clean graduation of `issues/0009` backlog items.
**Touches:** `standards/issue-standards.md`, `agents/reviewer-issue.md`.

## User story
As `reviewer-issue`, I need `issue-standards.md` to define a "ready" tier and a "backlog" tier with
distinct bars, so that I judge a backlog item against the backlog bar instead of failing it for
lacking an implementation plan it cannot yet have.

## Acceptance criteria
1. `standards/issue-standards.md` contains a section whose heading contains the literal string `Issue tiers`.
2. The `Issue tiers` section contains the literal string `ready tier` and each of these literal
   strings: `user story`, `Given/When/Then`, `implementation plan`, `Depends on`, `Blocks`, `Touches`.
3. The `Issue tiers` section contains the literal strings `backlog tier`, `Graduate after`, and
   `deterministic`, and a literal statement that the backlog tier omits `Blocks`/`Touches`.
4. The `Issue tiers` section contains the literal string `never implemented in place`.
5. `agents/reviewer-issue.md` contains the literal string `apply the tier the issue declares`, and
   contains the literal string `FAIL` within five lines of the literal string `human-approval`.

## Implementation plan
1. In `standards/issue-standards.md`, add a `## Issue tiers` section defining the `ready` and `backlog`
   tiers and their required fields exactly as in criteria 2–3.
2. In the same section, add the graduation rule from criterion 4 (backlog → numbered ready-issue; never
   implemented in place).
3. In `agents/reviewer-issue.md`, add a rule that the reviewer reads the issue's declared tier and
   applies the matching bar, and FAILs a backlog item whose `Graduate after` is a human approval rather
   than a deterministic condition.
4. Run `reviewer-issue` (or an equivalent adversarial review) against both edited files; fix to PASS.

## Out of scope
Changing the existing ready-tier fields; re-reviewing already-merged issues.
