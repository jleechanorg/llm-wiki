---
title: "Spicy Mode Toggle"
type: concept
tags: [feature, settings, model-switching, state-restoration]
sources: [spicy-mode-toggle-e2e-tests]
last_updated: 2026-04-08
---

## Description
A feature toggle pattern that switches between LLM providers while preserving the previous state for restoration. The toggle saves pre-spicy settings before switching and restores them when disabled.

## Flow
1. **Enable**: Save current model/provider → switch to Grok/OpenRouter → set spicy_mode=True
2. **Disable**: Read saved pre_spicy settings → restore model/provider → set spicy_mode=False

## Related Tests
- [[spicy-mode-toggle-e2e-tests]] — validates toggle behavior

## Related Entities
- [[SpicyMode]] — the feature itself
- [[OpenRouter]] — provider used in spicy mode
- [[Grok]] — model activated in spicy mode
