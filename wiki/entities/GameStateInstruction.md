---
title: "Game State Instruction"
type: entity
tags: [prompt-file, planning-blocks]
sources: [planning-block-cleanup-dev1314]
last_updated: 2026-04-08
---

Core prompt file defining game state handling and planning block requirements. Updated in dev1314 to remove narrative "--- PLANNING BLOCK ---" delimiters while preserving JSON field requirements.

**Key fields:**
- planning_block: Required JSON field for character options
- story_mode: Player-facing narrative
- god_mode: DM-facing instructions

**Related:** [[MechanicsSystemInstruction]], [[NarrativeSystemInstruction]], [[MasterDirective]]
