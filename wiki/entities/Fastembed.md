---
title: FastEmbed Semantic Router
type: entity
tags: [fastembed, embedding, semantic-routing, classifier]
date: 2026-05-16
---

## Summary
BAAI/bge-small-en-v1.5 (384-dim) embedding model used for semantic agent routing. Replaces keyword matching — 'I want to fight' and 'let's do battle' route identically. File: [intent_classifier.py](https://github.com/jleechanorg/worldarchitect.ai/blob/main/mvp_site/intent_classifier.py) (1,350 lines). Runs locally (<50ms, no API cost).

## Connections
- [[WorldArchitectAI]] — uses this for agent routing
- [[WorldArchitect System Architecture v3.0]] — §4.1
