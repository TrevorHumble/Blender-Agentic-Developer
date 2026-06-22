# Blender Orchestrator

**As a newcomer (human or agent) opening this repo, I need a front door that orients me and points me to the right file for depth, so I can engage the system without reading every file.**

This repo is a Claude Code orchestrator agent that builds and maintains Blender add-ons. All work — add-on features, skill updates, agent changes — flows through one pipeline: `issue → review → implement → PR → review → commit`. The system is self-maintaining: changes to the skills and agents that run it go through the same pipeline. Trevor sets vision; adversarial reviewer agents are the gate. See [DESIGN.md](DESIGN.md) for the full system design, [PLAN.md](PLAN.md) for the build sequence, and [CLAUDE.md](CLAUDE.md) for the operating rules loaded each session.

---

## The goal (this year)

*One year, landing with Trevor's master's in animation. This is the North Star every decision serves — written in his voice.*

**Who it's for:** you — the creator with a clear vision and a high bar, who can't read the code to know it's real.

**Today:** you *have to* police the work — re-reading, re-prompting, second-guessing — because AI so often ignores what it's told, ships spaghetti, or passes off slop, and you can't read the code to catch it yourself. The guard is warranted. It's also exhausting, and it's the job you can't actually do.

**Instead:** you *direct* the work — say what you want and what "good" means, hand the building off, and trust that your intent, your quality bar, and sound practice are enforced for you wherever a machine can. Your energy goes into the animation and the ideas, not the checking.

**The payoff:** the toil falls away — and the hours and attention you get back show up in the work: more ambitious animation, a stronger thesis. The anxiety of not being able to read the code is no longer the price it used to be.

### Goal 1 — Trust without checking
**Earn the confidence to direct your work and trust it meets your standard and sound practice — without reading a line of the code — by building the tool to enforce your quality bar automatically, so you create instead of police.**

- The work is checked automatically — the checks run on their own, on every build, without you having to ask or stand over them. Quality is the default, not something you chase.
- You've watched the checks catch deliberately-broken work — the tool is regularly fed known-bad changes to prove the guards fail when something's wrong — so you believe the green light instead of just hoping.
- You can say what you want and confirm the result is what you actually *meant* — your intent and standard, not a drift — and where a machine genuinely can't judge that, you're the final eye in Blender.
- The tool enforces a clear standard for what good looks like — *yours*, made automatic — across code, design, user experience, and how software gets built — so what it can catch doesn't slip past.
- Over the year, the tool has repeatedly delivered what you asked — clean, not spaghetti, not slop — and it held. The guard you've had to keep up, because AI kept earning it, can finally come down — and that attention goes back into the animation.

### Goal 2 — Software that holds up
**Make what the tool builds hold up as durable software — maintainable, secure, and staying clean as it grows — so it's built to a bar a developer could pick up and trust, if you ever took it further.**

- You can grow the work knowing nothing that already worked quietly breaks — every change is regression-tested, so moving forward never silently costs you ground.
- You could hand any of it to a developer and they could pick it up and run with it — maintainable, documented, hardened, not just "it runs."
- The risks you can't see — leaked secrets, security holes, fragile or compromised dependencies — are caught by checks that don't rely on you noticing or on an AI's opinion, but run the same way every time.
- It stays clean as it grows — what you build starts at a good standard and keeps it — so it's ready to scale or share if you ever choose to.
- The tool holds its own code to the same bar it enforces on everything else, even as it changes — it can get simpler, but never drops below its own standard.

### Out of scope (this year)
- **The products themselves** — you build the tool, not the add-ons it makes.
- **Actually selling it or putting it in other people's hands** — this year is about it being *ready* to, not doing it.
- **Hands-off autonomy** — you stay the director.

---

## Getting started

For the plain-language version of what a passing build proves — and where you're still the final eye — see [WHAT-IT-CHECKS.md](WHAT-IT-CHECKS.md).

**Run the checks locally.** `tests/run_tests.ps1` runs every gate, but it requires Blender for the Blender-side gates (it exits with `TESTS_FAILED: blender not found` if Blender is missing). With no Blender installed, run the three bpy-free pure gates standalone with plain Python: `python tests/run_pure.py`, `python tests/run_phyllotaxis_pure.py`, `python tests/mutation_harness.py`. Override the Blender path for the full run with `$env:BLENDER_EXE`:

```powershell
tests/run_tests.ps1
$env:BLENDER_EXE = "C:\path\to\blender.exe"; tests/run_tests.ps1
```

The three bpy-free gates need no Blender — run them with plain Python:

```powershell
python tests/run_pure.py            # bevel geometry
python tests/run_phyllotaxis_pure.py # phyllotaxis geometry
python tests/mutation_harness.py     # the tamper gate
```

**What CI runs on every push and PR** (`.github/workflows/`): `ci.yml` lints the add-ons (ruff + bandit), runs the geometry tests and the mutation/tamper gate, then downloads Blender and runs the headless operator tests + eval suite, and uploads a rendered preview of each add-on as a downloadable artifact. `codeql.yml` runs GitHub's CodeQL security scan. See [tests/README.md](tests/README.md) for the gate-by-gate table.

**Trigger a build.** Run `/build <goal>` (the orchestrator slash command at `.claude/commands/build.md`); it carries the goal through `issue → review → implement → PR → review → commit`.

**Where the add-ons live.** `addons/` holds the shipped Blender add-ons and their install instructions (`addons/README.md`). Full design rationale is in [DESIGN.md](DESIGN.md).

---

## Repo layout

| Path | Purpose |
|---|---|
| `standards/` | Authoring and review standards (adversarial protocol, documentation, skill, agent, issue, design-philosophy) |
| `skills/` | Orchestrator action skills (issue-create, spawn-adversarial-review, github-write, blender-rag, etc.) |
| `agents/` | Agent definitions (orchestrator, implementation-agent, reviewers, researcher, severity-adjudicator) |
| `addons/` | Blender add-ons: `bevel_bezier_corners.py`, `phyllotaxis.py` |
| `tests/` | Dependency-free headless test harness (`run_pure.py`, `run_headless.py`, `run_tests.ps1`) |
| `evals/` | Deterministic geometry + Claude-as-judge eval harness (`cases.py`, `run_evals.py`, `judge.md`) |
| `.github/workflows/` | CI pipeline (`ci.yml` — runs on every push and PR) |
| `config/` | Repo-level config (`github.txt` holds the remote URL) |
| `issues/` | Filed issues (`NNNN-*.md`) |
| `DESIGN.md` | Architecture decisions, rationale, lifecycle definitions |
| `PLAN.md` | Build plan: segment order, model policy, bootstrap protocol |
| `CLAUDE.md` | Operating rules loaded every session |
| `BUILDLOG.md` | One-line entry per committed segment |

---

## Build status

Live at [github.com/TrevorHumble/Blender-Agentic-Developer](https://github.com/TrevorHumble/Blender-Agentic-Developer). CI runs on every push and PR via GitHub Actions; two add-ons shipped (`bevel_bezier_corners`, `phyllotaxis`); headless test harness and eval harness passing.
