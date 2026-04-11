---
title: "Functional Validation Test Runner"
type: source
tags: [testing, functional-validation, ui-testing, automated-testing, bootstrap, campaign-dashboard]
source_file: "raw/test-functional-validation-runner.html"
sources: []
last_updated: 2026-04-08
---

## Summary
HTML-based test runner that validates multiple UI components and user-facing functionality including campaign dashboard, campaign wizard, search/filter capabilities, theme readability, checkbox alignment, and sort functionality.

## Key Claims
- **Test Runner Framework**: Automated test runner using Bootstrap CSS for styling with JavaScript-based test execution
- **UI Component Testing**: Validates campaign dashboard elements (search input, sort select, theme filter, campaign cards)
- **Campaign Wizard Testing**: Tests checkbox inputs for narrative-flair and mechanical-precision options
- **Theme Testing**: Validates readability across light/dark themes via data-theme attribute
- **Functional Validation**: Tests search, filter, sort, and modern mode default behaviors

## Test Categories
1. **Spinner Test**: Validates loading spinner behavior
2. **Search/Filter Test**: Tests campaign search and theme filtering
3. **Modern Mode Default**: Validates default interface mode
4. **Theme Readability**: Tests theme contrast and readability
5. **Checkbox Alignment**: Validates form control alignment
6. **Sort Functionality**: Tests sorting options (last played, date created, title)

## Connections
- [[CampaignDashboard]] — tested UI component for campaign management
- [[CampaignWizard]] — tested UI component for campaign creation
- [[UIAutomationTesting]] — concept for automated UI validation
- [[FunctionalTesting]] — broader testing category this belongs to

## Contradictions
- None identified
