---
title: "PR #5915: fix(smoke): decouple SMOKE_TOKEN auth from mock LLM activation"
type: source
tags: []
date: 2026-03-09
source_file: raw/prs-worldarchitect-ai/pr-5915.md
sources: []
last_updated: 2026-03-09
---

## Summary
- Real E2E `/smoke` tests were receiving mock LLM responses because `SMOKE_TOKEN` unconditionally activated `g.mock_services_mode = True` server-side
- Scenario 7 (streaming timing contracts) detected `mock_services_mode=True` in the done payload → failed as "mock fallback in real mode"
- This is the root cause of the `[Real E2E] MCP Smoke Tests Failed` on PR #5895

## Metadata
- **PR**: #5915
- **Merged**: 2026-03-09
- **Author**: jleechan2015
- **Stats**: +23/-6 in 2 files
- **Labels**: none

## Connections
