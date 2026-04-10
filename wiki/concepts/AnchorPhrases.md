---
title: "Anchor Phrases"
type: concept
tags: [intent-classification, nlp, routing]
sources: [modal-agent-intent-classifier-tdd-tests]
last_updated: 2026-04-08
---

## Description
Intent routing phrases in intent_classifier that trigger specific game modes. Each mode (CHARACTER_CREATION, LEVEL_UP) has a set of anchor phrases that determine user intent.

## Issue
PR #5225 identifies duplicate anchor phrases between CHARACTER_CREATION and LEVEL_UP modes causing routing conflicts.

## Related Constants
- `MODE_CHARACTER_CREATION` — Character creation flow mode
- `MODE_LEVEL_UP` — Level-up progression mode
