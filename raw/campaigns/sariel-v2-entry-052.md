---
title: "Sariel V2 — Scene 052"
type: source
tags: [campaign, scene, sariel-v2]
last_updated: 2026-04-12
scene_number: 52
scene_total: 252
source_file: /tmp/campaign_downloads_v2/
---

## Scene 052 Summary

============================================================ Game Master: [Mode: DM MODE] Understood. You have provided a `GOD MODE:` command to "wait nevermind, lets make it a day after." This directly overrides your previous approval for the one-year time skip in `SEQ_ID: 110`.  I acknowledge this directive. I will immediately revert the campaign state to reflect the original "day after" timeline, as previously established in `SEQ_ID: 1` and `SEQ_ID: 6`. This means:  *   **Timeline:** The camp

## Key Details

- **Word count:** 424
- **Campaign:** [[Sariel V2]]
- **Entry:** [[sariel-v2-entry-052]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]
Understood. You have provided a `GOD MODE:` command to "wait nevermind, lets make it a day after." This directly overrides your previous approval for the one-year time skip in `SEQ_ID: 110`.

I acknowledge this directive. I will immediately revert the campaign state to reflect the original "day after" timeline, as previously established in `SEQ_ID: 1` and `SEQ_ID: 6`. This means:

*   **Timeline:** The campaign remains on **Kythorn, Day 2, Year 11 of the New Peace**, the day after the Battle of the Sacrifice Fields and Alexiel's death.
*   **Character Ages:** All character ages will revert to their original "day after" values. Sariel will be 15, Cassian and Valerius 18, and Cressida and Rowan 16.
*   **Physical Manifestation of Trauma:** Sariel's ear will be freshly bandaged, reflecting the immediate aftermath of her trauma.
*   **Narrative Context:** The narrative will maintain the raw, immediate grief and shock of the previous day's events.

The following `STATE_UPDATES_PROPOSED` block will revert the game state to reflect these canonical decisions:

```
[STATE_UPDATES_PROPOSED]
{
  "player_character_data": {
    "age": 15,
    "backstory_summary": "Daughter of the legendary Alexiel and Prince Artorius. At age 15, she was kidnapped by the warlord Mordan. Under duress from torture, she revealed the secret of her mother's absolute moral vow to protect children. She then witnessed Mordan use this information to trap her mother, forcing Alexiel to sacrifice her own life to stop a demonic ritual and save Sariel. She is now consumed by guilt, believing her weakness directly caused her mother's death."
  },
  "npc_data": {
    "Cassian Arcanus": {
      "age": 18
    },
    "Valerius Arcanus": {
      "age": 18
    },
    "Cressida Valeriana": {
      "age": 16
    },
    "Rowan Thorne": {
      "age": 16
    }
  },
  "world_data": {
    "world_time": {
      "year": 11
    }
  },
  "custom_campaign_state": {
    "premise": "The day after her legendary mother sacrificed herself to save her, Sariel Arcanus must navigate a web of grief, guilt, and political intrigue, all while bearing the secret that she was the one who broke under torture and revealed the weakness that led to her mother's death."
  }
}
[END_STATE_UPDATES_PROPOSED]
```
**Explanation:** This `STATE_UPDATES_PROPOSED` block reverts the changes from `SEQ_ID: 110` and establishes the campaign's timeline to be "the day after" Alexiel's death, with Sariel at age 15 and all other affected NPCs at their corresponding ages.

Once this update is processed, I will resume the story at the exact point where we left off, with Sariel inside Sergeant Kaelan's cell, and present the `PLANNING BLOCK` with the correct `[CHOICE_ID]` format.

Please confirm by responding: `CONFIRM REVERT`.

God Mode:
CONFIRM REVERT

============================================================
