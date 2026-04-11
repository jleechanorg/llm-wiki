---
title: "Intent Classifier Context Tests"
type: source
tags: [python, testing, intent-classification, context, embedding]
source_file: "raw/test_intent_classifier_context.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite for context-aware classification in the LocalIntentClassifier. Tests verify that context is properly concatenated with user input text before embedding, and that long context is truncated to the last 500 characters.

## Key Claims
- **Context concatenation**: Context is prepended to user input with a separator (`\n\nUSER ACTION:`) before embedding
- **Context truncation**: Long context (1000+ chars) is truncated to last 500 characters before being passed to the embedding model
- **Mode-specific embeddings**: Classifier uses `anchor_embeddings` from `constants.MODE_CHARACTER` for classification
- **Mock-based testing**: Tests use `unittest.mock.patch` to mock TextEmbedding for isolated testing

## Key Quotes
> "Expected: Last AI text + separator + User text (Using last 500 chars)" — verifies truncation behavior

## Connections
- [[LocalIntentClassifier]] — class under test
- [[TextEmbedding]] — embedding model being mocked
- [[IntentClassifier]] — concept of context-aware classification

## Contradictions
- None detected
