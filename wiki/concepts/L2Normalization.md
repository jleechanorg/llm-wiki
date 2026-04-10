---
title: "L2 Normalization"
type: concept
tags: [math, normalization, embeddings, linear-algebra]
sources: [local-intent-classifier-fastembed]
last_updated: 2026-04-08
---

L2 normalization scales a vector so its magnitude (Euclidean norm) equals 1. Applied to all embeddings in the Local Intent Classifier to enable cosine similarity calculation via simple dot product.

## Formula
```
L2_normalize(v) = v / ||v||
where ||v|| = sqrt(sum(v_i²))
```

## Connections
- [[CosineSimilarity]] — enables simplified calculation
- [[EmbeddingVector]] — input/output type
- [[FastEmbed]] — performs normalization internally
