---
title: "Campaign Wizard Editable Preview Tests"
type: source
tags: [javascript, testing, campaign-wizard, ui-interaction]
source_file: "raw/test_campaign_wizard_editable_preview.html"
sources: []
last_updated: 2026-04-08
---

## Summary
Browser-based test suite validating the Campaign Wizard's editable preview functionality. Tests verify click-to-edit field activation, click-outside-to-save persistence, and Escape-to-cancel rollback behaviors for form inputs.

## Key Claims
- **Click-to-Edit**: Form fields (campaign-title, campaign-prompt, generate-companions) become editable on click
- **Click-Outside-to-Save**: Clicking outside the form saves changes automatically
- **Escape-to-Cancel**: Pressing Escape reverts changes to original values
- **Form Integration**: Tests validate the full form element integration including inputs and textareas

## Key Test Functions
- `testClickToEditFieldActivation`: Verifies fields become editable after click
- `testClickOutsideSavesChanges`: Confirms changes persist when clicking outside
- `testEscapeCancelsEditing`: Validates Escape key reverts to original values
- `testFormDataCollection`: Ensures form data is properly collected after edits

## Connections
- [[CampaignWizard]] — the component being tested
- [[EditablePreview]] — the UI pattern being validated

## Contradictions
- None identified
