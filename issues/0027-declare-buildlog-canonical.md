# Issue #0027 — Declare BUILDLOG + issues/ canonical; stop GitHub issue mirroring (graduates B12)

**Type:** ready. **Category:** standards / architecture / process.
**Depends on:** #0019 (in-license), B8 (remote, done).
**Blocks:** none.
**Touches:** `DESIGN.md`, `CLAUDE.md`, `PLAN.md`, `skills/github-write.md`,
`issues/0009-future-work-backlog.md`, `BUILDLOG.md`.

This issue changes the documented operating model (which artifacts are authoritative) and edits
`DESIGN.md` + `CLAUDE.md` + a skill, so it is a **system-level change**: its artifact is gated under the
two-independent-reviewer bar (`standards/adversarial-review-protocol.md`), the soft cap, and the
severity adjudicator.

## User story
As Trevor, whose GitHub issue board froze at a one-time manual snapshot (B8) while 14 more issues shipped
locally — so the board now shows shipped work as OPEN and is missing eight issues entirely — I need the
system to declare a single canonical tracker and to remove the only documented way it can write GitHub
issues, so the tracker cannot silently re-drift the next time it runs with me out of the loop.

## Background
Root cause (adversarial analysis, 2026-06-16): the GitHub mirror was a **one-time manual push that
nothing maintains.** No pipeline step creates or closes a GitHub issue on merge — every step ends at
`git commit` + a `BUILDLOG.md` append. `skills/github-write.md` still documents `gh issue create` and a
stale "no remote configured" note. The fix is not to add a sync step (which would re-drift the moment a
run skips it, by design Trevor is out of the loop) but to make the already-true canonical choice explicit
and remove the drift surface: `BUILDLOG.md` + `issues/` + the `DESIGN.md` "Delivered" list are
authoritative; the GitHub repo exists for code backup and public sharing only; issue tracking is not
mirrored. The GitHub board is annotated read-only and closed, pointing at the canonical source.

## Acceptance criteria
Every criterion resolves to a literal-string or structural grep a separate agent can verify by reading
only the produced artifact.

1. **Given** `DESIGN.md` after implementation, **When** a reader greps it, **Then** it contains a heading
   with the literal string `Source of truth` and a sentence containing all of the literal strings
   `BUILDLOG.md`, `issues/`, and `not mirrored to GitHub`.
2. **Given** that same section, **When** a reader greps it, **Then** it states the GitHub repo's purpose
   with the literal strings `backup` and `sharing` (the repo exists for code backup and public sharing,
   not issue tracking).
3. **Given** `skills/github-write.md` after implementation, **When** a reader greps it, **Then** it does
   **not** contain the literal string `gh issue create` and does **not** contain the literal string
   `Creating a GitHub issue` (the only documented issue-write path is removed).
4. **Given** `skills/github-write.md`, **When** a reader greps it, **Then** it contains the literal string
   `tracked locally in` and the literal string `do not create or sync GitHub issues`, and the stale
   `No GitHub remote is configured yet` line is gone (replaced by a note that the remote is live for
   `git push` / `gh pr create`).
5. **Given** `CLAUDE.md` after implementation, **When** a reader greps it, **Then** it contains a line
   beginning with `- ` that includes the literal strings `canonical` and `not mirrored to GitHub`.
6. **Given** `PLAN.md` after implementation, **When** a reader greps it, **Then** the "known-stale"
   phrasing is replaced — it contains the literal string `GitHub issue tracking is abandoned` (board
   archived read-only, pointing to BUILDLOG) and does **not** contain the literal string `known-stale`.
7. **Given** `issues/0009-future-work-backlog.md` after implementation, **When** a reader greps the B12
   entry, **Then** it contains the literal `Done` and the literal `#0027`.
8. **Given** the live GitHub board after the close step, **When** the orchestrator lists issues, **Then**
   every issue whose local counterpart shipped is CLOSED with a comment pointing to BUILDLOG/issues as
   canonical, and the genuinely-open backlog items (B4/B6/B7, EC1/EC2/EC3) are closed-as-archived with a
   comment that they remain open locally — no shipped issue remains OPEN on the board. (Orchestrator
   verification via `gh`, recorded in BUILDLOG — runtime check, not a literal-file AC.)

## Implementation plan
1. **`DESIGN.md`** — add a `## Source of truth` subsection (near "Where the documentation lives", ~line
   332): `BUILDLOG.md` + `issues/` + the DESIGN.md "Delivered" list are the canonical project state; the
   GitHub repo is for code `backup` and public `sharing` only; issue tracking is `not mirrored to GitHub`.
2. **`skills/github-write.md`** — delete the "Creating a GitHub issue" section and the `gh issue create`
   block; replace the stale "No GitHub remote is configured yet" note with: the remote is live for
   `git push` / `gh pr create`; issues are `tracked locally in` `issues/`, `do not create or sync GitHub
   issues`.
3. **`CLAUDE.md`** — add one operating-rule line: issues are `canonical` in `issues/` + BUILDLOG and
   `not mirrored to GitHub`. (Edit DESIGN.md first; CLAUDE.md derives from it.)
4. **`PLAN.md`** — replace the "known-stale" note with `GitHub issue tracking is abandoned` (archived
   read-only).
5. **`issues/0009-future-work-backlog.md`** — mark B12 `Done` (see `#0027`), matching the B8 pattern.
6. **Close the board** (`gh`, full path `C:\Program Files\GitHub CLI\gh.exe`): close each shipped issue
   (GH #15→#0022, #14→#0015, #10→#0013, #9→#0012, #8→#0010, #1→#0016, #2→#0024, #3→#0021, #5→#0026) with a
   canonical-pointer comment; close the still-open-locally backlog issues (#4/#6/#7, #11/#12/#13) as
   archived with a "remains open in issues/0009" comment. Do not file #0019/#0020/#0023/#0025 or B9–B13.
7. Record the close results in BUILDLOG.

## Out of scope
- Editing the GitHub repo description/README banner (optional follow-up; the canonical statement in
  DESIGN.md is the binding artifact).
- Deleting the GitHub issues (close + annotate only — closure is reversible, deletion is not, and the
  history stays as a pointer).
- Re-filing any local issue on GitHub (the whole point of Path B is to stop mirroring).
