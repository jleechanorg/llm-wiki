---
title: "Project 2026-05-31 Gemini Cost Decision Revert 7074"
type: source
tags: [project, memory-file]
date: 2026-05-31
source_file: raw/memory_backfill_2026_06_13/project_2026-05-31_gemini_cost_decision_revert_7074.md
---

## Summary

Decision answering "revert [#7074](https://github.com/jleechanorg/worldarchitect.ai/pull/7074) OR no cache for testing_mcp/?": If one action: revert #7074 (highest $). Clean fix: env-drive TTL, not the environment-blind constant. (Cloud Logging , 7d): 574 creates total (~82/day) — dev 181, previews s1–s10 386, stable .

## Key Claims

- 1h TTL: storage ~$14/day; +input/reads/output ~$9 → **~$23/day total**
- 4h TTL (#7074): storage ~$56/day → **~$65/day total** (storage ≈ 86% of bill, linear in TTL)
- **#7074 = +$42/day (~$1,270/mo)** to help prod that creates ~1 cache/day (saves one ~$0.09 rebuild). Net-negative on real traffic mix. Companion live sample ~$86/day ($603/7d) cross-checks the order.
- TTL env-blind: `mvp_site/gemini_cache_manager.py:46-47` (`CACHE_TTL = "14400s"`, `CACHE_TTL_SECONDS = 14400`). → rev-pu4wb
- Master switch (exists): `mvp_site/constants.py:139` `EXPLICIT_CACHE_ENABLED = _env_bool("WORLDARCH_EXPLICIT_CACHE_ENABLED", True)`. Set `false` off-prod.
- Mock-mode asymmetry BUG: streaming `mvp_site/llm_service.py:7787` gates `not is_mock_mode`; **non-streaming `:2523` does NOT** → billed remote cache in mock mode. → rev-368tq
- Two caches independent: local `WORLDAI_TEST_CACHE` (`:7484`, /tmp replay, free) has zero effect on the billed remote cache. Never conflate. See [[feedback_2026-05-31_two_cache_confusion_test_orphan_leak]].

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
