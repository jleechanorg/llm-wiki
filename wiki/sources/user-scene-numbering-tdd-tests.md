---
title: "User Scene Numbering TDD Tests"
type: source
tags: [testing, tdd, scene-numbering, turn-counter, game-state, bug-fix]
source_file: "raw/test_user_scene_numbering.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test validating that user-facing scene numbers (user_scene_number) only increment for AI (Gemini) responses, not user inputs. Addresses the "increment-by-2" bug where scene numbers would appear to skip values.

## Key Claims
- **Scene Numbering**: user_scene_number only increments for Gemini responses, user inputs receive None
- **Sequence ID**: sequence_id increments for ALL entries as absolute position identifier
- **Bug Fix**: This prevents the display issue where scene numbers skip values
- **Terminology**: turn_number counts all story entries; user_scene_number is user-facing

## Key Quotes
> "user_scene_number: User-facing 'Scene #X' counter. ONLY increments for AI (Gemini) responses." — code documentation

> "Key relationship (approximate, assumes alternating user/AI): user_scene_number ≈ story_entry_count / 2" — code documentation

## Connections
- [[SceneNumbering]] — concept of tracking player-visible scene progression
- [[TurnCounter]] — internal counter for all story entries
- [[StoryEntry]] — individual entries in the game's story array

## Contradictions
- None identified
