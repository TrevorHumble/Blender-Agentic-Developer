# Issue #0007 — Blender + ops skills (Layer F)

**Type:** skills. **Depends on:** #0003 (skill-standards). **Blocks:** running real Blender work.

## User story
As an implementation or reviewer agent, I need pull-able skills to confirm Blender facts, control
Blender, write to GitHub, and update the project state doc, so that I use the existing tools the
right way instead of rediscovering them.

## Deliverables (each conforms to `standards/skill-standards.md`)
- `skills/blender-rag.md` — thin wrapper: when to confirm a Blender fact via `search_blender_docs`,
  pointing to the existing skill and the RAG at `C:\Users\thumb\BlenderRag`.
- `skills/blender-connect.md` — thin wrapper for live Blender control, pointing to the existing
  `blender-mcp` skill.
- `skills/github-write.md` — how to create issues, commit, and open PRs using
  `C:\Program Files\GitHub CLI\gh.exe` (not on PATH) and git. Note: no remote configured yet.
- `skills/update-claude-md.md` — what to update in CLAUDE.md after every issue created and every PR merged.

## Source material (reuse, do not duplicate)
- Existing: `C:\Users\thumb\.claude\skills\blender-rag\SKILL.md` and
  `C:\Users\thumb\.claude\skills\blender-mcp\SKILL.md` — the wrappers POINT to these, they do not copy them.
- `standards/skill-standards.md` and `CLAUDE.md` environment notes (PowerShell; gh path).

## Acceptance criteria
Each file:
1. YAML frontmatter `name`+`description`; description has ≥2 strings in double-quotes or backticks.
2. Body under 500 lines; no banned slop words; no FINAL/LAST.
Content-specific:
3. `blender-rag.md` points to `C:\Users\thumb\.claude\skills\blender-rag` and names the tool
   `search_blender_docs`; it does NOT duplicate that skill's body.
4. `blender-connect.md` points to the existing `blender-mcp` skill and does NOT duplicate it.
5. `blender-rag.md` states the rule: confirm the API via the RAG, then execute via blender-connect.
6. `github-write.md` references the full gh path `C:\Program Files\GitHub CLI\gh.exe`, uses PowerShell
   syntax, and notes that no GitHub remote is configured yet (commits stay local).
7. `update-claude-md.md` states the two triggers: after every issue created and after every PR merged.

## Constraints
Markdown + YAML. Tight, no slop. Thin wrappers must not duplicate the skills they point to.
