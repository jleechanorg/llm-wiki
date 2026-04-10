---
title: "parse_structured_response"
type: entity
tags: [function, python, parsing]
sources: [state-update-integration-tests]
last_updated: 2026-04-08
---

## Description
Function that extracts structured response data from LLM JSON outputs, separating state updates from narrative text.

## Purpose
Critical for Bug 1 fix: ensures the LLM respects character actions by properly extracting state_updates from JSON responses rather than treating them as narrative.

## Connections
- [[LLMResponse]] — uses this to populate structured_response
- [[StateUpdateIntegrationTests]] — validates this function's behavior
