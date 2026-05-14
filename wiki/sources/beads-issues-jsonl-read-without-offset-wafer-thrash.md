---
title: ".beads/issues.jsonl Read Without Offset Causes Context Thrash in Wafer (GLM-5.1)"
date: 2026-05-13
type: feedback
bead: rev-wgtju
evidence_session: ~/.claude/projects/-Users-jleechan-projects-worktree-location-freeze/c03c7cd8-ad2a-4107-b27b-6ef0a5fd4635.jsonl
---

## Summary

Confirmed via Python analysis of conversation JSONL: `.beads/issues.jsonl` (1,044,983 bytes)
was read with **no `offset` or `limit`** in a GLM-5.1 (wafer) session on the
`worktree-location-freeze` project, causing context thrashing.

## Evidence

- **Session file**: `~/.claude/projects/-Users-jleechan-projects-worktree-location-freeze/c03c7cd8-ad2a-4107-b27b-6ef0a5fd4635.jsonl`
- **Model**: `GLM-5.1` / `<synthetic>` (wafer backend)
- **Unguarded Read #1**: `.beads/issues.jsonl` — 1,044,983 bytes, no offset, no limit
- **Unguarded Read #2**: `test_freeze_time_choices.py` — 45,318 bytes, no offset, no limit
- **Detection method**: `grep -o '"file_path":"[^"]*"'` then Python tool_use block inspection

## Extraction command

```python
# Parse conversation JSONL for unguarded Read calls
import json, os
with open(path) as f:
    for line in f:
        msg = json.loads(line.strip())
        for block in msg.get('message',{}).get('content',[]):
            if block.get('type')=='tool_use' and block.get('name')=='Read':
                inp = block.get('input',{})
                if inp.get('offset') is None and inp.get('limit') is None:
                    size = os.path.getsize(inp.get('file_path',''))
                    print(size, inp['file_path'])
```

## Fix applied

`~/.claude/CLAUDE.md` updated with explicit "Known large files — NEVER read whole" block:

```
- .beads/issues.jsonl — confirmed 1MB+ in wafer (GLM-5.1) sessions; always grep by bead ID or use offset/limit
- mvp_site/world_logic.py — 421KB / 9,890 lines; always use Grep to locate function, then targeted Read
```

## Related concepts

- [[Compaction]] — autocompact thrash loop mechanism
- [[ClaudeCodeCompaction]] — client-side compaction behavior
