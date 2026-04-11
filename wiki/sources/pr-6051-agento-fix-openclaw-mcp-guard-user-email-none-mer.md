---
title: "PR #6051: [agento] fix(openclaw,mcp): guard user_email=None + merge duplicate import"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldarchitect-ai/pr-6051.md
sources: []
last_updated: 2026-03-28
---

## Summary
Fixes two minor issues identified during skeptic review of PR #5879:
- Personal API key auth path now returns email from Firestore when available, preventing `user_email=None` crashes downstream
- Merged duplicate `streaming_orchestrator` import block

## Metadata
- **PR**: #6051
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +194/-15 in 3 files
- **Labels**: none

## Connections
