---
title: "Pause Menu Mode"
type: concept
tags: [game-design, character-creation, time-freeze]
sources: ["character-creation-level-up-mode"]
last_updated: 2026-04-08
---

Game design pattern where certain modes (like character creation) operate in a time-frozen state. The world pauses while the player focuses on building/editing. Time resumes from exactly where it stopped when the player exits.

## Application in WorldArchitect
- Character creation freezes world time
- No narrative events occur
- No NPC actions or reactions
- No combat or encounters
- Player returns to exact story state upon exit
