---
title: "Prompt Engineering"
type: concept
tags: [llm, ai, prompt, engineering, best-practices]
sources: [prompt-variant-loading-system]
last_updated: 2026-04-08
---

## Definition

Prompt engineering is the discipline of crafting, organizing, and managing prompts for LLM interactions to achieve consistent, controllable outputs.

## Best Practices

- **Version control** — Store prompts in version-controlled files rather than injecting strings at runtime (see [[PromptVariantLoadingSystem]])
- **Explicit variants** — Use strategy-specific prompt variants instead of conditional string injection
- **Separation of concerns** — Keep prompt logic separate from application code
- **Testability** — Each prompt variant should be independently testable

## Anti-Patterns

- **Hidden string injection** — Dynamically injecting override strings at runtime (what this source replaces)
- **Hardcoded prompts** — Prompts embedded directly in source code rather than externalized

## Related Concepts

- [[SystemInstruction]] — High-level directives establishing AI role
- [[DiceStrategy]] — Configuration driving prompt variant selection
