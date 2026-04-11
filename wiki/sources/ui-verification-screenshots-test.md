---
title: "UI Verification Screenshots Test"
type: source
tags: [testing, ui-verification, playwright, e2e, debug-mode]
source_file: "raw/ui_verification_screenshots_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Playwright test that screenshots all UI elements in debug mode to verify structured response fields display correctly. Tests complete campaign flow from dashboard through story interaction.

## Key Claims
- **Debug Mode Testing**: Enables debug mode checkbox to expose all structured fields
- **Screenshot Verification**: Takes screenshots of each UI element to prove the UI fix works
- **Full Response Capture**: Captures complete AI response with all debug_info fields
- **Element-Level Screenshots**: Tests .session-header, .planning-block, .dice-rolls, .resources individually
- **Campaign Flow**: Tests complete flow from dashboard to campaign creation to story interaction

## Key Quotes
> "test_ui_displays_all_fields" — Main test function validating all structured fields

## Connections
- [[Simple UI Check Test]] — simpler version without API campaign creation
- [[Structured Response Fields Display Frontend Tests]] — validates frontend rendering of these fields
- [[Structured Fields Storage Test]] — validates persistence through Firestore

## Contradictions
- None identified
