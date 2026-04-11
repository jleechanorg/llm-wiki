---
title: "Intent Classifier Initialization Tests"
type: source
tags: [python, testing, intent-classification, fastembed, offline-mode]
source_file: "raw/test_intent_classifier.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for LocalIntentClassifier initialization logic, validating semantic routing toggle behavior, FastEmbed model setup, and offline mode support with local files only.

## Key Claims
- **Semantic routing toggle**: ENABLE_SEMANTIC_ROUTING="false" skips classifier initialization
- **Explicit enablement in tests**: TESTING=true + ENABLE_SEMANTIC_ROUTING=true forces initialization
- **Offline mode**: HF_HUB_OFFLINE=1 uses local_files_only=True for model loading
- **FastEmbed model**: BAAI/bge-small-en-v1.5 with cache_dir and threads=1

## Key Quotes
> "mock_text_embedding_cls.assert_called_once_with(
model_name="BAAI/bge-small-en-v1.5",
threads=1,
cache_dir="/tmp/test-fastembed-cache",
local_files_only=True
)"

## Connections
- [[IntentClassifier]] — class under test
- [[FastEmbed]] — embedding model library used
- [[SemanticRouting]] — feature being toggled

## Contradictions
- None identified
