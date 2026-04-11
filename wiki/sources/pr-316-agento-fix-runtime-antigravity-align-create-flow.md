---
title: "PR #316: [agento] fix(runtime-antigravity): align create() flow with actual Manager UI"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-316.md
sources: []
last_updated: 2026-03-31
---

## Summary
The runtime-antigravity plugin's `create()` flow didn't match how Antigravity actually works — it clicked workspace labels instead of using the "Start new conversation" button, looked for separate conversation windows instead of operating within the Manager window, and tried to click Send buttons that are web-rendered and not in the A11y tree.

## Metadata
- **PR**: #316
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +1176/-402 in 10 files
- **Labels**: none

## Connections
