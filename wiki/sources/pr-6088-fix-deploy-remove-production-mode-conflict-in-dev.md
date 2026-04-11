---
title: "PR #6088: fix(deploy): remove PRODUCTION_MODE conflict in dev environments"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6088.md
sources: []
last_updated: 2026-04-04
---

## Summary
- **Root cause**: `deploy.sh` set `PRODUCTION_MODE=true` for ALL environments, then added `TESTING_AUTH_BYPASS=true` for dev/preview. The `_validate_production_environment()` check in `main.py` raises `RuntimeError` when both are present, crashing dev deploys.

- **Fix — `deploy.sh`** (3-way split):
  - `stable` / `staging`: `PRODUCTION_MODE=true` only — MCP auth enforced
  - `preview`: `PRODUCTION_MODE=true` only — required for SMOKE_TOKEN CI auth path (`main.py:1443-1451`). `TESTING_AUTH_BYPAS

## Metadata
- **PR**: #6088
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +19/-12 in 2 files
- **Labels**: none

## Connections
