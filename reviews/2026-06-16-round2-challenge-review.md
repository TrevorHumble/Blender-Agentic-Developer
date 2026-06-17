# Round 2 — Challenge Review (the panel attacks our own conclusions)

**Date:** 2026-06-16. **What this is:** After the first review (see `2026-06-16-major-adversarial-review.md`),
Trevor and the AI pushed back and reached new conclusions. Trevor then re-ran the same eight independent
agents with a sharper mandate: *judge against Trevor's REAL goal — a non-developer shipping maintainable,
scalable, hardened, handoff-able software via AI, who needs gates to do the code-checking he can't —
and attack OUR new conclusions, assuming we're rationalizing to keep what we built.* They did.

**Read this first:** the panel knocked down several of the conclusions the AI gave Trevor an hour earlier.
It took fresh agents told to distrust the AI to catch it; the AI did not catch itself. That is the whole
case for running these reviews — and the reason to trust this report over the plan it overturns.

---

## The headline

Our "make it real" plan (P0 fix the gate → P1 PR flow + wire dead reviewers → P2 coverage/geometry gates
→ P3 de-dup docs → P4 build the SVG editor) **repeats the original mistake**: four tiers of polishing the
factory ahead of the one product. Six of eight agents, independently, said the order is backwards: **build
the product first, and let its real failures reveal which gates actually earn their place.** Gates built
now are calibrated against two toy 150-line add-ons and will be the wrong shape for the multi-file SVG
editor anyway.

---

## What the panel KILLED (things we were about to do that don't help Trevor)

1. **"Context isolation makes the reviewer independent" — overclaimed; two different problems conflated.**
   Hiding the implementation plan from the reviewer fights *anchoring* (being talked into agreeing) — real,
   worth doing. It does **nothing** about *correlation* — two Claude reviewers share the same built-in
   blind spots regardless of what you show or hide. Independence is a property of the model's weights, not
   the prompt. Keep context isolation, but it's a small fix, not "independence." (It also isn't built yet:
   the PR reviewer currently reads the issue file, which contains the plan.)

2. **The coverage-% gate — it's the booby prize.** Coverage measures whether a line *ran*, not whether
   anything *checked the result*. You can hit 90% asserting nothing. For a non-coder a green "90%" is worse
   than no number — false confidence he can't audit. The honest metric is the **tamper/mutation test**
   (deliberately break the add-on, confirm the test catches it) — which Trevor already does by instinct but
   which lives nowhere as an automatic gate. Cut the coverage gate; promote the tamper test.

3. **P0–P4 sequencing — governance before product.** The SVG editor sat at P4 with zero discovery, behind
   four governance tiers. That guarantees product stays untouched. Reverse it.

4. **"Wire the 4 dead reviewers" — delete them instead.** Wiring them adds cost and more correlated opinion,
   not coverage. The fact they were never invoked is evidence they weren't needed.

---

## What the panel says Trevor is MISSING (where he's under-protected)

1. **Tests that check the output is *correct*, not just structural.** Today the tests check the add-on makes
   the right *number* of points, never that the geometry is right — a visibly-wrong fillet passes CI.
   `phyllotaxis` has zero automated tests. This is the real stand-in for the code-reading Trevor can't do.

2. **A non-LLM security layer — free, first-party, and currently OFF.** This was the strongest new finding.
   The repo has **zero** security checking. GitHub provides three free, in-license, first-party tools:
   **Secret Scanning + push protection, Dependabot, and CodeQL.** They deterministically catch leaked
   credentials, vulnerable dependencies, and injection-class bugs — the one layer a malicious file *can't
   talk its way past*, which is exactly what a non-coder needs. Trevor's own "in-license / no SaaS" rule was
   being misread to exclude them; they are GitHub-native and fully in license. This is the single
   highest-value, lowest-cost action in either review. (The SVG editor will parse untrusted SVG files — an
   XXE/injection surface — so the habit must be set now.)

