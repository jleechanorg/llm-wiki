---
title: "Test Mode"
type: concept
tags: [testing, development-pattern, authentication-bypass]
sources: ["campaign-wizard-browser-testing-instructions"]
last_updated: 2026-04-08
---

## Summary
Development testing pattern that enables bypassing normal authentication for automated testing. Activated via URL parameters (`test_mode=true`, `test_user_id`) to enable controlled testing environments without full authentication flow.

## Key Attributes
- **Activation**: URL parameters `test_mode=true&test_user_id=<user_id>`
- **Purpose**: Enable automated testing of authenticated features
- **Initialization**: `window.testAuthBypass !== undefined` verifies test mode is active

## Connections
- [[CampaignWizardBrowserTestingInstructions]] — uses test mode for wizard testing
- [[TestUIDisplayVerification]] — uses test_mode bypass for UI verification
- [[SimpleUICheckTest]] — uses test_mode for campaign UI testing
