---
title: "Root Cause Red/Green Test for Navigation Handler Missing wizard.enable()"
type: source
tags: [javascript, testing, red-green, tdd, navigation, wizard, root-cause, bug-fix]
source_file: "raw/test_root_cause_navigation_handler_missing_wizard_enable.html"
sources: []
last_updated: 2026-04-08
---

## Summary
Red/Green test demonstrating the actual root cause of a UI bug where the navigation handler performs route changes but never calls `wizard.enable()`, leaving the wizard in a disabled state after navigating to a new campaign page.

## Key Claims
- **Missing enable call**: Original navigation handler performs route change via `history.pushState()` but never calls `wizard.enable()`
- **Root cause identified**: The navigation handler itself is the bug source, not the wizard component
- **Fix validation**: Tests verify the fixed handler properly calls `wizard.enable()` during navigation
- **State preservation**: Enables the wizard after route change completes, ensuring UI remains interactive

## Test Structure
- **RED phase**: Test fails with broken handler (no `wizard.enable()` call)
- **GREEN phase**: Test passes with fixed handler (includes `wizard.enable()` call)
- **Root cause explanation**: Shows original vs fixed navigation handler code

## Connections
- [[RedGreenRefactoring]] — testing methodology used
- [[NavigationHandler]] — the component with the bug
- [[WizardComponent]] — UI component that stays disabled without proper enable call

## Contradictions
- None identified
