# Issue #0009 — Future-work backlog

**Type:** backlog. **Status:** backlog — none of these are ready to implement.

## What this is
A backlog of deferred work. Each entry is a **backlog item**, not a ready-to-implement issue. A
backlog item captures intent and a testable desired outcome; it deliberately has **no Haiku-ready
implementation plan**, because the feature has not been researched or designed yet — writing one now
would be fabrication. Before any item is implemented it **graduates** to its own numbered ready-issue
that meets full `standards/issue-standards.md`, starting with a research spike via `agents/researcher.md`.
A backlog item is never implemented in place.

## The backlog bar (what `reviewer-issue` judges these against)
Each entry has: a consumer-POV user story; a testable desired outcome; a `Depends on` line; and a
`Graduate after` line naming a **deterministic** condition that must hold before implementation.
Backlog entries omit the `Blocks` and `Touches` fields that a ready-issue requires, because the
artifacts and file paths do not exist yet — those fields are populated at the graduate step when the
paths are known. This is the only relaxation from the ready bar, and it is the reason these are
backlog, not ready.

---

## B1 — reviewer-architecture agent + even/odd routing
**User story:** As an issue author whose issue will be routed to architectural review, I need that
review to exist with a clear bar, so my issue's structural fit is judged consistently.
**Desired outcome:** An architecture reviewer exists that, given an issue and `DESIGN.md`, returns
PASS/FAIL and FAILs any issue that contradicts the documented architecture or duplicates an existing
component. (Even/odd routing is a mechanism decided during graduation, not part of this outcome.)
**Depends on:** a stable `DESIGN.md`. **Graduate after:** a research spike defines which architectural-fit
checks are objectively testable.

**Superseded by #0016** (regular architectural + design-philosophy review, trigger-based cadence).

## B2 — CI/CD enforcement
**User story:** As Trevor, who cannot personally audit every change, I need quality enforced
automatically rather than by an agent remembering to check.
**Desired outcome:** ruff lint+format, pytest with a ≥80% coverage gate, and pre-commit hooks run on
every commit and block the commit on failure.
**Depends on:** the first Python code artifacts existing. **Graduate after:** a research spike on the
Python/Blender add-on toolchain, and headless harness ready (#0022).

Graduated to #0024

## B3 — Ralph-loop stop-hook automation
**User story:** As Trevor, who needs the review loop to run to completion autonomously, I need it
enforced by a stop hook rather than by manual discipline.
**Desired outcome:** A stop hook intercepts any attempt to exit the loop before the reviewer returns
PASS (or the 3-round cap) and re-injects the task — verifiable by a test that forces an early exit and
asserts the loop continued. Specific anti-gaming guards are out of scope for this backlog entry.
**Depends on:** the built stop-condition, and Claude Code stop-hook support (an external capability,
not a repo artifact). **Graduate after:** a research spike on Claude Code stop-hook mechanics.

Graduated to #0021

## B4 — Blender add-on development standards
*Refined 2026-06-16, then DEMOTED. Picked as the third refinement, but an adversarial evaluation of the
selection found (a) a fabricated evidence claim here — corrected below — and (b) that B9 is a
higher-integrity third pick (it closes a falsified shipped promise, same class as B10/B11, zero research).
The selection was changed to B9, B10, B11; B4 keeps its corrected refinement but is no longer one of the
three. The original was a vague section list; this version ties the standard to the defects it must
prevent and makes the graduation trigger deterministic.*

**User story:** As an implementation agent building a Blender add-on, I need a written standard for what a
good add-on is — structure, registration, and the split that makes it testable — so my output is idiomatic
and passes the existing `reviewer-pr` + `reviewer-design-philosophy` gates on the first round instead of
needing refactors.

**Why this is needed (evidence):** one of the two add-ons shipped so far drew real
`reviewer-design-philosophy` findings before merge — #0018/bevel (duplicated vector helpers,
None-sentinel two-pass leak, dict/namedtuple inconsistency); #0025/phyllotaxis passed the design gate
clean ("zero red flags", BUILDLOG) but still re-derived the bpy-free-pure-function + thin-operator split
ad hoc rather than from a shared rule. So the gate is doing its job reactively, per add-on, with no
standard that names the split up front — every new add-on reinvents the structure and risks re-tripping
the same classes. A standard turns the convention into an up-front rule instead of a per-merge catch. (Note
this is a weaker "evidence" base than B10/B11, which fix already-shipped machinery that is provably inert —
B4 is preventive, not a correctness defect; see the selection note below.)

