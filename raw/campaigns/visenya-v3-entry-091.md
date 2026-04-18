---
title: "Visenya V3 — Scene 091"
type: source
tags: [campaign, scene, visenya-v3]
last_updated: 2026-04-12
scene_number: 91
scene_total: 173
source_file: /tmp/campaign_downloads_v2/
---

## Scene 091 Summary

============================================================ [Timestamp: 129 AC, The Sowing 23, 11:10:00 Location: Sea-Caves, Whispering Cliffs Status: Lvl 4 Dragon Lord | HP: 22/22 | XP: 4550/6500 | Gold: 25gp Conditions: Withdrawal Tremors | Exhaustion: 0 | Inspiration: No] [FACTION STATUS] Turn 1 | Rank #201/201 | FP: 0 ⚔️ Soldiers: 0 | 🕵️ Spies: 0 | 👑 Elites: 0 (Avg Lvl 6) 🏰 Territory: 0 | 🏛️ Citizens: 0/0 | 💰 Gold: 10 | ✨ Arcana: 0/0  Game Master: Yes, your roll of **18 vs DC 14** was a suc

## Key Details

- **Location:** Sea-Caves, Whispering Cliffs
- **Level hint:** 4
- **Word count:** 329
- **Campaign:** [[Visenya V3]]
- **Entry:** [[visenya-v3-entry-091]]

---

## Full Scene Content

============================================================
[Timestamp: 129 AC, The Sowing 23, 11:10:00
Location: Sea-Caves, Whispering Cliffs
Status: Lvl 4 Dragon Lord | HP: 22/22 | XP: 4550/6500 | Gold: 25gp
Conditions: Withdrawal Tremors | Exhaustion: 0 | Inspiration: No]
[FACTION STATUS] Turn 1 | Rank #201/201 | FP: 0
⚔️ Soldiers: 0 | 🕵️ Spies: 0 | 👑 Elites: 0 (Avg Lvl 6)
🏰 Territory: 0 | 🏛️ Citizens: 0/0 | 💰 Gold: 10 | ✨ Arcana: 0/0

Game Master:
Yes, your roll of **18 vs DC 14** was a successful check. The confusion stems from a discrepancy in how the Social HP and Tier systems were displayed in the last turn.

### Administrative Audit & Correction:

1.  **Roll Confirmation**: Your Persuasion roll of 18 (11 on the die + 7 modifier) successfully beat the DC 14. This was a success.
2.  **Tier Correction**: The previous response incorrectly assigned the Green Scout Wing-Leader 5 Social HP. Per the system authority in `game_state_instruction.md`, a **guard-tier** NPC has a maximum of **3 Social HP**. 
3.  **Mechanical Resolution**: In the Social HP system, a success deals 'damage' to an NPC's resistance. A success by a margin of 4 (18 vs 14) deals **1 Social HP damage**. 
4.  **State Sync**: The scout started with 3 HP. Your success reduced him to **2/3 Social HP**. He is currently **WAVERING**. 

**Why he didn't surrender immediately:**
Social HP functions like combat HP for significant NPCs. Unless the NPC only has 1 HP (like a commoner), a single successful roll will crack their resolve but usually requires follow-up pressure to achieve a total surrender. 

**Corrections Applied to State:**
- Adjusted `social_hp_max` to 3 (Guard Tier).
- Adjusted `social_hp` to 2 (1 damage applied from success).
- Set `cooldown_remaining` to 1 (Damage was dealt this turn).
- Fixed `successes` to 1.

Player (choice: god:return_story):
Return to Story - Resume the interrogation now that the math is settled. The scout is visibly shaken but still holding onto his secrets for another moment.

============================================================
