# Issue #0028 — GitHub is the single source of truth (supersedes #0027)

**Type:** ready. **Category:** standards / architecture / process.
**Depends on:** #0019 (in-license — GitHub is in-license), B8 (remote, done).
**Supersedes:** #0027 (which declared BUILDLOG canonical and stopped GitHub mirroring — reversed here).
**Blocks:** none.
**Touches:** `DESIGN.md`, `CLAUDE.md`, `PLAN.md`, `skills/github-write.md`, `agents/orchestrator.md`,
`.claude/commands/build.md`, `agents/reviewer-tracker-sync.md` (new),
`issues/0009-future-work-backlog.md`, `issues/0027-declare-buildlog-canonical.md`, `BUILDLOG.md`,
`C:\Users\thumb\.claude\CLAUDE.md` (the user's global rules — cross-project convention).

This issue changes the documented operating model and edits `DESIGN.md` + `CLAUDE.md` + a skill + the
orchestrator, so it is a **system-level change**: its artifact is gated under the two-independent-reviewer
bar (`standards/adversarial-review-protocol.md`), the soft cap, and the severity adjudicator.

## User story
As Trevor, who needs to open one place and see every task with its real status, I need GitHub to be the
single source of truth for tasks and documentation — with the board kept accurate by the pipeline itself,
not by anyone remembering to update it — so the board never silently goes stale the way it did under the
manual one-time mirror (B8) that #0027 reacted to.

## Background
#0027 chose the opposite fix (declare BUILDLOG canonical, stop mirroring) because the GitHub board had
drifted: a one-time manual push that nothing maintained. Trevor has reversed that decision: GitHub is
easier for him to see everything in one place. The drift risk #0027 identified is real, so this issue does
not just re-open mirroring — it adds the **maintaining step** (`#0027`'s root-cause fix, inverted): the
pipeline creates/updates/closes the GitHub issue at every lifecycle transition, and a new gate fails any
merge that leaves the board inconsistent with reality. This is the difference between the failed manual
mirror and a self-maintaining board.

**File model (chosen: "files = detail, issue = status"):** the rich `issues/NNNN-*.md` files stay in the
repo (full acceptance criteria + plan, version-controlled, diffable, read by the reviewer agents). Each
issue file has a corresponding GitHub issue that is **canonical for status** (open/closed/labels). The
discipline that prevents drift: a file describes the work; the GitHub issue owns the state; the pipeline
keeps them equal. Backlog items in `issues/0009-future-work-backlog.md` that have not graduated to an
issue file also get a GitHub issue (so all open work is visible).

**Cross-project scope:** the *enforceable* machinery (sync step + gate) exists only in this repo. For
Trevor's other Blender projects, "GitHub is the single source of truth" is recorded as a standing
convention in his global `~/.claude/CLAUDE.md`, followed by default but not auto-enforced unless those
projects adopt the same tooling.

## Acceptance criteria
Each criterion resolves to a literal-string/structural grep, or (AC8–AC9) a runtime `gh` check the
orchestrator verifies and records.

1. **Given** `DESIGN.md` after implementation, **When** a reader greps the "Source of truth" section,
   **Then** it contains the literal strings `GitHub is the single source of truth` and `kept in sync by
   the pipeline`, and it no longer contains the literal string `not mirrored to GitHub` (the #0027
   statement is removed).
2. **Given** `skills/github-write.md`, **When** a reader greps it, **Then** it again documents issue
   writes — it contains the literal `gh issue create`, and contains a section on keeping the issue in sync
   (contains the literals `open` and `close`), and does **not** contain the #0027 literal `do not create
   or sync GitHub issues`.
3. **Given** `CLAUDE.md` (repo), **When** a reader greps it, **Then** it contains a line with the literal
   `single source of truth` and the literal `GitHub`, and it no longer contains the #0027 rule literal
   `Never run \`gh issue create\``.
4. **Given** the user's global `C:\Users\thumb\.claude\CLAUDE.md`, **When** a reader greps it, **Then** it
   contains the literal strings `single source of truth` and `Blender projects` (the cross-project
   convention is recorded).
5. **Given** `agents/orchestrator.md` and `.claude/commands/build.md`, **When** a reader greps them,
   **Then** each contains a lifecycle step that writes the GitHub issue — containing the literal
   `gh issue` and both transition words `open` (on issue creation) and `close` (on PR merge).
6. **Given** the new file `agents/reviewer-tracker-sync.md`, **When** a reader greps it, **Then** it has
   frontmatter with `name:`, `description:`, `tools:`, `model: opus`; it describes failing a merge when the
   board disagrees with reality (contains the literals `out of sync` and `FAIL`); and it is a reviewer
   (its `tools:` contains `Bash` for `gh` reads but not `Write`/`Edit`).
7. **Given** `issues/0027-declare-buildlog-canonical.md` and `issues/0009-future-work-backlog.md`, **When**
   a reader greps them, **Then** #0027 contains the literal `Superseded by #0028` and the B12 entry in
   0009 contains the literal `reversed by #0028`.
8. **Given** the live GitHub board after the rebuild, **When** the orchestrator lists all issues, **Then**
   every local issue file `#0001`–`#0028` has exactly one GitHub card whose state matches its audited
   status (shipped → CLOSED; open work → OPEN), and every un-graduated backlog item (B4, B6, B7, B9, B10,
   B11, B13, EC1, EC2, EC3, plus #0014) has exactly one OPEN card with the correct `ready`/`backlog`/`low
   priority` label. (Orchestrator runtime verification via `gh`, recorded in BUILDLOG.)
9. **Given** the rebuilt board, **When** an independent agent re-audits it against `BUILDLOG.md` + the
   repo, **Then** no shipped issue is OPEN and no genuinely-unfinished item is CLOSED. (Runtime
   adversarial check, recorded — this is the "ready means ready" guarantee.)
10. **Given** `PLAN.md` after implementation, **When** a reader greps it, **Then** its status note no
    longer contains the literal `GitHub issue tracking is abandoned` (the #0027 phrasing) and instead
    contains the literal `GitHub is the single source of truth`.

## Implementation plan
1. **Reverse #0027 in the docs.** `DESIGN.md` "Source of truth" → GitHub canonical for task status, files
   = detail, pipeline keeps them in sync (AC1). `skills/github-write.md` → restore the `gh issue
   create`/update/close path plus a sync-discipline section (AC2). `CLAUDE.md` (repo) → replace the
   "Never gh issue create" rule with the single-source-of-truth rule (AC3). `PLAN.md` → update the status
   note. Mark #0027 `Superseded by #0028`; mark B12 `reversed by #0028` (AC7).
2. **Cross-project convention.** Add the standing rule to `C:\Users\thumb\.claude\CLAUDE.md` (AC4).
3. **Maintaining step (root-cause fix).** Add to `agents/orchestrator.md` + `.claude/commands/build.md` a
   lifecycle step: on issue creation, open the GitHub card; on PR merge, close it; on graduation, update
   it (AC5).
4. **Sync gate.** Write `agents/reviewer-tracker-sync.md` (Opus, reads `gh` via Bash, never edits): FAILs
   a merge when the board is `out of sync` with the issue files / BUILDLOG (AC6). Register it in the
   roster (`CLAUDE.md`, `DESIGN.md`).
5. **Rebuild the board** from the verified audit table (AC8): backfill `#0001–#0008` as CLOSED; file every
   missing shipped issue (`#0011, #0016, #0019, #0020, #0022, #0023, #0024, #0025, #0026, #0027`) as
   CLOSED; reopen/file the genuinely-open work (B4/B6/B7 reopen; B9/B10/B11/B13 file; EC1/EC2/EC3 reopen
   low-priority; #0014 file low-priority) as OPEN with correct labels; keep verified-shipped cards CLOSED.
   Each shipped-partial parent (#0021/#0024/#0026) closed, with its loose end (B10/B9/B11) open.
6. **Verify** (AC9): an independent agent re-audits the live board against reality; fix any mismatch;
   record the result in BUILDLOG.

## Out of scope
- Actually building any open task (B4/B6/B7/B9/B10/B11/B13/EC*) — those stay open work; this issue only
  makes the board reflect reality and keeps it synced.
- A GitHub Projects board / milestones / automation beyond issues + labels (a later option).
- Moving issue detail into GitHub issue bodies (that was Option B; rejected — files keep version history).
