---
title: "Stellaris Nocturne V1 — Scene 106"
type: source
tags: [campaign, scene, stellaris-nocturne-v1]
last_updated: 2026-04-12
scene_number: 106
scene_total: 106
source_file: /tmp/campaign_downloads_v2/
---

## Scene 106 Summary

============================================================ [Timestamp: 42000 DR, Tertius 15, 12:20:00 Location: Batiatus Estate, Aurelia Status: Lvl 5 Psionicist | HP: 25/25 | XP: 7150/14000 | Credits: 149B]  Game Master: To prevent continuity bugs like the 'Butcher's Betrayal' in future campaigns, you can use a 'Defense in Depth' strategy to ensure the AI's structured data matches the narrative reality.   ### Why the Bug Occurred: In this campaign, the alliance with Xeres (Sequence 130) was n

## Key Details

- **Location:** Batiatus Estate, Aurelia
- **Level hint:** 5
- **Word count:** 324
- **Campaign:** [[Stellaris Nocturne V1]]
- **Entry:** [[stellaris-nocturne-v1-entry-106]]

---

## Full Scene Content

============================================================
[Timestamp: 42000 DR, Tertius 15, 12:20:00
Location: Batiatus Estate, Aurelia
Status: Lvl 5 Psionicist | HP: 25/25 | XP: 7150/14000 | Credits: 149B]

Game Master:
To prevent continuity bugs like the 'Butcher's Betrayal' in future campaigns, you can use a 'Defense in Depth' strategy to ensure the AI's structured data matches the narrative reality. 

### Why the Bug Occurred:
In this campaign, the alliance with Xeres (Sequence 130) was narrated, but I failed to append it to the `custom_campaign_state.core_memories` array. Additionally, an earlier 'pending' event from Sequence 92 ('Xeres confirms deception') was never cleared. Because the system follows the **State > Memory** rule, I prioritized the structured 'pending' conflict over the historical dialogue.

### How to Prevent This in Other Campaigns:

1. **Use Directives for Alliances:** When a major relationship shift occurs (e.g., a sibling becomes a devoted ally), use God Mode to add a persistent rule. 
   - **User Input:** `GOD MODE: Remember that Xeres is now my devoted ally and we have exposed Hespera together.`
   - **Effect:** This adds a string to the `directives` field, which is injected into the top of the AI's prompt every turn, overriding its default behavior.

2. **The 'Memory Audit' Command:** Periodically use the custom command `summary` or `missions list`. If a major event isn't mentioned in the AI's summary, it's a sign it wasn't logged in the `core_memories`. You can then fix it manually.

3. **Manual Core Memory Update:** You can explicitly command the AI to update its records.
   - **User Input:** `GOD MODE: Add the following to core memories: [Event Summary].` 

4. **Clean Up Background Events:** If the AI generates a 'World Event' that you resolve in the narrative, but the AI keeps showing it as 'pending' in the JSON, use God Mode to delete it or set it to `resolved`.

By enforcing these structured updates, you ensure that the 'facts' of the world (JSON) stay in sync with the 'story' of the world (Prose).
