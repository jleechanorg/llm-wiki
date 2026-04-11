---
title: "PR #543: fix: remove conversation start tool"
type: source
tags: [codex]
date: 2025-11-04
source_file: raw/prs-/pr-543.md
sources: []
last_updated: 2025-11-04
---

## Summary
- remove the `conversation.start` MCP tool from the backend and rely on `conversation.send-message` for creation
- update backend README, CI smoke tests, and integration utilities to reflect the revised toolset
- adjust unit and integration tests plus the MCP simulator to exercise the new creation flow

## Metadata
- **PR**: #543
- **Merged**: 2025-11-04
- **Author**: jleechan2015
- **Stats**: +218/-326 in 8 files
- **Labels**: codex

## Connections
