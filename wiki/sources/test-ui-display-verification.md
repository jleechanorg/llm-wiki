---
title: "Test UI Display Verification"
type: source
tags: [testing, ui-verification, playwright, e2e, structured-fields]
source_file: "raw/test_ui_display_verification.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Playwright test that verifies structured response fields (session-header, planning-block, dice-rolls, resources) display correctly in the campaign UI. Uses test_mode URL parameter to bypass authentication and tests complete campaign flow from dashboard through story interaction.

## Key Claims
- **Test Mode Authentication Bypass**: Uses ?test_mode=true&test_user_id=ui-test-user URL parameters to bypass authentication for manual testing
- **Structured Fields Verification**: Validates display of session-header, planning-block, dice-rolls, and resources UI elements
- **Full Campaign Flow**: Tests complete journey from dashboard to campaign creation to story interaction to AI response
- **Browser Automation**: Uses Playwright sync_api with Chromium in non-headless mode for visual inspection
- **Screenshot Verification**: Captures screenshots at key points for manual review and debugging

## Key Quotes
> "test_structured_fields_display" — Main test function validating all structured fields

## Connections
- [[Playwright]] — Browser automation framework used for UI testing
- [[StructuredResponseFields]] — UI elements being verified (session-header, planning-block, dice-rolls, resources)
- [[TestMode]] — URL parameter pattern for bypassing authentication in local testing
