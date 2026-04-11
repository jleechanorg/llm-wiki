---
title: "PR #5878: fix(settings): settings button click now renders settings page correctly"
type: source
tags: []
date: 2026-03-08
source_file: raw/prs-worldarchitect-ai/pr-5878.md
sources: []
last_updated: 2026-03-08
---

## Summary
- **Root cause**: `document.querySelector('.container.mt-4')` matched `#dashboard-view` (which carries that class), so `settings-view` was appended as a *child* of dashboard. When `showView('settings')` removed `active-view` from dashboard, dashboard became `display:none` and hid its child `settings-view` with it — despite `settings-view` itself having `active-view`.
- **Fix**: Use `document.getElementById('main-content')` to append `settings-view` as a sibling of other views, matching `index.ht

## Metadata
- **PR**: #5878
- **Merged**: 2026-03-08
- **Author**: jleechan2015
- **Stats**: +171/-17 in 2 files
- **Labels**: none

## Connections
