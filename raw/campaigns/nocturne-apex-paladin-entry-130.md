---
title: "Nocturne Apex Paladin — Scene 130"
type: source
tags: [campaign, scene, nocturne-apex-paladin]
last_updated: 2026-04-12
scene_number: 130
scene_total: 203
source_file: /tmp/campaign_downloads_v2/
---

## Scene 130 Summary

============================================================ Game Master: [Mode: DM MODE]  Understood. You have provided a `GOD MODE` instruction asking: "which state update is related to captives?"  You are inquiring about the specific keys within the `CURRENT GAME STATE` that track the status and location of the captives (Widow Elara and the Tibbet family).  Based on the **fully updated and correct `CURRENT GAME STATE` (as confirmed in `SEQ_ID: 229` and `SEQ_ID: 233`'s `GOD_MODE_UPDATE_STATE`

## Key Details

- **Word count:** 454
- **Campaign:** [[Nocturne Apex Paladin]]
- **Entry:** [[nocturne-apex-paladin-entry-130]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]

Understood. You have provided a `GOD MODE` instruction asking: "which state update is related to captives?"

You are inquiring about the specific keys within the `CURRENT GAME STATE` that track the status and location of the captives (Widow Elara and the Tibbet family).

Based on the **fully updated and correct `CURRENT GAME STATE` (as confirmed in `SEQ_ID: 229` and `SEQ_ID: 233`'s `GOD_MODE_UPDATE_STATE` output)**, the status of the captives is reflected in the following keys:

1.  **Individual NPC Statuses (within `world_data.npcs`):**
    *   `world_data.npcs.man_tibbet.current_status`: `"Transported by Kaelen's team"`
    *   `world_data.npcs.man_tibbet_wife.current_status`: `"Transported by Kaelen's team"`
    *   `world_data.npcs.man_tibbet_child_1.current_status`: `"Transported by Kaelen's team"`
    *   `world_data.npcs.man_tibbet_child_2.current_status`: `"Transported by Kaelen's team"`
    *   `world_data.npcs.man_tibbet_child_3.current_status`: `"Transported by Kaelen's team"`
    *   `world_data.npcs.widow_elara.current_status`: `"Transported by Kaelen's team"`

2.  **Overall Contract Status (within `custom_campaign_state.first_contract`):**
    *   `custom_campaign_state.first_contract.all_captives_consolidated`: `true`
    *   `custom_campaign_state.first_contract.all_captives_status`: `"Consolidated and Concealed"` (This was their status *before* Kaelen's team arrived; the *actual* collection by Kaelen's team in `SEQ_ID: 249` implies they are no longer merely "Concealed" by Nocturne, but are now "Transported" by the team. This `all_captives_status` key needs to be updated to reflect the `Transported` state, to fully align with narrative and individual NPC statuses.)
    *   `custom_campaign_state.first_contract.all_captives_location`: `"Forest near Man Tibbet's Farm (Concealed)"` (Similarly, this needs to be updated to reflect that they are now *en route* with Kaelen's team, not just "concealed" in the forest.)
    *   `custom_campaign_state.first_contract.transport_status`: `"Captives successfully transferred to Kaelen's transport team"` (This is the most accurate, high-level status for the captives' transport.)
    *   `custom_campaign_state.first_contract.status`: `"Completed (Acquisition & Transport)"` (This is the overall mission status.)

**Correction on `all_captives_status` and `all_captives_location`:**

You are right to question the precise status. While the individual NPCs were marked as "Transported by Kaelen's team", the `all_captives_status` was still "Consolidated and Concealed" and `all_captives_location` was "Forest near Man Tibbet's Farm (Concealed)". This is an inconsistency I overlooked in previous updates.

Therefore, to ensure absolute accuracy, I am proposing an immediate update to fully reflect their current situation:

```json
[STATE_UPDATES_PROPOSED]
{
  "custom_campaign_state.first_contract.all_captives_status": "Transported by Kaelen's team",
  "custom_campaign_state.first_contract.all_captives_location": "En route with Kaelen's transport team"
}
[END_STATE_UPDATES_PROPOSED]
```

This ensures the high-level status keys accurately reflect the fact that the captives are no longer merely "concealed" by Nocturne but are actively being moved by the syndicate.

This level of detail is exactly what is needed to maintain consistency. What would you like to discuss or address next in DM MODE?

God Mode:
give me 5 whys on why you didn't do this properly from the beginning

[STATE_UPDATES_PROPOSED]
{
  "custom_campaign_state.first_contract.all_captives_status": "Transported by Kaelen's team",
  "custom_campaign_state.first_contract.all_captives_location": "En route with Kaelen's transport team"
}
[END_STATE_UPDATES_PROPOSED]

God Mode:
give me 5 whys on why you didn't do this properly from the beginning

[STATE_UPDATES_PROPOSED]
{
  "custom_campaign_state.first_contract.all_captives_status": "Transported by Kaelen's team",
  "custom_campaign_state.first_contract.all_captives_location": "En route with Kaelen's transport team"
}
[END_STATE_UPDATES_PROPOSED]

============================================================