**Desired outcome:** `standards/blender-addon-standards.md` exists and is testable by literal-anchor
checks, with at minimum these named sections: (1) **structure** — the mandatory split between a
`bpy`-free pure-geometry function (unit/eval-testable, the deep module) and a thin `bpy.types.Operator`
(the registration shell); (2) **registration** — `bl_info`, `register`/`unregister`, menu append/remove,
and the `mesh.*`/`curve.*` `bl_idname` convention; (3) **extension packaging** — the Blender 5.x
`blender_manifest.toml` extension format (the 4.2+ replacement for the legacy add-on install path);
(4) **headless testability** — the add-on must be exercisable by `tests/run_pure.py` (stubbed bpy) and
`tests/run_headless.py` (`--python-exit-code 1`) with at least one eval case. It must reference
`standards/design-philosophy.md` for the deep-module rationale rather than restating it (anti-bloat), and
the existing `reviewer-pr`/`reviewer-design-philosophy` gates apply the standard — no new reviewer agent.

**Depends on:** the Blender RAG (`C:\Users\thumb\BlenderRag`) and the two shipped add-ons as exemplars
(`addons/bevel_bezier_corners.py`, `addons/phyllotaxis.py`); `standards/design-philosophy.md` (built),
which it must cite, not duplicate.
**Graduate after (deterministic trigger):** `agents/researcher.md` produces a sourced findings artifact at
`research/blender-addon-standards-findings.md` that (a) cites Blender 5.x manifest/registration/headless
sources (RAG hits or `download.blender.org`/docs URLs, in-license), and (b) records, for each of the two
shipped add-ons, whether the proposed standard's checks would have caught its actual design-philosophy
findings (non-vacuousness evidence). The existence of that artifact is the trigger.

## B5 — documentation-currency reviewer agent
**User story:** As Trevor, whose `DESIGN.md` drifted during this very build, I need an agent that catches
stale docs so the drift does not recur.
**Desired outcome:** A documentation-currency reviewer agent exists that, given a PR diff and
`standards/documentation-standards.md`, returns PASS/FAIL and FAILs when a file under a currency
trigger was changed without its corresponding doc updated.
**Depends on:** `standards/documentation-standards.md` (built). **Graduate after:** the currency-check
rule set is designed.

Graduated to #0026

## B6 — comment-review agent
**User story:** As a reviewer, I need code comments held to the why-not-what, one-line, anti-slop standard.
**Desired outcome:** A `reviewer-comments` agent exists that FAILs a comment that describes what the code
does, exceeds one line, or contains a quotable slop word.
**Depends on:** the first code artifacts, and a written comment standard. **Graduate after:** the comment
standard is written.

