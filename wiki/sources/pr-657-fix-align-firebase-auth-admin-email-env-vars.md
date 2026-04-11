---
title: "PR #657: fix: align firebase auth admin email env vars"
type: source
tags: [codex]
date: 2025-11-12
source_file: raw/prs-/pr-657.md
sources: []
last_updated: 2025-11-12
---

## Summary
- load admin email allowlist in `FirebaseAuthTool` from `ADMIN_EMAILS` with fallback to `FIREBASE_ADMIN_EMAILS`
- keep admin detection consistent between Firebase auth and rate limit tooling

## Metadata
- **PR**: #657
- **Merged**: 2025-11-12
- **Author**: jleechan2015
- **Stats**: +5/-2 in 1 files
- **Labels**: codex

## Connections
