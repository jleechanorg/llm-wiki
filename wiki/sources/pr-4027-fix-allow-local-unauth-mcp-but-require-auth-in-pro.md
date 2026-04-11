---
title: "PR #4027: fix: allow local unauth mcp but require auth in prod"
type: source
tags: []
date: 2026-01-25
source_file: raw/prs-worldarchitect-ai/pr-4027.md
sources: []
last_updated: 2026-01-25
---

## Summary
- allow unauthenticated /mcp access only when PRODUCTION_MODE is not true
- keep auth-enforced /mcp behavior in production and preserve user_id override tests
- update API route tests for prod vs local behavior

## Metadata
- **PR**: #4027
- **Merged**: 2026-01-25
- **Author**: jleechan2015
- **Stats**: +178/-335 in 9 files
- **Labels**: none

## Connections
