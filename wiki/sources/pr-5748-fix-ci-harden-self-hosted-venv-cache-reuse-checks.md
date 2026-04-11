---
title: "PR #5748: fix(ci): harden self-hosted venv cache reuse checks"
type: source
tags: []
date: 2026-02-24
source_file: raw/prs-worldarchitect-ai/pr-5748.md
sources: []
last_updated: 2026-02-24
---

## Summary
- hardens cached `venv` reuse checks in `.github/workflows/test.yml`
- only reuses cached `venv` when both `venv/bin/python` and `venv/bin/pip` exist and execute successfully
- recreates `venv` when cached wrapper scripts are stale/corrupt (prevents `exit 127` from missing `pip`)
- includes resolver dedupe so install step uses the same resolved interpreter path

## Metadata
- **PR**: #5748
- **Merged**: 2026-02-24
- **Author**: jleechan2015
- **Stats**: +6/-4 in 1 files
- **Labels**: none

## Connections
