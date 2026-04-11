---
title: "Spicy Mode: Literary Intimate Content System Instruction"
type: source
tags: [game-mechanic, content-rating, narrative-system, worldarchitect]
source_file: "raw/spicy-mode-literary-intimate-content-system-instruction.md"
sources: []
last_updated: 2026-04-08
---

## Summary
System instruction document for handling romantic and intimate scenes in the WorldArchitect.AI game system. Provides dual-mode content approach: full literary erotic writing when Spicy Mode is enabled, and tasteful fade-to-black when disabled with periodic suggestions to enable.

## Key Claims
- **Dual-Mode System**: Spicy Mode enabled produces explicit content; disabled provides romantic tension with fade-to-black
- **Suggestion Frequency**: When disabled, suggest enabling once every 10 turns (`turn_number % 10 == 0`)
- **Literary Standards**: Writing should match published literary fiction with emotional weight and character development
- **Core Pillars**: Character-driven intimacy, sensory immersion, and narrative integration
- **Four-Stage Pacing**: The Approach → The Threshold → The Exploration → The Resolution

## Key Techniques
- **Sensory Immersion**: Engage all five senses with specific, concrete details
- **Dialogue Integration**: Characters speak naturally; dialogue reveals desire and vulnerability
- **Consent Framework**: All intimate content must be clearly consensual; respect player agency

## Scene Conclusion
- Set `recommend_exit_spicy_mode: true` when: intimate encounter completes, characters transition to post-intimate conversation, or scene shifts to non-intimate activities

## Connections
- Related to [[Settings Page - AI Provider Selection]] content settings
- [[NPC Relationship Trust System]] affects character dynamics that inform intimate scene writing
