---
title: "K-means Post-Processing for Pixel Art"
type: concept
tags: [sprite-generation, pixel-art, k-means, color-quantization]
date: 2026-04-27
---

## Summary

K-means color quantization is used to reduce AI-generated sprites to a pixel-art-consistent palette (typically k=24 or k=32 colors). Critical insight: alpha-binarize BEFORE K-means clustering to prevent background colors from bleeding into sprite edges during quantization.

## Pipeline

```
1. Binarize alpha channel (alpha > 10 → 255, else 0)
2. Separate opaque and transparent pixels
3. Run k-means on RGB of opaque pixels only
4. Map each opaque pixel to nearest centroid
5. Preserve transparent pixels (alpha=0)
```

## Critical Requirement

**Alpha-binarize BEFORE K-means**: Without this, background colors near the sprite edge (that weren't fully removed by corner sampling) get clustered and averaged with foreground colors, causing:
- Ghost halos around sprites
- Background colors bleeding into sprite edges
- Loss of crisp pixel-art silhouettes

## Validation Results

At k=32, 64×64 resolution:
- 11/12 archetypes survive alpha-binarize+KMeans intact
- 1/12 (Senator/Mage) fails due to upstream Grok generation issue (magic swirls instead of character body)

## Implementation Notes

- Random seed (42) for reproducible centroids
- 15-20 iterations per run
- Minimum cluster size check: if cluster too small, keep original color
- k=24 for 64×64 sprites (smaller palette = more pixel-art look)
- k=32 for 128×128 sprites
