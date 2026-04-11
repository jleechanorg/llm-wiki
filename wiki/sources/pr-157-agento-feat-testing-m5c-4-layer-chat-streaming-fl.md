---
title: "PR #157: [agento] feat(testing): M5c 4-layer chat streaming flow integration test"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-157.md
sources: []
last_updated: 2026-03-31
---

## Summary
- Add `testing_mcp/test_streaming_flow.py` — a real integration test for the 4-layer SSE streaming chain
- Exercises: client POST `/sessions/:id/turn` → server turn endpoint → OpenClaw gateway → SSE event emission back to client
- Verifies: (1) SSE stream returns HTTP 200, (2) at least one delta/chunk event has text content, (3) stream closes with a done/complete event
- Uses `testing_mcp` style: real local server via `running_backend()`, no mocks

## Metadata
- **PR**: #157
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +244/-0 in 2 files
- **Labels**: none

## Connections
