---
title: "Claude History Taste Ingestor"
type: concept
tags: [taste, claude, history, ingestion, worldai]
last_updated: 2026-04-14
---

## Summary

The Claude History Taste Ingestor processes conversation history from Claude Code sessions to build a "taste profile" — learned preferences for code style, architecture patterns, and quality bar. It extracts exemplars from past successful generations.

## Purpose

As Claude Code generates code over time, it accumulates a history of:
- Which patterns were accepted vs. rejected
- What refinement cycles looked like
- User feedback on quality

This history feeds back into future generation to improve taste alignment.

## Key Concepts

**Taste exemplar extraction** — From each conversation, extract:
- Preferred naming conventions
- Architectural choices (e.g., class vs. functional)
- Error handling patterns
- Comment/documentation density

**Taste vector representation** — Each exemplar becomes a vector in taste-space for similarity search:
```python
@dataclass
class TasteExemplar:
    code_snippet: str
    pattern_type: str  # naming, structure, error-handling, etc.
    user_feedback: str  # "loved it", "too verbose", "needs types"
    embedding: list[float]
```

## Connections
- [[TasteLearningLoop]] — The broader taste learning system
- [[ProductTasteLayer]] — Product-specific taste considerations
- [[ClaudeHistoryTasteIngestor]] — Self-reference for deep dive
