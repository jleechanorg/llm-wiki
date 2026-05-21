---
title: Deterministic Token Budget
type: entity
tags: [token-budget, context-compaction, gemini, allocation]
date: 2026-05-16
---

## Summary
5-component min-first/fill-to-max token allocation engine. File: [context_compaction.py](https://github.com/jleechanorg/worldarchitect.ai/blob/main/mvp_site/context_compaction.py) (1,005 lines). Story context guaranteed ≥30%.

## Allocation
| Component | Min % | Max % |
|---|---|---|
| system_instruction | 10% | 50% |
| game_state | 5% | 20% |
| core_memories | 20% | 30% |
| entity_tracking | 3% | 15% |
| story_context | **30%** | 60% |

Story context gets all leftover budget after other components fill to max.

## Connections
- [[WorldArchitectAI]] — uses this system
- [[WorldArchitect System Architecture v3.0]] — §4.3
