---
title: "PR #207: [antig] fix: remove duplicate knownActionTypes guard (TS error) and normalize partyId in sessions list"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-207.md
sources: []
last_updated: 2026-04-04
---

## Summary
Two bugs introduced during PR #196 review iteration:
1. **TS compile error** – a duplicate `knownActionTypes.has()` guard was accidentally left in `faction_simulator.ts` after moving the check before `resolveAction`. The original code used `KNOWN_ACTION_TYPES` (module-level const) but the duplicate referenced an undeclared `knownActionTypes`, causing `TS2552` across 51 test suites.
2. **API contract inconsistency** – `GET /sessions` returned `party_id` (snake_case) while all other fields used ca

## Metadata
- **PR**: #207
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +1/-3 in 2 files
- **Labels**: none

## Connections
