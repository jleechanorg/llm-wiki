---
title: "Root Cause: Navigation Handler Missing wizard.enable()"
type: source
tags: [javascript, testing, red-green, navigation, wizard, root-cause, bug-fix]
source_file: "raw/test_root_cause_navigation_handler_missing_wizard_enable.js"
sources: []
last_updated: 2026-04-08
---

## Summary
Red/Green test reproducing the actual root cause of a UI bug: the "go-to-new-campaign" button performs navigation but never calls `wizard.enable()`, leaving the wizard in a disabled state after navigating to the new campaign page.

## Key Claims
- **Missing enable call**: Original navigation handler performs route change but never calls `wizard.enable()`
- **Root cause identified**: The navigation handler is the actual source of the bug, not the wizard itself
- **Fix validation**: Tests verify that the fixed handler properly calls `wizard.enable()` during navigation
- **State preservation**: Enables the wizard after route change completes, ensuring UI is interactive

## Test Structure
- **RED test**: Reproduces the problematic sequence where `wizard.enable()` is NOT called
- **GREEN test**: Validates the fixed navigation handler calls `wizard.enable()` correctly
- **Mock objects**: `mockCampaignWizard`, `mockOriginalNavigationHandler`, `mockFixedNavigationHandler`

## Connections
- [[CampaignWizard]] — the UI component that needs enabling after navigation
- [[NavigationHandler]] — the handler that must call wizard.enable()
- [[RedGreenTesting]] — the test methodology used

## Contradictions
- None identified
