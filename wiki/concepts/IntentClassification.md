---
title: "Intent Classification"
type: concept
tags: [ml, classification, nlp, intent]
sources: []
last_updated: 2026-04-08
---

## Description
The task of determining the intent or goal behind user input. Implemented using text embeddings and cosine similarity comparison against anchor embeddings for different modes (character, story, etc.).

## Process
1. Generate embedding vector for user input (with optional context)
2. Compare against pre-computed anchor embeddings for each mode
3. Return the mode with highest similarity

## Related Concepts
- [[TextEmbedding]] — converting text to vectors
- [[LocalIntentClassifier]] — implementation using embeddings
- [[ContextTruncation]] — limiting context length for performance
