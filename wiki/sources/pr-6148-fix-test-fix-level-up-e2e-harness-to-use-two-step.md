---
title: "PR #6148: fix(test): fix level-up E2E harness to use two-step routing verification"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6148.md
sources: []
last_updated: 2026-04-09
---

## Summary
Fixes a "level-up agent hijacking" bug where the `LevelUpAgent` was being hijacked by `CharacterCreationAgent` due to unconditional `level_up_pending` flag setting in `world_logic.py`. Also hardens the E2E test harness to comply with "Bulletproof Evidence" v3 standards, adding HMAC-SHA256 response signing and mandatory server log capture.

## Key Claims
- Level-up modal was appearing during character creation flow due to unguarded flag updates
- Added `character_creation_in_progress` guards in `_maybe_trigger_level_up_modal` (Lines 3472, 3500)
- E2E harness now uses two-step routing verification (validate AFTER Firestore state reload)
- Evidence capture includes HMAC-SHA256 signed LLM traces and server audit logs
- `EVIDENCE_SIGNATURE_GUARD` requires multiple properly-shaped signed responses

## Key Quotes
> "The `LevelUpAgent` routing was being hijacked by the `CharacterCreationAgent` because `world_logic.py` was unconditionally setting the `level_up_pending` flag even when a character creation session was in progress."

## Metadata
- **PR**: #6148
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +731/-152 in 9 files
- **Labels**: none

## Connections
- [[LevelUpAgent]] — routing hijacking fixed with character creation guard
- [[E2E test harness]] — hardened with bulletproof evidence v3 standards
- [[world_logic.py]] — guarded `_maybe_trigger_level_up_modal` with `character_creation_in_progress` checks
