---
title: "PR #4833: fix(secondo): use correct VITE_AI_UNIVERSE_FIREBASE_* env var prefix"
type: source
tags: []
date: 2026-02-05
source_file: raw/prs-worldarchitect-ai/pr-4833.md
sources: []
last_updated: 2026-02-05
---

## Summary
- Fix `/secondo` command failing with `auth/api-key-not-valid` error on cross-machine usage
- The auth-cli.mjs expects `VITE_AI_UNIVERSE_FIREBASE_*` env vars, not `FIREBASE_*`

**Key themes:**
- Environment variable prefix alignment with auth-cli.mjs

## Metadata
- **PR**: #4833
- **Merged**: 2026-02-05
- **Author**: jleechan2015
- **Stats**: +22/-23 in 3 files
- **Labels**: none

## Connections
