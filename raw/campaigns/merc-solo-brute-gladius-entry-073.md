---
title: "Merc Solo Brute Gladius — Scene 073"
type: source
tags: [campaign, scene, merc-solo-brute-gladius]
last_updated: 2026-04-12
scene_number: 73
scene_total: 110
source_file: /tmp/campaign_downloads_v2/
---

## Scene 073 Summary

============================================================ Game Master: `[Mode: DM MODE]`  Understood. You are asking for clarification on Gladius's XP and Level, specifically how much XP is needed for Level 5, and why his current XP value is displayed as it is.  Let's break down the XP progression as defined in the `Destiny Core Rules` (Section 3.2.B, XP Progression Table):  1.  **XP to *be* Level 5:**     *   To *reach* Level 5, a character needs to have accumulated a **Total XP for Level**

## Key Details

- **Level hint:** 5
- **Word count:** 432
- **Campaign:** [[Merc Solo Brute Gladius]]
- **Entry:** [[merc-solo-brute-gladius-entry-073]]

---

## Full Scene Content

============================================================
Game Master:
`[Mode: DM MODE]`

Understood. You are asking for clarification on Gladius's XP and Level, specifically how much XP is needed for Level 5, and why his current XP value is displayed as it is.

Let's break down the XP progression as defined in the `Destiny Core Rules` (Section 3.2.B, XP Progression Table):

1.  **XP to *be* Level 5:**
    *   To *reach* Level 5, a character needs to have accumulated a **Total XP for Level** of **5,700 XP**. This is the cumulative XP earned from Level 1 up to the point of becoming Level 5.

2.  **XP *from* Level 5 *to* Level 6:**
    *   Once a character *is* Level 5, they need an additional **5,000 XP** to reach Level 6. This is the amount listed under "XP to Next Level" for Level 5.

**Gladius's Situation:**
You specified that Gladius *starts* at Level 5. This means he has already achieved the cumulative 5,700 XP needed to be a Level 5 character.

In our system, the `xp_current` value tracked in the `Key Game Stats` header and in the `game_state` represents the XP earned **since the character's last level-up.** It is the progress towards their *next* level.

*   When Gladius started at Level 5, his `xp_current` was effectively `0` (towards Level 6).
*   He then earned `40 XP` from eliminating the Miller family.
*   He then earned `20 XP` from eliminating the Blackwood family.
*   Therefore, his `xp_current` should be `0 + 40 + 20 = 60 XP`.

The `Key Game Stats` in the `STORY MODE` output currently shows `XP 0/5000 (Lvl 5)`. This is because, as we've identified, the `player_character_data.xp_current` value in the `CURRENT GAME STATE` was not being correctly updated by previous actions.

To rectify this and ensure Gladius's XP is accurately tracked from this point forward, the `GOD_MODE_SET:` command I provided in the previous turn (Sequence ID 145) is necessary. It will update his `xp_current` to `60`.

---
`GOD_MODE_SET:`
`player_character_data.xp_current = 60`
`custom_campaign_state.core_memories.append = "Gladius gained 60 XP from eliminating the Miller (40 XP) and Blackwood (20 XP) families, updating his current XP total."`
---

Once you send that `GOD_MODE_SET:` command, Gladius's current XP will be correctly reflected in the `CURRENT GAME STATE` as `60`, and the `Key Game Stats` header in future `STORY MODE` responses will display `XP 60/5000 (Lvl 5)`.

Does this explanation clarify the XP system and Gladius's current progression?

I am in DM MODE and will remain here until you explicitly instruct me to return to STORY MODE, or if you send the `GOD_MODE_SET:` command to fix the state.

God Mode:
Shouldn't it be 5,760

============================================================
