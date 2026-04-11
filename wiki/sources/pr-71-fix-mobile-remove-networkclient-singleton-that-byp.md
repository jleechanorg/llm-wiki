---
title: "PR #71: fix(mobile): remove networkClient singleton that bypasses AppContext"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-71.md
sources: []
last_updated: 2026-03-26
---

## Summary
Bead `worldai_claw-6w9`: The exported `networkClient` singleton in `packages/mobile/src/services/networkClient.ts` used hardcoded `localhost:3000` and empty auth token, bypassing `AppContext` `baseUrl`/`authToken` settings. Any screen importing this singleton would not reflect user-configured backend URLs.

## Metadata
- **PR**: #71
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +9/-1596 in 2 files
- **Labels**: none

## Connections
