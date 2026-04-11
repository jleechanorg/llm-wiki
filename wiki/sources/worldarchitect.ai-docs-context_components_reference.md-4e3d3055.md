---
title: "WorldArchitect.AI Context Components Reference"
type: source
tags: [worldarchitect, context, token-budget, llm, architecture]
sources: []
last_updated: 2026-04-07
---

## Summary
Comprehensive reference for LLM context composition in WorldArchitect.AI game platform, detailing target token allocations across scaffold components, entity tracking reserve, and story budget. The context window is partitioned to ensure reliable output generation while maintaining story continuity and entity awareness.

## Key Claims

- **Token Budget Allocation**: Model context window split into Safe Budget (90%) containing Output Reserve (20%) and Max Input (80%), with the remaining 10% as safety margin
- **Scaffold Components**: ~15-20% of input includes System Instruction (5,000-8,000 tokens), Checkpoint Block (1,000-2,000 tokens), Core Memories (2,000-3,000 tokens), Sequence IDs (200-500 tokens), and Game State JSON (2,000-4,000 tokens)
- **Entity Tracking Reserve**: Fixed 10,500 tokens pre-reserved after story truncation for Entity Preload Text (2,000-3,000 tokens), Entity Instructions (1,500-2,000 tokens), Entity Tracking Rules (1,000-1,500 tokens), and Timeline Log (3,000-4,000 tokens)
- **Story Budget**: Remaining ~50-60% of input allocated across Start Turns (25%), Middle Summary (10%), End Turns (60%), and 5% safety margin
- **Code Assembly**: Components assembled in `llm_service.py` via `build_core_system_instructions()`, `_get_static_prompt_parts()`, and `_prepare_entity_tracking()` methods

## Key Quotes

> "Token Budget Allocation: Safe Budget (90% - CONTEXT_WINDOW_SAFETY_RATIO) → Output Reserve (20% - OUTPUT_TOKEN_RESERVE_RATIO) + Max Input Allowed (80%)"

> "Entity Tracking Reserve: 10,500 tokens (fixed) — added AFTER story truncation to ensure entity awareness is never lost"

## Connections

- [[WorldArchitect.AI]] — the platform this context architecture supports
- [[Token Budget]] — the concept of reserving tokens for different prompt components
- [[Entity Tracking]] — the system for maintaining NPC and character awareness across turns

## Contradictions

- None identified — this is a technical reference document with no conflicting claims