## B7 — resilience & reliability testing agent
**User story:** As Trevor, I need the pipeline stress-tested so failure modes surface before they hit real work.
**Desired outcome:** An agent that produces a structured report (one finding per section: failure mode
tested, result, PASS/FAIL) covering at least three modes — a reviewer that always passes, a runaway loop,
and a biased spawn.
**Depends on:** the full pipeline (issues #0002–#0008, built). **Graduate after:** a research spike on
agentic-system reliability testing.

## B8 — GitHub remote + live github-write integration
**User story:** As Trevor, I need the local repo pushed to GitHub so the work is backed up and shareable.
**Desired outcome:** A remote is configured under TrevorHumble, commits push, and `skills/github-write.md`
creates real issues/PRs via `gh`.
**Depends on:** the repo name/URL (open item). **Graduate after:** Trevor provides the repo name/URL as a
committed file (e.g., `config/github.txt`); the existence of that file is the deterministic trigger — not
a verbal approval.

Done — remote pushed to github.com/TrevorHumble/Blender-Agentic-Developer.

---

*The following were captured 2026-06-16 by the adversarial roadmap/backlog audit (recorded in
BUILDLOG): real follow-ups that existed only as "out of scope" prose inside already-shipped issues, plus
two inert-gate defects. Captured here so the work is not silently lost.*

## B9 — CI coverage-% gate + ruff (B2's unmet residual)
*Refined 2026-06-16 (promoted to the third pick after an adversarial evaluation flagged it as
higher-integrity than B4). This closes a falsified shipped promise: B2's `Desired outcome` (above)
explicitly promised "ruff lint+format, pytest with a ≥80% coverage gate," and #0024 graduated B2 while
shipping only the test/eval gate — the same docs-say-X-machinery-doesn't class as B10/B11.*

**User story:** As Trevor, who was told B2 was graduated, I need the `ruff` lint/format and the
coverage-percentage gate B2 promised but #0024 did not ship, so "B2 done" stops overstating what CI
actually enforces.

**Desired outcome (testable):** `.github/workflows/ci.yml` gains two exit-gated steps that run in the
existing in-license job (no hosted SaaS — no Codecov/Coveralls): (1) `ruff check` and `ruff format
--check` over `addons/`, `tests/`, `evals/`, failing the build on any lint/format violation; (2) a
coverage measurement of the pure-logic tests with a fail-under threshold (e.g. `coverage run` +
`coverage report --fail-under=<N>`), failing the build below `N`. A test/demo confirms a planted lint
violation reds the build and coverage below `N` reds the build (non-vacuous in both directions). `ruff` is
a single pip-installed dev tool on the GitHub-hosted runner (in-license under GitHub Pro); coverage uses
`coverage.py`.

**Open design question to resolve at graduation:** the `addons/*.py` operators need `bpy`, so coverage is
honest only over the bpy-free pure functions exercised by `tests/run_pure.py` (plain Python), OR
`coverage.py` must run under `blender --background` for the headless tests. Pick the scope (pure-only vs
headless) and set `N` against the measured baseline so the gate ratchets, never retroactively fails.

**Depends on:** #0024 (CI, shipped), #0022 (the pure + headless harness, shipped), #0019 (in-license — the
no-hosted-SaaS constraint).
**Graduate after (deterministic trigger):** a spike artifact at `research/coverage-gate-findings.md`
records (a) whether `coverage.py` runs under `blender --background` or coverage is scoped to the bpy-free
`run_pure.py` path, and (b) the measured current coverage number that sets the initial `--fail-under=N`
baseline. The existence of that artifact (with both values filled) is the trigger.

## B10 — Orchestrator writes the review verdict artifact (#0021's missing producer half)
*Refined 2026-06-16 (one of three picked). The capture was already concrete; this version pins the exact
write contract, the race with the hook's clear step, and a non-vacuous test, and flags it system-level.*

**User story:** As the orchestrator whose Stop hook (`.claude/hooks/review-gate.ps1`) blocks exit until
`.review_state/verdict.txt` shows `PASS` or `EXIT_AUTHORIZED`, I need to actually WRITE that file at each
gate decision, because today nothing in `agents/orchestrator.md` writes it — so a legitimate PASS is
re-injected every Stop until the `MAX_ITERS=25` backstop trips `CAP_HIT` (≈25 wasted rounds per segment;
fails open, so never catastrophic but never a clean first-Stop exit either).

**Why this is the highest-integrity pick:** #0021 SHIPPED the enforcement half and DESIGN.md documents the
hook as live Ralph-loop enforcement — but the producer half does not exist, so a documented safety gate is
half-wired. This is shipped machinery that does not do what the docs say.

