# Issue #0026 — Documentation-currency reviewer agent (graduates B5)

**Type:** ready. **Category:** agents / governance.
**Depends on:** #0013 (reviewer independence), and `standards/documentation-standards.md` currency triggers (built).
**Blocks:** none.
**Touches:** `agents/reviewer-doc-currency.md` (new), `CLAUDE.md`, `DESIGN.md`,
`issues/0009-future-work-backlog.md`.

This issue adds a new governing agent (an `agents/` artifact and edits to `DESIGN.md` + `CLAUDE.md`), so
it is a **system-level change**: its artifact is gated under the two-independent-reviewer bar
(`standards/adversarial-review-protocol.md`), the soft cap, and the severity adjudicator.

## User story
As Trevor, whose front-door docs (README, DESIGN.md structure maps, CLAUDE.md "where things live"
rosters) drifted during this very build and were only caught because I asked, I need an adversarial
reviewer that judges a **PR diff** for currency violations — a file changed under a currency trigger
without its corresponding index/front-door doc updated in the same diff — so the drift is failed at
commit time instead of relying on me to notice it.

## Background
`standards/documentation-standards.md` ("Currency triggers") already enumerates when a doc MUST be
updated: an interface/path changes, a decision is reversed or superseded, an acceptance criterion
changes, an external source goes stale, a named consumer changes, or a downstream artifact contradicts
or extends a claim. The existing `agents/reviewer-documentation.md` judges **one doc file** against the
standard — it never sees a diff and cannot know that a *sibling* index doc went stale. This issue adds
the complementary reviewer: it reads the **diff** (the set of changed files) and FAILs when a
currency-triggering change landed without the matching index/front-door doc updated in the same diff.

The drift class this targets, concretely: a PR adds a new top-level directory (`addons/`, `tests/`,
`evals/`, `.github/`) or a new agent/skill/standard, but does not update the README layout table, the
`DESIGN.md` repo-structure map, or the CLAUDE.md "Where things live" roster. Each is a currency trigger
("a named consumer / path changes"); each was missed tonight.

## Acceptance criteria
Every criterion resolves to a literal-string or structural grep a separate agent can verify by reading
only the produced artifact. Where intent matters, it is encoded AS a required literal string.

1. **Given** the new file `agents/reviewer-doc-currency.md`, **When** a reader greps it, **Then** it has
   YAML frontmatter containing `name:`, `description:`, `tools:`, and `model: opus`, and the `tools:`
   list contains `Read` and does **not** contain `Write` or `Edit` (a reviewer never edits).
2. **Given** the file, **When** a reader greps it, **Then** it contains the literal string
   `currency trigger` and references `standards/documentation-standards.md`, and contains the literal
   string `diff` (its unit of review is the diff, not a single file — the distinction from
   `reviewer-documentation`).
3. **Given** the file, **When** a reader greps it, **Then** it names the three front-door/index docs it
   guards by their literal paths: `README.md`, `DESIGN.md`, and `CLAUDE.md`.
4. **Given** the file, **When** a reader greps it, **Then** it contains a `## Bias check` section with
   the literal string `Spawner injected intent`, matching the protocol's de-bias contract used by the
   other reviewers.
5. **Given** the file, **When** a reader greps it, **Then** its output contract contains the literal
   strings `PASS`, `FAIL`, and `blocker`, and the literal rule that a PASS with an open blocker or major
   is not a PASS (contains the literal string `not a PASS`).
6. **Given** `CLAUDE.md` after implementation, **When** a reader greps the agents roster, **Then** it
   lists `reviewer-doc-currency` with a one-line description that contains the literal string `diff`.
7. **Given** `DESIGN.md` after implementation, **When** a reader greps it, **Then** it documents when the
   doc-currency reviewer fires (contains the literals `reviewer-doc-currency` and `PR`).
8. **Given** `issues/0009-future-work-backlog.md` after implementation, **When** a reader greps the B5
   entry, **Then** it contains the literal `Graduated to #0026`.

## Implementation plan
1. Write `agents/reviewer-doc-currency.md` following the `agents/reviewer-documentation.md` shape (Role,
   When to invoke, Protocol → `standards/adversarial-review-protocol.md`, Bias check, Input/output
   contract, Checklist). Single responsibility: **judge a diff for currency-trigger violations.** Input
   is the diff (or the list of changed files + their hunks); it reads
   `standards/documentation-standards.md` and `standards/adversarial-review-protocol.md`. The checklist
   maps each currency trigger to "did the diff touch a triggering file without updating the matching
   index/front-door doc (`README.md` layout, `DESIGN.md` structure map, `CLAUDE.md` roster)?" FAIL with
   `file:line` evidence on any unmet trigger.
2. Distinguish it from `reviewer-documentation` in the Role section: that agent judges one doc against
   the standard; this agent judges a diff for cross-file staleness. No overlap.
3. Add `reviewer-doc-currency` to the CLAUDE.md agents roster and to `DESIGN.md` (when it fires:
   PR-review time, on any diff that touches a currency-triggering path).
4. Graduate B5 in `issues/0009-future-work-backlog.md` (`Graduated to #0026`).

## Out of scope
- Wiring it into the orchestrator's PR-review fan-out as a mandatory gate (a follow-up that edits
  `skills/spawn-adversarial-review.md` / `agents/orchestrator.md`; this issue creates the agent).
- Auto-detecting which doc is the "matching" index for an arbitrary new path (the checklist enumerates
  the three known front-door docs; a general path→doc map is a follow-up).
- Re-reviewing already-merged diffs for historical drift.
