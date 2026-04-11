---
title: "PR #6180: fix(wizard): normalize whitespace in campaign description input"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6180.md
sources: []
last_updated: 2026-04-11
---

## Summary
- Fix whitespace handling bug in campaign wizard description input (rev-xcak)
- `rawDescription.trim()` was used for the truthiness check but the untrimmed `rawDescription` was returned on the truthy branch
- Now returns `rawDescription.trim()` so leading/trailing whitespace is normalized

## Metadata
- **PR**: #6180
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
