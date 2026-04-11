---
title: "PR #5853: Fix campaign_id log context lifecycle in interaction flows (TDD)"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldarchitect-ai/pr-5853.md
sources: []
last_updated: 2026-03-04
---

## Summary
- Added red tests that prove `campaign_id` log context leaked after `/api/campaigns/<campaign_id>/interaction` and `/interaction/stream` lifecycle completion.
- Implemented minimal token-based log context lifecycle management using contextvars reset tokens.
- Ensured streaming still logs with the correct `campaign_id` during generation while cleaning context at stream teardown.
- Preserved existing endpoint behavior and response contracts.

## Metadata
- **PR**: #5853
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +70/-10 in 3 files
- **Labels**: none

## Connections
