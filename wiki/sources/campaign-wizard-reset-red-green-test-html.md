---
title: "Campaign Wizard Reset Red/Green Test"
type: source
tags: [testing, red-green, tdd, wizard, campaign, frontend, javascript, dom]
source_file: "raw/campaign-wizard-reset-test.html"
sources: []
last_updated: 2026-04-08
---

## Summary
HTML test interface for Red/Green TDD testing of campaign wizard reset functionality. Provides browser-based testing UI to validate the wizard state transitions after campaign completion — specifically the user journey of create campaign → complete → navigate back → click "Start Campaign".

## Key Claims
- **Test Target**: Wizard reset workflow after campaign completion
- **Test Type**: Red/Green TDD (should fail initially in Red state)
- **Files Tested**: campaign-wizard.js and app.js
- **DOM Elements Validated**: Wizard container, form reset, spinner removal, step navigation

## Key Test Cases
- Wizard container exists after enable() is called
- Wizard has content (not empty after reset)
- No spinner present in reset state
- Wizard has step navigation functionality
- Form properly resets between campaign completions

## Technical Details
- Testing framework: Custom JavaScript test class
- DOM simulation: Creates mock form elements (campaign-title, campaign-prompt)
- UI styling: Bootstrap-inspired with red/green color coding for pass/fail states
- Run mechanism: Browser-based onclick handler invoking test instance

## Connections
- [[CampaignWizard]] — the JavaScript class being tested
- [[RedGreenTesting]] — the TDD methodology used
- [[CampaignWizardResetCodeAnalysisTest]] — companion code analysis test

## Contradictions
- None identified
