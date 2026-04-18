---
title: "Sariel Assiah — Scene 045"
type: source
tags: [campaign, scene, sariel-assiah]
last_updated: 2026-04-12
scene_number: 45
scene_total: 58
source_file: /tmp/campaign_downloads_v2/
---

## Scene 045 Summary

============================================================ Game Master: [Mode: DM MODE] Understood. You have provided a `DM Note` to award appropriate XP for Sariel's recent discoveries.  Sariel has uncovered fundamental, world-altering truths about her mother's true nature, the Null Genesis Project, and the terrifying concept of the "Joyful Predator." These revelations are pivotal to her understanding of her own lineage and the core mysteries of the campaign. This constitutes a "Formidable/Le

## Key Details

- **Word count:** 1088
- **Campaign:** [[Sariel Assiah]]
- **Entry:** [[sariel-assiah-entry-045]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]
Understood. You have provided a `DM Note` to award appropriate XP for Sariel's recent discoveries.

Sariel has uncovered fundamental, world-altering truths about her mother's true nature, the Null Genesis Project, and the terrifying concept of the "Joyful Predator." These revelations are pivotal to her understanding of her own lineage and the core mysteries of the campaign. This constitutes a "Formidable/Legendary Task" in terms of intellectual discovery, providing a significant XP award.

**XP Award:** 1000 XP

This award reflects the profound nature and strategic importance of the knowledge she has just acquired.

[STATE_UPDATES_PROPOSED]
{
  "player_character_data": {
    "xp_current": 1000,
    "level": 2,
    "hp_max": 14,
    "hp_current": 14
  },
  "custom_campaign_state": {
    "core_memories": {
      "append": "Sariel discovers the Null Genesis Project, learning her mother, Alexiel, was a hidden magical prodigy whose 'Null' status was a lifelong deception. She uncovers the existence of the 'Joyful Predator' trait within her bloodline, tied to Lucifer's celestial essence."
    }
  }
}
[END_STATE_UPDATES_PROPOSED]

**LEVEL UP!**

Sariel Arcanus has reached **Level 2**!
She gains +6 maximum HP (rolling a d6 for a Wizard's Hit Die and adding her Health modifier of +0, I'll take the average of 4 + 0 = 4, plus 2 base for a level up + 2 from health mod. I am going to re-evaluate this as the formula for HP is `(rolled Hit Die) + Health modifier`. So Level 1 is `(max Hit Die) + Health Mod`, and subsequent levels are `(rolled Hit Die) + Health Mod`. For a d6, that's 1d6 + 0. I will assume an average roll of 3 for now, bringing her HP up by 3 from 8 to 11. I made a mistake in the state update in the previous prompt, assuming the base HP was 8, meaning she'd have 4 points from a d6 at Level 1, then adding the health mod. Re-calculating: Level 1 is 6 (max d6) + 0 (Health Mod) = 6 HP. Then Level 2 would be 1d6 (average 3.5, round to 4) + 0 Health Mod = 4 HP. So 6+4 = 10 HP. Let me correct the state update to reflect this.

**HP Correction:** Sariel's HP should be 6 at Level 1. Upon leveling to Level 2, she gains 1d6 HP. Assuming an average roll of 3, her new max HP is 6 + 3 = 9.
*I must be careful with HP calculation based on the rules. Level 1 HP is Max Hit Die + Health Modifier. Subsequent levels are Rolled Hit Die + Health Modifier.*
Sariel is Level 1, HP 8/8. Her Health Aptitude is 10 (+0). Her Hit Die is a d6.
So at Level 1, Max HP should be `6 (max d6) + 0 (Health Mod) = 6`.
This means the initial state for Sariel had an error in HP calculation. I will correct this first.

Let me propose a `GOD_MODE_SET` to correct Sariel's HP to 6/6 at Level 1, before applying the Level 2 increase.
Then, for Level 2, she gains 1d6 + 0. Average 3.5, so 4. New Max HP = 6 + 4 = 10.

**HP Calculation Correction Process:**
1.  **Initial State HP Correction:** Sariel Level 1, d6 Hit Die, Health Mod +0. Max HP should be 6. `player_character_data.hp_max = 6`, `player_character_data.hp_current = 6`.
2.  **Level 2 HP Gain:** Sariel gains `1d6` (average 4, rounding up for consistency) + `0` Health Mod = 4 HP.
3.  **New Max HP:** `6 + 4 = 10`.

I will provide a `GOD_MODE_SET` command for the user to correct the current HP in the state, then explain the level up benefits.

```
GOD_MODE_SET:
player_character_data.hp_max = 6
player_character_data.hp_current = 6
```
**Explanation:** Princess Sariel, your starting HP was miscalculated. As a Level 1 Wizard with a d6 Hit Die and a +0 Health modifier, your maximum HP should be 6. You will need to apply this correction before leveling up.

Once you have applied this correction, please paste the following into your next message to confirm and proceed with the Level 2 benefits: `CONFIRM HP CORRECTION`.

***
Once the user confirms the correction, I will then apply the Level 2 benefits.
For now, the story is paused.[Mode: DM MODE]
Understood. You have provided a `DM Note` to award appropriate XP for Sariel's recent discoveries.

Sariel has uncovered fundamental, world-altering truths about her mother's true nature, the Null Genesis Project, and the terrifying concept of the "Joyful Predator." These revelations are pivotal to her understanding of her own lineage and the core mysteries of the campaign. This constitutes a "Formidable/Legendary Task" in terms of intellectual discovery, providing a significant XP award.

**XP Award:** 1000 XP

**HP Calculation Correction:**
Before applying the Level 2 benefits, we need to correct Sariel's initial HP. According to the `Destiny Core Rules`, a Level 1 character's maximum HP is calculated as the maximum roll of their class's Hit Die plus their Health modifier. For Sariel, a Level 1 Wizard with a d6 Hit Die and a +0 Health modifier, her maximum HP should be 6 (max d6) + 0 = 6. The current state has her at 8 HP, which is incorrect.

Please apply the following `GOD_MODE_SET:` command to correct her current HP. Once applied, confirm with "CONFIRM HP CORRECTION".

```
GOD_MODE_SET:
player_character_data.hp_max = 6
player_character_data.hp_current = 6
```
**Explanation:** Princess Sariel, your starting HP was miscalculated in the initial character generation. As a Level 1 Wizard with a d6 Hit Die and a +0 Health modifier, your maximum HP should be 6. You will need to apply this correction now. Once you have applied this correction, please paste "CONFIRM HP CORRECTION" as your next message, and I will then detail your Level 2 benefits.

[SEQ_ID: 89]

God Mode:
DM note: the joyful predator thing should not be purely academic. It should be about dominating or destroying people in a clever way on a personal level, so it seems evil.

You felt a dizzying surge of both fear and a chilling fascination. The text described how this 'joy' wasn't mere sadism, but the profound intellectual satisfaction of solving a complex problem through absolute control and overwhelming force. The same cold, analytical clarity that you felt when a star chart perfectly aligned, when a cryptographic puzzle yielded its secrets. The same feeling that had driven your mother to impossible victories. You closed the journal, its ancient leather suddenly feeling hot in your trembling hands. The weight of this inheritance, the potential for that terrifying 'joy' within your own blood, was a burden far heavier than any guilt you had carried before.

============================================================
