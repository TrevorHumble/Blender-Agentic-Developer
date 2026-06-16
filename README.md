# Blender Orchestrator

**As a newcomer (human or agent) opening this repo, I need a front door that orients me and points me to the right file for depth, so I can engage the system without reading every file.**

This repo is a Claude Code orchestrator agent that builds and maintains Blender add-ons. All work — add-on features, skill updates, agent changes — flows through one pipeline: `issue → review → implement → PR → review → commit`. The system is self-maintaining: changes to the skills and agents that run it go through the same pipeline. Trevor sets vision; adversarial reviewer agents are the gate. See [DESIGN.md](DESIGN.md) for the full system design, [PLAN.md](PLAN.md) for the build sequence, and [CLAUDE.md](CLAUDE.md) for the operating rules loaded each session.

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
