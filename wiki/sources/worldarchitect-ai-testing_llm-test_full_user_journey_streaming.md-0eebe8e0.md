---
title: "WorldArchitect.AI Full User Journey Test Spec"
type: source
tags: [worldarchitect-ai, E2E, testing, streaming, browser-automation, user-journey]
sources: [worldarchitect-ai]
date: 2026-04-07
source_file: raw/full_user_journey_streaming.md
last_updated: 2026-04-07
---

## Summary
End-to-end test specification for validating the complete user workflow from campaign creation through character creation to story continuation with streaming enabled. Uses real browser automation with evidence capture (screenshots, DOM captures, server logs) at each step.

## Key Claims
- Tests campaign creation → character creation → three story actions workflow
- Validates streaming is properly enabled and functional throughout the journey
- Evidence directory structure captures screenshots, page DOM, and server logs per iteration
- Preconditions: local server on port 8005, authenticated browser session, clean campaign state
- Test mode auth bypass via `TESTING_AUTH_BYPASS=true` and `ALLOW_TEST_AUTH_BYPASS=true`
- Fixed action prompts for evidence tracing: tavern approach, ask about quests, accept quest

## Key Quotes
> "BROWSER_JOURNEY_TEST_2026" — campaign title for test tracing
> "JOURNEY_ACTION_1: I look around the tavern and approach the innkeeper" — first story action

## Connections
- [[WorldArchitect.AI]] — the platform being tested
- [[WorldArchitect.AI 20-Turn Test Improvement]] — related E2E testing work

## Contradictions
- None identified