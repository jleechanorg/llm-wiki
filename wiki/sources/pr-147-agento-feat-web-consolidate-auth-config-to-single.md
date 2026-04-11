---
title: "PR #147: [agento] feat(web): consolidate auth config to single localStorage source"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-147.md
sources: []
last_updated: 2026-03-29
---

## Summary
apiClient.ts had a `VITE_WORLDCLAW_TOKEN` env var check that ran before localStorage lookup. This allowed the build-time env var to bypass the settings UI — users who changed their token in Settings would find their API calls still using the stale env var token.

Additionally, `AppContext` stored `baseUrl`/`authToken` in React state but never hydrated from localStorage on initialization, creating a parallel source of truth disconnected from what the Settings screen saves.

## Metadata
- **PR**: #147
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +161/-9 in 5 files
- **Labels**: none

## Connections
