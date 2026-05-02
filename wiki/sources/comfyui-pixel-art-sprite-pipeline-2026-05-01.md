---
title: "ComfyUI Pixel Art Sprite Pipeline"
type: source
tags: [sprite-generation, pixel-art, comfyui, sdxl, lora]
date: 2026-05-01
source_file: worldai_claw
---

## Summary
ComfyUI + SDXL + pixel_icon_v1 LoRA successfully generates 128x128 pixel art sprites with ~16KB file sizes. RTX 4090 (16.6GB VRAM free) handles generation in ~2 seconds. Available LoRA: pixel_icon_v1.safetensors.

## ComfyUI System
- Version: 0.20.1 on CUDA/RTX 4090
- VRAM: 22.3GB free of 23.6GB total
- Checkpoint: sd_xl_base_1.0.safetensors
- LoRA: pixel_icon_v1.safetensors

## Test Results
| Test | Output | Size | Notes |
|------|---------|------|-------|
| Basic (no LoRA) | test_basic_00001_.png | 5,745 bytes | 128x128 |
| With pixel_icon_v1 | pixel_lora_test_00001_.png | 16,991 bytes | 3x larger = more complexity |

## SDXL Pixel Art LoRAs Available on Civitai
- Pixel Art Stylizer SDXL (civitai.com/models/27486) - SDXL 1.0, ~100-200MB
- 8-bit Arcade SDXL (civitai.com/models/117111) - Game asset focused
- Pixel Art 8-bit XL (civitai.com/models/304098) - For game sprites
- Pixel Style XL (civitai.com/models/256677) - Another SDXL option

## Workflow
CheckpointLoaderSimple (sd_xl_base_1.0)
  → LoraLoader (pixel_icon_v1, strength=1.0)
    → CLIPTextEncode (positive + negative)
    → EmptyLatentImage (128x128)
    → KSampler (seed=42, steps=25, cfg=8.0, euler)
    → VAEDecode
    → SaveImage

## Next Steps
1. Download SDXL pixel art LoRA from Civitai (pixel_icon_v1 already works)
2. Add Quantize node to cap colors at 64-256
3. Test with AnimateDiff for frame-to-frame consistency
4. Try higher resolutions (256x256)