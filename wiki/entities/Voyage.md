---
title: "Voyage — AI-narrated RPG platform"
type: entity
tags: [platform, ai-rpg, playtest]
sources: [2026-08-04-bg3-voyage-campaign-summary]
last_updated: 2026-08-04
---

# Voyage

AI-narrated RPG platform on which the player ran the 107-turn [[NocturneSosuke]] campaign ([[2026-08-04-bg3-voyage-campaign-summary]]), using a community scenario set in [[BaldursGate]] after the events of Baldur's Gate 3. Sibling platform to the [[ChatGPT]]/[[Gemini]] DM lineage used in the Aizen campaigns and to [[AIDungeon]].

## Player evaluation (2026-08-04)

- **Verdict**: "night and day difference" better than [[AIDungeon]].
- **Bugs**: leveling up, ability points, occasional combat/narrative misses — all recoverable via [[NarratorBugCorrection]].
- **Biggest gap**: the [[Worldsmith]] world builder "needs a huge revamp" — slow and opaque about what it is doing.

## Observed engine features

- Modified 5e/BG3 framework with [[TieredSuccessOutcomes]] and [[DynamicSituationalModifiers]].
- [[ConsequenceEnforcement]]: the engine disrupts player commands based on ambient fiction state instead of always complying.
- Backend UI tags in raw logs: `w_user`, `w_open_book`, `w_gear`, `w_globe`, `w_comment`, `w_mute`, `w_group` (party tracking).
