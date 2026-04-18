---
title: "spriteGenerator.ts - Grokmage LLM Sprite Service"
type: source
tags: [backend, sprites, grok-api, llm-generation, 16-bit, chrono-trigger]
date: 2026-04-16
source_file: packages/backend/src/services/spriteGenerator.ts
---

## Summary
spriteGenerator.ts provides LLM-powered 16-bit sprite generation using the Grok image generation API (x.ai). It generates Chrono Trigger-style pixel art sprites with animations, directional variants, and consistent color palettes. Follows worldai_claw CLAUDE.md pattern using `AI_UNIV_GROK_KEY` environment variable.

## Key Claims
- Uses Grok API at `https://api.x.ai/v1/images/generations` with `grok-imagine-image` model
- Supports character types: knight, mage, rogue, beast, boss, npc
- Animation types: idle, walk, attack, magic, hurt, death
- Pre-defined color palettes inspired by Chrono Trigger SNES sprites
- Sprite caching system to avoid redundant API calls
- Configurable sizes: tiny (16x16), small (24x32), medium (32x48), large (48x64)

## Key Quotes
> "Generates Chrono Trigger-level 16-bit pixel art sprites using Grok image generation API" — module docstring

> "Follows worldai_claw CLAUDE.md: must use real LLM API calls, NOT direct OpenAI keys" — module docstring

> "Use x.ai API (not api.grok.com) - model is grok-imagine-image" — inline comment

## Connections
- [[spritesheet-ts]] — Procedural fallback when LLM generation unavailable
- [[SpriteGenerationSystem]] — Both are part of the dual sprite system
- [[GrokImageAPIIntegrationForGameAssets]] — API integration details
- [[ChronoTriggerStyleSpriteSheets]] — Target art style
