---
title: "PR #5679: fix(preview): remove dead auth-bypass env vars from PR preview deploy"
type: source
tags: []
date: 2026-02-21
source_file: raw/prs-worldarchitect-ai/pr-5679.md
sources: []
last_updated: 2026-02-21
---

## Summary
- Remove `TESTING_AUTH_BYPASS=true` and `ALLOW_TEST_AUTH_BYPASS=true` from PR preview Cloud Run deploy
- These env vars have no effect because `PRODUCTION_MODE=true` gates off all bypass paths in `check_token`
- Prevents future misreadings of the deploy config as a security exposure

## Metadata
- **PR**: #5679
- **Merged**: 2026-02-21
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
