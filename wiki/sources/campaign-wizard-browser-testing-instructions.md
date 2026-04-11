---
title: "Campaign Wizard Browser Testing Instructions"
type: source
tags: [puppeteer, testing, campaign-wizard, browser-testing, manual-testing]
source_file: "raw/campaign-wizard-testing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Manual testing guide for campaign wizard functionality using Puppeteer MCP. Covers wizard initialization, input field testing (particularly `wizard-setting-input`), form validation, and preview system testing with step-by-step procedures.

## Key Claims
- **Wizard Initialization**: Validates wizard loads and replaces original form in modern mode with 4-step progress bar
- **wizard-setting-input Testing**: Primary focus on textarea field with auto-generation placeholders that change based on campaign type
- **Campaign Type Switching**: Dragon Knight shows pre-filled World of Assiah description; Custom shows "Random fantasy D&D world (auto-generate)" placeholder
- **Preview System**: Real-time preview updates reflecting current selections across all steps
- **Puppeteer MCP Integration**: Code examples for automated browser testing via Claude Code CLI

## Key Quotes
> "This test focuses on the `wizard-setting-input` field as the primary validation target" — core testing objective

## Connections
- [[CampaignWizardResetRedGreenTest]] — related wizard testing
- [[CampaignWizardResetCodeAnalysisTest]] — code-level wizard validation
- [[CampaignWizardTimingTests]] — performance testing for wizard

## Contradictions
- []
