---
title: "Nocturne Apex Paladin — Scene 070"
type: source
tags: [campaign, scene, nocturne-apex-paladin]
last_updated: 2026-04-12
scene_number: 70
scene_total: 203
source_file: /tmp/campaign_downloads_v2/
---

## Scene 070 Summary

============================================================ Game Master: [Mode: STORY MODE] Sequence ID: 140 | Timestamp: 1492 DR, Ches 20, 06:08:00 PM | Location: Ridge Overlooking Man Tibbet's Farm | Narrative State Summary: Nocturne has silently neutralized the road patrol, looted and concealed their bodies, and is now observing Man Tibbet's farm, aware of its hidden guards and magical ward. She has devised a plan to lure out and neutralize the internal guards using a subtle sound. | Key Gam

## Key Details

- **Location:** Ridge Overlooking Man Tibbet's Farm | Narrative State Summary: Nocturne has silently neutralized the road patrol, looted and concealed their bodies, and is now observing Man Tibbet's farm, aware of its hidden guards and magical ward. She has devised a plan to lure out and neutralize the internal guards using a subtle sound. | Key Game Stats: XP 5960/10700 (Lvl 5), Followers: 0, Income: 0gp/day, Gold: 255gp, HP: 43/43, EP: 16/36, CP: 1 | Missions: Kidnap peasants to sell as slaves: *Secure Widow Elara, Scout Tibbet's Farm, Neutralize Road Patrol.* | [HASH:G5H6I7J8K9L0M1N2]
- **Level hint:** 5
- **Word count:** 861
- **Campaign:** [[Nocturne Apex Paladin]]
- **Entry:** [[nocturne-apex-paladin-entry-070]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: STORY MODE]
Sequence ID: 140 | Timestamp: 1492 DR, Ches 20, 06:08:00 PM | Location: Ridge Overlooking Man Tibbet's Farm | Narrative State Summary: Nocturne has silently neutralized the road patrol, looted and concealed their bodies, and is now observing Man Tibbet's farm, aware of its hidden guards and magical ward. She has devised a plan to lure out and neutralize the internal guards using a subtle sound. | Key Game Stats: XP 5960/10700 (Lvl 5), Followers: 0, Income: 0gp/day, Gold: 255gp, HP: 43/43, EP: 16/36, CP: 1 | Missions: Kidnap peasants to sell as slaves: *Secure Widow Elara, Scout Tibbet's Farm, Neutralize Road Patrol.* | [HASH:G5H6I7J8K9L0M1N2]

Location: Approaching Man Tibbet's Farm, Barn Side, Early Evening

The detailed blueprint of Man Tibbet's farm, etched into Nocturne's (Level 5 Paladin, Age 16) mind by her **Apex Senses** scan, guided her every step. The primary target was the "large family," but the immediate obstacle was the two professional guards nestled within the farmhouse and the arcane ward pulsating near the barn. Her meticulous plan to lure them out, isolate them, and eliminate them silently was already in motion. This was the precise strike an Apex Predator favored, minimizing chaos and maximizing efficiency.

She moved with a chilling grace, her Masterwork Shadow-Weave Half Plate absorbing the dim, moon-dappled light as she slipped down from the ridge. Her route took her through a winding path of tall, whispering crops and sparse trees, keeping her out of sight of the farmhouse windows. The air was cool, carrying the earthy scent of the farm and, faintly, the underlying thrum of the magical ward near the barn. Her Coordination (14) was a silent symphony, ensuring no leaf crunched too loudly, no branch snapped underfoot. Every movement was economical, a testament to her honed discipline (Conscientiousness 4/5).

Action: [Nocturne attempts to stealthily move to the far side of the barn to set up the lure.]
Roll Type: d20 (Advantage) + Coordination Modifier
DC/TN: 14 (Challenging, given the active arcane ward and vigilant guards nearby)
Dice Rolled (Advantage): 18, 11
Roll Used: 18
Modifiers:
- Coordination Modifier: +2
- Situational Bonus (Masterwork Shadow-Weave Half Plate in dim light): Advantage
Total: 18 + 2 = 20
Result: 20 >= 14 — Success!

