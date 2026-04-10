---
title: "Planning Block Normalization"
type: concept
tags: [worldarchitect, data-processing, game-state]
sources: []
last_updated: 2026-04-08
---

The process of converting planning_block choices from dict format (key-value pairs) to list format with unique identifiers. Handles multiple edge cases:

- String-valued choices → converted to dict with text/description fields
- Missing IDs → auto-generated from choice text (lowercased, underscores, 30-char max)
- ID collisions → retry with numeric suffix (up to 1000 attempts)
- Malformed JSON/None values → graceful fallback to empty dict

Used to standardize choice format across the game state system.
