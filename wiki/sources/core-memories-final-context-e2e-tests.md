---
title: "Core Memories from Final Truncated Context E2E Tests"
type: source
tags: [python, testing, e2e, context-compaction, core-memories, narrative-regression]
source_file: "raw/worktree_logs6-d2r"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end tests verifying that core memories in LLM requests come from truncated_story_context (the final allocated story), not sequence_id_context (which is bounded to only 20% of the story). The tests validate the fix that prevents narrative regression from using wrong memory selection.

## Key Claims
- **Correct Memory Source**: Core memories are derived from truncated_story_context (full allocated story), not sequence_id_context (bounded 20%)
- **Compaction Applied**: compaction is applied to core_memories_summary from the final context
- **Narrative Regression Fix**: Fix prevents regression where memory selection used minimal 20% bounded view instead of full truncated context
- **Recent Memories Preserved**: Recent memories like "DRAGON_ALLIANCE", "CRYSTAL_SHARD_FOUND", "BETRAYAL_REVEALED" are now properly visible in memory selection

## Bug Description
Previously, compacted_core_memories was derived from temp_core_memories which was built from sequence_id_context (bounded to 20% of story). This meant memories were selected based on a minimal view of the story, potentially missing critical recent memories visible in the actual truncated story context.

## Fix Description
Now core_memories_summary is generated from truncated_story_context (the full allocated story), then compacted to budget as final_core_memories.

## Connections
- [[Context Compaction]] — the compaction mechanism this test validates
- [[Core Memories]] — the memory system being tested
- [[Narrative Regression]] — the bug this fix prevents

## Contradictions
- None detected
