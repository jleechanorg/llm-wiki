---
title: "Stellaris Nocturne V1 — Scene 105"
type: source
tags: [campaign, scene, stellaris-nocturne-v1]
last_updated: 2026-04-12
scene_number: 105
scene_total: 106
source_file: /tmp/campaign_downloads_v2/
---

## Scene 105 Summary

============================================================ [Timestamp: 42000 DR, Tertius 15, 12:20:00 Location: Batiatus Estate Terrace, Aurelia Status: Lvl 5 Psionicist | HP: 25/25 | XP: 7150/14000 | Credits: 149,000,000,000]  Game Master: I misplayed the encounter because of a discrepancy between the narrative resolution and the underlying state logs. Here is the technical breakdown of why the error occurred:  1. **Incomplete Core Memory Log:** The `core_memories` array contained an entry fo

## Key Details

- **Location:** Batiatus Estate Terrace, Aurelia
- **Level hint:** 5
- **Word count:** 286
- **Campaign:** [[Stellaris Nocturne V1]]
- **Entry:** [[stellaris-nocturne-v1-entry-105]]

---

## Full Scene Content

============================================================
[Timestamp: 42000 DR, Tertius 15, 12:20:00
Location: Batiatus Estate Terrace, Aurelia
Status: Lvl 5 Psionicist | HP: 25/25 | XP: 7150/14000 | Credits: 149,000,000,000]

Game Master:
I misplayed the encounter because of a discrepancy between the narrative resolution and the underlying state logs. Here is the technical breakdown of why the error occurred:

1. **Incomplete Core Memory Log:** The `core_memories` array contained an entry for the 'Shadow King's Gambit' that logged the *initial suspicion* from Prince Xeres, but it lacked the entry for the 'Butcher's Alliance' (Sequence 130) where the conflict was resolved. When scanning high-priority context, I saw 'incurred suspicion' and defaulted to that conflict state.

2. **Stale Background Events:** There was a background event generated in Sequence 92 ('Xeres confirms the deception') labeled as a 'Severe diplomatic crisis' that remained in a 'pending' state in the game data. I prioritized this structured data over the dialogue history, causing the narrative to 'regress' to the conflict.

3. **Heuristic Bias:** Without the alliance milestone in the core memory summary, the logic interpreted the messenger's arrival through the lens of that pending crisis event rather than the later alliance.

**Corrections Applied:**
- I have updated the `core_memories` to explicitly include the 'Butcher's Alliance' and the resolution of the deception.
- I have cleared the stale 'diplomatic crisis' events from the background tracker.
- Xeres is now firmly established as a devoted **ALLY** in all internal tracking logic.

Time remains frozen. You may return to the story to address the Legion messenger (who is now correctly framed as panicking over the war's start, not your identity).

God Mode:
I wanna prevent this bug in other campaigns. It sounds like you didn’t have this in core memories?

============================================================
