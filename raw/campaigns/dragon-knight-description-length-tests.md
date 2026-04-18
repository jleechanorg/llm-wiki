---
title: "Dragon Knight Description Length Tests"
type: source
tags: [javascript, testing, campaign-wizard, dragon-knight]
source_file: "raw/test_dragon_knight_description_length.js"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit test suite validating the Dragon Knight campaign description handling in CampaignWizard. Tests verify that the longer campaign description is properly defined, displayed in preview with truncation, and collected through form data without errors.

## Key Claims
- **DEFAULT_DRAGON_KNIGHT_DESCRIPTION**: Must be defined, contain specific narrative content, and exceed 1000 characters
- **Character Content**: Description must include 'Ser Arion', 'Celestial Imperium', 'Empress Sariel', and 'Campaign summary'
- **Truncation Behavior**: `_formatDescription()` helper truncates long descriptions to 50 characters + "..."
- **Form Data Collection**: `collectFormData()` and `populateOriginalForm()` properly handle descriptions over 1000 characters

## Test Framework
- **SimpleTestRunner**: Custom test runner class with `expect(actual)` method supporting:
  - `toBeDefined()` - validates defined values
  - `toContain(expected)` - substring validation
  - `toBe(expected)` - exact equality
  - `toBeGreaterThan(expected)` - numeric comparison
  - `toBeLessThanOrEqual(expected)` - numeric comparison
  - `not.toContain(expected)` - negative substring check

## Connections
- [[CampaignWizard]] - the JavaScript class being tested
- [[DragonKnight]] - the campaign type being validated
- [[SerArion]] - character referenced in description
- [[EmpressSariel]] - ruler referenced in description
- [[CelestialImperium]] - faction referenced in description
