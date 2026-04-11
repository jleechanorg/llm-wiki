---
title: "PR #1951: Second Opinion: Attach PR context to MCP requests"
type: source
tags: [codex]
date: 2025-11-05
source_file: raw/prs-worldarchitect-ai/pr-1951.md
sources: []
last_updated: 2025-11-05
---

## Summary
- add a request builder that collects branch metadata, diffs, and per-file patches so the second opinion MCP call sees the full PR delta
- update the second opinion helper script to invoke the builder and automatically resolve a comparison base before sending the request
- refresh the command and skill docs to describe the automated git-context capture and new tuning options

## Metadata
- **PR**: #1951
- **Merged**: 2025-11-05
- **Author**: jleechan2015
- **Stats**: +313/-102 in 4 files
- **Labels**: codex

## Connections
