---
title: "Simple UI Check Test"
type: source
tags: [testing, ui-verification, playwright, browser-automation]
source_file: "raw/simple_ui_check_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Playwright-based test that navigates to a campaign at localhost:8081 and verifies structured response fields display correctly in the UI. Takes screenshots at each step and checks for .session-header, .planning-block, .dice-rolls, and .resources elements.

## Key Claims
- **UI Element Verification**: Checks that session-header, planning-block, dice-rolls, and resources elements render in the story content
- **Browser Automation**: Uses Playwright sync_api to drive a Chromium browser in non-headless mode for visual inspection
- **Complete Flow Testing**: Tests the full campaign journey from dashboard through user input to AI response
- **Screenshot Verification**: Captures screenshots at key points (initial load, before send, after response) for manual review

## Key Quotes
> "test_simple_ui_check" — Main test function that validates UI display

## Connections
- [[Playwright]] — Browser automation library used for the test
- [[Structured Fields]] — UI elements being verified (.session-header, .planning-block, .dice-rolls, .resources)
- [[UI Verification Testing]] — Testing methodology employed

## Contradictions
- None identified
