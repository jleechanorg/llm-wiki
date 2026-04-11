---
title: "CampaignCreationV2 Memory Leak Tests"
type: source
tags: [python, testing, playwright, memory-leaks, component-lifecycle, timer-cleanup]
source_file: "raw/campaign-creation-v2-memory-leak-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite with Playwright integration testing memory leak fixes in CampaignCreationV2 component. Tests verify that all JavaScript timers (setTimeout, setInterval) are properly cleaned up on component unmount using monkey patching to track active timer IDs.

## Key Claims
- **Timer Cleanup on Unmount**: CampaignCreationV2 must clear all active setTimeout and setInterval timers when component unmounts
- **Monkey Patch Tracking**: JavaScript test uses monkey patching of window.setTimeout/setInterval to count active timers
- **CI Environment Handling**: Tests detect CI environment and skip server-dependent tests
- **Playwright Integration**: Uses Playwright for browser automation to navigate campaign creation flow

## Key Quotes
> "const originalSetTimeout = window.setTimeout;" — Monkey patching approach to track active timers

## Connections
- [[Playwright]] — Browser automation framework used for E2E testing
- [[CampaignCreationV2]] — React component being tested for memory leaks

## Contradictions
- None identified
