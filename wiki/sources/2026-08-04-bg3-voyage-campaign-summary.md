---
title: "BG3 Voyage campaign — Nocturne Sosuke playtest: 107-turn soul-harvest run with platform feedback"
type: source
tags: [campaign, voyage, bg3, dnd-5e, playtest, platform-feedback, sosuke, soul-consumption]
sources: [2026-08-04-bg3-voyage-campaign-summary]
last_updated: 2026-08-04
---

# BG3 Voyage Campaign Summary — Nocturne Sosuke

**Source**: Player writeup + statistical ledger of a 107-turn campaign run on the [[Voyage]] platform, using a community scenario set in [[BaldursGate]] after the events of Baldur's Gate 3 ([reddit scenario post](https://www.reddit.com/r/Voyage/comments/1sv5uig/voyage_scenario_bg3_after_the_events_of_the_game/)). This is both a **campaign record** and a **platform evaluation** — the player compares Voyage favorably against [[AIDungeon]] ("night and day difference") while flagging concrete defects.

## Platform feedback (the load-bearing part)

- **Verdict**: Dramatically better than AI Dungeon overall.
- **Bugs observed**: leveling up, ability points, occasional "weird combat or narrative misses" — all recoverable via [[NarratorBugCorrection]] (asking the narrator to fix state in-fiction).
- **Biggest gap**: the world builder needs "a huge revamp." The player used [[Worldsmith]] (`pr-9837.preview.voyage.io/worldsmith?worldId=21869`) — "a step in the right direction but it is slow and doesn't provide enough visibility into what it's doing."

## Campaign shape

- **107 recorded turns** (Turn 0: Nocturne declares intent to raid the Grove → Turn 106: Githyanki vanguard enters the Devil's Ribs bottleneck).
- Inputs formatted as `Nocturne Sosuke: [action]`; backend UI tags visible in the raw log (`w_user`, `w_open_book`, `w_gear`, `w_globe`, `w_comment`, `w_mute`, `w_group` for party tracking).
- **Party roster**: Vaelith, Gloomstalker 2, Gloomstalker 3, [[Shadowheart]], [[Minthara]].

## System mechanics

- Heavily modified 5e/BG3 framework with [[TieredSuccessOutcomes]] ("Basic Success", "Mixed Results", "Success", "Great Success").
- Epic-tier attribute scaling: Charisma +24, Persuasion +25, Intelligence +12.
- [[DynamicSituationalModifiers]]: contextual bonuses/penalties applied mathematically (Distracted Enemy +6, Elite Drow Support +10, Recent Success +13, High-stakes Combat −7, etc.).
- [[ConsequenceEnforcement]]: Nocturne's own ink cloud caused allied Shadow Stalkers to take friendly fire from Asharak and Zevlor; Shadowheart's artifact's "psychic static" garbled a telepathic assassination command against Zevlor — the engine disrupts player commands based on ambient conditions rather than always complying.

## Protagonist: [[NocturneSosuke]]

Half-Elf with infernal/abyssal bloodline (wings, horns), patron **[[Malacharet]]** ("Mother"). Titles: Arch Shadow Druid of the True Winter, Voice of the Purified Grove, Sovereign of the Shattered Rose. Another member of the player's recurring Sosuke lineage (see [[house-sosuke]], [[SosukeAizen]]) — and the same predator-ascension arc as the Aizen god campaign: [[SoulEssenceHarvesting]] of powerful entities to graft their magic and divine sparks.

**Harvested souls**: [[WyllRavengard]] (spark siphoned after Dror Ragzlin slew him), [[DrorRagzlin]] (martial essence extracted while thorn-bound), [[PriestessGut]] (psychic energy unraveled, desiccated to a husk), [[LarinnaDuskweaver]] (essence drawn, rapid magical aging).

**Acquired abilities**: Abyssal Performance / Siren's Leverage (morality-blurring seductive performance), Fatal Seduction (mind-shattering hypnotic gaze).

## Relation to the wiki

This is the first source documenting the **Voyage** platform (sibling to the [[ChatGPT]]→[[Gemini]] DM-handoff lineage in the Aizen campaigns). The soul-consumption mechanic is the same player pattern captured in [[DivineAscensionByConsumption]] and [[Divine-Portfolio-Consumption]] — consumption-based power accretion is a stable preference across platforms and characters.
