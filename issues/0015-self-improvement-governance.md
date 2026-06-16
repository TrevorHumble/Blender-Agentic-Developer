# Issue #0015 — Self-improvement governance: capture protocol + self-modification bar

**Type:** ready. **Category:** standards / architecture.
**Depends on:** #0006 (orchestrator), #0010 (issue tiers), #0013 (reviewer independence).
**Blocks:** none.
**Touches:** `agents/orchestrator.md`, `DESIGN.md`, `CLAUDE.md`,
`standards/adversarial-review-protocol.md`, `skills/capture-system-defect.md` (new).

This issue is itself a system-level change (it touches the protocol, `DESIGN.md`, and `CLAUDE.md`). It
does not exempt itself: when implemented, its artifact is reviewed under the two-independent-reviewer bar
it defines — the bar applies to the change that creates it. No bootstrap exemption is written.

## User story
As the operator who is out of the operational loop, I need the orchestrator to (a) notice and capture
defects in its own machinery that surface while it is doing ordinary Blender work, instead of silently
working around them, and (b) hold changes to its own governing rules to a higher review bar than
ordinary work, so the system gets safer as it improves itself rather than quietly drifting.

## Background
Two gaps were found by inspection (2026-06-16):

1. **No capture loop.** `agents/orchestrator.md` only knows how to execute a designated segment. Nothing
   tells it that when a *system* defect surfaces during a Blender-development run — a skill returns a
   wrong result, the RAG is stale, a reviewer rubber-stamps or false-flags, a standard is ambiguous, a
   process step misroutes — it must capture that defect and route it through the living-repo pipeline.
   Today it would most likely work around the problem or not notice it. The mechanism to make a change
   exists (DESIGN.md "Living-repo-same-pipeline"); the *trigger* from "doing the work" to "improving the
   system" does not.
2. **Self-modification has the same bar as ordinary work.** The orchestrator authors and gates changes
   to its own governing standards and protocol — a closed loop with no external reference. In a
   self-modifying system this is the integrity risk that matters most. A single reviewer (even an
   independent-model one per #0013) is a thin gate for a change to the rules that make the rules.

## Acceptance criteria

Every criterion resolves to a literal-string or structural grep that a separate agent can verify by
reading only the produced artifact — no semantic interpretation. Where intent matters, the intent is
encoded AS a required literal string the implementer must include, so the check stays a grep. The
Given/When/Then frame names the artifact, the grep, and the location.

### Capture protocol
1. **Given** `agents/orchestrator.md` after implementation, **When** a reader greps it, **Then** it has
   a section heading containing the literal string `system defect`, and that section contains the
   literal string `do not silently work around`.
2. **Given** that section, **When** a reader greps it, **Then** it contains the literal string
   `capture it as an issue` and the literal string `issue → review`.
3. **Given** that section, **When** a reader greps it, **Then** it contains all four literal strings
   `fix-now`, `backlog`, `blocks the current task`, and `does not derail`.
4. **Given** the new file `skills/capture-system-defect.md`, **When** a reader opens it, **Then** it has
   YAML frontmatter containing `name:` and `description:`, contains the literal string
   `do not silently work around`, contains the literal strings `standards/issue-standards.md` and
   `skills/issue-create.md`, and does **not** contain the literal string `Graduate after:` (the
   anti-bloat check: it references the tier definitions, it does not paste them).

### Self-modification bar
5. **Given** `standards/adversarial-review-protocol.md` after implementation, **When** a reader greps
   it, **Then** it contains each of these literal strings: `two independent reviewers`,
   `system-level change`, `independent of each other and of the implementer`, and
   `disagreement is treated as FAIL`.
6. **Given** the `system-level change` definition in `DESIGN.md`, **When** a reader greps it, **Then**
   it contains each of these exact literal strings — `standards/adversarial-review-protocol.md`,
   `standards/`, `agents/`, `DESIGN.md`, `CLAUDE.md` — and contains the literal string `not system-level`.
7. **Given** `CLAUDE.md` after implementation, **When** a reader greps it, **Then** it contains a line
   beginning with `- ` that includes the literal string `do not silently work around`, and a line
   beginning with `- ` that includes the literal string `two independent reviewers`.
8. **Given** `CLAUDE.md` after implementation, **When** a reader greps it, **Then** it contains the
   literal string `the soft cap and the severity adjudicator still apply` (reconciled with #0020 — the
   two-reviewer bar is additive on top of the soft cap + severity gate, not the old hard cap).

## Implementation plan
1. **Capture protocol in `orchestrator.md`.** Add a `## Capturing a system defect mid-run` section:
   the trigger (a defect in the machinery surfaces during a run), the rule `do not silently work
   around`, the action `capture it as an issue` routed through `issue → review`, and the
   fix-now-vs-backlog decision: choose `fix-now` only when the defect `blocks the current task`'s
   correctness or safety and cannot be worked around without compromising the deliverable (pause →
   fix through the pipeline → resume); otherwise file at `backlog`, the run `does not derail`, continue.
2. **Capture skill.** Write `skills/capture-system-defect.md` (single responsibility: turn a noticed
   system defect into a correctly-tiered issue without derailing the current task). Cross-reference
   `skills/issue-create.md` and the issue tiers; do not duplicate them.
3. **Self-modification bar in the protocol.** Add the `two independent reviewers` rule for a
   `system-level change`, with the literal independence and disagreement conditions (AC5).
4. **Define `system-level change` in `DESIGN.md`** with the enumerated artifact list and the explicit
   carve-out that ordinary add-ons / non-governing skills are single-reviewer.
5. **`CLAUDE.md` operating rules.** Add the two one-line rules (capture; two-reviewer bar), the literal
   `the soft cap and the severity adjudicator still apply`, and keep the stop-condition cross-reference intact.

(Gating policy is not an implementation step — see the self-binding note near the top for how this issue
itself is reviewed.)

## Out of scope
- Building the regular architectural / design-philosophy review gates (separate issue).
- Automating defect detection (the trigger is the agent noticing; no telemetry/heuristics here).
- Retroactively re-reviewing already-merged system artifacts under the new bar.
