---
title: "PR #361: [agento] ci: add builtin plugin deps gate + fix wholesome evidence label patterns"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-361.md
sources: []
last_updated: 2026-04-04
---

## Summary
1. **CI gate gap**: `test_builtin_plugin_deps.test.ts` existed (PR #334) but was not enforced in CI — a new builtin plugin added without updating `packages/cli/package.json` would silently bypass the test.
2. **wholesome.yml broken**: The `grep -qF` and `awk` patterns for evidence label detection were missing the closing `**` before the colon. Evidence Has Media Attachment was failing for all PRs.

## Metadata
- **PR**: #361
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +56/-42 in 4 files
- **Labels**: none

## Connections
