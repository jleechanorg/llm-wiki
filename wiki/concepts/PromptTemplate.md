---
title: "Prompt Template"
type: concept
tags: [prompt-engineering, llm, pattern]
sources: [keyword-parsing-refactor-tests]
last_updated: 2026-04-08
---

## Definition
A structured format for generating prompts sent to the LLM, containing placeholders for user input, system instructions, and context.

## In This Context
The keyword parsing refactor ensures all character mode inputs use the same prompt template, generating consistent "Continue the story" prompts regardless of input content. The LLM's system instructions handle interpreting user intent.

## Key Properties
- **Consistency**: Same template for all character mode inputs
- **Prefix**: Standard "Main character:" prefix
- **Content**: "Continue the story" instruction

## Related Concepts
- [[KeywordDetection]] — the pattern this replaces
- [[SystemInstructions]] — LLM guidance for intent interpretation
- [[CharacterMode]] — one of the prompt modes
