---
title: "Dice Notation"
type: concept
tags: [dnd, dice, game-mechanics]
sources: [equipment-display-inventory-formatting-utilities]
last_updated: 2026-04-08
---

## Definition
Standard D&D dice notation pattern `\b\d*d\d+(?:\s*[+-]\s*\d+)?\b` matching expressions like 2d6+1, 1d8-2, 3d4.
## Structure
- Count (optional, defaults to 1): number of dice
- Die type: d4, d6, d8, d10, d12, d20
- Modifier (optional): + or - followed by integer
## Usage
Used in equipment-display to detect stat suffixes like "Dagger (1d4)" or "Rope (50 feet)" and parse them for display.
