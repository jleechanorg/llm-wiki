---
title: "AI Directives"
type: concept
tags: [token-pattern, instruction-encoding, prompt-engineering]
sources: [narrative-sample-token-analysis]
last_updated: 2026-04-08
---

AI directives are high-level tokens that encode specific instructions for the LLM, such as behavior constraints, output format requirements, or meta-instructions about response style.

## Related Patterns
- Implemented through combination of [[MarkupTokens]], [[SpecialPunctuation]], and [[StateCommands]]
- Documented in [[GameStateInstructionTokens]]
- Analyzed for presence in narrative samples via deletion_tokens patterns
