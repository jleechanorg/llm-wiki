---
title: "PR #4968: fix(ci): eliminate duplicate test execution + integrate PR coverage (~14min savings)"
type: source
tags: []
date: 2026-02-08
source_file: raw/prs-worldarchitect-ai/pr-4968.md
sources: []
last_updated: 2026-02-08
---

## Summary
- Integrate coverage collection into `test.yml` core group so PRs get coverage reports WITHOUT a separate workflow re-running all ~276 tests
- Remove `pull_request` trigger from `coverage.yml` (now main-only for baseline updates)
- Delete misplaced duplicate `mvp_site/test_documentation_performance.py`
- Update all doc-size-check references to use the correct `tests/` location

**Key themes:**
- CI deduplication: coverage.yml was re-running all ~276 tests already executed by test.yml (~14 min wa

## Metadata
- **PR**: #4968
- **Merged**: 2026-02-08
- **Author**: jleechan2015
- **Stats**: +182/-242 in 5 files
- **Labels**: none

## Connections
