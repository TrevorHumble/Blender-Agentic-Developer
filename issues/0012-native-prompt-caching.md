# Issue #0012 — Native prompt caching of standards (E2)

**Type:** feature (ready). **Status:** ready.
**Depends on:** #0006 (the running pipeline). **Blocks:** none.
**Touches:** `skills/spawn-adversarial-review.md`, `CLAUDE.md`.

## User story
As the operator paying for pipeline runs, I need the static standards/protocol files that every
spawned reviewer re-reads to be served from cache instead of re-billed on each spawn, so that runs
cost less while every reviewer still sees byte-identical content.

## Acceptance criteria
1. `skills/spawn-adversarial-review.md` contains a section that documents structuring each spawn so
   the static standard(s) form a stable prefix eligible for prompt caching, with the volatile artifact
   placed after it.
2. That section contains the literal string `content hash` describing the guardrail: cache validity is
   tied to the standards file's content, so a standards edit is never served stale.
3. That section contains the literal string `cache_read_input_tokens` in a verification step that
   confirms a cache hit on a repeat spawn.
4. That section contains the literal statement that caching changes ordering only, not the content any
   reviewer receives.

## Implementation plan
1. Confirm how prompt caching applies to Claude Code Task-spawned subagents (automatic vs explicit
   `cache_control`); record the finding in the skill.
2. Update `skills/spawn-adversarial-review.md` with the stable-prefix structure, the content-hash
   invalidation guardrail, the `cache_read_input_tokens` verification step, and the ordering-only
   statement (acceptance criteria 1–4).
3. Add one line to `CLAUDE.md` stating spawns place static standards before the volatile artifact for cache reuse.
4. Verify the skill against acceptance criteria 1–4.

## Out of scope
Third-party compression proxies; caching volatile artifact content; changing what reviewers see.
