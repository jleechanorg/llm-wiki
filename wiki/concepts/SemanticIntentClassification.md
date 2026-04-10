---
title: "Semantic Intent Classification"
type: concept
tags: [classification, nlp, embeddings, semantics]
sources: [local-intent-classifier-fastembed]
last_updated: 2026-04-08
---

Semantic Intent Classification determines user intent by understanding the meaning of input text rather than matching keywords. The Local Intent Classifier uses embedding similarity to compare user input against anchor phrases representing each agent mode.

## Approach
1. Generate embeddings for user input and anchor phrases
2. Compute cosine similarity between embeddings
3. Return mode with highest similarity above threshold

## Comparison to Keyword Routing
- **Keyword routing**: Matches specific words/phrases (e.g., "attack" → combat)
- **Semantic classification**: Understands meaning ("I strike the goblin" → combat via embedding)

## Connections
- [[FastEmbed]] — tool for generating embeddings
- [[CosineSimilarity]] — similarity metric used
- [[L2Normalization]] — normalization applied to embeddings
- [[AgentRouting]] — result of classification used for routing
