---
title: "PR #5725: Add preview-only MCP smoke auth bypass"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldarchitect-ai/pr-5725.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Add a narrow preview-only `/mcp` smoke auth bypass in `mvp_site/main.py` using `X-Smoke-Test-Auth` plus the `SMOKE_SMOKE_TOKEN` secret.
- Inject `SMOKE_SMOKE_TOKEN` into PR preview deployment secrets in `.github/workflows/pr-preview.yml`.
- Pass `SMOKE_SMOKE_TOKEN` into preview smoke test job env in `.github/workflows/mcp-smoke-tests.yml`.
- Update `scripts/mcp-smoke-tests.mjs` to send `X-Smoke-Test-Auth` on smoke-check requests.

## Metadata
- **PR**: #5725
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +36/-2 in 5 files
- **Labels**: none

## Connections
