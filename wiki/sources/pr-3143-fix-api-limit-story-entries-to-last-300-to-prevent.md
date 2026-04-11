---
title: "PR #3143: fix(api): Limit story entries to last 300 to prevent Cloud Run 500 errors"
type: source
tags: []
date: 2026-01-05
source_file: raw/prs-worldarchitect-ai/pr-3143.md
sources: []
last_updated: 2026-01-05
---

## Summary
- Campaign `kuXKa6vrYY6P99MfhWBn` had 1620 story entries = **34.7MB** response
- Exceeds Cloud Run's **32MB** limit, causing intermittent 500 errors
- GCP logs: `Response size was too large`

## Metadata
- **PR**: #3143
- **Merged**: 2026-01-05
- **Author**: jleechan2015
- **Stats**: +70/-0 in 2 files
- **Labels**: none

## Connections
