# Issue #0019 — In-license constraint (GitHub Pro + Anthropic Max only)

**Type:** ready. **Category:** governance / standards.
**Depends on:** #0001 (DESIGN.md), #0010 (issue tiers in `standards/issue-standards.md`).
**Blocks:** none.
**Touches:** `DESIGN.md`, `CLAUDE.md`, `standards/issue-standards.md`.

## User story
As the operator who holds only a GitHub Pro license and an Anthropic Max subscription, I need the
system to refuse, at review time, any work that would require an external or paid API, account, key, or
third-party SaaS, so that I am never asked to buy, sign up for, or wire up a service outside those two
entitlements.

## Background
An audit (2026-06-16) confirmed the repo is currently 100% in-license. This issue encodes the constraint
so `reviewer-issue` enforces it on every future issue, and the in-license eval/CI stack is documented.
The only sanctioned model access is the Anthropic subscription; the only sanctioned CI is GitHub Actions
on the public repo; the external asset generators in the Blender MCP toolset are prohibited.

## Acceptance criteria
1. **Given** `DESIGN.md` after implementation, **When** a reader greps it, **Then** it contains a heading
   containing the literal `Governance: in-license constraint`, and that section contains each literal:
   `GitHub Pro`, `Anthropic Max`, `no other external/paid API`, and `Claude-as-judge`.
2. **Given** that DESIGN.md section, **When** a reader greps it, **Then** it lists the prohibited Blender
   asset generators with each literal: `download_polyhaven_asset`, `download_sketchfab_model`,
   `generate_hyper3d_model_via_text`, and `generate_hunyuan3d_model`; and it names the local-only allowed
   call with the literal `execute_blender_code`.
3. **Given** that DESIGN.md section, **When** a reader greps it, **Then** it names prohibited hosted
   eval/judge services with each literal: `Braintrust`, `LangSmith`, and `OpenAI Evals`.
4. **Given** `CLAUDE.md` after implementation, **When** a reader greps it, **Then** it contains a line
   beginning with `- ` that includes the literals `GitHub Pro`, `Anthropic Max`, and `no external`.
5. **Given** `standards/issue-standards.md` after implementation, **When** a reader greps it, **Then** it
   contains a review check containing each literal: `out of license`, `external/paid API`,
   `non-Anthropic model key`, `hosted third-party service`, and `FAIL`.

## Implementation plan
1. Add a `## Governance: in-license constraint` section to `DESIGN.md` with the two-entitlement rule,
   the Anthropic-only model rule, the local-only Blender rule (allowed local call: `execute_blender_code`;
   prohibited asset generators listed by exact name: `download_polyhaven_asset`, `download_sketchfab_model`,
   `generate_hyper3d_model_via_text`, `generate_hunyuan3d_model`), the GitHub-Actions-on-public-repo CI
   note, and the `Claude-as-judge` eval stack naming the prohibited services `Braintrust`, `LangSmith`,
   `OpenAI Evals` (ACs 1-3).
2. Add one operating-rule line to `CLAUDE.md` (AC4).
3. Add an issue-review check to `standards/issue-standards.md`: an issue that requires anything beyond
   GitHub Pro + Anthropic Max is `out of license` and is FAILed (AC5).

## Out of scope
- Rewriting historical BUILDLOG entries (append-only; the Supabase mention there records a rejection).
- Adding the constraint to every existing closed issue (it is enforced going forward).
