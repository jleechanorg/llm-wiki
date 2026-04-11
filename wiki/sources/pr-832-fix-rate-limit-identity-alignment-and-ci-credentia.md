---
title: "PR #832: Fix rate-limit identity alignment and CI credential guard"
type: source
tags: [codex]
date: 2025-11-25
source_file: raw/prs-/pr-832.md
sources: []
last_updated: 2025-11-25
---

## Summary
- Align preliminary and final rate-limit subjects to avoid trusting client-supplied userIds when auth is unavailable and reuse provisional identities
- Add coverage for missing-auth-tool scenario and tighten integration error assertion to production message
- Skip GCP dashboard validation when secrets are absent to keep forked CI green

## Metadata
- **PR**: #832
- **Merged**: 2025-11-25
- **Author**: jleechan2015
- **Stats**: +59/-30 in 4 files
- **Labels**: codex

## Connections
