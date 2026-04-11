---
title: "PR #1844: Add Codex MCP launcher with legacy bash support"
type: source
tags: []
date: 2025-10-08
source_file: raw/prs-worldarchitect-ai/pr-1844.md
sources: []
last_updated: 2025-10-08
---

## Summary
- add a repo-root Codex MCP launcher that reuses the shared installer and re-execs under Homebrew Bash when the system shell is too old
- make the shared mcp_common helpers portable by avoiding bash-4-only syntax and skipping --scope for the Codex CLI
- ensure test mode returns immediately so Codex smoke checks can run without provisioning every server

## Metadata
- **PR**: #1844
- **Merged**: 2025-10-08
- **Author**: jleechan2015
- **Stats**: +101/-33 in 4 files
- **Labels**: none

## Connections
