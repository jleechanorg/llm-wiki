---
title: "PR #149: fix: Simplify CORS wildcard to allow all ai-universe-frontend deployments"
type: source
tags: []
date: 2025-10-03
source_file: raw/prs-/pr-149.md
sources: []
last_updated: 2025-10-03
---

## Summary
- Simplifies CORS configuration to allow any `ai-universe-frontend*` deployment
- Removes production-only CORS_ALLOWED_ORIGINS requirement
- Removes unnecessary PR preview pattern (already covered by wildcard)
- Fixes CORS blocking for frontends deployed to non-us-central1 regions
- Adds missing `async-mutex` dependency

## Metadata
- **PR**: #149
- **Merged**: 2025-10-03
- **Author**: jleechan2015
- **Stats**: +7/-22 in 4 files
- **Labels**: none

## Connections