3. **A real product/handoff documentation layer.** The docs aren't *too much*, they're the *wrong kind*.
   Nothing says, in plain words, what each add-on does, why it's built that way, and what a developer
   inheriting it must know. For someone who only knows the software through docs, that's the real gap;
   "trim the docs" would have missed it. (The one genuinely good Trevor-facing doc, `addons/README.md`,
   isn't even covered by the documentation standard.)

---

## The two hard truths Trevor asked for

**1. You probably need a human who can read code — occasionally — and the current rules steer you away from
it.** Every "independent" reviewer is the same AI family grading its own family's work, and you (the only
human) can't read the answer key. For a corner-rounder, irrelevant. For "something we want to scale," it's
*the* gap. A few hours of a real developer (a contractor, an OIT colleague) a few times a year covers the
blind spot more cheaply than thousands of lines of AI-checking-AI. The "no human in the loop" + "in-license"
framing *feels* disciplined but is quietly talking you out of the one thing that actually protects you.
Demote "no human in the loop" from an architectural law to "default, with a scheduled human audit for
anything meant to scale."

**2. A one-sentence test so "I need gates" doesn't become a blank check.** Your instinct — "I can't verify
code, so I need gates" — is right, but as stated it could justify *infinite* governance. The usable line:

> **A gate protects you only if (a) it runs automatically — nobody has to remember to run it — and
> (b) it checks the *product*, not the *process*.**

Your headless test and your live-Blender check pass. The coverage gate, the severity adjudicator, the
self-modification bar, the reviewer roster, the celebratory BUILDLOG — none run automatically against your
product. That test lets you cut the theater yourself, with confidence, without reading any code.

---

## Still broken on disk (we paused, then planned — never fixed)

- The Stop-hook's exit token is spelled two ways (`EXIT AUTHORIZED` vs `EXIT_AUTHORIZED`) and nothing writes
  the verdict file it reads — the gate's happy path is still dead code (entangled with the undecided
  "do we run autonomously at all" question — left alone deliberately).
- `DESIGN.md` still asserts a "≥80% coverage" gate and a "pytest/coverage.py" stack that don't exist — the
  doc defining the gate describes fiction.

---

## The recommended path — PRODUCT FIRST

1. **Start the SVG editor as a small discovery spike** — import one real SVG into grease pencil, export it
   back, by hand in Blender. It's far bigger than the toys and nobody has scoped it. Output: the 3–5 real
   hard problems, which then become the actual product issues.
2. **Wire only the gates that pass the one-sentence test, behind that product:** output-correctness tests,
   the tamper test as a real automatic gate, the live-Blender check named as the official feature gate,
   branch protection so nothing reaches `main` unchecked, and the three free security scanners.
3. **Fix-or-delete the broken bits** — don't keep machinery that lies about what it does.
4. **Add the occasional human audit** for anything meant to scale.
5. **Cut the governance-about-governance; add the product/handoff docs; de-slop the BUILDLOG.**

The SVG editor stops being a someday-item and becomes the thing that *proves* which governance is real.

---

## Actions taken while Trevor was out (2026-06-16)

See the BUILDLOG and the commit log for specifics. In short: produced this report; turned on the free,
deterministic security layer (the panel's #1 recommendation, in-license, reversible); clarified the
in-license rule so it no longer blocks those tools; and filed the round-2 findings as GitHub issues so the
board reflects the real path and Trevor can reprioritize. No governance was ripped out and no architecture
decision was made unilaterally — those await Trevor's call.

## Open decisions waiting for Trevor

- **Direction:** product-first (recommended) vs keep fixing the factory first.
- **The human audit:** yes/no, and who, for anything meant to scale.
- **Autonomy:** does the loop ever run unattended (the security review says not safely today), or does it
  stay supervised with Trevor as the live gate?
- **How much governance to cut** (the adjudicator, self-mod bar, unwired reviewers, duplicated docs).

---

## Where the round-2 evidence and sources live

Eight agent reports (with `file:line` citations and external research links) underpin this summary. Topics
researched include: LLM-as-judge self-preference / same-family correlation, anchoring/confirmation bias in
code review, Goodhart's law on coverage gaming, mutation/golden-file/property-based testing, the real Ralph
loop, prompt-injection in agentic systems, and the free GitHub security tooling. Available on request.
