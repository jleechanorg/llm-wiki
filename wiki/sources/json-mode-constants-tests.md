---
title: "JSON Mode Constants Tests"
type: source
tags: [python, testing, constants, json-mode, state-updates]
source_file: "raw/test_json_mode_constants.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite verifying that constants have been updated for JSON mode. Tests validate that CHARACTER_DESIGN_REMINDER no longer instructs to include [STATE_UPDATES_PROPOSED] blocks in narrative text, and instead directs state updates to be placed in a JSON field.

## Key Claims
- **No STATE_UPDATES_PROPOSED instruction**: CHARACTER_DESIGN_REMINDER must not contain "[STATE_UPDATES_PROPOSED]" or "MANDATORY: Include [STATE_UPDATES_PROPOSED]"
- **JSON field guidance**: Reminder must state "State updates must be included in a JSON field" and "not in the narrative text"
- **Preserved instructions**: Other critical instructions remain: CRITICAL REMINDER, character design, numeric responses, selections from presented list

## Key Quotes
> "CHARACTER_DESIGN_REMINDER should not instruct to include STATE_UPDATES_PROPOSED blocks"

> "State updates must be included in a JSON field, not in the narrative text"

## Connections
- [[JSONMode]] — the mode this constant supports
- [[StateUpdatesProposed]] — the old pattern being replaced

## Contradictions
- None
