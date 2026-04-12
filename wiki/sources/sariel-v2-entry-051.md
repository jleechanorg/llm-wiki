---
title: "Sariel V2 — Scene 051"
type: source
tags: [campaign, scene, sariel-v2]
last_updated: 2026-04-12
scene_number: 51
scene_total: 252
source_file: /tmp/campaign_downloads_v2/
---

## Scene 051 Summary

============================================================ Game Master: [Mode: DM MODE] Understood. You have provided a `DM Note` with a critical instruction: "retcon my bandaged ear. it's been a year since alexiel died now, not one day after."  I acknowledge this directive. This is a major retcon that directly contradicts our previously established and confirmed campaign start point (Kythorn 2, Year 11 of the New Peace, the day after Alexiel's death, as confirmed in `SEQ_ID: 5` and `SEQ_ID: 6

## Key Details

- **Word count:** 549
- **Campaign:** [[Sariel V2]]
- **Entry:** [[sariel-v2-entry-051]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]
Understood. You have provided a `DM Note` with a critical instruction: "retcon my bandaged ear. it's been a year since alexiel died now, not one day after."

I acknowledge this directive. This is a major retcon that directly contradicts our previously established and confirmed campaign start point (Kythorn 2, Year 11 of the New Peace, the day after Alexiel's death, as confirmed in `SEQ_ID: 5` and `SEQ_ID: 6`).

**Conflict:** The immediate "day after" premise of the campaign and Sariel's fresh wound directly conflicts with the new directive for "one year later."

**Proposed Resolution:**
I propose we implement this change as a major retcon. This means:

1.  **Timeline Shift:** The campaign will now be considered to have begun **one year after** Alexiel's death.
    *   Current `world_time` will advance to `Year 12 of the New Peace`.
    *   All current events will be understood to have transpired over that intervening year.
2.  **Character Age Adjustments:**
    *   Sariel's age: 15 -> **16**
    *   Twins' age (Cassian, Valerius): 18 -> **19**
    *   Cressida's age: 16 -> **17**
    *   Rowan's age: 16 -> **17**
    *   Gideon's age remains 25 (his character dossier defines him as older and already in the Starfall Guard before Alexiel's death, so this age difference is consistent with his background as a veteran).
3.  **Physical Manifestation of Trauma:** Sariel's bandaged ear will now be a **healed scar**, signifying a year has passed since the physical trauma, though the emotional and psychological wounds remain.
4.  **Narrative Recontextualization:**
    *   Sariel's grief will be understood as having persisted intensely over the year, perhaps even deepening due to isolation and the court's judgment.
    *   Her initial confrontations with Cassian and Valerius (as narrated in previous turns) will be recontextualized as interactions that have occurred over this past year, shaping her isolation.
    *   Her research into her mother's life and the Null Genesis Project, and her discovery of the "Joyful Predator" trait, will be understood as dedicated work she has undertaken throughout this year.
    *   The current scene in the Archives with Kantos, and the encounter with the Silent Guard, now takes place after this year of intense personal struggle and hidden research. Her physical exhaustion is from the psychic backlash, not from the immediate trauma of the previous day.

This significant change will require a formal `STATE_UPDATES_PROPOSED` block to update all relevant character ages and the campaign premise.

**Please confirm:** Do you approve this major retcon, including the timeline shift, character age adjustments, and narrative recontextualization? Once approved, I will implement it and resume the story.

[STATE_UPDATES_PROPOSED]
{
  "player_character_data": {
    "age": 16
  },
  "npc_data": {
    "Cassian Arcanus": {
      "age": 19
    },
    "Valerius Arcanus": {
      "age": 19
    },
    "Cressida Valeriana": {
      "age": 17
    },
    "Rowan Thorne": {
      "age": 17
    }
  },
  "world_data": {
    "world_time": {
      "year": 12
    }
  },
  "custom_campaign_state": {
    "premise": "One year after her legendary mother sacrificed herself to save her, Sariel Arcanus continues to navigate a web of grief, guilt, and political intrigue, all while bearing the secret that she was the one who broke under torture and revealed the weakness that led to her mother's death. Her research into this past year has led her to terrifying new truths about her lineage."
  }
}
[END_STATE_UPDATES_PROPOSED]

God Mode:
wait nevermind, lets make it a day after

============================================================
