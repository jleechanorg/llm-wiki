---
title: "Eternal GM Sprite Generation 2026-05-01"
type: source
tags: [sprite-generation, eternal-gm, ragnarok, pollingations]
date: 2026-05-01
source_file: worldai_claw/assets/eternal_gm_sprites/
---

## Summary
Generated 3 Eternal GM character sprites via Pollinations.ai at 128x128. File sizes 5-6KB suggest moderate detail. CC0 packs also downloaded for reference.

## Generated Sprites
| File | Size | Character |
|------|------|-----------|
| ramsay.png | 5,011 bytes | Dark assassin, hooded, dual daggers |
| frey_guard.png | 5,329 bytes | Medieval soldier, chainmail, halberd |
| wildling_berserker.png | 6,072 bytes | Furry beast race, animal hides, greatsword |

## Prompt Template Used
Ragnarok style pixel art sprite, [character description], 128x128, transparent background, crisp pixel art with smooth shading, 64 colors

## User Recommendations for Higher Quality
From second opinion / parallel teammate research:

### Better Prompts for FLUX/Kontext/Ludo
Base: "High-detail pixel art sprite sheet, 64-128 colors with smooth cel-shading like Ragnarok Online, clean hard edges, transparent background, [character], 8-direction walk cycle, idle, attack, 128x128 per frame"

Consistency: "Use IP-Adapter reference image [upload CC0 base], LoRA trained on campaign style"

Palette: "Restrict to 64-128 color palette with smooth shading, retro pixel art but higher fidelity than 16-color"

### Top CC0 Packs for Reference
1. Anokolisa Sidescroller Fantasy Forest Pack (itch.io) - 600+ sprites
2. Wyrmsun CC0 (opengameart) - 900+ items
3. Memao Fantasy Characters (itch.io) - 10+ animated characters, 16-32px

## Next Steps
1. Combine Pollinations output with CC0 base sprites
2. Apply k-means palette quantization (k=32-64)
3. Test silhouette extraction on generated sprites
4. Build sprite sheets with 8-frame walk cycles