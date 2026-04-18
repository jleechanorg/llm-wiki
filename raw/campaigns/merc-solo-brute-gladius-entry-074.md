---
title: "Merc Solo Brute Gladius — Scene 074"
type: source
tags: [campaign, scene, merc-solo-brute-gladius]
last_updated: 2026-04-12
scene_number: 74
scene_total: 110
source_file: /tmp/campaign_downloads_v2/
---

## Scene 074 Summary

============================================================ Game Master: `[Mode: DM MODE]`  Understood. You are asking for further clarification regarding Gladius's XP and Level, specifically questioning if his current XP should be 5,760.  This is a common and excellent question, as different RPG systems track XP in slightly different ways. In our **Destiny Core Rules**, the `xp_current` value (which is displayed in the `Key Game Stats` line as `XP current_xp/xp_to_next_level`) represents the *

## Key Details

- **Word count:** 362
- **Campaign:** [[Merc Solo Brute Gladius]]
- **Entry:** [[merc-solo-brute-gladius-entry-074]]

---

## Full Scene Content

============================================================
Game Master:
`[Mode: DM MODE]`

Understood. You are asking for further clarification regarding Gladius's XP and Level, specifically questioning if his current XP should be 5,760.

This is a common and excellent question, as different RPG systems track XP in slightly different ways. In our **Destiny Core Rules**, the `xp_current` value (which is displayed in the `Key Game Stats` line as `XP current_xp/xp_to_next_level`) represents the **Experience Points earned *since the character's last level-up***. It is the progress Gladius has made *towards his next level*.

Let's break it down for Gladius:

1.  **Starting Level and Cumulative XP:** When you initially defined Gladius as "Level 5," it meant he had *already accumulated* the necessary **5,700 total XP** to reach Level 5. This cumulative XP is essentially "spent" to attain that level.
2.  **XP for the Next Level:** From Level 5, Gladius needs **5,000 more XP** to reach Level 6 (as per the "XP to Next Level" column in the Destiny XP Progression Table for Level 5).
3.  **XP Earned Since Level 5:**
    *   Elimination of Miller Family: +40 XP
    *   Elimination of Blackwood Family: +20 XP
    *   **Total XP earned since starting Level 5 = 60 XP.**

Therefore, Gladius's `xp_current` (meaning, his progress *towards Level 6*) is indeed **60**. His overall cumulative XP would technically be 5,700 (for Level 5) + 60 (earned since Level 5) = 5,760. However, the `xp_current` field in the game state and the `Key Game Stats` header is specifically designed to show his current progress *towards the next level*, not his lifetime cumulative total.

So, the proposed `GOD_MODE_SET:` command to set `player_character_data.xp_current = 60` is correct for reflecting his progress towards Level 6.

Does this distinction between "cumulative XP to reach a level" and "XP earned since last level-up" clarify why his `xp_current` is 60 rather than 5,760?

I am in DM MODE and will remain here until you explicitly instruct me to return to STORY MODE, or if you send the `GOD_MODE_SET:` command to finalize the state change.

God Mode:
`GOD_MODE_SET:`
`player_character_data.xp_current = 60`
`custom_campaign_state.core_memories.append = "Gladius gained 60 XP from eliminating the Miller (40 XP) and Blackwood (20 XP) families, updating his current XP total."`

============================================================
