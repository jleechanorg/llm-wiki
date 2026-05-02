---
title: "Body Parts Pipeline Sprite Generation - Failure Analysis"
type: source
tags: [sprite-generation, body-parts, pixel-art, pollingations, kmeans, failure-analysis]
date: 2026-05-01
source_file: testing_ui/generate_10_sprites_pol.py
---

## Summary

Attempted to generate 10 game sprites via a body-parts pipeline using Pollinations AI (free) + Grok fallback. The pipeline generated parts (head, body, arms, legs) separately and composited them into 128x128 sprites. The results were visually poor — composite sprites had washed-out gray/blue colors, misaligned anatomy, and no coherent character silhouette.

## Key Claims

1. **Pollinations AI ignores pixel art prompts** — Despite including "16-bit pixel art RPG", "SNES Chrono Trigger style" in prompts, Pollinations generates generic AI art with smooth gradients and anti-aliasing, not pixel art.

2. **K-means quantization destroys pixel art** — Applying k-means (k=32) AFTER corner background removal washes all colors to similar gray-blue tones. The crisp pixel art palette becomes mud.

3. **Corner background removal fails for AI art** — Unlike photography or clean renders, AI-generated images have soft edges and inconsistent corner colors. Corner sampling produces wrong background estimates, making the alpha cut worthless.

4. **Fixed-position compositing doesn't work** — Parts are placed at arbitrary y-positions (head at y=4, body at y=36) that don't align into proper anatomy. Parts don't overlap correctly to form a character.

5. **Original full-body LLM sprites look better** — The original Crimson_Assassin_128.png has 6,988 opaque pixels with rich crimson colors (RGB[91 16 33]). The composite had 5,242 opaque pixels with gray-blue colors (RGB[54 55 72]).

6. **Grok body parts also failed** — The team agents generated body parts via Grok's grok-imagine-image model, but the parts arrived as malformed floating figures, not pixel art sprites.

## What Worked

- **Full-body LLM generation** (not body parts) — Grok generates complete character sprites that look coherent, even if not pixel art
- **Cordon CC0 assets** — 205 sci-fi sprites at 128x128, directly usable
- **Pollinations for tiles/backgrounds** — Free, 512x512, works for non-character assets

## What Failed

- Body-parts generation via Pollinations (ignores pixel art prompts)
- Body-parts generation via Grok (malformed figures)
- K-means post-processing on AI-generated art
- Corner background removal on non-photography sources
- Fixed-position canvas compositing

## Key Metrics

| Metric | Original LLM Sprite | Body-Parts Composite |
|--------|---------------------|----------------------|
| Opaque pixels | 6,988 | 5,242 |
| Unique colors | 92 | 33 |
| Color richness | RGB[91,16,33] crimson | RGB[54,55,72] gray-blue |
| Visual quality | Decent (full body) | Poor (mismatched parts) |

## Connections
- [[K-means Post-Processing]] — k-means works on photography, fails on AI art
- [[parametric-body-part-generator]] — parametric approach may work better than LLM for body parts
- [[Pollinations AI]] — free image generation, ignores style prompts

## Lessons Learned

1. **Verify visual output automatically** — Never assume generation succeeded; always view and score the result
2. **Pixel art requires pixel art models** — General AI image generators produce smooth gradients, not crisp pixels
3. **Body parts pipeline needs validation** — Each part must be checked for quality before compositing
4. **Composite quality ≠ sum of parts** — Parts that look okay individually may not form coherent whole

## Evidence Artifacts

- `/tmp/sprite_parts/batch1/Cyber_Ninja/` — 4 body parts (head, body, arms, legs)
- `/tmp/sprite_parts/full/Cyber_Ninja_full.png` — Composite result (128x128, washed out)
- Original: `docs/evidence/testing_ui/2026-04-30-llm-game-sprites/Crimson_Assassin_128.png`