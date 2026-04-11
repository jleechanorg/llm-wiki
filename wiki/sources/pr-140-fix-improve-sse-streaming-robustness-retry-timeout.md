---
title: "PR #140: fix: improve SSE streaming robustness - retry, timeout, error UX"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-140.md
sources: []
last_updated: 2026-03-29
---

## Summary
The SSE/streaming path in the web frontend (`handleSendMessage` in `App.tsx`) had several robustness gaps: silent failure on partial stream loss, no retry on transient network disconnects, no timeout indicator, and no visible connection state for the user.

## Metadata
- **PR**: #140
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +214/-128 in 5 files
- **Labels**: none

## Connections
