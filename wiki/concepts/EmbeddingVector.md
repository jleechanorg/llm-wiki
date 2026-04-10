---
title: "Embedding Vector"
type: concept
tags: [embeddings, vector, nlp, representation]
sources: [local-intent-classifier-fastembed]
last_updated: 2026-04-08
---

An embedding vector is a numerical representation of text that captures semantic meaning in a fixed-dimensional space. The Local Intent Classifier uses 384-dimensional vectors from the BGE-small-en-v1.5 model.

## Properties
- Dimensions: 384 (for BGE-small-en-v1.5)
- Dense: all values non-zero
- L2 normalized: magnitude = 1

## Usage
1. User input → 384-dim embedding
2. Anchor phrases → 384-dim embeddings per mode
3. Cosine similarity between user embedding and each mode's anchors

## Connections
- [[BGE-small-en-v1.5]] — model generating embeddings
- [[FastEmbed]] — library for embedding generation
- [[CosineSimilarity]] — comparison metric
- [[L2Normalization]] — preprocessing
