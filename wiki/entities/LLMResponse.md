---
title: "LLMResponse"
type: entity
tags: [class, python, api]
sources: [state-update-integration-tests]
last_updated: 2026-04-08
---

## Description
Python class that wraps LLM responses, containing both narrative text and structured responses with state updates.

## Key Properties
- `narrative_text`: The narrative portion of the response
- `structured_response`: Structured data including state_updates
- `state_updates`: Property that extracts state_updates from structured_response

## Usage
Used in main.py to process AI responses and extract state changes for game state application.

## Connections
- [[NarrativeResponse]] — contains the structured response data
- [[StateUpdateIntegrationTests]] — tests this class's behavior
