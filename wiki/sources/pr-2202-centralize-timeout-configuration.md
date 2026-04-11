---
title: "PR #2202: Centralize timeout configuration"
type: source
tags: [codex]
date: 2025-11-30
source_file: raw/prs-worldarchitect-ai/pr-2202.md
sources: []
last_updated: 2025-11-30
---

## Summary
- add `scripts/timeout_config.sh` to export the shared 10-minute timeout and source it from deployment scripts while passing Cloud Run env vars
- align Gunicorn, MCP client, and both frontends to `WORLDARCH_TIMEOUT_SECONDS`, with docs (README/DEPLOYMENT/CLAUDE/AGENTS) reflecting the centralized guardrail
- extend timeout tests to cover the new environment override path

## Metadata
- **PR**: #2202
- **Merged**: 2025-11-30
- **Author**: jleechan2015
- **Stats**: +163/-31 in 13 files
- **Labels**: codex

## Connections
