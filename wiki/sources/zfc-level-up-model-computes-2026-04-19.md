---
title: "ZFC Level-Up Model Computes Design (Full v2 — 2026-04-19)"
type: source
tags: [worldarchitect, level-up, zfc, backend-architecture]
date: 2026-04-19
source_file: roadmap/zfc-level-up-model-computes-2026-04-19.md
---

## Summary
Full ZFC architecture for level-up: model computes level-up signal, backend is pure formatter. Supersedes backend-centralization-only approach. 5-stage rollout: Stage 0 (delete/cleanup, net ≤ 0 LOC) → Stage 1 (MVP compliance probe) → Stage 2 (formatter narrowing) → Stage 3 (transport parity) → Stage 4 (delete legacy inference) → Stage 5 (enforcement).

**Companion**: [[zfc-level-up-model-computes-north-star-2026-04-19]] — shorter version; this is the fuller 796-line design doc.

## Key Claims

- **Core ZFC principle**: Never implement keyword routing, heuristic scoring, semantic analysis, or classification logic in application code — delegate all judgment to model API calls
- **Forbidden patterns**: `if text.contains("fix")`, regex intent detection, hand-tuned scoring functions, hardcoded routing tables, explicit `if/else` chains guessing user intent
- **Correct pattern**: Pass text/context to model with clear prompt, use model's response as the decision
- **Level-up ownership**: Model computes level_up_signal; backend formats for UI; rewards_engine is pure formatter
- **Normalization atomicity**: rewards_box and planning_block are atomic — if one is None, both must be None
- **Single-entrypoint invariant**: `rewards_engine.canonicalize_rewards()` is the only rewards entrypoint from llm_parser

## Key Quotes

> "Never implement keyword routing, heuristic scoring, semantic analysis, or classification logic in application code. Delegate all such judgment to model API calls." — ZFC Core Rule

> "ONE job: ALL rewards/progression decisions (detect, build, normalize, decide visibility). What it does NOT do: XP math (→ game_state), Firestore I/O (→ llm_parser), modal injection (→ world_logic)." — rewards_engine.py v4 design header

## Core Tenets

1. **ZFC Boundary**: Model decides XP/level-up facts; backend must not decide those semantic facts on the new model-owned path
2. **Centralization Boundary**: One canonical backend formatting path: level_up_signal → format_model_level_up_signal() → canonicalize_rewards() → world_logic modal wrapper → response/persistence → app.js render
3. **Single Responsibility Per File**: Every file gets one job; if a second job appears, move that logic to the file that owns it

## rewards_engine Public API

| Function | Role |
|----------|------|
| `canonicalize_rewards(structured_fields, game_state, original_state)` | streaming/non-streaming entry point |
| `project_level_up_ui(game_state_dict)` | polling path entry point (no LLM output) |
| `is_level_up_active(game_state_dict)` | detector (replaces 3 parallel checks) |
| `resolve_level_up_signal(...)` → (detected, target, max_level) | signal resolver — legacy, to be quarantined |
| `ensure_rewards_box()` / `ensure_planning_block()` | canonical builders |
| `normalize_rewards_box()` | guarantees clean booleans/coerced ints |
| `should_show_rewards_box()` | visibility decision |

## _canonicalize_core() Paths

- **Path A**: Level-up detected → atomic (rewards_box, planning_block) pair
- **Path B**: XP-progress without level-up → non-atomic rewards_box only
- **STUCK COMPLETION FALLBACK**: level_up_complete=True triggers special stuck-state recovery (live code, not legacy)

## 5-Stage Rollout

| Stage | Focus | Status |
|-------|-------|--------|
| 0 | Delete/cleanup first, net ≤ 0 LOC | Partial: #6431 (duplicate removal), #6434 (gemini_request rename) |
| 1 | MVP real-model compliance probe | Pending |
| 2 | Formatter narrowing | Pending |
| 3 | Transport parity (streaming/non-streaming) | Pending |
| 4 | Delete legacy backend inference | Pending |
| 5 | Enforcement grep gates + architecture tests | Pending |

## Stage 0 Acceptance Criteria

- `rg -n "trigger coderabbit|TODO delete|temporary review" testing_mcp mvp_site roadmap` → no transient scaffolding ✅ (verified)
- Net ≤ 0 production LOC ✅ (net -20 LOC for duplicate removal)
- No production behavior changes unless deletion is evidence-backed
- Skipped assertion at test_rewards_engine_wiring.py:116 tracked as named temporary exception

## Known Hazards (from design doc)

- **Silent CI success**: Green Gate exits 0 at job level even when VERDICT step fails — must use REST API for VERDICT existence
- **Commitment substitution**: PR lifecycle consuming deletion work bandwidth (3rd recurrence 2026-04-21)
- **Git worktree identity**: worktree-local git config silently overrides global
- **Schema-first vs deletion-first**: Net LOC gate exists in CLAUDE.md but has zero CI enforcement

## Connections

- [[RewardsEngineArchitecture]] — Single-responsibility successor to scattered level-up logic
- [[NormalizationAtomicity]] — rewards_box/planning_block atomicity invariant
- [[Level-Up ZFC Loop]] — Launchd-based autonomous loop
- [[ZeroFrameworkCognition]] — Core principle: model owns judgment, app code is pure formatter
- [[SkepticGate]] — skeptic-gate.yml — Gate 7 evaluation workflow
- [[Level-Up Bug Chain]] — Historical bug chain traced through PRs #6273/#6275/#6276
- [[RewardsEngineWiringTests]] — test_rewards_engine_wiring.py — Layer 2 integration tests
