---
title: "Kling"
type: entity
tags: [ai, video-model, game-dev]
sources: []
last_updated: 2026-05-01
---

AI video generation model used as the animation engine in the [[SpriteSheetPipeline]]. The Kling model receives a chroma-green first frame from an image model (GPT Image 2 or Nano Banana 2) and generates motion video. Key to solving the leg/motion problem that image models fail on.

**Why Kling:** Understands walking/running mechanics inherently — image models cannot reliably draw frame-perfect leg positions, but video models animate them correctly because they model motion, not static poses.

**Related:** [[LayrKits]], [[SpriteSheetPipeline]], [[ChromaKeyBackground]]
