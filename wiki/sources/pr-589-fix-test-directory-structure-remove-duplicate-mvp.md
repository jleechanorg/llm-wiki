---
title: "PR #589: Fix test directory structure: Remove duplicate mvp_site nesting"
type: source
tags: []
date: 2025-07-14
source_file: raw/prs-worldarchitect-ai/pr-589.md
sources: []
last_updated: 2025-07-14
---

## Summary
- Fixed incorrect test directory structure with duplicate `mvp_site/mvp_site/tests/test_end2end/`
- Moved all end-to-end test files to correct location: `mvp_site/tests/test_end2end/`
- Updated `run_e2e_tests.sh` script to reference correct path

## Metadata
- **PR**: #589
- **Merged**: 2025-07-14
- **Author**: jleechan2015
- **Stats**: +5/-5 in 6 files
- **Labels**: none

## Connections
