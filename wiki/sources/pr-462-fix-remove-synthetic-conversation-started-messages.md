---
title: "PR #462: fix: remove synthetic 'Conversation started' messages and add auto-dependency installation"
type: source
tags: []
date: 2025-10-31
source_file: raw/prs-/pr-462.md
sources: []
last_updated: 2025-10-31
---

## Summary
- Removes synthetic "Conversation started: {title}" messages that were causing duplicate conversation entries in the UI
- Makes `initialMessage` required for all new conversations
- Deprecates `startConversation()` method to prevent future synthetic message creation
- Adds automatic dependency check and installation to `run-local-server.ts`

## Metadata
- **PR**: #462
- **Merged**: 2025-10-31
- **Author**: jleechan2015
- **Stats**: +298/-135 in 10 files
- **Labels**: none

## Connections
