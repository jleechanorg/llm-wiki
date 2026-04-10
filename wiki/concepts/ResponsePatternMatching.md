---
title: "Response Pattern Matching"
type: concept
tags: [testing, mock, pattern-matching, prompt-analysis]
sources: [mock-gemini-api-service-function-testing]
last_updated: 2026-04-08
---

## Description
Technique used by mock LLM services to determine appropriate response types based on prompt content analysis. Enables realistic test responses without hardcoding specific prompts.

## How It Works
1. Convert prompt to lowercase for analysis
2. Check for forced response modes first
3. Search for keyword patterns (e.g., "initial story", "unconscious", "dragon")
4. Select corresponding response generator
5. Return generated response

## Response Types
- **initial_story**: Campaign/story creation prompts
- **continue_story**: Continuing existing narrative
- **hp_discrepancy**: Health-related edge cases
- **location_mismatch**: Location consistency testing
- **mission_completion**: Quest/objective completion
- **validation_prompt**: Data validation scenarios

## Related
- [[MockLLMClient]] — implements pattern matching
- [[ForcedResponseMode]] — explicit response forcing
