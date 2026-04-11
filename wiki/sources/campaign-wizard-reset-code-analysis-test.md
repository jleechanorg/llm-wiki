---
title: "Campaign Wizard Reset Code Analysis Test"
type: source
tags: [testing, javascript, code-analysis, wizard, campaign, frontend]
source_file: "raw/campaign-wizard-reset-test.js"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript test class that analyzes the campaign wizard reset flow by examining campaign-wizard.js and app.js code. Validates that forceCleanRecreation properly restores wizard state without triggering problematic form reset sequences.

## Key Claims
- **Test Target**: Validates wizard reset flow code correctness
- **Files Analyzed**: campaign-wizard.js and app.js
- **Key Methods Tested**: forceCleanRecreation, replaceOriginalForm
- **State Management**: Wizard visibility, content, spinner handling

## Key Test Cases
- forceCleanRecreation method exists and calls replaceOriginalForm with skipCleanup=true
- replaceOriginalForm accepts skipCleanup parameter
- replaceOriginalForm skips cleanup when parameter is true
- app.js checks wizard state before form reset
- forceCleanRecreation restores wizard content visibility

## Connections
- [[CampaignWizard]] — the wizard component being tested
- [[CampaignWizardReset]] — the reset flow being validated
- [[ForceCleanRecreation]] — method that ensures clean wizard recreation

## Contradictions
- None identified
