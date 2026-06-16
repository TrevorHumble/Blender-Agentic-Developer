# Issue #0002 — Cross-cutting standards (Layer A)

**Type:** documentation / standards
**Status:** draft — pending adversarial review
**Depends on:** none (bootstrap layer). **Blocks:** every later segment (reviewers and docs use these).

## User story
As a reviewer agent about to judge an artifact, I need one written protocol that tells me exactly
how to be adversarial without being biased, and one written documentation standard that tells me
what a good doc must contain, so that I judge against the system's real rules instead of my priors.

## Deliverables
Two files:
- `standards/adversarial-review-protocol.md`
- `standards/documentation-standards.md`

## Source material (steal, do not reinvent)
- `C:\Users\thumb\.claude\skills-cloud-staging\adversarial-agents\SKILL.md` — the protocol source.
- `C:\Users\thumb\.claude\skills\rigorous-eval\SKILL.md` and
  `C:\Users\thumb\.claude\skills-cloud-staging\rigorous-agent-harness\SKILL.md` — depth/independence.
- For documentation: the lesson from issue #0001 in this repo — acceptance criteria for prose
  converge on **literal string / structural matches**, not "an agent can answer X."
- `claude-md-improver` and `software-design-philosophy` marketplace skills if useful.

## Acceptance criteria (checkable by an agent reading the produced files)
adversarial-review-protocol.md must contain sections/content establishing each of:
1. The literal phrase `assume total failure` (the stance).
2. A "de-bias the setup" rule set that includes giving the goal but **not** the implementation, no
   positive hints, planting no suspicions, and giving full scope.
3. A calibration rule that adversarial is not fabrication: every finding cites evidence, and the
   reviewer must retract its own over-flags.
4. An independence rule: fresh context, different identity than the author; for high stakes, multiple
   independent adversaries with majority agreement.
5. The literal phrase `research-first` (establish the current yardstick before judging).
6. A "bias gate" rule: audit the briefing for bias before fan-out.
7. A rule that human-in-the-loop resolutions are not allowed — translate any "owner reviews/approves"
   into a deterministic check or an independent adversary.
8. The literal token `PASS/FAIL` and an output-discipline rule (item-by-item, numbered defects, severities).
9. A list of at least four actions the spawner must never take when handing an artifact to a reviewer.

documentation-standards.md must contain sections/content establishing each of:
10. The rule that acceptance criteria for a documentation artifact must be **literal string or
    structural checks**, with the phrase `literal` present, and must not depend on a reader agent's
    nondeterministic answer.
11. The rule that a doc's user story is written from the consumer's POV (the phrase `consumer`).
12. An anti-bloat rule and an anti-AI-slop rule (no filler like "elegantly/robustly/seamlessly").
13. The naming rule: no FINAL/LAST/v2_final.
14. The roles of `DESIGN.md`, `CLAUDE.md`, and `README.md` (the documentation split).
15. Documentation currency triggers (when a doc must be updated).

## Constraints
Markdown only. Tight, no slop. Each file self-contained. Apply documentation-standards to themselves.
