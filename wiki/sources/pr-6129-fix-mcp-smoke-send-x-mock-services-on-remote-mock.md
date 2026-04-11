---
title: "PR #6129: fix(mcp-smoke): send X-Mock-Services on remote mock runs to avoid Gemini billing"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldarchitect-ai/pr-6129.md
sources: []
last_updated: 2026-04-07
---

## Summary
- **MCP preview smoke (GitHub Actions + `MCP_SERVER_URL`)**: When `SMOKE_TOKEN` is set and `MCP_TEST_MODE` is not `real`, the harness now sends `X-Mock-Services: true` so the preview server sets Flask `g.mock_services_mode` and uses the mock LLM path instead of billing Gemini for every scenario.
- **Parity**: `llm_service._is_mock_services_mode()` now treats the same `MOCK_SERVICES_MODE` env values as truthy as `world_logic.is_mock_services_mode()` (e.g. `1`, `yes`, `y`, `on`), and the MCP strea

## Metadata
- **PR**: #6129
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +219/-130 in 9 files
- **Labels**: none

## Connections
