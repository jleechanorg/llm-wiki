---
title: "PR #5660: fix(openclaw): strip openclaw/ prefix in context window token lookups"
type: source
tags: []
date: 2026-02-20
source_file: raw/prs-worldarchitect-ai/pr-5660.md
sources: []
last_updated: 2026-02-20
---

## Summary
- Context window lookups for OpenClaw models fell back to 128K instead of 1M
- \`_get_gateway_url()\` returned stale import-time URL, inconsistent with runtime env reads in \`_resolve_gateway_url\`
- Added unit tests for both fixes (33 passing total)

## Metadata
- **PR**: #5660
- **Merged**: 2026-02-20
- **Author**: jleechan2015
- **Stats**: +102/-10 in 3 files
- **Labels**: none

## Connections
