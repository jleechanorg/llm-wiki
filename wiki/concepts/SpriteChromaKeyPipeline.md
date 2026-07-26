---
title: "SpriteChromaKeyPipeline"
type: concept
tags: [dk2d-chrono]
date: 2026-07-14
last_updated: 2026-07-14
---

Two adversarial defects in generate-then-key sprite pipelines: (1) image models bake "translucency" (smoke, shadow) as literal RGB blends WITH their own background color — no real alpha, so no fixed-radius chroma tolerance separates it; use a hue-FAMILY channel test (for magenta: G clearly below both R and B, R≈B) validated against sampled colors; (2) palette quantization (PIL median-cut) applied AFTER keying can remap edge pixels back onto keyed-family palette entries — key BEFORE quantize and apply the family test again on the FINAL shipped bytes, verified at zoom. Numeric pre-quantize checks passed while shipped pixels were still magenta.

Source: [[feedback-2026-07-14-dk2d-chrono-operational-lessons]] · Related: [[chrono-trigger-style-sprite-sheets]]
