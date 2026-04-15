---
title: "PR #6276 rev-v4ci Status 2026-04-15 Night"
type: source
tags: [worldarchitect.ai, level-up, rev-v4ci, design-doc, harness, runners-offline]
date: 2026-04-15
---

## Summary
PR #6276 (feat/world-logic-clean-layer3) OPEN at 7e0a24c8a1. All 5 harness beads COMPLETE. rev-v4ci06/07 done (PR #5 llm-wiki). rev-v4ci01 still BLOCKED. Runners still OFFLINE.

## PR Status

| PR | Branch | Status | Description |
|----|--------|--------|-------------|
| #6276 | feat/world-logic-clean-layer3 | OPEN, MERGEABLE | Layer 3 CLEAN — runners OFFLINE, CI queued |
| #6285 | fix/claude-md-design-doc-gate-rule | OPEN | CLAUDE.md Design Doc Compliance section |
| #6287 | fix/resolve-signal-rename | OPEN, may have conflicts | Rename _resolve_level_up_signal → _is_level_up_ui_active |
| #6289 | fix/br-4bk-design-doc-skill | OPEN | design-doc-as-contract.md skill update (+4 lines) |
| #6292 | fix/br-4bk-green-gate-design-doc | OPEN | design_doc_gate blocking step in green-gate.yml (+112 lines) — replaces #6290 |
| #5 | fix/br-4bk-green-gate-design-doc-v2 | OPEN (llm-wiki) | rev-v4ci06 design doc + rev-v4ci07 loot/gold audit |

## rev-v4ci Chain Status

| Bead | Description | Status |
|------|-------------|--------|
| rev-v4ci01 | Strip world_logic.py 8896→~1500 | 🚨 BLOCKED — needs rev-v4ci05/06/07 outputs |
| rev-v4ci02 | Integration tests | ✅ DONE |
| rev-v4ci03 | agents.py delegate | ✅ DONE |
| rev-v4ci04 | CI line-count gate | ✅ DONE |
| rev-v4ci05 | Behavioral equivalence audit | ✅ DONE — 0/3 pairs equivalent |
| rev-v4ci06 | Design doc update (Two-Path Architecture) | ✅ DONE — PR #5 llm-wiki |
| rev-v4ci07 | loot/gold extraction audit | ✅ DONE — PR #5 llm-wiki |
| rev-v4ci08 | Rename _resolve_level_up_signal → _is_level_up_ui_active | ✅ DONE — PR #6287 OPEN |

## rev-v4ci06 + rev-v4ci07 Summary (from harness-fixes)

**rev-v4ci06 — Two-Path Architecture** (PR #5 llm-wiki):
- rewards_engine = causal XP-threshold computation (polling path)
- world_logic = flag-driven UI state synthesis including STUCK COMPLETION (streaming/agent path)
- Design doc updated: wrong "5 functions map to rewards_engine" claim removed
- **STUCK COMPLETION stays in world_logic** (correct by design)

**rev-v4ci07 — Loot/Gold Audit** (PR #5 llm-wiki):
- 7 loot/gold extraction functions in world_logic.build_level_up_rewards_box
- 0 in rewards_engine
- **Recommendation: keep in world_logic** — LLM output coupling makes moving inappropriate
- No code change

## Harness Fix PRs — ALL COMPLETE

| Bead | PR | Description | Status |
|------|-----|-------------|--------|
| br-4bk | #6289 (worldarchitect.ai) | design-doc-as-contract.md skill +4 lines | ✅ |
| br-dcf | #6292 (worldarchitect.ai) | design_doc_gate blocking step in green-gate.yml | ✅ |
| br-kf7/br-u8l | #6285 (worldarchitect.ai) | CLAUDE.md Design Doc Compliance + skeptic limits | ✅ |
| rev-v4ci05 | /tmp/equiv-audit-2026-04-15.md | 0/3 pairs equivalent audit | ✅ |
| rev-v4ci06 | #5 (llm-wiki) | Two-Path Architecture design doc | ✅ |
| rev-v4ci07 | #5 (llm-wiki) | Loot/gold extraction audit | ✅ |

## CI Status

- **Self-hosted runners**: ALL OFFLINE (wa-oss-runner-4rwP3w53oUewm, wa-oss-runner-7Ail89sxJvib7, wa-oss-runner-PkxaPD4ACDCnS)
- **Design Doc Grep Gates**: PASS (verified locally at 7e0a24c8a1 — 6/6 gates)
- **green-gate CI**: Cannot run — runners offline
- **skeptic-gate**: Cannot run — blocked on green-gate

## Video Evidence

Fresh browser UI video evidence captured at correct commit `7e0a24c8a1`:
- `/tmp/worldarchitect.ai/feat_world-logic-clean-layer3/es_video/latest/`
- `669eda94cf2ce1afb880ae5242147be3.webm` (4.2MB)
- Note: seeded pending-level-up scenario fails to render (campaign past level-up state), but multi-level and god mode scenarios work

## Merge Order (pending runner recovery)

1. #6289 (design-doc-skill) → merge first
2. #6292 (green-gate blocking step) → then
3. #6285 (CLAUDE.md rule) → then (all three harness fix PRs)
4. #6287 (rename) → rebase if conflicts, then merge
5. PR #5 (llm-wiki) → merge design doc updates
6. rev-v4ci01 → unblocks after above complete

## Connections
- [[BehavioralEquivalenceAudit]] — concept: rewards_engine vs world_logic two philosophies
- [[design-doc-as-contract-skill]] — skill for grep gate enforcement
- [[green-gate-workflow]] — CI workflow
- [[rev-v4ci05_equivalence_audit]] — 0/3 pairs equivalent finding
