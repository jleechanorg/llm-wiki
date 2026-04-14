---
title: "test_campaign_creation_v2_memory_leaks.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Playwright-based tests for CampaignCreationV2 memory leak fixes. Tests that all timeouts and intervals are properly cleaned up on component unmount.

## Key Claims
- Component unmount clears all active timers
- Error handling properly clears timers on failure
- Completion flow shows "Campaign ready!" message
- Skips server-dependent tests in CI environment
- Uses JavaScript monkey-patching to track active timeouts/intervals

## Connections
- [[frontend_v1]] — frontend component being tested
- [[BaseTestUI]] — base test class