---
title: "PR #244: feat: allow disabling auth for local dev"
type: source
tags: [codex]
date: 2025-11-16
source_file: raw/prs-/pr-244.md
sources: []
last_updated: 2025-11-16
---

## Summary
- add a `--disable-auth` option to `run_local_server.sh` so the dev server can export `VITE_AUTH_DISABLED=true`, document the flag, and always bind the Vite server to `0.0.0.0`
- plumb a new `isAuthDisabled` flag through the auth context so the UI, Firebase helpers, and conversation hooks can bypass Google Sign-In when the flag is active
- add the new env typing and docs to clarify the workflow

## Metadata
- **PR**: #244
- **Merged**: 2025-11-16
- **Author**: jleechan2015
- **Stats**: +1271/-51 in 19 files
- **Labels**: codex

## Connections
