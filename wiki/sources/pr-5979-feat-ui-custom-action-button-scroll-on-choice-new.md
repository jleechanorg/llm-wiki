---
title: "PR #5979: feat(ui): custom action button, scroll-on-choice, new-campaign first-entry scroll, streaming guard"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5979.md
sources: []
last_updated: 2026-03-15
---

## Summary
- **Custom action button**: Always appended at the bottom of every planning block choices list; clicking focuses the text input instead of submitting a preset choice
- **Scroll on choice click**: `scrollToBottom` called (via form submit handler at 30ms) when a planning block choice is selected, so the streaming response is immediately visible
- **New campaign scroll**: On campaign creation, scrolls to the first AI narrative entry (`entries[1]` / Scene #1, skipping the god-mode setup entry) using

## Metadata
- **PR**: #5979
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +387/-8 in 3 files
- **Labels**: none

## Connections
