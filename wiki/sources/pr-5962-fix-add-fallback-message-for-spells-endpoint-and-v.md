---
title: "PR #5962: fix: add fallback message for spells endpoint and validate classifier timeout"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5962.md
sources: []
last_updated: 2026-03-14
---

## Summary
- Add fallback message in `/api/campaigns/<id>/spells` endpoint when spell slots exist but no spells/cantrips are recorded
- Add validation for `INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS` env var to emit warning when invalid

## Metadata
- **PR**: #5962
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +220/-549 in 8 files
- **Labels**: none

## Connections
