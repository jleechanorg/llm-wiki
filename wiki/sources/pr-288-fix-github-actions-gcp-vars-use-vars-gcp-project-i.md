---
title: "PR #288: fix: GitHub Actions GCP vars use ${{ vars.GCP_PROJECT_ID }} syntax"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-/pr-288.md
sources: []
last_updated: 2026-03-26
---

## Summary
- Fixes 4 Critical CodeRabbit findings: `$GCP_PROJECT_ID` used as literal string in YAML `env:` and `with:` blocks instead of proper `${{ vars.GCP_PROJECT_ID }}` syntax
- 8 files, 12 changes total
- Shell `run:` blocks (gcloud commands) are unaffected — shell variables are correct there

## Metadata
- **PR**: #288
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +12/-12 in 8 files
- **Labels**: none

## Connections
