---
title: "PR #173: [agento] fix(ci): replace trigger-poll skeptic gate with deterministic 6-green check"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-173.md
sources: []
last_updated: 2026-03-31
---

## Summary
The worldai_claw skeptic-gate.yml used `-d "{\"body\": $BODY}"` to post comments via `gh api`, where `$BODY` is a multi-line printf string. This produces invalid JSON, causing the 'Post skeptic trigger comment' step to fail with exit code 1 for all PRs (#170, #171, #172).

## Metadata
- **PR**: #173
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +301/-170 in 1 files
- **Labels**: none

## Connections
