---
title: "Auto-Save"
type: concept
tags: [persistence, user-experience, event-handling, debouncing]
sources: []
last_updated: 2026-04-08
---

Auto-save is a UX pattern that automatically persists user input without requiring explicit save actions. In WorldAI settings, API key changes save automatically on blur event when the value has been modified.

## Implementation Details
- Triggered on blur (focus loss) event
- Only saves when `byok-dirty` flag indicates modification
- Checks for actual value change vs. original value
- Excludes placeholder values from saving

## Related Pages
- [[Settings Page JavaScript Functionality]] — implements auto-save

## Connections
- Dirty State Tracking — implementation technique
- Blur Event — trigger mechanism
- Debouncing — related pattern
