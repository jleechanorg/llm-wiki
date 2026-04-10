---
title: "TextEmbedding"
type: entity
tags: [python, ml, embedding, model]
sources: []
last_updated: 2026-04-08
---

## Description
A text embedding model class that converts text strings into numerical vector representations.

## Usage
Used by LocalIntentClassifier to generate embeddings for classification. The `embed()` method returns an iterator of embedding arrays.

## Connections
- [[LocalIntentClassifier]] — uses this for embedding generation
- [[TextEmbedding]] — concept of text embedding
