---
title: "Keyword Detection"
type: concept
tags: [prompt-engineering, pattern, deprecated]
sources: [keyword-parsing-refactor-tests]
last_updated: 2026-04-08
---

## Definition
A pattern where specific words in user input trigger different behavior, typically via substring/keyword matching in code.

## In This Context
The keyword detection being removed checked for "think" and "plan" substrings in user input to switch prompt templates. This caused false positives:
- "I plan to attack" → incorrectly → think mode
- "I think the guard is lying" → incorrectly → think mode

## Why It Was Removed
- False positives from innocent usage of words like "plan" and "think"
- LLM system instructions already know how to handle these commands
- Keyword matching is a ZFC violation — model should interpret intent

## Related Concepts
- [[IntentClassifier]] — semantic routing replaces keyword detection
- [[PromptTemplate]] — consistent template approach
- [[ZFC]] — Zero-Framework Cognition principle
