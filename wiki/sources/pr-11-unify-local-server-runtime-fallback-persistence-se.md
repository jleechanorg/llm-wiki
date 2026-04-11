---
title: "PR #11: Unify local server runtime + fallback persistence + setup wizard OpenClaw proof"
type: source
tags: []
date: 2026-02-23
source_file: raw/prs-worldai_claw/pr-11.md
sources: []
last_updated: 2026-02-23
---

## Summary
- Unified local runtime: single `run_local_server.sh` process serves both API and frontend on one port, replacing the separate Vite dev server model.
- Removed dead-code backend stubs: deleted 8 files (`openclaw_client.ts`, `routes/turn.ts`, `routes/sessions.ts`, `memory/session_store.ts`, `services/sessionStore.ts`, `storage/firestore.ts`, `storage/index.ts`, `tests/firestoreSync.test.ts`) that were superseded by the real OpenClaw proxy in `server.ts`.
- Added auth token injection to all fronte

## Metadata
- **PR**: #11
- **Merged**: 2026-02-23
- **Author**: jleechan2015
- **Stats**: +2210/-986 in 50 files
- **Labels**: none

## Connections
