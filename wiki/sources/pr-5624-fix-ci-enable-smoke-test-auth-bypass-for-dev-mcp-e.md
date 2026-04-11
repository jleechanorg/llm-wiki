---
title: "PR #5624: fix(ci): enable smoke test auth bypass for dev MCP endpoint"
type: source
tags: []
date: 2026-02-18
source_file: raw/prs-worldarchitect-ai/pr-5624.md
sources: []
last_updated: 2026-02-18
---

## Summary
- Fixed HTTP 401 on auto-deploy-dev smoke tests that prevented real LLM smoke validation
- Root cause: PRODUCTION_MODE=true enforces Firebase auth on /mcp, but smoke tests sent no auth headers
- Fix: Enable TESTING_AUTH_BYPASS=true on dev deployments only + add X-Test-Bypass-Auth header to smoke test requests

## Metadata
- **PR**: #5624
- **Merged**: 2026-02-18
- **Author**: jleechan2015
- **Stats**: +10/-2 in 2 files
- **Labels**: none

## Connections
