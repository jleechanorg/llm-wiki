---
title: "Error State Display"
type: concept
tags: [ui-pattern, error-handling, css]
sources: [planning-block-choice-buttons-styles]
last_updated: 2026-04-08
---

A UI pattern for displaying malformed or invalid content within interactive narrative experiences. Provides visual feedback without breaking the narrative flow.


## Implementation
- **Warning Background** — Yellow (#fff3cd) background color
- **Border Accent** — Orange left border for emphasis
- **Monospace Text** — Preserves formatting for debugging
- **Word Wrap** — Prevents text overflow

## Purpose
- Display JSON parse errors from LLM responses
- Show malformed content for debugging
- Maintain narrative visibility even with broken content

## Connected Concepts
- [[NarrativeDirectives]] — Requires graceful error handling
- [[SimplifiedStructuredNarrativeGenerationSchemas]] — JSON parsing error handling
