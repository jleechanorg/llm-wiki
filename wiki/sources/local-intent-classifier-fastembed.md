---
title: "Local Intent Classifier using FastEmbed"
type: source
tags: [intent-classification, fastembed, agent-routing, embeddings, onnx-runtime, semantic-classification]
source_file: "raw/local-intent-classifier-fastembed.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Lightweight local classification system using FastEmbed library with ONNX Runtime and BAAI/bge-small-en-v1.5 model to determine appropriate agent mode based on user input. Embeds user queries and compares against pre-computed anchor phrases using cosine similarity.

## Key Claims
- **Model**: FastEmbed with BAAI/bge-small-en-v1.5 (~133MB, 384-dimensional embeddings)
- **Process**: Pre-computes anchor embeddings from ANCHOR_PHRASES, L2 normalizes all vectors
- **Classification**: Computes cosine similarity vs anchor groups, returns highest-scoring mode if ≥0.65 threshold
- **Default**: Falls back to MODE_CHARACTER (story mode) when no threshold met
- **Integration**: Runs at Priority 5 in get_agent_for_input() routing logic
- **Precedence**: String prefixes ("GOD MODE:", "THINK:") override classifier completely
- **Valid Patterns**: CombatAgent, RewardsAgent, CharacterCreationAgent can all initiate new states from semantic intent alone

## Key Function

```python
# Classification process
1. Embed user input → 384-dim vector
2. L2 normalize embedding
3. Compute cosine similarity vs each anchor group
4. Return mode with max similarity if ≥ 0.65, else MODE_CHARACTER
```

## Connections
- [[FastEmbed]] — embedding library used
- [[BGE-small-en-v1.5]] — model for 384-dim embeddings
- [[ONNX Runtime]] — runtime for model execution
- [[Agent Routing]] — integration point for classification results
- [[Semantic Intent Classification]] — classification approach used

## Contradictions
- None identified
