---
title: "Campaign Wizard Reset Red/Green Test"
type: source
tags: [testing, red-green, tdd, wizard, campaign, frontend, javascript]
source_file: "raw/campaign-wizard-reset-test.js"
sources: []
last_updated: 2026-04-08
---

## Summary
Red/Green test class validating the campaign wizard reset workflow. Tests the exact user journey: create campaign → complete → navigate back → click "Start Campaign". Simulates DOM state and validates wizard container creation, content rendering, step navigation, and form visibility toggling.

## Key Claims
- **Test Target**: Wizard reset functionality after campaign completion
- **Test Type**: Red/Green TDD approach validating state transitions
- **Files Tested**: campaign-wizard.js and app.js
- **DOM Elements Validated**: Wizard container, form reset, spinner removal, step navigation

## Key Test Cases
- Wizard container exists after enable() is called
- Wizard has content (not empty after reset)
- No spinner present in reset state
- Wizard has step navigation (.wizard-step elements)
- Original form is hidden (display: none) after wizard activation

## Connections
- [[CampaignWizard]] — the component being tested
- [[AppJs]] — contains form reset logic at line 56
- [[RedGreenTesting]] — TDD methodology used

## Contradictions
- None identified
