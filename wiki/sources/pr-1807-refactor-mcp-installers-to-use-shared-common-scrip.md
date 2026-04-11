---
title: "PR #1807: Refactor MCP installers to use shared common script"
type: source
tags: [codex]
date: 2025-10-02
source_file: raw/prs-worldarchitect-ai/pr-1807.md
sources: []
last_updated: 2025-10-02
---

## Summary
- extract the large shared MCP installation logic into `scripts/mcp_common.sh` parameterized by CLI-specific variables
- reduce `claude_mcp.sh` and `codex_mcp.sh` to lightweight wrappers that configure product defaults and source the shared implementation
- add a configurable CLI availability guard so Codex can fail fast when its binary is missing while preserving Claude defaults

## Metadata
- **PR**: #1807
- **Merged**: 2025-10-02
- **Author**: jleechan2015
- **Stats**: +1939/-1776 in 3 files
- **Labels**: codex

## Connections
