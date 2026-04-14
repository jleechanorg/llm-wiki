---
title: "mvp_site intent_classifier"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/intent_classifier.py
---

## Summary
Local intent classifier using FastEmbed (ONNX Runtime) with BAAI/bge-small-en-v1.5 embeddings for semantic classification of user input to agent modes. Runs in Priority 5 of routing after string prefix detection.

## Key Claims
- FastEmbed model BAAI/bge-small-en-v1.5 for 384-dim embeddings
- SIMILARITY_THRESHOLD = 0.65 for mode classification
- Precedence over string prefixes: GOD MODE: and THINK: take priority over classifier
- Mode toggle (mode parameter) checked at different priorities before classifier
- Priority routing: GOD MODE (P1) > completion (P2) > creation (P3) > THINK (P4) > classifier (P5)

## Connections
- [[LLMIntegration]] — semantic intent routing for agent selection
