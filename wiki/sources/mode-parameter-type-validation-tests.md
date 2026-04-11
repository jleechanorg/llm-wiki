---
title: "Test Mode Parameter Type Validation"
type: source
tags: [python, testing, regression, bug-fix, type-validation]
source_file: "raw/test_mode_parameter_type_validation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Regression test suite for a bug where the mode parameter was sent as dict/list/int instead of string, causing AttributeError: 'dict' object has no attribute 'lower'. Tests validate that invalid mode types default to MODE_CHARACTER instead of crashing.

## Key Claims
- **Dict mode defaults to CHARACTER**: Mode sent as dict should be rejected and default to MODE_CHARACTER
- **Int mode defaults to CHARACTER**: Mode sent as int should be rejected and default to MODE_CHARACTER
- **List mode defaults to CHARACTER**: Mode sent as list should be rejected and default to MODE_CHARACTER
- **None mode defaults to CHARACTER**: Mode sent as None should default to MODE_CHARACTER
- **Missing mode uses default**: Mode omitted from request should default to MODE_CHARACTER
- **Valid string modes work**: Valid string mode values ("character", "god", "narrator") should work correctly

## Key Connections
- Related to [[LLMRequest validation tests]] — validates type checks for request parameters
- Related to [[Provider settings selection tests]] — validates mode parameter handling in settings

## Bug Details
- Bug file: .beads/mode-parameter-type-validation-bug.md
- Occurred: 2026-01-23 04:43:11 UTC
- Campaign: JXXNfJpdqNtH60HN942q
- Error: AttributeError: 'dict' object has no attribute 'lower'
