---
title: "Semantic Routing"
type: concept
tags: [routing, intent-classification]
sources: []
last_updated: 2026-04-08
---

Semantic routing is a feature that uses embedding-based intent classification to route user inputs to appropriate handlers. Controlled by ENABLE_SEMANTIC_ROUTING environment variable.

## Behavior
- When disabled (false): skip classifier initialization
- When enabled (true): initialize LocalIntentClassifier
- Default: disabled
