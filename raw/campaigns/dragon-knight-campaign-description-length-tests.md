---
title: "Dragon Knight Campaign Description Length Tests"
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

## Key Test Functions
- `should handle long Dragon Knight description without errors`: Validates description content and length
- `should properly format long descriptions in preview`: Tests truncation logic
- `should handle Dragon Knight description in form data collection`: Tests `collectFormData()`
- `should populate original form with long description`: Tests `populateOriginalForm()`
- `should handle campaign type change to Dragon Knight`: Tests campaign type switching

## Connections
- [[CampaignWizard]] — main class under test
- [[Ser Arion]] — protagonist in Dragon Knight campaign
- [[Empress Sariel]] — ruler of Celestial Imperium
- [[Celestial Imperium]] — campaign setting
