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

## Related Concepts
- [[Memory System]] — underlying storage mechanism
- [[Compaction]] — memory management before context limit
