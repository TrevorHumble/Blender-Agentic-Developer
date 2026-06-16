# Blender Orchestrator — System Design

## Prime directive

Trevor is a product manager at the University of Idaho OIT. He sets vision and tests outcomes. He does not write Python. Trevor is out of the operational loop. The adversarial review agents are the gate for all merges and approvals; no human approval is in the critical path.

## What the system is

A Claude Code orchestrator agent that builds Blender add-ons and maintains itself. All work — including updates to the skills and agents that run it — flows through one pipeline:

`issue → review → implement → PR → review → commit`

The system is self-maintaining: when a skill, agent, or standard needs to change, that change is issued, reviewed, implemented, and merged through the same pipeline as any add-on feature.

## Core principles

**Human-out-of-loop.** Trevor is never a required approver. The adversarial review agents approve or reject every artifact. Humans set goals; agents execute and gate.

**Unbiased reviewers.** Reviewers receive minimum context. Prior feedback, author identity, and intent framing are withheld so the reviewer evaluates what the artifact actually says, not what it was meant to say.

**Adversarial-by-design.** Reviewers are instructed to find failure, not to confirm success. A passing review means nothing was left to object to, not that the reviewer was satisfied.

**Model-by-role.** The orchestrator runs on Opus. The implementation agent runs on Sonnet. Reviewers run on a different model from the implementer. All reviewer agents run on Opus so they do not inherit the implementer's correlated blind spots. Non-reviewer spawned agents (researcher, etc.) run on Sonnet. Haiku serves as the plan-clarity bar: if a plan would send a weak model off the rails, it is not ready to ship.

**Skill-bloat guard.** When updating a skill, apply the author's intent rather than transcribing the user's words. See the Skill-bloat problem section.

**Living-repo-same-pipeline.** Skills and agents are never patched in place without review. Every change — including changes to this system itself — goes through `issue → review → implement → PR → review → commit`.

## Repo structure

```
skills/
agents/
standards/
issues/
config/         — repo-level config (github.txt holds the remote URL)
.claude/commands/build.md  — /build slash command that triggers a pipeline run
PLAN.md         — segment-by-segment build sequence
BUILDLOG.md     — one-line entries appended after each commit or halt
README.md
CLAUDE.md
DESIGN.md
```

Names only. This document describes the structure; it does not create or modify those files.

## MVP scope

### Skills

- `blender-connect` — connect to a running Blender instance
- `blender-rag` — retrieve Blender API documentation for bpy code
- `github-write` — create issues, branches, PRs, and commits
- `issue-create` — draft and file issues through the issue lifecycle
- `spawn-adversarial-review` — spawn a reviewer agent with minimum context
- `skill-writer` — write or update a skill file through the PR pipeline
- `agent-writer` — write or update an agent file through the PR pipeline
- `update-claude-md` — update CLAUDE.md after issues and PRs
- `research-prior-art` — time-boxed prior-art lookup before drafting
- `write-documentation` — write or update documentation through the PR pipeline

### Agent roster

| Role | Tier |
|---|---|
| orchestrator | Opus |
| implementation agent | Sonnet |
| reviewer-issue | Opus |
| reviewer-pr | Opus |
| reviewer-skill | Opus |
| reviewer-agent | Opus |
| reviewer-documentation | Opus |
| researcher | Sonnet |

Reviewers run on Opus so they do not share the implementer's correlated blind spots. Non-reviewer spawned agents run on Sonnet. `reviewer-architecture` is not in scope for MVP; see Deferred items.

### Process flows

- **Issue creation + review loop:** orchestrator drafts issue → `spawn-adversarial-review` sends it to reviewer-issue → PASS creates the issue; FAIL triggers revision and a fresh reviewer.
- **PR creation + review loop:** implementation agent builds the implementation → pushes PR → `spawn-adversarial-review` sends the diff to reviewer-pr → PASS merges; FAIL triggers revision and a fresh reviewer.
- **Skill/agent update loop:** changes to skills or agents enter the same `issue → review → implement → PR → review → commit` pipeline, using reviewer-skill and reviewer-agent respectively.

## Adversarial review protocol

### Minimum context

The reviewer receives only the artifact under review plus the single relevant standard. Nothing else is provided. "No framing" means the spawner adds no editorializing or expectation — it does not mean withholding the standard the reviewer requires.

