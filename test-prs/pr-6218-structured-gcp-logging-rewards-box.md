---
title: "PR #6218: feat(world-logic): add structured GCP logging for rewards_box"
type: test-pr
date: 2026-04-13
pr_number: 6218
files_changed: [world_logic.py, test_world_logic.py, test_rewards_box_normalizer_sentinel.py, pr-6218.md]
---

## Summary
Adds structured GCP logging to `_enforce_primary_rewards_box_postcondition` function in world_logic.py. Logs three distinct events: LLM-provided, LLM-omitted+server-synthesized, and failure cases. Each log includes event_type, mode, and relevant context for debugging in GCP Logs.

## Key Changes
- **world_logic.py**: Added structured logging with `extra` dict containing:
  - `event_type`: rewards_box_llm_provided, rewards_box_synthesized, rewards_box_missing
  - `rewards_required`, `mode`, `failure_reason`

## Motivation
This logging replaces observability that existed when `_process_rewards_followup` made a second LLM call. Now that the followup is removed (PR #6214), server-side logging is needed to track when postcondition triggers synthesis vs when LLM provides rewards_box directly.