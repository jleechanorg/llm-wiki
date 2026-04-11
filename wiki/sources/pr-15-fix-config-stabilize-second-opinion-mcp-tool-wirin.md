---
title: "PR #15: fix(config): stabilize second-opinion MCP tool wiring"
type: source
tags: []
date: 2026-03-03
source_file: raw/prs-worldai_claw/pr-15.md
sources: []
last_updated: 2026-03-03
---

## Summary
- switch second-opinion policy from `tools.allow` to additive `tools.alsoAllow`
- align second-opinion tool IDs with adapter-safe names (`second-opinion-tool_agent_second_opinion`, `second-opinion-tool_rate_limit_status`, `second-opinion-tool_health-check`)
- enable/configure `openclaw-mcp-adapter` in baseline and discord bot templates
- update discord bot README to document the exact allowlisted tool IDs

## Metadata
- **PR**: #15
- **Merged**: 2026-03-03
- **Author**: jleechan2015
- **Stats**: +616/-132 in 7 files
- **Labels**: none

## Connections
