---
title: "PR #5741: fix(ci): fix venv and setup-python failures on self-hosted runners"
type: source
tags: []
date: 2026-02-23
source_file: raw/prs-worldarchitect-ai/pr-5741.md
sources: []
last_updated: 2026-02-23
---

## Summary
- Jeff-Ubuntu: python -m venv creates broken venv/bin/python symlink — fixed by using python3
- claude-drift-runner (Mac): actions/setup-python fails with mkdir /Users/runner Permission denied — fixed by removing the step (Python 3.11 already installed)

## Metadata
- **PR**: #5741
- **Merged**: 2026-02-23
- **Author**: jleechan2015
- **Stats**: +428/-208 in 7 files
- **Labels**: none

## Connections
