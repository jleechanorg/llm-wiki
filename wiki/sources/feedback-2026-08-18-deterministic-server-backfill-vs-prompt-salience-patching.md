---
title: "Deterministic Server Backfill vs Prompt Salience Patching"
type: source
tags: [llm, prompt-engineering, backend-architecture, bigquery, forensics]
date: 2026-08-18
source_file: raw/feedback_2026-08-18_deterministic_server_backfill_vs_prompt_salience_patching.md
---

## Summary
When BigQuery forensic data shows models drop structured JSON fields during long outputs despite 100% prompt reminder presence, prefer deterministic server-side extraction and backfill from verified execution stdout over prompt-level salience stacking.

## Key Claims
- Prompt-level reminders for JSON field copying often fail on models like Gemini 3.7 Flash due to context/attention drop during long structured generation.
- Production BigQuery data proved FactionManagementAgent had a ~90% loss rate despite 100% prompt presence on the wire.
- Deterministic backend recovery with RNG/authenticity validation in `mvp_site/dice_integrity.py` provides a 100% mathematical guarantee while keeping prompts lean.

## Connections
- [[worldarchitect-ai]] — Primary repository implementing deterministic dice backfill
- [[gemini-3.7-flash]] — Model exhibiting attention drop on JSON stdout copying
- [[root-cause-first]] — Engineering principle guiding deterministic fixes over prompt bloat
