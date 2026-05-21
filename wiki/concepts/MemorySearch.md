---
title: "MemorySearch"
type: concept
tags: ["memory", "search", "semantic"]
sources: ["genesis-persistent-orchestration-layer-openclaw"]
last_updated: 2026-04-07
---

OpenClaw's configurable hybrid search system combining vector and text-based retrieval.

## Configuration Options
```jsonc
{
  "memorySearch": {
    "enabled": true,
    "extraPaths": ["path/to/project"],
    "query": {
      "hybrid": {
        "enabled": true,
        "vectorWeight": 0.7,
        "textWeight": 0.3,
        "temporalDecay": {
          "enabled": true,
          "halfLifeDays": 30
        },
        "mmr": {
          "enabled": true,
          "lambda": 0.7
        }
      }
    }
  }
}
```

## Key Parameters
- **vectorWeight 0.7**: Semantic search contribution
- **textWeight 0.3**: Keyword search contribution
- **temporalDecay**: Prefer recent memories (30-day half-life)
- **mmr**: Maximum Marginal Relevance for diversity in results

## /ms Skill — Known Thrash Triggers (2026-05-14)

The `/ms` slash command (`~/.claude/skills/memory-search/SKILL.md`) runs 9 parallel subagents. Two steps contain forbidden patterns that cause autocompact thrash loops in wafer sessions:

| Step | Forbidden pattern | Safe replacement |
|------|------------------|-----------------|
| Beads (step 2) | Read `.beads/issues.jsonl` raw (1MB+) | `br search "$QUERY" --json \| head -40` |
| History (step 9) | `grep -H` across `*.jsonl` files (reads full content) | `grep -rl` (filenames only) |

**Thrash mechanism**: Post-compaction, session invokes `/ms` → 9 subagents return MB+ of JSONL content → context refills within 3 turns → compact fires → repeat 3× → "Autocompact is thrashing."

Fixed in `~/.claude/skills/memory-search/SKILL.md` 2026-05-14. See [[conflict-resolution-large-file-thrash]] for a parallel thrash trigger.

## Related Concepts
- [[Memory System]] — underlying storage mechanism
- [[Compaction]] — memory management before context limit
