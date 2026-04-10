---
title: "Timeline Log"
type: concept
tags: [prompt-engineering, conversation-history, context]
sources: ["llm-api-call-capture-gemini-logging"]
last_updated: 2026-04-08
---

## Description
Previous interaction history injected into prompts to maintain narrative continuity. Formatted as a list of sequence IDs with "You:" and "Story:" prefixes showing the exchange so far.

## Purpose
- Provides conversation history for context-aware responses
- Enables the model to reference previous narrative beats
- Supports multi-turn interactive storytelling

## Format
```
[SEQ_ID: 1] You: <user request>
[SEQ_ID: 2] Story: <previous response>
```

## Connections
- [[GameState]] — state alongside history
- [[SceneManifest]] — current scene context
- [[CampaignWizard]] — creates the campaign being logged

## Source Evidence
"TIMELINE LOG (FOR CONTEXT):\n[SEQ_ID: 1] You: Create a new D&D campaign...\n[SEQ_ID: 2] Story: ```json..."
