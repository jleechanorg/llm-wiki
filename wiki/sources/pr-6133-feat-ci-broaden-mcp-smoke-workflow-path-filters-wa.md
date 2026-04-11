---
title: "PR #6133: feat(ci): broaden MCP smoke workflow path filters (wa-6129)"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldarchitect-ai/pr-6133.md
sources: []
last_updated: 2026-04-07
---

## Summary
- Expand `pull_request` and `push` path filters in `.github/workflows/mcp-smoke-tests.yml` so edits to MCP smoke comment generation, mode-contract scripts, `scripts/lib/**`, or `tests/test_mcp_global_installation.py` trigger the MCP Smoke Tests workflow.
- Add a regression test that locks in those path entries.
- Align `isolation_info` docstring example in `testing_mcp/lib/evidence_utils.py` with the `shared_campaigns` key used at runtime.

## Metadata
- **PR**: #6133
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +120/-32 in 4 files
- **Labels**: none

## Connections
