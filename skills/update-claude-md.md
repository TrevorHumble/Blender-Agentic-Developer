---
name: update-claude-md
description: >-
  What to update in CLAUDE.md after project state changes. Triggers: "after
  creating an issue", "after merging a PR", "update the project doc", "record
  this in CLAUDE.md", any task that changes issue or PR state in
  blender-orchestrator.
---

# update-claude-md

Two triggers — both require a CLAUDE.md update:

1. **After every issue created** — add a row to the issue table (number, title,
   status `open`, depends-on, blocks).
2. **After every PR merged** — update the affected issue rows to `closed` and
   note the merged PR number.

## Where

`C:\Users\thumb\blender-orchestrator\CLAUDE.md` — the project-level doc.
Do not touch `C:\Users\thumb\.claude\CLAUDE.md` (global user config).

## What to write

Keep entries terse: issue number, one-line title, current status, dependency
chain. No prose summaries. Match the existing table format already in the file.

## When NOT to update

Do not update CLAUDE.md for draft issues that haven't been created yet, or for
PRs that are open but not merged. State changes only.
