---
title: "Merc Solo Brute Gladius — Scene 072"
type: source
tags: [campaign, scene, merc-solo-brute-gladius]
last_updated: 2026-04-12
scene_number: 72
scene_total: 110
source_file: /tmp/campaign_downloads_v2/
---

## Scene 072 Summary

============================================================ Game Master: `[Mode: DM MODE]`  You are absolutely right to point that out. My apologies; that is another oversight in my state management and XP tracking.  **Explanation of the Discrepancy:**  You are correct that Gladius should have gained Experience Points (XP) from the elimination of the Miller and Blackwood families. As per the `Destiny Core Rules` (Section 3.2.C.1), "XP is awarded for overcoming Combat Encounters" and for "clever

## Key Details

- **Word count:** 390
- **Campaign:** [[Merc Solo Brute Gladius]]
- **Entry:** [[merc-solo-brute-gladius-entry-072]]

---

## Full Scene Content

============================================================
Game Master:
`[Mode: DM MODE]`

You are absolutely right to point that out. My apologies; that is another oversight in my state management and XP tracking.

**Explanation of the Discrepancy:**

You are correct that Gladius should have gained Experience Points (XP) from the elimination of the Miller and Blackwood families. As per the `Destiny Core Rules` (Section 3.2.C.1), "XP is awarded for overcoming Combat Encounters" and for "cleverly bypassing a dangerous combat encounter without direct violence." The silent elimination of these families certainly qualifies.

My error was in not processing and proposing an XP update for those successful eliminations in the game state after each family was dealt with. This is a recurring issue with dynamic stats not being fully integrated into the `CURRENT GAME STATE` from the outset, which we are now actively rectifying.

**XP Calculation for Past Eliminations:**

*   **Miller Family:** 4 souls. Treating them as Level 1 foes (as "peasants" and "simple folk" would suggest).
    *   XP per foe = (Level^2) \* 10 = (1^2) \* 10 = 10 XP.
    *   Total for Miller Family = 4 souls \* 10 XP/soul = **40 XP**.
*   **Blackwood Family:** 2 souls. Also treated as Level 1 foes.
    *   XP per foe = 10 XP.
    *   Total for Blackwood Family = 2 souls \* 10 XP/soul = **20 XP**.

**Total XP to be added: 40 XP + 20 XP = 60 XP.**

To rectify this and ensure accurate XP tracking going forward, we need to update Gladius's `xp_current` in the `CURRENT GAME STATE`.

Please copy and paste the entire block below as your next message to your server/API call to inject this XP into Gladius's profile:

---
`GOD_MODE_SET:`
`player_character_data.xp_current = 60`
`custom_campaign_state.core_memories.append = "Gladius gained 60 XP from eliminating the Miller (40 XP) and Blackwood (20 XP) families, updating his current XP total."`
---

Once you send that `GOD_MODE_SET:` command, Gladius's current XP will be correctly reflected in the `CURRENT GAME STATE`, and the `Key Game Stats` header will update accordingly in future `STORY MODE` responses.

I am in DM MODE and will remain here until you explicitly instruct me to return to STORY MODE, or if you send the `GOD_MODE_SET:` command to fix the state.

God Mode:
How much exp does a character need to be level 5? Is that is X then I hsould have X+60

============================================================
