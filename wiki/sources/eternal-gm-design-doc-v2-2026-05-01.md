---
title: "Eternal GM Design Doc v2.0 - The Architect Edition"
type: source
tags: [eternal-gm, product-design, ttrpg, langgraph, pixijs, flux, sprite-pipeline]
date: 2026-05-01
source_file: user-provided-design-doc
---

## Summary
Eternal GM v2.0 is a full LLM campaign system with real-time 2D animated sprites, one-sentence world generation, and dynamic emergent NPCs. Key innovation: pre-cached archetype sprites + FLUX.1 background generation for zero-latency NPC popups. Target: $10-12M ARR Year 1, 5,000 premium users.

## Core Architecture

### The Zero-Latency Visual Pipeline (Key Innovation)
1. Emergent NPC needed → render pre-cached archetype sprite immediately (<0.5s)
2. Background: FLUX.1 schnell generates custom sprite (~5-8s)
3. WebSocket sends new S3 URL → PixiJS hot-swaps texture seamlessly
4. Result: player sees "generic assassin fades in, then resolves into specific character"

### Sprite Generation Target
- Cost: ~$0.02 per 128x128 sprite sheet (FLUX.1 schnell on serverless GPU)
- Format: 128x128 sprite sheet with Idle, Walk, Attack, Death frames
- Consistency: FLUX.1 Kontext + IP-Adapter lock character features across poses
- ControlNet OpenPose maps to standard sprite grid

### Tech Stack
- Frontend: Next.js 15, PixiJS v8 (WebGL/WebGPU), Zustand
- Backend: FastAPI, LangGraph multi-agent swarm, WebSockets
- LLM: Gemini 1.5 Pro (narrative), separate Mechanics Agent, Visual Agent, Auditor Agent
- DB: PostgreSQL + pgvector, Redis, S3
- Image: FLUX.1 schnell + Kontext + IP-Adapter + ControlNet

### Multi-Agent Swarm
1. **Narrative Agent**: prose, dialogue, atmospheric (streams to user)
2. **Mechanics Agent**: dice simulation, stat updates, custom ruleset enforcement
3. **Visual Agent**: LLM output → rendering commands (`{"action": "play_animation", "sprite_id": "guard_01", "anim": "melee_strike"}`)
4. **Auditor Agent**: monitors JSON state delta, catches desyncs

### Deterministic Logic Layer (Critical)
LLMs banned from X/Y coordinates. LLM outputs intent:
```json
{"npc_id": "guard_2", "intent": "investigate_noise", "target_zone": "hallway"}
```
Deterministic Python service calculates exact coords, validates wall collisions, sends rigid X/Y to frontend.

## Product Tiers
- **Wanderer (Free)**: text engine, generic archetype sprites, aggressively pruned memory
- **Architect Pro ($29/mo)**: unlimited sprite generation, God Mode JSON editor, deep vector memory
- **God-Emperor Legend ($79/mo)**: multiplayer, custom LoRA training, export to Unity/Godot

## Unit Economics
- LLM cost per active hour: ~$0.15
- Image generation: ~$0.02 per sprite sheet
- COGS per heavy user (2hr/day): $12-15/month

## Development Phases
1. **Months 1-3**: LangGraph backend, text-only interface, God Mode JSON overlay
2. **Months 4-6**: PixiJS canvas, FLUX.1 pipeline, hot-swap system, A* pathfinding
3. **Months 7-9**: UI/UX polish, Stripe billing, Vector RAG, community hub
4. **Months 10-12+**: Multiplayer WebSocket, custom LoRA training, Godot/Unity export

## Key Design Decisions
- PixiJS v8 with sprite pooling (dead NPCs return to pool, not destroyed)
- Y-sorting for proper environment overlap
- Two-stage loading: archetype → custom sprite
- A/B testing on pixel vs hand-drawn vs cel-shaded styles
- LoRA hot-swapping for aesthetic flexibility

## Technical Challenges Solved
1. **Spatial hallucination**: LLM never outputs coordinates, deterministic layer handles all physics
2. **Context window drift**: Auditor Agent cross-references live JSON with Vector DB
3. **Generation latency**: Two-stage loading reduces perceived latency to <0.5s
4. **Cost control**: token-limit enforcement on free tier, vector summarization for older arcs

## Sprite Pipeline Specs
- Resolution: 128x128 per frame
- Frames: Idle, Walk (8-dir), Attack, Death, Alert
- Hot-swap: archetype → generated in 5-8s via WebSocket
- Cost target: $0.02 per full sheet
- Consistency: IP-Adapter locks face + clothing across frames
