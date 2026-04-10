---
title: "Banned Name Prevention"
type: concept
tags: [ai-generation, character-naming, prompt-engineering, enforcement]
sources: ["banned-names-loading-unit-tests", "ai-character-banned-name-prevention-tests"]
last_updated: 2026-04-08
---

## Description
System for preventing overused/banned character names in AI-generated content. Involves loading a predefined list of banned names and including enforcement directives in the system instruction to ensure AI checks against the list before generating character names.

## Mechanism
1. **Name List**: 56+ banned names in banned_names.md (primary + extended)
2. **Master Directive**: Instructions requiring pre-generation name checking
3. **NO EXCEPTIONS Policy**: Absolute prohibition with no workarounds
4. **Enforcement Directive**: Section emphasizing compliance requirements

## Related Concepts
- [[PromptEngineering]] — how the banned names are integrated into system instructions
- [[CharacterGeneration]] — the process being protected by name prevention
- [[WorldLoader]] — module that loads the banned names for use
