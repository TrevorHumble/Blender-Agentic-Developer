# Issue #0011 — `/build` slash command

**Type:** feature (ready-issue). **Status:** ready.
**Depends on:** #0006 (agents/orchestrator.md), repo CLAUDE.md. **Blocks:** none.
**Touches:** `.claude/commands/build.md`.

## User story
As the orchestrator agent — or any Claude Code session opened in this repo — I need a `/build` slash
command that takes a goal and triggers the pipeline, so that one command starts a run without
retyping the framing.

## Acceptance criteria
1. A file exists at `.claude/commands/build.md`.
2. It has YAML frontmatter containing a `description:` field.
3. Its body contains the literal string `$ARGUMENTS` (the goal is passed in).
4. Its body contains the literal strings `agents/orchestrator.md`, `CLAUDE.md`, and `standards/`.
5. Its body contains the literal string `Sonnet` (the spawned-agent model policy) and the literal
   string `issue → review → implement → PR → review → commit`.
6. Its body contains the literal string `stop-condition` or `no author override` (the loop rule).
7. The body contains no `FINAL`/`LAST` and none of the banned slop words listed in
   `standards/documentation-standards.md`.
8. The file begins with a line containing only `---`, and the frontmatter block closes with a second
   line containing only `---` before the body.

## Implementation plan
1. Create `.claude/commands/build.md` with YAML frontmatter (`description:` one line) and a body.
2. The body instructs Claude to act as the orchestrator in `agents/orchestrator.md`, following
   `CLAUDE.md` and `standards/`, with the run goal supplied as `$ARGUMENTS`.
3. The body enumerates the pipeline (research-first → draft issue → reviewer-issue → implement via the
   Sonnet implementation agent → review → commit), states spawned agents run on `Sonnet`, and references
   the stop-condition (no author override; cap 3 rounds; independent adjudication).
4. Verify the file against every acceptance criterion — confirm the `---` frontmatter fences are
   present, `$ARGUMENTS` appears in the body, and the file is under `.claude/commands/`. Keep it tight.

## Out of scope
Registering a `.claude/agents/orchestrator.md` subagent; a remote/CI trigger.
