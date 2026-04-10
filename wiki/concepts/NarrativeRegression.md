---
title: "Narrative Regression"
type: concept
tags: [bug, narrative, story-generation, testing]
sources: []
last_updated: 2026-04-08
---

## Definition
A bug where the story generation produces inconsistent or regressed narrative content because memory selection used the wrong context source.

## Root Cause
Previously, compacted_core_memories was derived from temp_core_memories built from sequence_id_context (bounded to 20% of story). This caused memory selection to miss critical recent memories visible in the actual truncated story context.

## Fix
Core memories now sourced from truncated_story_context (full allocated story), then compacted to budget as final_core_memories.

## Related Concepts
- [[Context Compaction]] — the compaction mechanism
- [[Core Memories]] — the memory system
