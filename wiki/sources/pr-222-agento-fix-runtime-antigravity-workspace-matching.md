---
title: "PR #222: [agento] fix(runtime-antigravity): workspace matching, scrolling, Send button click"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-222.md
sources: []
last_updated: 2026-03-27
---

## Summary
The runtime-antigravity plugin drives Antigravity IDE via the Peekaboo macOS accessibility API. Five bugs prevented `ao spawn --runtime antigravity` from working in practice: workspace matching was too strict, no scrolling to find off-screen workspaces, wrong conversation window detection, pressing Return instead of clicking Send, and sendMessage targeting the wrong window.

## Metadata
- **PR**: #222
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +277/-44 in 2 files
- **Labels**: none

## Connections
