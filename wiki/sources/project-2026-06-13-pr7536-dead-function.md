---
title: "PR #7536 unmergeable: tested function removed by PR #7480"
type: source
tags: ["project", "worldarchitect"]
date: 2026-06-13
source_file: raw/project_2026-06-13_pr7536_dead_function.md
---

## Summary
PR #7536 (`test(bq): cover Gemini usage_metadata path in _bq_log_spell_repair_interaction`) is **unmergeable as-is**.

## Key Claims
- PR #7536 (`test(bq): cover Gemini usage_metadata path in _bq_log_spell_repair_interaction`) is **unmergeable as-is**.
- The test it adds calls `world_logic._bq_log_spell_repair_interaction(...)` directly. That function:
- - Existed in `b26a5eb1e9` (PR #7536's actual base) — 2 refs
- - Was **removed** by `ed5a97b2c7` (PR #7480 "Remove deliberate second LLM calls") — landed on main
- - Is **NOT present** on `origin/main` — 0 refs
- - Is **NOT present** on any levelup v2 train branch:

## Connections
- [[WorldarchitectAI]] — worldarchitect.ai project memory
- Source: `raw/project_2026-06-13_pr7536_dead_function.md`
