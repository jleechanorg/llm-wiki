---
title: "PR #794: chore: disable local server rate limits by default (rerun tests)"
type: source
tags: []
date: 2025-11-21
source_file: raw/prs-/pr-794.md
sources: []
last_updated: 2025-11-21
---

## Summary
- Default local runs to `RUN_LOCAL_SERVER_DISABLE_RATE_LIMIT=true` in `run_local_server.sh` so developers don’t burn real API quotas when using real APIs locally.
- Cloud Run/production remain unchanged: bypass still only applies in non-Cloud Run envs and can be turned off by setting the flag to false.

## Metadata
- **PR**: #794
- **Merged**: 2025-11-21
- **Author**: jleechan2015
- **Stats**: +76/-9 in 5 files
- **Labels**: none

## Connections
