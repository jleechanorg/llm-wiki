---
title: "ONNX Runtime"
type: entity
tags: [runtime, machine-learning, onnx]
sources: [local-intent-classifier-fastembed]
last_updated: 2026-04-08
---

ONNX Runtime is a cross-platform machine learning runtime that executes ONNX models. Used by FastEmbed to run the BGE-small-en-v1.5 embedding model efficiently in-memory.

## Connections
- [[FastEmbed]] — uses ONNX Runtime as backend
- [[Local Intent Classifier]] — indirect consumer via FastEmbed
