---
name: spawn-adversarial-review
description: >
  How to spawn an unbiased adversarial reviewer. Use when asked to "spawn a reviewer",
  "run an adversarial review", "get an independent review of X", or "review this with
  no bias" — and when the reviewer must enter with no prior attachment to the artifact.
---

# Spawning an adversarial reviewer

**Protocol:** `C:\Users\thumb\blender-orchestrator\standards\adversarial-review-protocol.md` — read it in full before spawning any reviewer.

## De-bias rules (required; no exceptions)

**Give the goal, not the implementation.** State the objective the artifact is judged against. Do not name the mechanisms ("it uses X loop, a Y gate") — that pre-confirms their existence and narrows the review.

**No positive hints.** Never include "the one thing we got right is…" or any framing that pre-establishes a passing area. The reviewer enters assuming everything is bad and discovers what survives.

**Plant no suspicions.** "Suspect X is broken" leads the witness toward a predetermined finding and away from problems you did not anticipate. Say "assume failure, look hard."

**Minimum context — no biasing framing.** Give the artifact + the relevant standard + the protocol, and none of your hopes or explanations. Every additional sentence is a potential bias vector.

**Full scope — list every artifact actually under review.** Anything not listed is itself a finding. Do not give the reviewer a curated subset.

## Bias gate (required before fan-out)

Before spawning N reviewers, spawn one independent agent to audit the briefing for bias. That agent returns required edits with quoted evidence. Apply the edits. Then fan out.

## Fan-out threshold

High-stakes reviews: minimum three independent adversaries. A finding is recorded only when ≥2 of 3 confirm it. A verdict of fine requires the same threshold. Fewer than three = invalid review.

## Spawner must never

1. Name suspected weak parts — that leads the witness.
2. Include positive framing or "we tried hard on X."
3. Allow the producing agent to review its own output.
4. Accept a PASS without verifying every cited URL, every `file:line` reference, and every in-scope item has an explicit finding.

## Output contract for the reviewer

Numbered defects, each with severity (blocker / major / minor / nit) and a copy-pasteable fix. Final verdict: **PASS** or **FAIL** — one token, no hedging. PASS with open blockers or majors is not a PASS.