For a PR review the "single relevant standard" is the linked issue's `## Acceptance criteria` section (per `agents/reviewer-pr.md`), not a separate standards file. Artifact-to-standard mapping:

| Artifact | Standard the reviewer receives |
|---|---|
| Issue | `standards/issue-standards.md` |
| PR diff | The linked issue's `## Acceptance criteria` section |
| Skill | `standards/skill-standards.md` |
| Agent | `standards/agent-standards.md` |
| Doc | `standards/documentation-standards.md` |

### Spawner constraints

The spawner must never:

- state what the artifact is trying to accomplish
- express any expectation about the outcome
- pre-answer anticipated objections
- summarize the artifact before handing it over
- identify the author
- use pass-leaning language such as "just verify" or "looks good, please confirm"

### Canonical reviewer framing

> "Your job is to find every way this artifact fails. Assume the author made mistakes. Do not give the benefit of the doubt. If something is ambiguous, treat it as a defect. Return a PASS only if there is nothing left to object to."

### Anchoring and position-bias mitigations

- A fresh reviewer is spawned for each review round. Prior reviewers' feedback is never passed to the next reviewer.
- When comparing two versions of an artifact, order is randomized and versions are labeled A/B — never "old/new" or "before/after."

### Output contract

The reviewer returns PASS/FAIL followed by a numbered list of specific defects. A PASS with no defects closes the review loop. A FAIL sends the artifact back for revision.

## Lifecycles

### Issue lifecycle

1. Orchestrator identifies a need (feature, bug, system change, documentation gap).
2. If the issue touches Blender APIs, pull the `blender-rag` skill to retrieve relevant bpy documentation.
3. Read `CLAUDE.md` and scan open issues for repo awareness before drafting.
4. Draft the issue: write an end-consumer user story, Given/When/Then acceptance criteria, an implementation plan, and a dependencies block.
5. Hand the raw issue to reviewer-issue with no framing — no summary, no intent statement.
6. Reviewer returns PASS/FAIL with a numbered list of defects.
7. On FAIL, revise the issue and re-submit to a fresh reviewer (the Ralph loop). Repeat until PASS.
8. On PASS, create the issue via `github-write`.
9. Update `CLAUDE.md` to reflect the new issue.

### PR lifecycle

1. The Sonnet implementation agent builds toward the passing issue, consulting `blender-rag` for any bpy code.
2. Push the branch and open a PR via `github-write`.
3. Hand the raw diff to reviewer-pr with no framing.
4. Reviewer checks: correctness, tests tracing to acceptance criteria, coverage ≥ 80%, lint/format, comment quality, naming, and architectural fit.
5. On FAIL, fix the implementation and re-submit to a fresh reviewer (the Ralph loop). Repeat until PASS.
6. On PASS, merge the PR.
7. Update `CLAUDE.md` and the README if public-facing behavior changed.

### Skill/agent-update lifecycle

Updates to skills or agents follow the same pipeline. The artifact goes to reviewer-skill or reviewer-agent (as appropriate) rather than reviewer-pr. No skill or agent is patched in place without a passing review. This lifecycle is the enforcement mechanism for the living-repo-same-pipeline principle.

### The Ralph loop

An external evaluator (a fresh reviewer agent) checks the work and re-injects the task until it passes. Self-assessment is not trusted — the agent that produced the artifact does not evaluate it.

**Stop condition (as-built):** a FAIL is fixed, never overridden by the author. Cap is 3 review rounds per artifact. After 3 rounds without PASS, an independent adjudicator is spawned (a fresh reviewer-class agent given adjudicator instructions — not a separate committed agents/adjudicator.md file). For every finding the adjudicator retains as blocking, it must cite — by exact text — either the specific acceptance criterion it violates or the specific clause of `standards/adversarial-review-protocol.md` it contravenes. Reclassifying a finding as non-blocking or stylistic likewise requires an explicit textual basis from one of those two sources; no finding is cleared, downgraded, or retained on bare assertion. Genuinely stylistic issues are logged to `BUILDLOG.md` as follow-up items — not silently dropped and not declared nitpicks by the author. If unresolved after adjudication, that segment halts and independent segments continue.

## Standards

### User story

Each issue begins with an end-consumer user story written from the perspective of the person or system consuming the artifact. It states who needs what and why, with no implementation detail.

### Acceptance criteria

