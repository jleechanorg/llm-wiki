---
title: "ENTITY_TRACKING_TOKEN_RESERVE"
type: concept
tags: [token-budgeting, context-management, bug-fix]
sources: [entity-tracking-budget-fix-end2end-test]
last_updated: 2026-04-08
---

Fix for context overflow when entity tracking is added after truncation. The scaffold calculation now reserves ~3,500 tokens for entity tracking, preventing errors like qwen-3-235b receiving 97,923 tokens when max allowed was 94,372.