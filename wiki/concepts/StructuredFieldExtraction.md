---
title: "Structured Field Extraction"
type: concept
tags: [llm-response, structured-data, data-mapping]
sources: []
last_updated: 2026-04-08
---

## Definition
Structured field extraction is the process of parsing and validating structured data from LLM responses, mapping JSON fields to typed objects with proper defaults and validation.

## Context
Used in the NarrativeResponse class to extract fields like session_header, planning_block, dice_rolls, resources, debug_info, entities_mentioned, and location_confirmed from LLM output.

## Related Concepts
- [[LLMResponse]] — parent class that uses NarrativeResponse for structured output
- [[Planning Block]] — structured choice data embedded in LLM responses
- [[Type Coercion]] — converting None/incorrect types to valid defaults
