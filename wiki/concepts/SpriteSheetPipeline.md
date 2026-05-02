---
title: "SpriteSheetPipeline"
type: concept
tags: [game-dev, sprite-pipeline, ai-pipeline, computer-graphics]
sources: []
last_updated: 2026-05-01
---

The complete 9-step pipeline for creating game-ready 2D sprite sheets using AI, documented by [[LayrKits]].

## Pipeline Steps

1. **Create first pose** — Image model (GPT Image 2 or Nano Banana 2) generates a full-body character on exact #00FF00 chroma green background
2. **Animate in Kling** — Video model animates the pose into a motion clip, locked camera
3. **Extract frames** — FFmpeg extracts full-resolution PNG frames
4. **Visual review** — Contact sheet + frame selection (12 or 24 frames)
5. **Matte background** — Fallback for non-chroma backgrounds
6. **Chroma removal + sprite sheet** — Python/Pillow removes #00FF00, builds 256×256 cell sheet
7. **Validation** — Sheet dimensions, stability, clipping checks
8. **Preview gallery** — JavaScript manifest + static HTML sprite viewer
9. **Cleanup** — Stage temp files

## Key Insight

Video models understand motion and leg mechanics in a way image models don't. Extract frames from AI-generated video → process into sprite sheets locally.

**Related:** [[LayrKits]], [[Kling]], [[ChromaKeyBackground]], [[PreserveCanvasMode]]
