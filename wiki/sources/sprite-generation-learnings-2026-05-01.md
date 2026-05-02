---
title: "Sprite Generation Learnings (2026-05-01)"
type: source
tags: [sprite-generation, pixel-art, game-dev, comfyui, pollinations, grok]
date: 2026-05-01
source_file: raw/sprite-generation-learnings-2026-05-01.md
---

## Summary
Benchmarked sprite generation pipelines for a 2D RPG game. ComfyUI SDXL (local) is the clear winner for exact size control. Pollinations.ai is the best free option. Grok API ignores size parameters entirely. k-means palette reduction destroys LLM sprite colors.

## Key Claims
- ComfyUI SDXL produces best pixel art at exact 64x64/128x128 with local RTX 4090
- Pollinations.ai generates good 256x256 sprites for free and respects size parameters
- Grok `grok-imagine-image` ignores `image_size` — always returns 1408x768 landscape
- k-means palette reduction destroys LLM sprite colors (92 → 33 colors) because alpha-binarize must happen first
- Battle Brothers is hand-drawn 2D paintings, NOT pixel art — quality bar is unreachable
- Kenney 128x128 sprite packs don't exist — closest available is 80x110 (Platformer Characters)
- Cordon CC0 is the only 128x128 pixel art source available for sci-fi assets
- LLM sprites cannot match hand-drawn pixel art quality — best approach is compositing real LPC + LLM for props
- Animation (8-frame walk cycles) is the hardest part — requires consistent pose across frames

## Key Quotes
> "LLM sprites cannot match hand-drawn pixel art quality" — sprite-generation-learnings
> "Best approach: compositing real pixel art (LPC) + LLM for environment/props" — sprite-generation-learnings
> "Grok ignores image_size parameter - returns 1408x768 always" — Grok pixel art failure notes

## Connections
- [[Pollinations.ai]] — free sprite generation, best no-cost option
- [[ComfyUI SDXL]] — local GPU pipeline, exact size control
- [[Cordon CC0]] — sci-fi sprite library (128x128, 205 PNGs)
- [[Body Parts Pipeline]] — failed approach for pixel art generation
- [[K-means Post-Processing]] — color quantization technique (use with alpha-binarize first)
- [[Vibe Code 2D Game]] — rapid 2D game dev methodology