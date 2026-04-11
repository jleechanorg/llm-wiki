---
title: "Context Components Reference"
type: source
tags: [context-window, token-allocation, llm, architecture, worldarchitect]
source_file: "raw/context-components-reference.md"
sources: ["context-budget-design-document", "PR #2311"]
last_updated: 2026-04-08
---

## Summary
Comprehensive reference for every component that makes up the LLM context in WorldArchitect.AI, including target token allocations and code pointers. Describes scaffold components, entity tracking reserves, and story budget allocation with exact token targets and implementation locations.

## Key Claims
- **10,500 token entity reserve**: Entity tracking components added after story truncation, requiring pre-reserved tokens
- **Scaffold components ~15-20%**: System instruction (5,000-8,000 tokens), checkpoint block (1,000-2,000), core memories (2,000-3,000), game state JSON (2,000-4,000)
- **Story budget ~50-60%**: Allocated as 25% start turns, 10% middle summary, 60% end turns with 5% safety margin
- **Code pointer architecture**: All components have specific file locations in llm_service.py for token calculation

## Key Technical Details
- **System Instruction**: 5,000-8,000 tokens assembled from narrative, mechanics, game state instructions and world content
- **Entity Preload Text**: 2,000-3,000 tokens for NPC summaries and entity context per scene
- **Output Reserve**: 20% of safe budget reserved for output generation
- **Fixed Entity Tracking**: 10,500 tokens fixed reserve added post-truncation

## Key Files Referenced
1. `llm_service.py:600-656` — InstructionBuilder.build_core_system_instructions
2. `llm_service.py:858-910` — _get_static_prompt_parts (checkpoint block)
3. `llm_service.py:658-740` — Core memories assembly
4. `llm_service.py:2874-2877` — Game state JSON serialization
5. `llm_service.py:213-219` — Entity tracking token reserve constants
6. `llm_service.py:2902` — Entity preloader.create_entity_preload_text
7. `entity_preloader.py` — Entity preload text generation

## Connections
- [[Context Budget System]] — Token allocation architecture this document details
- [[PR #2311]] — Removed auto-fallback, established truncation-first approach
- [[WorldArchitect]] — Company owning this context system

## Contradictions
- None identified — this document is consistent with context-budget-design-document
