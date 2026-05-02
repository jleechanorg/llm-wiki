---
name: sprite-generation-learnings-2026-05-01
description: Key learnings from LPC + ComfyUI + Grok sprite generation project
type: project
originSessionId: c1920ddc-319b-4071-b914-e11eeda538c2
---
# Sprite Generation Learnings (2026-05-01)

## Pipeline Rankings
1. **ComfyUI SDXL (local)** - BEST: generates at exact 64x64/128x128, RTX 4090, no API costs
2. **Pollinations.ai** - Good: 256x256, free, respects size param
3. **Grok API** - OK but ignores image_size, returns 1408x768 always

## Technical Findings
- Grok `grok-imagine-image` ignores `image_size` parameter - returns 1408x768 landscape
- k-means palette reduction destroys LLM sprite colors (92 → 33 colors)
- Battle Brothers is hand-drawn 2D paintings (1920x1080), NOT pixel art
- Kenney 128x128 sprite packs don't exist - closest is 80x110 (Platformer Characters)
- Cordon CC0 is only 128x128 source available

## Setup Notes
- ComfyUI: `cd ~/ComfyUI && ./venv/bin/python3 main.py --force-fp16 --cuda-device 0`
- SDXL base model: ~/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors (6.5GB)
- Pollinations URL: `https://image.pollinations.ai/prompt/[prompt]?width=256&height=256`
- Grok key that worked: xai-REDACTED

## Quality Expectations
- LLM sprites cannot match hand-drawn pixel art quality
- Best approach: compositing real pixel art (LPC) + LLM for environment/props
- Local SD with Pixel Art LoRA would improve quality further
- Animation (walk cycles) require 8 frames with consistent pose - hardest part

## Relevant Memory Files
- sprite-generation-strategy-2026-04-30.md
- project_grok_pixel_art_failure_2026-04-27.md
- project_pixel_art_postprocess_2026-04-27.md