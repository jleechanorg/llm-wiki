---
title: "PR #179: fix(backend): shared helper for persisted history dice reminder (#81)"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-179.md
sources: []
last_updated: 2026-04-03
---

## Summary
Implements worldai_claw#81 by extracting `chatMessagesForPersistedHistory()` so streaming and non-streaming `session.history` persistence share one code path (system drop, context-injection drop, DICE_REMINDER strip on user messages).

## Metadata
- **PR**: #179
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +88/-24 in 3 files
- **Labels**: none

## Connections
