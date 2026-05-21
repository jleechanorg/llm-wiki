---
name: ms-skill-forbidden-patterns-thrash
description: /ms skill reads .beads/issues.jsonl raw and grep -H session JSONL files — floods context post-compaction → autocompact thrash loop
metadata:
  type: feedback
  bead: none
  originSessionId: f6c08ed2-9a66-45b2-9ecb-2784de0ecba6
---

## Rule

The `/ms` (memory-search) skill has two **forbidden** read patterns that cause autocompact thrashing in wafer (GLM-5.1) sessions:

1. **Beads step** — reads `.beads/issues.jsonl` raw — 1MB+ file, forbidden
2. **History step** — `grep -H` across session JSONL files — reads full content of large conversation transcripts

**Why**: After compaction, a session invokes `/ms` to re-orient. 9 parallel subagents flood results back into context, including MB+ JSONL content. Context refills within 3 turns → compact → repeat 3× → "Autocompact is thrashing".

**Fix**: beads step → `br search "$QUERY" --json`; history step → `grep -rl` (filenames only, no content).

Fixed in `~/.claude/skills/memory-search/SKILL.md` 2026-05-14.

Session: claudewc in ~/projects/worktree_runner4 (worldarchitect.ai, PR #6902) on 2026-05-14.
