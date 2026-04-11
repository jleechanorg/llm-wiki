---
title: "Structured Fields Storage Test"
type: source
tags: [testing, firestore, storage, python, structured-data]
source_file: "raw/structured-fields-storage-test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit test verifying that structured fields (session_header, planning_block, dice_rolls, resources, debug_info) are properly stored and retrieved from Firestore alongside story entries. Tests the persistence layer for campaign data with AI-generated narrative content.

## Key Claims
- **session_header Preservation**: Session header text must persist unchanged through Firestore write/read cycle
- **planning_block Preservation**: Planning block content (multi-line choice prompts) must remain intact
- **dice_rolls Preservation**: Dice roll annotations stored as string list must be retrievable
- **resources Preservation**: Resource string (HP/gold status) must persist accurately
- **debug_info Preservation**: Debug info dictionary must serialize and deserialize correctly

## Connections
- [[Firestore]] — backend persistence for structured field storage
- [[Story Entries]] — data structure that carries structured fields alongside narrative text

## Contradictions
- None identified
