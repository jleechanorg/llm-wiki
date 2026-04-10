---
title: "Spell Slot Fallback"
type: concept
tags: [api-endpoint, user-experience, fallback-behavior]
sources: [spells-endpoint-fallback-tests]
last_updated: 2026-04-08
---

## Definition

The spell slot fallback is a user experience pattern in the `/api/campaigns/<id>/spells` endpoint where users who have spell slots allocated but have not yet configured their spell list receive a helpful prompt to set up their spells.

## Behavior

**Trigger Condition**: When `spell_slots` (or `resources.spell_slots`) exists AND all of `spells_known`, `cantrips`, and `spells_prepared` are empty/undefined.

**Fallback Message**: `"No spell list recorded. Type: \"What spells do I know?\" to set them up."`

**Non-Trigger Conditions**:
- Any of spells_known, cantrips, or spells_prepared is populated
- No spell_slots exist at all (non-spellcaster classes)

## Implementation

Located in main.py lines 2568-2574, the endpoint checks for this condition and returns the fallback message in the spells_summary field.

## Related Concepts
- [[FirestoreService]] — provides game state via get_campaign_game_state
- [[PlayerCharacterSpellManagement]] — user-facing spell list configuration
