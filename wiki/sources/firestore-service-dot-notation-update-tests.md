---
title: "Firestore Service Dot-Notation Update Tests"
type: source
tags: [python, testing, firestore, update-campaign, dot-notation, nested-paths]
source_file: "raw/test_update_campaign_dot_notation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test coverage for the `update_campaign` function in firestore_service.py, specifically validating that dot-notation path updates correctly create nested structures. Tests address a bug where dot-notation updates like `game_state.custom_campaign_state.arc_milestones.wedding_tour` were creating literal field names instead of nested dictionaries.

## Key Claims
- **Dot-notation creates nested structure**: Updates with dots like `game_state.custom_campaign_state.arc_milestones.wedding_tour` expand to proper nested dicts
- **Simple key updates work**: Regular updates without dot notation continue to function correctly
- **Merge with existing nested**: Dot-notation updates merge into existing nested fields without overwriting unrelated data
- **Mock singleton persistence**: Mock Firestore maintains document state across get_db() calls

## Key Quotes
> "This is the core fix for the issue where dot-notation updates like 'game_state.custom_campaign_state.arc_milestones.wedding_tour' were creating literal field names instead of nested structures."

## Connections
- [[FirestoreService]] — the module being tested
- [[UpdateCampaign]] — the function under test
- [[DotNotationPathUpdates]] — the technical pattern being validated

## Contradictions
- None identified