**Desired outcome (testable):** `agents/orchestrator.md` (and `.claude/commands/build.md`) specify, as an
executable step, that on each gate decision the orchestrator writes `.review_state/verdict.txt` with the
real result token — `PASS` (reviewer PASS), `FAIL` (continue the loop), or `EXIT_AUTHORIZED` (from #0020's
severity adjudicator) — using a single agreed token form that the hook's CHECK 3 already matches. The
write/clear ownership is stated explicitly to avoid a race: the orchestrator WRITES the token before
yielding; the hook READS it and, on a legitimate-exit token, CLEARS it (per #0021 CHECK 3) so a stale
verdict cannot authorize the next segment's exit. A headless test forces a reviewer PASS, asserts the loop
exits on the FIRST Stop with no `CAP_HIT`, and a second test asserts a `FAIL` token does NOT exit — proving
the gate is non-vacuous in both directions.

**Depends on:** #0021 (hook, shipped) and #0020 (the `EXIT_AUTHORIZED` token's source, shipped).
**Graduate after (deterministic trigger):** a one-page verdict-write contract is committed (a section in
`agents/orchestrator.md` or a named skill) fixing four things — the file path, the exact token set and
match rule (resolving #0021's deferred first-token/contains-vs-whole-string note), who writes, who clears —
AND the two test cases above are enumerated. The existence of that committed contract section is the
trigger. (Implementation is itself a **system-level change** — it edits `orchestrator.md` — so it routes to
the two-independent-reviewer bar.)

## B11 — Reviewer-routing table in the orchestrator (inert specialized gates)
*Refined 2026-06-16 (one of three picked). This version enumerates the exact routing map, splits the
honesty fix from the wiring fix, and makes the trigger deterministic.*

**User story:** As a self-modifying system, I need `agents/orchestrator.md` to actually spawn the right
specialized reviewer per artifact type, because it names none of `reviewer-skill`, `reviewer-agent`,
`reviewer-documentation`, or `reviewer-doc-currency` — so a skill, agent, or doc change currently falls
through to the generic `reviewer-pr` and the specialized standard the roster advertises is never applied.
(`reviewer-doc-currency` is already honestly marked "not yet live" in DESIGN.md:91 per #0026;
`reviewer-skill`/`reviewer-agent`/`reviewer-documentation` are NOT caveated and are the actual false
live-gate claims.)

**The routing map to encode (artifact → reviewer, derived from DESIGN.md):** issue → `reviewer-issue`;
skill → `reviewer-skill`; agent → `reviewer-agent`; documentation file → `reviewer-documentation`; any PR
diff that touches a currency-triggering path → `reviewer-doc-currency`; every (non-doc) implementation
artifact → `reviewer-design-philosophy`; any system-level change or component-adding issue →
`reviewer-architecture` (at issue time). System-level changes additionally route to the
two-independent-reviewer bar (#0015). These gates compose — a single artifact can hit several.

**Desired outcome (testable):** `orchestrator.md` and `.claude/commands/build.md` carry this map as an
executable step-5 routing table (not just prose in DESIGN.md). A headless/structural test asserts at least:
a skill diff selects `reviewer-skill`, an agent diff selects `reviewer-agent`, and a currency-triggering
diff selects `reviewer-doc-currency`. Split into two deliverables so the honesty fix can land immediately:
(1) **now** — DESIGN.md marks `reviewer-skill`/`reviewer-agent`/`reviewer-documentation`/`reviewer-doc-currency`
as "selected via the routing table, not yet routed in orchestrator.md" (removes the false live-gate claim,
same defect class the doc-currency gate exists to catch); (2) **graduation** — the table is wired and tested.

**Depends on:** #0016 (reviewer-architecture/design-philosophy) and #0026 (reviewer-doc-currency) — the
reviewers exist; this only routes to them.
**Graduate after (deterministic trigger):** the artifact→reviewer table above is committed in
`agents/orchestrator.md` step 5 with each row naming a literal reviewer file, AND the test cases are
enumerated. The existence of that committed table is the trigger. (Implementation edits `orchestrator.md`
→ **system-level change** → two-independent-reviewer bar.)

## B12 — GitHub issue tracker reconciliation (or declare BUILDLOG canonical)
**User story:** As anyone reading the GitHub board, I need it to match reality, because every implemented
and graduated issue is still OPEN, and #0019–#0026 (eight shipped issues) were never filed — the board
misrepresents project state.
**Desired outcome:** Either (a) the tracker is reconciled — shipped/graduated GH issues closed with a
"see BUILDLOG" reference and #0019–#0026 filed — or (b) the repo declares BUILDLOG + `issues/` canonical
and stops mirroring to GitHub. One source of truth, stated in DESIGN.md.
**Depends on:** none. **Graduate after:** Trevor picks (a) reconcile or (b) abandon GitHub mirroring.

Done — Trevor chose (b) via adversarial diagnosis (#0027): BUILDLOG + `issues/` declared canonical, the
`gh issue create` path removed from `github-write.md`, and the GitHub board archived read-only. See #0027.

## B13 — Per-add-on eval coverage (phyllotaxis + future add-ons)
**User story:** As the eval suite, I need a case per shipped add-on, because `evals/cases.py` covers only
the bevel add-on; the phyllotaxis add-on (#0025) shipped with zero eval coverage.
**Desired outcome:** `evals/cases.py` includes a phyllotaxis case (e.g., count→vertex-count and
golden-angle spacing), and the eval harness generalizes to N add-ons; CI runs them all.
**Depends on:** #0023 (eval harness), #0025 (phyllotaxis). **Graduate after:** the multi-add-on eval shape
is designed (one module per add-on vs a shared case list).

---

*(The ready-vs-backlog tier itself is not a backlog item — it is small and ready, so it lives as a
ready-issue: see `issues/0010-issue-tiers.md`.)*
