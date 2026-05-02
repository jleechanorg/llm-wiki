---
title: "PreserveCanvasMode"
type: concept
tags: [game-dev, sprite-pipeline, image-processing]
sources: []
last_updated: 2026-05-01
---

A critical setting in the [[SpriteSheetPipeline]] animation_pipeline.py script. Instead of cropping/recenter each frame individually, it scales the **entire fixed video camera canvas** into each 256×256 cell.

## Why It Matters

Per-frame cropping/recenter creates **fake camera movement** — each cell shows a slightly different framing, making the animation feel like it's zooming/panning. Preserve-canvas mode uses the fixed video camera as the cell boundary, keeping all frames consistent.

## The Rule

If the source video drifts (character not centered in some frames), fix the video prompt (regenerate with locked camera) — do NOT repair by shifting individual cells.

## Output Dimensions

- 12 frames → 3072×256 (12 × 256)
- 24 frames → 6144×256 (24 × 256)

## Related

[[SpriteSheetPipeline]], [[ChromaKeyBackground]], [[Kling]]
