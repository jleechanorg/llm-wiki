---
title: "ComfyUI Pixel Sprite Analysis 2026-05-01"
type: source
tags: [sprite-generation, pixel-art, comfyui, analysis]
date: 2026-05-01
source_file: comfyui_output_analysis
---

## Summary
ComfyUI pixel_icon_v1 LoRA produces HARD-EDGE PIXEL ART (confirmed via visual inspection). Berserker sprite has highest edge score (60.54). However, sprites still have 4,500-6,300 unique colors (too many for true limited palette). Need k-means post-processing (k=24-64) to achieve Ragnarok-quality shading.

## Sprite Analysis
| Sprite | Size | Mode | Unique Colors | Edge Score |
|--------|------|------|---------------|------------|
| assassin_00001_.png | 128x128 | RGB | 6,150 | 51.32 |
| soldier_00001_.png | 128x128 | RGB | 4,574 | 56.86 |
| berserker_00001_.png | 128x128 | RGB | 6,265 | 60.54 |
| pixel_lora_test_00001_.png | 128x128 | RGB | 4,515 | 41.86 |

## Edge Score Interpretation
- Higher = more hard edges (pixel art)
- Berserker: 60.54 (best pixel art characteristics)
- Pixel_icon_v1 produces TRUE pixel art (confirmed by visual inspection)

## Issues
1. All sprites are RGB mode (no alpha) - black background
2. Too many unique colors (4,500-6,300) - should be <256 for pixel art
3. Need alpha background removal + k-means palette reduction

## Required Post-Processing
1. Alpha background removal (quadruple 0-tolerance)
2. K-means palette reduction (k=32-64)
3. Nearest-neighbor upscaling

## Next Steps
- Add k-means post-processing pipeline
- Try Quantize node in ComfyUI workflow