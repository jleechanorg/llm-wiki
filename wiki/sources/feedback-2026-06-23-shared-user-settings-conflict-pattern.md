---
title: "_shared_user_settings conflict pattern in llm_service.py"
type: source
tags: [worldarchitect, latency, conflict-resolution, llm_service]
date: 2026-06-23
source_file: raw/feedback_2026-06-23_shared_user_settings_conflict_pattern.md
last_updated: 2026-06-23
---

## Summary

PRs modifying `_continue_story()` in `mvp_site/llm_service.py` to add per-user settings reads will conflict with main if `_shared_user_settings` (the jleechan-1hy7 latency fix) is present. The shared variable pre-fetches settings once and must be used for all per-user decisions in the function.

## Key Claims

- `_shared_user_settings` is fetched at line ~6362 in `_continue_story()` by PR #7818 (`081bf8aea9`) to eliminate a 20-100ms duplicate Firestore call.
- Any PR that adds a new `get_user_settings(user_id)` call inside `_continue_story()` will conflict with this.
- Resolution: always use `rag_mode.get_rag_mode(_shared_user_settings)` instead of re-fetching.

## Connections

- [[worldarchitect-ai]] — repo where this pattern lives
- [[jleechan-1hy7-latency-fix]] — the fix that introduced `_shared_user_settings`