She reached the weathered, wooden wall of the barn's far side, near the overgrown wagon path, unseen and unheard. The arcane thrum was more pronounced here, a subtle vibration that hinted at its detection capabilities. She knelt, producing the tarnished silver bell from her Bag of Holding. Its cold metal felt insignificant, yet its potential for disruption was immense. She positioned it carefully, ready to create a barely audible, intermittent jingle, mimicking a distressed animal or a loose latch, something just compelling enough to draw a professional guard's curiosity without triggering a full alarm.

With a whisper-soft touch, she activated the lure, a single, faint jingle echoing briefly in the still air, then silenced it. A moment later, another. Then silence. She waited, perfectly still, her senses straining, her intellect mapping the expected reactions.

From the farmhouse, after a tense moment, she detected a subtle shift. A window, likely on the second floor, was opened a crack, then closed. A low murmur of voices, too faint to discern words, but conveying a sense of muted inquiry. Then, the distinct sound of a door opening softly, followed by hushed footsteps. One set. Slow, deliberate.

One of the internal guards was responding to the lure.

Nocturne's eyes narrowed, a cold satisfaction blossoming in her chest. The bait had been taken. The first piece of the puzzle was isolating itself. Now, the hunt truly began.

--- PLANNING BLOCK ---
What would you like to do next?
1.  **[AmbushLuredGuard_1]:** Prepare an immediate ambush for the single guard who has emerged, aiming for a silent, decisive takedown.
2.  **[WaitAndObserve_2]:** Remain hidden and observe, waiting to see if the second guard also emerges, or if the first guard returns to the farmhouse.
3.  **[CircleFarmhouseNow_3]:** Use the distraction of the lone guard to quickly circle the farmhouse and identify a new, unguarded entry point.
4.  **[DisableMagicWardNow_4]:** Use this opportunity to focus on disabling the magical ward near the barn while the guard is distracted.

[STATE_UPDATES_PROPOSED]
{
  "player_character_data.current_location": "Hidden at Man Tibbet's Farm (Barn Side, Lure Set)",
  "world_data.npcs.man_tibbet_guard_1": {
    "name": "Man Tibbet's Farm Guard 1",
    "level": 3,
    "hp_current": 25,
    "hp_max": 25,
    "defense": 15,
    "aptitudes": {
      "physique": {"score": 14, "potential_coefficient": 3},
      "coordination": {"score": 14, "potential_coefficient": 3},
      "health": {"score": 12, "potential_coefficient": 2},
      "intelligence": {"score": 10, "potential_coefficient": 2},
      "wisdom": {"score": 12, "potential_coefficient": 2}
    },
    "equipment": ["Dark leather armor", "Shortsword", "Crossbow"],
    "is_hostile": false,
    "is_aware_of_pc": false,
    "current_status": "Investigating Lure, Approaching Barn"
  },
  "world_data.npcs.man_tibbet_guard_2": {
    "name": "Man Tibbet's Farm Guard 2",
    "level": 3,
    "hp_current": 25,
    "hp_max": 25,
    "defense": 15,
    "aptitudes": {
      "physique": {"score": 14, "potential_coefficient": 3},
      "coordination": {"score": 14, "potential_coefficient": 3},
      "health": {"score": 12, "potential_coefficient": 2},
      "intelligence": {"score": 10, "potential_coefficient": 2},
      "wisdom": {"score": 12, "potential_coefficient": 2}
    },
    "equipment": ["Dark leather armor", "Shortsword", "Crossbow"],
    "is_hostile": false,
    "is_aware_of_pc": false,
    "current_status": "Vigilant (within farmhouse)"
  },
  "custom_campaign_state.first_contract.scouting_status": "Man Tibbet's Farm - Lure Active, One Guard Investigating"
}
[END_STATE_UPDATES_PROPOSED]

Player (freeform):
DM note: don't explicitly say big 5 stuff like this. (Conscientiousness 4/5

============================================================
