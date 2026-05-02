---
title: "Texture Atlas"
type: concept
tags: [sprite-optimization, rendering, game-dev]
last_updated: 2026-05-01
---

# Texture Atlas

Optimized sprite packing into single image to reduce draw calls. Critical optimization for games with many sprites.

## Key Properties
- **What:** Single image containing multiple sprites packed efficiently
- **Why matters:** Reduces GPU draw calls from N to 1
- **Packing algorithms:** Grid, MaxRects, Polygon
- **Output formats:** JSON/XML metadata for sprite coordinates

## Tools
- [[TexturePacker]] — 48+ engine presets, CLI for CI/CD
- [[Aseprite]] — built-in sprite sheet export
- [[PixiJS]] — native texture atlas support

## Related Concepts
- [[Sprite Sheet Compositing]] — assembly of parts
- [[Nearest-Neighbor Upscaling]] — pixel-perfect scaling
- [[K-means Post-Processing]] — palette reduction per sprite

## See Also
- [[Pollinations.ai]] — sprite generation source
- [[ComfyUI SDXL]] — local sprite generation