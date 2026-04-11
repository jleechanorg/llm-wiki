---
title: "PR #3139: test: Add mode parameter validation test with agent_mode verification"
type: source
tags: []
date: 2026-01-06
source_file: raw/prs-worldarchitect-ai/pr-3139.md
sources: []
last_updated: 2026-01-06
---

## Summary
- Remove story pagination pipeline: Firestore aggregation/query helpers, `/api/campaigns/<id>/story` endpoint, frontend load-older UI, and the real pagination E2E test; replace with a capped last-300 story response in `/api/campaigns/<id>` to stay under Cloud Run size limits; update API route tests/fake Firestore accordingly.
- Add mode-parameter validation harness and evidence capture (new `testing_mcp/test_mode_parameter_real_api.py`, evidence utils env masking tweaks), plus tighter validation

## Metadata
- **PR**: #3139
- **Merged**: 2026-01-06
- **Author**: jleechan2015
- **Stats**: +532/-16 in 6 files
- **Labels**: none

## Connections
