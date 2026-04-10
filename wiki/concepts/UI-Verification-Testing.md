---
title: "UI Verification Testing"
type: concept
tags: [testing, e2e, visual-testing, ui-validation]
sources: [ui-verification-screenshots-test, simple-ui-check-test, structured-response-fields-display-frontend-tests]
last_updated: 2026-04-08
---

## Summary
UI verification testing is an E2E testing approach that validates web application UI elements render correctly. In OpenClaw, this involves using Playwright to navigate to campaigns and verify structured response fields (session_header, planning_block, dice_rolls, resources) display in the story content.

## Testing Approach
1. **API-first campaign creation**: Bypass UI form issues by creating campaigns via API
2. **Browser automation**: Use Playwright sync_api to drive Chromium
3. **Element verification**: Check for specific CSS selectors (.session-header, .planning-block, etc.)
4. **Screenshot capture**: Take screenshots at key steps for visual verification
5. **Debug mode**: Enable debug mode to expose all structured fields

## Key Test Elements
- .session-header — Session metadata display
- .planning-block — AI planning/thinking display
- .dice-rolls — Dice roll results display
- .resources — Resource/inventory display

## Connections
- [[Playwright]] — browser automation tool used
- [[Structured Response Fields]] — fields being verified
- [[E2E Testing]] — broader testing concept
