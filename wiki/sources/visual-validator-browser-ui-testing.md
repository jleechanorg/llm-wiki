---
title: "Visual Validator - Browser-based UI Testing"
type: source
tags: [javascript, ui-testing, browser, validation, accessibility]
source_file: "raw/visual-validator.md"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript module providing browser-based visual validation for UI testing. Runs in the browser console to check for overlapping elements, text readability issues, and checkbox alignment problems.

## Key Claims
- **Overlapping Elements Detection**: Iterates through .btn, .dropdown-menu, .modal elements and checks for geometric overlap, excluding parent-child relationships
- **Text Readability Checks**: Validates opacity, transparent text, and contrast ratio (requires 4.5:1 for WCAG compliance)
- **Checkbox Alignment Validation**: Validates checkbox-label alignment for form accessibility
- **Configurable Highlighting**: Red/orange borders highlight problematic elements for easy identification

## Key Quotes
> "Check for overlapping elements" — core validation function

## Connections
- [[Playwright]] — similar automated testing approach
- [[UIVerificationScreenshotsTest]] — screenshot-based UI verification

## Contradictions
- None