Criteria are Given/When/Then criteria testable by an agent — literal, mechanically checkable properties of the artifact. Semantic interpretation is not required. If a criterion cannot be checked by string match or structural inspection, rewrite it until it can.

### Implementation plan

Every issue contains an implementation plan that meets the Haiku bar. The Haiku bar is a clarity heuristic: the plan must be unambiguous enough that following it would not send a weak model off the rails. The implementer is a Sonnet agent; Opus is used only when called for.

### Skills

A skill applies the author's intent rather than transcribing the user's words. When feedback arrives, diagnose the root cause and make the smallest edit that addresses it. See the Skill-bloat problem section.

### Agents

Each agent has a single responsibility, the least-privilege tool set needed for that responsibility, and a defined input/output contract. An agent that does too much is a design defect.

### Comments

Comments state why, not what. One line maximum. No filler, no restatement of what the code already says, no AI-slop voice.

### Naming

No FINAL, LAST, or v2_final in any filename. Use version numbers (v1, v2), dates, or descriptive deltas that remain accurate after the next iteration.

### Test coverage

Code artifacts require ≥ 80% test coverage. Documentation artifacts are exempt.

### CLAUDE.md update triggers

Update `CLAUDE.md` after every issue created and after every PR merged. The orchestrator loads CLAUDE.md at the start of each session; stale content degrades every subsequent decision.

### Documentation currency

When public-facing behavior changes, update the README in the same PR. When operating rules change, update CLAUDE.md. When the system design changes, update DESIGN.md.

## Skill-bloat problem

**The failure mode.** When updating a skill from feedback, the model over-indexes on the user's literal words, appends them verbatim, and bloats a tight skill into long, unfocused mush. The original intent is diluted. The skill becomes harder to invoke and harder to review.

**The discipline.** Treat feedback as a symptom report. Diagnose the root cause of the symptom, make the smallest edit that fixes it, and default to subtraction over addition. Never paste the user's sentence into the skill. Re-review the skill after every update, using reviewer-skill through the standard PR pipeline.

## Deferred items

The following are not in MVP scope. Each becomes a future issue when the system is ready for it.

- `reviewer-architecture` — even/odd architecture-review routing: every other architecture-touching PR is routed through an architecture reviewer before the standard reviewer-pr. Deferred because the architecture is not stable enough to review against.
- CI/coverage enforcement — automated enforcement of the ≥ 80% coverage standard on every PR. Currently manual.
- Ralph-loop stop hooks — automated hooks that detect a looping review and escalate or halt rather than continuing indefinitely.
- Documentation-enforcement agent — checks that CLAUDE.md and README are updated when required triggers fire.
- Comment-review agent — enforces the why-not-what, one-line, anti-slop comment standard.
- Blender add-on development standards — a `standards/` document defining bpy patterns, Eevee Next conventions, and API version constraints.
- Resilience and reliability testing — testing the orchestrator's behavior under failed tool calls, bad reviewer outputs, and looping conditions.

## Open items

Resolved (2026-06-15): repo name and URL — `github.com/TrevorHumble/Blender-Agentic-Developer` (recorded in `config/github.txt`).

Resolved: Blender RAG location — `C:\Users\thumb\BlenderRag`.

Open: license is undecided (MIT recommended) (still open as of 2026-06-15).

Resolved (2026-06-15): how Trevor triggers a run — the `/build` slash command at `.claude/commands/build.md`.

## Bootstrap

The build was bootstrapped using the global `adversarial-agents` skill at `~/.claude/skills-cloud-staging/adversarial-agents` (not an in-repo file) as the held protocol, with direct git commits and direct spawning, until the committed standards and skills in this repo took over. PLAN.md has the segment-by-segment build sequence.

## Where the documentation lives

**DESIGN.md** is the full evolving design and the source of truth for the system. When in doubt about how something works or why a decision was made, this is the document to consult. It grows with the system. On any conflict between DESIGN.md and CLAUDE.md, DESIGN.md governs and CLAUDE.md is corrected to match.

**CLAUDE.md** is the distilled operating rules the orchestrator loads at the start of each session. It is derived from DESIGN.md. It contains what the orchestrator needs to act correctly — not the full rationale, just the rules. It is kept short enough to load every time.

**README.md** is the short human-facing front door. It orients a newcomer, links to DESIGN.md for depth, and links to CLAUDE.md for operating rules. It does not duplicate content from either.
