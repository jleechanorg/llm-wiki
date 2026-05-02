---
title: "WorldAI Claw Sprite Generation Pipeline"
type: source
tags: [sprite-generation, pixel-art, llm, game-dev]
date: 2026-04-30
source_file: docs/evidence/testing_ui/2026-04-30-llm-game-sprites/test_sprite_llm_game_sprites.py
---

## Summary

WorldAI Claw's sprite generation pipeline combines LLM image generation (Grok, Pollinations), CC0 asset libraries (LPC, Kenney), K-means color quantization, and parametric body part generation to produce game-ready 64×64 pixel art sprites with walk cycle animations.

## Key Claims

1. **Grok `grok-imagine-image` ignores `image_size` param** — Always returns 1408×768 (16:9 landscape), never the requested 1024×1024 square. Makes single-image full-body generation unsuitable for sprite grids without post-cropping.

2. **Grok `grok-2` model not available** — Team endpoint (`f8bd23e4-3467-40de-abb9-c6322209db34`) returns 404 "model does not exist or your team does not have access to it."

3. **Pollinations AI is free fallback** — `image.pollinations.ai` accepts prompts and returns square 512×512 images. No API key needed. HTTP 200 confirmed.

4. **K-means with alpha-binarize BEFORE clustering** — Prevents background colors from bleeding into sprite edges during quantization. Rescues 11/12 archetypes at 64×64, k=32.

5. **2x Nearest-Neighbor upscale fixes thin sprites** — LPC parts at native 64×64 have 1px line weights. 2x NN upscale doubles line weight to 2px, matching AI-generated detail density.

6. **Canvas silhouette extraction is viable** — Prompt with high-contrast background (lime green), flood-fill corners to set alpha=0, binarize alpha BEFORE K-means.

## Key Quotes

> "Grok `grok-imagine-image` ignores pixel-art prompts. Replicate `pixel-art-xl` is the gold standard for pixel art, excels at sci-fi armor and organic monsters. Mandatory: downscale by exactly 8x with Nearest Neighbor for pixel-perfect grid." — Second Opinion (AI Universe, 2026-04-28)

> "Hybrid approach wins for sci-fi + monster: Kenney CC0 as foundation + AI texture overlays on procedural silhouettes. Preserves 100% transparency compatibility." — Second Opinion (AI Universe, 2026-04-28)

> "Alpha-binarize BEFORE KMeans prevents background colors from bleeding into sprite edges during clustering." — Memory record (wc-od5, 2026-04-27)

## Sprite Generation Pipeline

```
LLM Generation (Grok/Pollinations)
  ↓
Corner Background Removal (threshold=30)
  ↓
Smart Crop (content bounds + 8% padding)
  ↓
Nearest-Neighbor Resize → 64×64
  ↓
K-means Quantization (k=24, 15 iterations)
  ↓
Game-Ready Sprite (64×64, RGBA, pixel-art palette)
```

## Character Types Generated

| Character | Style | Key Features |
|-----------|-------|-------------|
| Crimson Assassin | Dark fantasy | Hooded, red eyes, crimson cloak, twin daggers |
| Astral Mage | High fantasy | Wizard hat with stars, constellation robes, crystal staff |
| Steam Juggernaut | Steampunk | Brass mechanical armor, LED eyes, steam vents |
| Forest Druid | Nature fantasy | Antler crown, mossy tunic, vine-wrapped staff |

## Asset Libraries Used

- **LPC (Liberated Pixel Cup)** — CC0 spritesheets, 576×256 PNG = 9 cols × 4 rows of 64×64 cells. Row=direction (S/W/N/E), col=animation frame (0-8).
- **Kenney** — 255 PNGs (Monster Builder 180, Simple Space 4, Mini Dungeon 28, Modular Dungeon 43). Default/Double/Retina subdirs are duplicates, removed.
- **Pollinations** — Free AI image generation, free alternative to Grok.

## Walk Cycle Animation

8-frame walk cycle with body bob and leg swing per frame:

| Frame | Body bob | Left leg | Right leg |
|-------|----------|----------|-----------|
| 0 | 0 | -1 | +2 |
| 1 | -1 | -2 | +3 |
| 2 | 0 | -1 | +1 |
| 3 | +1 | 0 | -1 |
| 4 | 0 | +2 | -2 |
| 5 | -1 | +3 | -2 |
| 6 | 0 | +1 | -1 |
| 7 | +1 | -1 | 0 |

## Connections

- [[ParametricBodyPartGenerator]] — Procedural body part generation (head, body, arms, legs) from parameters
- [[LPCSpriteComposer]] — Fetches LPC CC0 spritesheets, composites head/body/arms/legs/feet
- [[GrokSpritePartGenerator]] — LLM-based sprite part generation via Grok API
- [[K-means Post-Processing]] — Color quantization for pixel-art palette consistency
- [[Pollinations Fallback]] — Free AI image generation when Grok unavailable
- [[Canvas Silhouette Extraction]] — Background removal via corner sampling + alpha threshold
