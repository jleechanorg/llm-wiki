---
title: "Project 2026-06-03 Pr7215 Cacheoff Merged Verified"
type: source
tags: [project, worldarchitect-ai, memory-file]
date: 2026-06-03
source_file: raw/memory_backfill_2026_06_13/project_2026-06-03_pr7215_cacheoff_merged_verified.md
---

## Summary

PR #7215 (rev-vm10b, the largest single Gemini cost lever, ~$1,690/mo cache-storage ceiling) was merged by jleechan2015 as commit ("[antig] fix(cache): keep explicit cache off by default for test contexts"). Tested the MERGED behavior via testing_mcp real services on 2026-06-03. where default = .

## Key Claims

- `constants.EXPLICIT_CACHE_ENABLED = _env_bool("WORLDARCH_EXPLICIT_CACHE_ENABLED", _is_explicit_cache_enabled_by_default())` where default = `ENVIRONMENT==stable AND not _is_non_production_request()`.
- `llm_service._should_use_explicit_cache(uid) = EXPLICIT_CACHE_ENABLED and not _is_test_cache_disabled_context() and not _is_test_user(uid)`.
- `gemini_cache_manager.CampaignCacheManager.CACHE_TTL_SECONDS = 14_400 if _is_real_user_cache_context() else 3_600` (bound at import).
- ZFC: removed `WORLDARCH_EXPLICIT_CACHE_TTL_SECONDS` and `_env_int`; no new env knobs.
- test/CI (TESTING_AUTH_BYPASS=true) → ENABLED=False, _should_use=False, TTL=3600 ✓
- real gameplay (ENVIRONMENT=stable, no test flags) → ENABLED=True, _should_use=True, TTL=14400 ✓
- override (TESTING_AUTH_BYPASS + WORLDARCH_EXPLICIT_CACHE_ENABLED=true) → flag True but _should_use=False (test-ctx guard = defense-in-depth) ✓

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
