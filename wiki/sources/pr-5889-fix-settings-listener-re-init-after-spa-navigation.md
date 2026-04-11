---
title: "PR #5889: Fix settings listener re-init after SPA navigation"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5889.md
sources: []
last_updated: 2026-03-14
---

## Summary
This is a clean extraction of the true settings navigation fix from #5511 onto current `main`.

When the SPA loads `/settings`, it replaces `settingsView.innerHTML` with fresh DOM. On repeat visits, [`initializeSettings()`](mvp_site/frontend_v1/app.js) skipped `setupSettingsEventListeners()` because `window.settingsListenersAttached` was already set from the first visit. That left the replacement settings DOM without model/BYOK listeners.

This PR fixes only that re-initialization bug.

## Metadata
- **PR**: #5889
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +149/-4 in 2 files
- **Labels**: none

## Connections
