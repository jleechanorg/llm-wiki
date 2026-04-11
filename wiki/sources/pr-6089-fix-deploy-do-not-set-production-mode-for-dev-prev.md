---
title: "PR #6089: fix(deploy): do not set PRODUCTION_MODE for dev/preview environments"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6089.md
sources: []
last_updated: 2026-04-04
---

## Summary
- **Bug 1 fix (root cause)**: `deploy.sh` no longer sets `PRODUCTION_MODE=true` for dev/preview environments. Dev/preview use `TESTING_AUTH_BYPASS=true` (no `PRODUCTION_MODE`), staging/stable get `PRODUCTION_MODE=true`. This resolves the RuntimeError crash in dev Cloud Run deployments.
- **Bug 2 fix**: `main.py` error formatter now shows actual flag values (e.g. `TESTING_AUTH_BYPASS=true`) instead of truncated names with empty values (`TESTING_AUTH_BYPASS=`).

## Metadata
- **PR**: #6089
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +9/-6 in 1 files
- **Labels**: none

## Connections
