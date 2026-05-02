---
title: "Pixel Art AI Generation Research 2026-05-01"
type: source
tags: [sprite-generation, pixel-art, ai-generation, ragnarok]
date: 2026-05-01
source_file: second-opinion-results
---

## Summary
Second opinion research on AI services that can produce true pixel art sprites (256x256, 64-256 colors, transparent background, frame consistency). Key finding: ComfyUI + SDXL + Pixel Art LoRA is the best approach currently available.

## AI Service Audit

| Platform | True Pixel Art | 256x256 | Transparent | Palette Control | Frame Consistency |
|----------|---------------|---------|-------------|-----------------|-------------------|
| SD 1.5 + Pixel-Art LoRA | ✅ hard edges | ✅ | ✅ Transparent extension | ✅ pngquant | ✅ seed lock |
| **ComfyUI + SDXL + Pixel LoRA** | ✅ BEST | ✅ | ✅ AlphaChannel node | ✅ Quantize node | ✅ AnimateDiff |
| Leonardo.ai Pixel Art | ❌ anti-aliasing | ✅ | ❌ no alpha | ❌ | ❌ |
| Midjourney | ❌ smooth gradients | ✅ | ❌ | ❌ | ❌ |
| DALL-E 3 | ❌ smooth gradients | ✅ | ❌ | ❌ | ❌ |
| Pollinations | ❌ smooth gradients | ✅ | ✅ PNG | ❌ | ❌ |

## Best Approach: ComfyUI + SDXL + Pixel Art LoRA

### Why
- SDXL base has higher quality latent space
- Pixel Art LoRA forces hard-edge pixel style
- AlphaChannel node preserves transparency
- Quantize node caps colors at 64-256
- AnimateDiff locks seed/cfg across frames

### Available LoRAs (Civitai)
- pixel_icon_v1.safetensors - ALREADY INSTALLED, works
- Pixel Art Stylizer SDXL (civitai.com/models/27486)
- 8-bit Arcade SDXL (civitai.com/models/117111)
- Pixel Art 8-bit XL (civitai.com/models/304098)

### ComfyUI Workflow
1. CheckpointLoaderSimple → LoraLoader → CLIPTextEncode
2. EmptyLatentImage (128x128 or 256x256)
3. KSampler (Euler a, 20-25 steps, cfg 7-8)
4. VAEDecode → Quantize (64-256 colors)
5. SaveImage

## User Goal: Ragnarok Not 16-Color Retro
- Target: 64-256 colors with smooth shading like Ragnarok Online
- NOT: strict 16-color retro pixel art
- Solution: Use LoRA for style + Quantize for palette control

## Next Actions
1. Download SDXL pixel art LoRAs from Civitai
2. Add Quantize node to ComfyUI workflow
3. Test 256x256 generation
4. Add AnimateDiff for sprite sheet consistency
