---
title: "PR #5691: feat: streaming contracts, smoke auth token, CI hardening, and REV-fd2 mode confidence design"
type: source
tags: []
date: 2026-02-23
source_file: raw/prs-worldarchitect-ai/pr-5691.md
sources: []
last_updated: 2026-02-23
---

## Summary
- **Streaming contracts** — SCENARIO 7 (character / think / god-mode) now pass 9/9 in both mock and real CI mode; removed `response_json_schema` from streaming calls that broke code execution and caused double-streaming
- **Smoke auth token** — `SMOKE_TOKEN` injected into preview server via `pr-preview.yml`; sent as `X-MCP-Smoke-Token` header by CI; server validates it to bypass Firebase auth for preview smoke tests without exposing production credentials
- **CI hardening** — `STREAM_RESPONSE_SI

## Metadata
- **PR**: #5691
- **Merged**: 2026-02-23
- **Author**: jleechan2015
- **Stats**: +5034/-326 in 76 files
- **Labels**: none

## Connections
