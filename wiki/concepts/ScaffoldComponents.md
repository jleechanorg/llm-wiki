---
title: "Scaffold Components"
type: concept
tags: [prompt-engineering, llm, system-instruction]
sources: ["context-components-reference"]
last_updated: 2026-04-08
---

## Description
Static or semi-static parts of the prompt that don't change based on story length. Target ~15-20% of input tokens.

## Components
1. **System Instruction** (5,000-8,000 tokens): Narrative, mechanics, game state instructions + world content
2. **Checkpoint Block** (1,000-2,000 tokens): Session continuity markers, last known game state references
3. **Core Memories Summary** (2,000-3,000 tokens): Companion instruction + background summary
4. **Sequence ID List** (200-500 tokens): Turn sequence numbers for continuity
5. **Game State JSON** (2,000-4,000 tokens): Serialized player stats, inventory, quests, location, combat

## Code Location
`llm_service.py:600-656` — InstructionBuilder.build_core_system_instructions

## Related Concepts
- [[System Instruction]] — core prompt components
- [[Game State JSON]] — serialized game state
- [[Token Budget Allocation]] — overall allocation strategy
