---
title: "Nocturne Apex Paladin — Scene 039"
type: source
tags: [campaign, scene, nocturne-apex-paladin]
last_updated: 2026-04-12
scene_number: 39
scene_total: 203
source_file: /tmp/campaign_downloads_v2/
---

## Scene 039 Summary

============================================================ Game Master: [Mode: DM MODE]  Understood. You have provided a `DM Note` (treated as `GOD MODE`) requesting a significant retcon: "My MC is smart and wouldn't use plate armor for a mission like this. Give me equivalent medium armor or something better for stealth, give me a hideout and put my plate armor there."  This is a valid point, and Nocturne's high Intelligence and meticulous nature (`Conscientiousness: 4/5`) would indeed dictate

## Key Details

- **Location:** ** A well-concealed, multi-story apartment above a disused weaver's shop in a quiet, less-patrolled alley of Baldur's Gate's **Lower City**, near the border with the Upper City.
- **Word count:** 782
- **Campaign:** [[Nocturne Apex Paladin]]
- **Entry:** [[nocturne-apex-paladin-entry-039]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]

Understood. You have provided a `DM Note` (treated as `GOD MODE`) requesting a significant retcon: "My MC is smart and wouldn't use plate armor for a mission like this. Give me equivalent medium armor or something better for stealth, give me a hideout and put my plate armor there."

This is a valid point, and Nocturne's high Intelligence and meticulous nature (`Conscientiousness: 4/5`) would indeed dictate optimal gear for a discreet mission. I will implement this change and establish a hideout for her.

However, this retcon has a **direct and substantial impact on the previous narrative sequence** (specifically `SEQ_ID: 57`, `59`, and `62`), as it means the initial stealth attempt would have been resolved differently.

### Proposed Retcon: Gear & Hideout

1.  **New Stealth Armor:** Nocturne's **Fine Plate Armor** (Defense +8, DR 1, Stealth Disadvantage) is replaced with **Masterwork Shadow-Weave Half Plate**.
    *   **Masterwork Shadow-Weave Half Plate:**
        *   **Defense Bonus:** +5 (Nocturne's total Defense would now be 10 (base) + 5 (armor) + 2 (Coord Mod) + 1 (Battle-Hardened Fighting Style) = **18**).
        *   **Damage Reduction (DR):** 1.
        *   **Properties:** Grants **Advantage on Stealth checks** in dim light or darkness. Does not impose disadvantage on Stealth checks in bright light.
    *   *Rationale:* This armor offers substantial protection while being far superior for stealth, especially in low-light conditions, perfectly suiting a discreet operation and Nocturne's tactical brilliance.

2.  **Nocturne's Hideout:** A secure and discreet base of operations.
    *   **Name:** The Black Lily's Den
    *   **Location:** A well-concealed, multi-story apartment above a disused weaver's shop in a quiet, less-patrolled alley of Baldur's Gate's **Lower City**, near the border with the Upper City.
    *   **Features:** Secured doors and windows, a hidden compartment for valuables (where her Fine Plate Armor is now stored), and basic amenities. It is an ideal, low-profile staging and planning hub, known only to Nocturne and a very select few.

### Impact on Previous Narrative & Re-calculation

Since Nocturne, with her intelligence, *would* have worn this new armor for the Oakhaven mission, the initial stealth attempt (`SEQ_ID: 57`) needs to be re-evaluated.

**Original Stealth Roll (with Plate Armor's Disadvantage):**
*   Action: [Nocturne attempts to stealthily approach the Oakhaven Mastiffs for a silent neutralization]
*   Roll Type: d20 (Disadvantage) + Coordination Modifier (+2)
*   Dice Rolled (Disadvantage): 8, 15
*   Roll Used: 8
*   Total: 8 + 2 = 10
*   Mastiff Perception: 15
*   Result: PC Stealth (10) vs. Mastiff 1 Perception (15) — **Mastiff Success! (Detection)**

**Re-calculated Stealth Roll (with Masterwork Shadow-Weave Half Plate's Advantage, and in dim light/darkness):**
*   Action: [Nocturne attempts to stealthily approach the Oakhaven Mastiffs for a silent neutralization]
*   Roll Type: d20 (Advantage) + Coordination Modifier (+2)
*   Dice Rolled (Advantage): **[Rolling 2d20 now: 18, 5]**
*   Roll Used: **18**
*   Modifiers:
    *   Coordination Modifier: +2
    *   Situational Bonuses (Shadow-Weave Half Plate): Advantage (as rolled)
*   Total: 18 + 2 = **20**
*   Mastiff Perception: 15
*   Result: PC Stealth (20) vs. Mastiff 1 Perception (15) — **Nocturne Success! (Undetected)**

**Conclusion of Retcon Impact:**
The re-calculation indicates that with the appropriate gear, Nocturne's initial stealth attempt would have succeeded. This means the mastiffs **would not have barked**, and the villagers **would not have been alerted** or subsequently interrogated. The events of `SEQ_ID: 57` (from the barks onward), `SEQ_ID: 59` (the planning block in response to detection), and `SEQ_ID: 62` (the interrogation scene) **would not have occurred as described.**

### Your Decision

Given this significant narrative alteration, please confirm how you wish to proceed:

1.  **[ProceedWithNewStealthOutcome_1]:** Accept the full retcon. The mastiffs were silently neutralized, the villagers were never alerted, and the interrogation never took place. The narrative will resume from Nocturne, undetected, having silently dealt with the mastiffs and now planning her next move *without* the immediate pressure of approaching villagers.
2.  **[MaintainPreviousNarrative_2]:** Decline the full retroactive change. The previous events (mastiffs barking, villagers alerted, interrogation) remain canon. The new armor and hideout will be applied to Nocturne's character sheet *from this point forward*, meaning this armor will be used for all future stealth rolls, but the opening sequence remains as it was. This implicitly means that for *this specific first mission*, Nocturne *did* wear the plate armor or somehow failed despite superior gear.

Please choose one option. Once confirmed, I will display Nocturne's finalized character sheet and commence the campaign.

[STATE_UPDATES_PROPOSED]
{
  "player_character_data.inventory.plate_armor": {
    "name": "Fine Plate Armor",
    "defense_bonus": 8,
    "dr": 1,
    "stealth_disadvantage": true
  },
  "player_character_data.inventory.longsword": {
    "name": "Masterwork Longsword",
    "damage_die": "1d8 slashing",
    "versatile_damage_die": "1d10 slashing",
    "attack_bonus": 0,
    "damage_bonus": 0
  },
  "player_character_data.inventory.potion_of_greater_healing": null,
  "player_character_data.inventory.potion_of_healing": 3,
  "player_character_data.inventory.gold": 200,
  "player_character_data.aptitudes.physique.potential_coefficient": 5,
  "player_character_data.aptitudes.coordination.potential_coefficient": 4,
  "player_character_data.aptitudes.health.potential_coefficient": 4,
  "player_character_data.aptitudes.intelligence.potential_coefficient": 5,
  "player_character_data.aptitudes.wisdom.potential_coefficient": 5,
  "custom_campaign_state.campaign_difficulty_scaled_up": true,
  "player_character_data.secret_myers_briggs_type": "INTJ",
  "world_data.npcs.valerius_julian.secret_myers_briggs_type": "INTJ"
}
[END_STATE_UPDATES_PROPOSED]

God Mode:
MaintainPreviousNarrative_2

============================================================
