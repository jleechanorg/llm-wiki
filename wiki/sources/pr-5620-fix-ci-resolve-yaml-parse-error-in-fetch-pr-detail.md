---
title: "PR #5620: fix(ci): resolve YAML parse error in fetch-pr-details action"
type: source
tags: []
date: 2026-02-18
source_file: raw/prs-worldarchitect-ai/pr-5620.md
sources: []
last_updated: 2026-02-18
---

## Summary
- **Fixed YAML parse error** in `.github/actions/fetch-pr-details/action.yml` that caused Deploy to Production workflow #33 to fail
- **Root cause**: Multi-line Python heredoc inside `run: |` block had lines starting at column 1, which terminates YAML block scalars
- **Fix**: Replaced 7-line Python script with single-line one-liner that stays properly indented within the YAML block

## Metadata
- **PR**: #5620
- **Merged**: 2026-02-18
- **Author**: jleechan2015
- **Stats**: +1/-8 in 1 files
- **Labels**: none

## Connections
