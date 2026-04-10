---
title: "Structured Generation"
type: concept
tags: [llm, prompting, entity-tracking]
sources: ["complete-combined-approach-tests"]
last_updated: 2026-04-08
---

## Description
LLM prompting technique that embeds structured entity manifest into generation prompt to guide model output. Part of Milestone 1 Combined approach.

## Key Components
- Entity manifest created from game state
- Hidden entities excluded from manifest
- Prompt injection with CRITICAL ENTITY TRACKING REQUIREMENT
- JSON format instructions for structured output

## Related Concepts
- [[StructuredResponse]] — output format from structured generation
- [[EntityTracking]] — entity manifest creation
- [[JSONSchemaValidation]] — response validation

## Test Coverage
- test_step1_structured_generation_prompt_creation validates prompt creation
