---
title: "LocalIntentClassifier"
type: entity
tags: [python, intent-classification, embedding]
sources: []
last_updated: 2026-04-08
---

LocalIntentClassifier is a Python class in the intent_classifier module that provides intent classification using FastEmbed embeddings. It supports semantic routing, offline mode with local model files, and configurable anchor embeddings.


## Key Attributes
- `ready`: Boolean indicating if model is initialized
- `model`: FastEmbed TextEmbedding instance
- `anchor_embeddings`: Embeddings for intent anchors

## Configuration
- Model: BAAI/bge-small-en-v1.5
- Cache dir: configurable via _FASTEMBED_CACHE_DIR
- Offline mode: HF_HUB_OFFLINE environment variable
- Semantic routing: ENABLE_SEMANTIC_ROUTING env var toggle
