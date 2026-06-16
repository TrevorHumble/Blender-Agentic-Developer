---
name: github-write
description: >-
  How to commit changes and open PRs in this project using git and the GitHub
  CLI. Triggers: "open a PR", "commit this", "push to GitHub", any task that
  writes to git or GitHub for the blender-orchestrator project. Issues are NOT
  written to GitHub — they live in issues/ (see DESIGN.md "Source of truth").
---

# github-write

## Critical: gh path and issue tracking

`gh` is NOT on PATH. Always use the full path:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" <subcommand>
```

The remote is live (github.com/TrevorHumble/Blender-Agentic-Developer) — `git push`
and `gh pr create` are available. **Issues are tracked locally in `issues/NNNN-title.md`,
not on GitHub — do not create or sync GitHub issues.** Per DESIGN.md "Source of truth",
`BUILDLOG.md` + `issues/` are canonical and the GitHub board is archived read-only. There is
no `gh issue` write step in this project.

## Committing

```powershell
git add <specific files>   # never git add -A blindly
git commit -m @'
Short imperative summary

Co-Authored-By: <committing model> <noreply@anthropic.com>
'@
```

Run `git status` before staging to avoid committing `.env` or large binaries.

## Opening a PR

```powershell
git push -u origin <branch>
& "C:\Program Files\GitHub CLI\gh.exe" pr create `
  --title "Short title" `
  --body @'
## Summary
- ...

## Test plan
- [ ] ...
'@
```

## Conventions

- No FINAL / LAST / TRULY_FINAL in branch names or commit messages.
- Prefer specific file staging over `git add .`.
- PowerShell line continuation: backtick `` ` ``, not `\`.
