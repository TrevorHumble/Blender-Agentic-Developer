# Issue Standards

**As a reviewer or implementer of an issue, I need a single checkable standard so I can determine whether an issue passes or fails without guessing.**

---

## User story

Written from the end-consumer POV: the agent, human, or system that will use the produced artifact. Format: `As a [consumer], I need… so that….` If you cannot name a consumer, the issue has no purpose.

---

## Acceptance criteria

Written as Given/When/Then criteria testable by an agent. Each criterion must be a literal string or structural check — present/absent phrase, section header, file path, token count — that a separate agent can verify by reading only the produced artifact, with no semantic interpretation required.

For a documentation issue, acceptance criteria must reduce to literal string or structural checks (no criterion of the form "an agent can understand X" — that is unfalsifiable). Lesson from issue #0001: every AC that said "an agent can answer X" was unfalsifiable; rewrite as "the file contains the phrase `X`".

---

## The Haiku bar

The implementation plan is a clarity heuristic: it must be clear and unambiguous enough that following it would not send a weak model off the rails. It is a thought experiment about plan clarity, not a requirement to inline every fact. The implementer is a Sonnet agent; Opus is used only for review.

---

## Dependency map

Every issue must include:

```
Depends on: <issue number(s) or "none">
Blocks: <issue number(s) or "none">
Touches: <file paths or artifacts modified>
```

All three fields are required. Missing a field is a FAIL.

---

## Reviewer checklist

- [ ] PASS/FAIL — User story names an end-consumer (not the author) and follows `As a [consumer], I need…` form.
- [ ] PASS/FAIL — Every acceptance criterion is in Given/When/Then form and resolves to a literal string or structural check.
- [ ] PASS/FAIL — Implementation plan is present and contains at least three numbered steps, each naming a file path or a concrete deliverable.
- [ ] PASS/FAIL — Dependency map contains all three fields: `Depends on`, `Blocks`, `Touches`.
- [ ] PASS/FAIL — No FINAL, LAST, or TRULY_FINAL in filenames or section headers referenced by this issue.
