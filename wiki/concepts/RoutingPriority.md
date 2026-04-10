---
title: "Routing Priority"
type: concept
tags: [routing, priority, modal, state-machine]
sources: ["level-up-modal-routing-scenarios"]
last_updated: 2026-04-08
---

A system for resolving conflicts when multiple modal agents could be activated simultaneously. Uses hierarchical priority levels to ensure correct modal display.


## Priority Levels (highest to lowest)
1. **1_modal_character_creation** — CharacterCreationAgent
2. **3_modal_level_up** — LevelUpAgent
3. Other priorities...

## Override Behavior
Higher-priority states can override lower-priority ones (e.g., in_progress flags override pending flags).
