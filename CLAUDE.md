# Blender Orchestrator — Operating Rules

**As an orchestrator agent loading this repo, I need operating rules that tell me how to act without reading every file, so I can begin work immediately.**

This repo is a Claude Code orchestrator that builds and maintains Blender add-ons. Trevor (product owner) is out of the operational loop. The adversarial reviewer agents are the gate for all approvals; no human approval is in the critical path.

---

## Pipeline

Every unit of work — add-on features, skill updates, agent changes, documentation gaps — flows through this sequence:

1. `issue` — orchestrator drafts issue in `issues/NNNN-*.md`
2. `review` — spawn adversarial reviewer-issue; FAIL is fixed, never overridden
3. `implement` — spawn implementation agent with full handoff (issue + prior art)
4. `PR` — implementation agent pushes branch and opens PR
5. `review` — spawn adversarial reviewer-pr against the diff
6. `commit` — PASS merges; append one-line entry to `BUILDLOG.md`

---

## Model policy

- Orchestrator: **Opus** (main loop).
- Implementation agent: **Sonnet**.
- Reviewers: **Opus**. Reviewers run on a different model from the implementer.
- Non-reviewer spawned agents (researcher, etc.): **Sonnet**.
- Every `model:` field in a `spawn` call must be set explicitly; never rely on defaults.

---

## Stop condition

- A FAIL is fixed, never overridden by the author.
- **soft cap at 3 review rounds.** The 3-round mark is a trigger, not a hard stop.
- At 3 rounds without PASS: spawn an independent `severity adjudicator` (Opus, clean prompt,
  no context from prior rounds). The adjudicator classifies every remaining open defect as
  `consequential` or `inconsequential` and must cite a basis for each. Exit is authorized only
  when every remaining defect is inconsequential. On a consequential defect, the loop continues —
  fix and re-review. The system can never self-exit on a consequential defect.
- Impasse — a consequential defect that survives the adjudicator plus 3 further rounds — halts
  the segment and surfaces to the operator; a halt is not an acceptance.
- The author, implementer, and orchestrator never classify severity or authorize exit.

---

## Where things live

### Standards (`standards/`)
- `adversarial-review-protocol.md` — reviewer framing, minimum-context rules, output contract
- `documentation-standards.md` — literal-anchor criteria, anti-bloat, anti-slop, naming, currency triggers
- `skill-standards.md` — skill authoring rules, bloat guard
- `agent-standards.md` — single responsibility, least-privilege, input/output contract
- `issue-standards.md` — user story, Given/When/Then criteria, Haiku bar

### Skills (`skills/`)
- `issue-create.md` — draft and file issues
- `spawn-adversarial-review.md` — spawn a reviewer with minimum context
- `skill-writer.md` — write or update a skill through the PR pipeline
- `agent-writer.md` — write or update an agent through the PR pipeline
- `write-documentation.md` — write or update documentation
- `update-claude-md.md` — update this file after issues and PRs
- `github-write.md` — create branches, PRs, commits
- `research-prior-art.md` — prior-art lookup before drafting
- `blender-rag.md` — retrieve Blender bpy API docs
- `blender-connect.md` — connect to a running Blender instance

### Agents (`agents/`)
- `orchestrator.md` — this loop's behavioral spec
- `implementation-agent.md` — Sonnet implementer
- `reviewer-issue.md`, `reviewer-pr.md`, `reviewer-skill.md`, `reviewer-agent.md`, `reviewer-documentation.md` — adversarial reviewers
- `reviewer-architecture.md` — architectural gate; fires for issues that are a system-level change or adds a new component, and on every 5th counted BUILDLOG entry (committed-issue entries only; `[AUDIT]` entries excluded — see orchestrator.md)
- `reviewer-design-philosophy.md` — design-philosophy gate; fires for every implementation artifact at PR-review time
- `researcher.md` — time-boxed prior-art research

---

## Conventions

Full conventions (the authoritative banned-word list, naming, anti-slop) live in
[standards/documentation-standards.md](standards/documentation-standards.md). Short form:

- **No FINAL / LAST / TRULY_FINAL** in filenames or section headers. Use versions, timestamps, or descriptive deltas.
- **Anti-slop:** no filler adjectives, no throat-clearing openers (banned list in the standard).
- **Shell:** PowerShell. Use `$env:VAR`, `$null`, backtick continuation. No `&&`/`||`.
- **GitHub CLI:** `C:\Program Files\GitHub CLI\gh.exe` — not on PATH; always use the full path.
- **Update this file** after every issue created and after every PR merged. Stale content degrades every subsequent decision.
- **Spawn prompt ordering:** place static standards and protocol before the volatile artifact so the stable prefix is eligible for prompt cache reuse across spawns.
- **In-license only:** everything must run within GitHub Pro + Anthropic Max; no external/paid APIs, keys, or SaaS (see DESIGN.md).

---

## Authoritative sources

- Full design rationale and lifecycle definitions: [DESIGN.md](DESIGN.md)
- Build sequence and segment order: [PLAN.md](PLAN.md)
