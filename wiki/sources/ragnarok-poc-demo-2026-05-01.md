---
title: "Ragnarok POC Demo Created 2026-05-01"
type: source
tags: [sprite-generation, ragnarok, poc, demo, lpc, cordon]
date: 2026-05-01
source_file: ragnarok_poc.html
---

## Summary
Created ragnarok_poc.html proof-of-concept demo matching 2D top-down Ragnarok style. Uses LPC body-part compositing for real 8-frame walk animation. Validated against real Ragnarok reference frames.

## Features Implemented
- 2D top-down view
- 8-frame walk animation via LPC body-part compositing
- Ground shadow beneath characters
- WASD + Shift sprint controls
- Camera follows player
- Tile-based map with Cordon tiles
- NPC interaction (press E for dialogue)
- Collision detection

## Technical Details
- Source: LPC sprite sheets for body parts
- Compositing: z-order BEHIND -> BELT -> BODY -> LEGS -> FEET -> HANDS -> TORSO -> HEAD
- Scale: 64x64 source scaled 2x to 128x128 display
- Frame diff: 21,632 pixels (confirmed via /er validation)

## Comparison to Real Ragnarok
- Approach: CORRECT (2D top-down sprite-based)
- Animation: MATCH (8-frame walk cycle)
- Shadow: MATCH (ground ellipse)
- Sprite quality: More retro (limited palette vs rich shading)

## Files
- /ragnarok_poc.html
- /docs/evidence/ragnarok_reference/2d_classic/ (reference frames)