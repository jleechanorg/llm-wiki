---
title: "WorldArchitect.AI PRs 5500+ — Jeffrey's Recent PR Descriptions"
type: source
tags: [worldarchitect, prs, github, development, jleechan]
date: 2026-04-10
source_file: gh api repos/jleechanorg/worldarchitect.ai/pulls
---

## Summary

A collection of 18 open PRs (#5500-6183) in WorldArchitect.AI representing active development work. The PRs span fix, chore, feat, and ci categories covering temporal correction logic, deployment hardening, state management, evidence gates, Claude Code tooling, and agent orchestration. All use structured PR descriptions with Summary, Production Code Changes, Test Changes, and Known Limitations sections. Bead IDs track each change against the beads issue system.

## Key Themes

**Fix PRs** (12 PRs):
- Temporal correction warnings: edge case where `attempts=0, max=0` silently returned None
- Deployment hardening: `PRODUCTION_MODE=true` for preview environment auth
- State management: empty dict truthiness bug in Dragon Knight template merging
- Wizard: whitespace normalization in campaign description input
- Living world: `inject_persisted_living_world_fallback` was debug-gated but should be always visible
- Model config: `gemini-3.1-flash-lite` added to code execution models
- UI+state: final launch CTA visibility and level-up atomicity
- Rewards/planning block: atomicity fixes and `get_campaign_state` hardening
- Skeptic cron: fail-closed evidence gate, pagination fix, bugbot check-run
- Test CI: schema prompt load perf ceiling blocking directory tests
- Claude hooks: slim Claude Code settings hooks

**Feature PRs** (3 PRs):
- Custom Campaign Wizard re-enabled with bug fixes (PR #6034)
- Claude Code repro copy command and workflow (PR #6156)
- Cursor hooks and tracked AO metadata updater (PR #6135)

**CI/Chore PRs** (3 PRs):
- Self-hosted runners required for private workflows (PR #6145)
- Claude Code settings hooks slimming (PR #6106, #6136)
- ProxyFix rate-limit regression + beads (PR #6126)

## Notable PR Descriptions

### PR #6183 — Temporal Correction Edge Case
Fixes `build_temporal_warning_message()` to warn when corrections are disabled (`max_attempts=0`). Changed early return guard from `temporal_correction_attempts <= 0` to `temporal_correction_attempts <= 0 and max_attempts > 0`. Changed comparison from `>` to `>=` for limit check. Added regression test for `(0,0)` edge case.

### PR #6182 — Preview Auth Hardening
Added `PRODUCTION_MODE=true` to preview environment in `deploy.sh`. Fixes bug rev-w1dt where preview had weaker auth enforcement than staging/stable.

### PR #6181 — Dragon Knight Template State Merging
Fixed falsy check on `state_updates` dict. `isinstance(state_updates, dict) and state_updates` is falsy for `{}` — removed truthy guard since `isinstance` already excludes `None` and non-dict types. Fixed both Dragon Knight template path and LLM response path.

### PR #6179 — Living World Backend Bug
`inject_persisted_living_world_fallback` was gated by `debug_mode=True`, preventing non-debug users from seeing living world updates on page reload. Backend bug contradicted frontend comment that living world should always be visible.

### PR #6177 — Cost Cleanup
Pruned preview artifacts and gated Gemini mock mode.

### PR #6156 — Claude Code Repro Workflow
Added repro copy command and workflow for easier bug reproduction.

### PR #6135 — Agent Orchestrator Cursor Hooks
Cursor hooks and tracked AO metadata updater for improved worker visibility.

### PR #6116 — Skeptic Evidence Gate
Fail-closed evidence gate + pagination fix + bugbot check-run integration.

### PR #6034 — Campaign Wizard
Re-enabled LLM-driven Custom Campaign Wizard with bug fixes.

### PR #6145 — Private Repo CI Policy
Requires self-hosted runners for private workflows (private repo Actions policy enforcement).

## Connections

- [[Claude]] — PR descriptions follow structured format mandated by CLAUDE.md
- [[Beads]] — each PR linked to bead IDs (rev-*, bd-*)
- [[AgentOrchestration]] — Cursor hooks in PR #6135 relate to AO worker tracking
- [[EvidenceStandards]] — skeptic evidence gate in PR #6116

## Contradictions

- None identified
