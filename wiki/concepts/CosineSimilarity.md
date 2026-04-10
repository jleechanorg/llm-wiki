---
title: "Cosine Similarity"
type: concept
tags: [math, similarity, embeddings, vector]
sources: [local-intent-classifier-fastembed]
last_updated: 2026-04-08
---

Cosine similarity measures the cosine of the angle between two vectors. Used in the Local Intent Classifier to compare user input embeddings against anchor phrase embeddings.

## Formula
```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
```

## Usage in Classifier
- Both embeddings L2 normalized → ||A|| = ||B|| = 1
- Simplifies to: A · B (dot product)
- Higher values = more similar

## Threshold
- SIMILARITY_THRESHOLD = 0.65
- Below threshold → defaults to MODE_CHARACTER

## Connections
- [[SemanticIntentClassification]] — uses cosine similarity
- [[L2Normalization]] — preprocessing step
- [[EmbeddingVector]] — inputs to similarity calculation
