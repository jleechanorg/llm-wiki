---
title: "Bg3 Astarion — Scene 108"
type: source
tags: [campaign, scene, bg3-astarion]
last_updated: 2026-04-12
scene_number: 108
scene_total: 122
source_file: /tmp/campaign_downloads_v2/
---

## Scene 108 Summary

============================================================ Game Master: **DM Note: State Discrepancy Detected!**  It appears there was a miscalculation in the damage dealt to the Shadow Mastiff during Astarion's critical hit in the previous turn (SEQ_ID: 223). A critical hit doubles the total damage dealt.  *   **Original Calculation (SEQ_ID: 223):**     *   Base damage: `1d8 (6) + 3 (DEX Mod) = 9 damage`.     *   This was incorrectly applied directly. *   **Correct Critical Hit Calculation (a

## Key Details

- **Word count:** 183
- **Campaign:** [[Bg3 Astarion]]
- **Entry:** [[bg3-astarion-entry-108]]

---

## Full Scene Content

============================================================
Game Master:
**DM Note: State Discrepancy Detected!**

It appears there was a miscalculation in the damage dealt to the Shadow Mastiff during Astarion's critical hit in the previous turn (SEQ_ID: 223). A critical hit doubles the total damage dealt.

*   **Original Calculation (SEQ_ID: 223):**
    *   Base damage: `1d8 (6) + 3 (DEX Mod) = 9 damage`.
    *   This was incorrectly applied directly.
*   **Correct Critical Hit Calculation (as per Rule 6.7.A):**
    *   Base damage: `1d8 (6) + 3 (DEX Mod) = 9 damage`.
    *   **Total Critical Damage:** `9 * 2 = 18 damage`.
*   **Current Shadow Mastiff HP in State:** `33/33`.
*   **Corrected Shadow Mastiff HP:** `33 - 18 = 15 HP`.

Therefore, the Shadow Mastiff should currently have 15 HP, not 33 HP.

To resynchronize the game state and accurately reflect the damage from the critical hit, please copy and paste the following command as your next message:

`GOD_MODE_SET:`
`npc_data.Shadow Mastiff.hp_current = 15`

After you send this command, I will proceed with Astarion's next action (`AttackShadowMastiff_1`) and continue the narrative.

God Mode:
`GOD_MODE_SET:`
`npc_data.Shadow Mastiff.hp_current = 15`

Player (freeform):
continue

============================================================
