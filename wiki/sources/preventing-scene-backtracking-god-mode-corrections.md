---
title: "Preventing Scene Backtracking and Missed God-Mode Corrections"
type: source
tags: [game-state, validation, god-mode, auto-reshot, continuity, narrative-sync]
source_file: "raw/preventing-scene-backtracking-god-mode-corrections.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Operational plan for reorienting game safeguards from blocking errors toward proactive prevention, automatic state repair, and low-friction guidance. Covers automatic god-mode directive application, auto-filled time/resource updates, and continuity locks that guide the model forward.

## Key Claims
- **Auto god-mode application**: Detect directives in `llm_service.continue_story` prompt, set `pending_god_mode` flag, pre-apply state deltas before narrative generation
- **Auto-fill resource updates**: Infer high-impact events (loot, combat, travel) and auto-fill default deltas in structured response before validation
- **Continuity locks**: Track `last_scene_id`, `last_location`, active entities to prevent scene rewinds; `NarrativeSyncValidator` auto-adjusts minor regressions

## Key Technical Components
- `mvp_site/preventive_guards.py` — preventive guards implementation
- `mvp_site/world_logic.py` — wired via this module
- `mvp_site/tests/test_preventive_guards.py` — guard tests
- `structured_fields_utils.extract_structured_fields` — infers events and auto-fills deltas
- `world_logic.process_action_unified` — patches missing state_updates with defaults
- `NarrativeSyncValidator` — auto-adjusts minor regressions, triggers reshot for severe conflicts
- `GameState.custom_campaign_state` — stores pending_god_mode flag and continuity fingerprints

## Connections
- [[GameState]] — stores custom_campaign_state with god-mode and continuity tracking
- [[NarrativeSyncValidator]] — validates and auto-adjusts narrative consistency
- [[PreventiveGuards]] — current implementation for preventive guards
