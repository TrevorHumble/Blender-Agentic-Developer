# Issue #0014 — Efficiency: adopt-with-conditions (low priority)

**Type:** backlog. **Status:** backlog — **low priority**.

Each item was rated "adopt-with-guardrail" by the adversarial efficiency assessment (2026-06-15): the
saving is real but it can silently degrade quality without the stated guardrail. These are backlog
items — graduate to a numbered ready-issue before implementing. The backlog bar applies (consumer-POV
user story, testable desired outcome, `Depends on`, deterministic `Graduate after`).

---

## EC1 — Script the literal acceptance-criteria checks (E1)
**User story:** As the reviewer system, I need the literal/structural acceptance-criteria checks run by
a deterministic script so the LLM reviewer spends tokens only on the judgment pass.
**Desired outcome:** a script verifies the literal/structural acceptance criteria for an artifact and
the LLM reviewer runs only the judgment pass; critically, the script and the LLM's criteria are
generated from ONE criteria source so they cannot drift apart.
**Depends on:** issue-standards (built). **Graduate after:** a single criteria-spec format (the
no-drift guardrail) is decided — without it the script silently diverges from the criteria.

## EC2 — Haiku for mechanical re-checks (E5)
**User story:** As the operator, I need cheap mechanical re-checks routed to Haiku while judgment stays
on the reviewer model.
**Desired outcome:** mechanical re-checks run on Haiku (or a script), and a periodic audit compares
Haiku vs the reviewer-model PASS/FAIL rates on the same inputs to detect a capability gap before it
passes bad artifacts.
**Depends on:** the running pipeline (built). **Graduate after:** the "what counts as mechanical"
routing rule and the audit procedure are defined.

## EC3 — Terse structured reviewer output (E6)
**User story:** As the orchestrator consuming review output, I need reviewers to return compact
structured results so output tokens drop, without losing actionability.
**Desired outcome:** reviewers return PASS/FAIL plus numbered defects that each carry a severity field
and name a specific location/fix, and the reviewer still reasons before emitting the verdict (no
verdict-before-reasoning).
**Depends on:** the reviewer agents (built). **Graduate after:** the output schema (severity field +
reason-then-summarize order) is specified.
