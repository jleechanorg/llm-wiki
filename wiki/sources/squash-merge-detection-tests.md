---
title: "Squash-Merge Detection Tests"
type: source
tags: [tdd, unit-testing, bash, integration, regex, git]
source_file: "raw/squash-merge-detection-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for squash-merge detection functionality in integrate.sh. Tests critical bug fixes for false positive detection when parsing Git commit messages for PR references.

## Key Claims
- **Regex Requires Digits**: The sed regex pattern must require at least one digit (`[0-9][0-9]*`) to prevent matching empty parentheses like `(#)`
- **Empty String Guard**: Must check for empty base_subject to prevent false positives when stripping produces empty results
- **Fixed-Strings Flag**: git log --grep must use --fixed-strings to prevent regex interpretation of the search pattern
- **Sed Behavior Verified**: Multiple test cases validate the sed regex strips valid PR numbers but preserves edge cases like `(#)`, `(#abc)`, and commits with spaces

## Test Functions
- `test_integrate_script_syntax` — validates bash syntax is valid
- `test_detect_function_exists` — verifies detect_squash_merged_commits function exists
- `test_regex_bug_fix` — ensures regex requires at least one digit
- `test_empty_string_check` — validates empty string guard with continue
- `test_fixed_strings_flag` — verifies --fixed-strings flag usage
- `test_sed_regex_behavior` — tests sed regex with various inputs

## Connections
- [[integrate-sh]] — the script being tested for squash-merge detection
