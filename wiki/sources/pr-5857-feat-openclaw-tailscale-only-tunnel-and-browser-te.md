---
title: "PR #5857: feat: OpenClaw Tailscale-only tunnel and browser test hardening"
type: source
tags: []
date: 2026-03-08
source_file: raw/prs-worldarchitect-ai/pr-5857.md
sources: []
last_updated: 2026-03-08
---

## Summary
- Add Tailscale tunnel script + install automation (LaunchAgent for macOS auto-start)
- Add CLI-based Tailscale tunnel E2E test with **semantic content validation** (proof token echo required, not just HTTP 200)
- Separate localhost vs Tailscale testing_mcp tests
- Fix browser test infrastructure: MCP-to-HTTP fallback when MCP client unavailable
- Fix test_openclaw_browser.py to set gateway token (prevents 401 on LLM calls)
- Fix classifier startup to degrade gracefully on HuggingFace 429 (extra

## Metadata
- **PR**: #5857
- **Merged**: 2026-03-08
- **Author**: jleechan2015
- **Stats**: +3289/-742 in 32 files
- **Labels**: none

## Connections
