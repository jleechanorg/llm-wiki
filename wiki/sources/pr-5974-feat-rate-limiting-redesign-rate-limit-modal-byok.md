---
title: "PR #5974: feat(rate-limiting): redesign rate limit modal, BYOK CTA, cache fix"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5974.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Redesigned rate-limit modal with dark-card theme, removed red header, replaced email CTA with "Go to Settings" button directing users to add their own API key (BYOK)
- Added dismissable "Add your key — unlimited turns" CTA banner in the game toolbar, shown when no BYOK provider is active
- Fixed BYOK settings cache not invalidating after MCP `update_user_settings` call, causing users to stay rate-limited for up to 60s after adding a key
- Fixed false "API key expired" errors from BYOK cache pr

## Metadata
- **PR**: #5974
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +995/-82 in 12 files
- **Labels**: none

## Connections
