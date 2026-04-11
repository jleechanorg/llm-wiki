---
title: "PR #1769: Fix: Build iOS Simulator MCP server before configuration"
type: source
tags: [codex]
date: 2025-09-28
source_file: raw/prs-worldarchitect-ai/pr-1769.md
sources: []
last_updated: 2025-09-28
---

## Summary
- run the iOS Simulator MCP npm build step during installation so the compiled entrypoint exists
- detect the built entrypoint when configuring Claude and fall back to index.js with clear logging

## Metadata
- **PR**: #1769
- **Merged**: 2025-09-28
- **Author**: jleechan2015
- **Stats**: +67/-4 in 1 files
- **Labels**: codex

## Connections
