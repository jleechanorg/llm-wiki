---
title: "Playwright UI Display Test"
type: source
tags: [playwright, testing, ui, display, integration]
source_file: "raw/test_ui_display.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Integration test using Playwright to validate structured field display in the campaign UI. Navigates directly to a campaign URL and verifies presence of session-header, planning-block, dice-rolls, and resources blocks.

## Key Claims
- **UI Navigation**: Test navigates to localhost:8081 and detects campaign view
- **Structured Field Detection**: Validates display of session-header, planning-block, dice-rolls, and resources in story entries
- **Screenshot Validation**: Captures before/after screenshots for visual verification
- **Story Entry Parsing**: Locates and inspects .story-entry elements to verify field rendering

## Test Flow
1. Launch Chromium browser in non-headless mode
2. Navigate to http://localhost:8081
3. Detect dashboard vs campaign view
4. Click first campaign if available
5. Submit test message and wait for AI response
6. Verify structured field presence in last story entry

## Technical Details
- Uses playwright.sync_api with sync_playwright
- Waits for #user-input disabled state to detect response completion
- Validates DOM structure within .story-entry elements

## Connections
- [[Playwright]] — browser automation framework used
- [[StructuredFieldDisplay]] — UI pattern being tested

## Contradictions
- None identified
