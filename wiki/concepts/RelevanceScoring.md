---
title: "Relevance Scoring"
type: concept
tags: [algorithm, ranking, memory, search]
sources: []
last_updated: 2026-04-08
---

## Definition
Algorithm for ranking memory entities by relevance to a query, using weighted matching across entity fields.

## Scoring Weights
- **Name match** (0.4): Exact or close match on entity name
- **Type match** (0.1-0.2): Entity type aligns with query semantics
- **Observation match** (0.1-0.3): Observations contain query terms

## Implementation
```python
score = calculate_relevance_score(entity, query):
  if name matches: +0.4
  if type matches: +0.1 to 0.2
  if observations contain terms: +0.1 to 0.3
```

## Related Concepts
- [[MemoryIntegration]]
- [[Search Caching]]
