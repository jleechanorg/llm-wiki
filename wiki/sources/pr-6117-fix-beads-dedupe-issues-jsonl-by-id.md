---
title: "PR #6117: fix(beads): dedupe issues.jsonl by id"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldarchitect-ai/pr-6117.md
sources: []
last_updated: 2026-04-06
---

## Summary
- Removed duplicate JSONL lines with the same `id` (keep first occurrence).
- Fixes `br sync` error: `Prefix mismatch ... expected 'rev', found issue 'rev-stream-sign-env'` caused by repeated rows.

## Metadata
- **PR**: #6117
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +21/-721 in 2 files
- **Labels**: none

## Connections
