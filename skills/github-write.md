---
name: github-write
description: >-
  How to create GitHub issues, commit changes, and open PRs in this project
  using git and the GitHub CLI. Triggers: "create an issue", "open a PR",
  "commit this", "push to GitHub", any task that writes to git or GitHub for
  the blender-orchestrator project.
---

# github-write

## Critical: gh path and no remote

`gh` is NOT on PATH. Always use the full path:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" <subcommand>
```

**No GitHub remote is configured yet.** Commits stay local. Do not attempt
`gh pr create` or `git push` until a remote is added and confirmed.

## Creating a GitHub issue

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" issue create `
  --title "Short title" `
  --body @'
## Summary
...

## Acceptance criteria
- [ ] ...
'@
```

If the repo has no remote yet, draft the issue body in `issues\NNNN-title.md`
following the existing issue format, then create it when the remote is live.

## Committing

```powershell
git add <specific files>   # never git add -A blindly
git commit -m @'
Short imperative summary

Co-Authored-By: <committing model> <noreply@anthropic.com>
'@
```

Run `git status` before staging to avoid committing `.env` or large binaries.

## Opening a PR (once remote exists)

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
