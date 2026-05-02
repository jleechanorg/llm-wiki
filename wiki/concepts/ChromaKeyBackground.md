---
title: "ChromaKeyBackground"
type: concept
tags: [game-dev, sprite-pipeline, image-processing]
sources: []
last_updated: 2026-05-01
---

A background removal technique using exact #00FF00 chroma green. Core enabling technology of the [[SpriteSheetPipeline]].

## Requirements

- Background must be **exact #00FF00** flat green — no shadows, floor, gradients
- Character must **never use green** anywhere: clothing, gems, magic effects, outlines, antialiasing, glow
- If green appears in character, video model will treat it as background and clip it out

## Why Green?

Green is used because human skin doesn't contain green wavelengths, making it easy to separate. #00FF00 specifically (not a range) is required for the Pillow/chroma removal script to work reliably.

## Related

[[SpriteSheetPipeline]], [[PreserveCanvasMode]], [[Kling]]
