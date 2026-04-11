---
title: "PR #5996: fix(ci): remove Claude settings.json validation from run_tests.sh"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5996.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Removes `validate_claude_settings()` function and its call site from `run_tests.sh`
- `.claude/settings.json` is no longer committed to the repo, so the check was blocking all test runs with a hard `exit 1`

## Metadata
- **PR**: #5996
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +0/-43 in 1 files
- **Labels**: none

## Connections
