---
title: "PR #6083: [agento] fix(testing_http): start local server dynamically for HTTP tests"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldarchitect-ai/pr-6083.md
sources: []
last_updated: 2026-04-03
---

## Summary
- **Root cause**: `WAHttpTest` extended `HttpTestBase` (generic base) which does NOT manage server lifecycle. All HTTP tests hardcoded `BASE_URL = "http://localhost:8086"` with no server starting, causing "connection refused" on every test run.
- **Fix**: `WAHttpTest.setup()` now starts a local gunicorn server before tests run; `teardown()` stops it after. `BASE_URL` resolved via `_resolve_http_base_url()`. External `TEST_SERVER_URL` env var respected for CI preview server.

## Metadata
- **PR**: #6083
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +210/-15 in 2 files
- **Labels**: none

## Connections
