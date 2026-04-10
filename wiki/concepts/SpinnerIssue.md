---
title: "Spinner Issue"
type: concept
tags: [bug, ui, loading-state]
sources: []
last_updated: 2026-04-08
---

## Summary
A spinner issue refers to a UI bug where a loading indicator remains visible indefinitely, preventing user interaction with the interface. This occurs when loading state fails to transition to complete state, often due to missing cleanup, race conditions, or improper state management.

## Common Causes
- **Missing State Clear**: Loading flag not reset after async operation completes
- **Race Conditions**: Multiple async operations conflicting
- **Component Unmount**: Cleanup not properly executed on navigation away
- **Error Handling**: Error state not properly handled, keeping spinner visible

## Campaign Wizard Context
The Campaign Wizard experiences a persistent spinner issue where after creating a campaign and navigating away, returning to start a new campaign shows a stuck spinner instead of the clean wizard form.

## Connections
- [[CampaignWizard]] — component affected
- [[CampaignWizardResetIssueReproductionTest]] — test that reproduces this specific issue
- [[BrowserAutomation]] — how the issue is detected and validated
