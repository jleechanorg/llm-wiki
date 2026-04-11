---
title: "Spicy Mode Toggle End-to-End Tests"
type: source
tags: [e2e, testing, settings, openrouter, grok, python, flask]
source_file: "raw/spicy-mode-toggle-e2e-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end tests validating the complete spicy mode toggle flow: enabling switches to Grok on OpenRouter, disabling restores previous model/provider, and settings persist across enable/disable cycles.

## Key Claims
- **Enable Switches to Grok**: Enabling spicy mode switches llm_provider to "openrouter" with SPICY_OPENROUTER_MODEL
- **Preserves Pre-Spicy State**: Enabling saves pre_spicy_model and pre_spicy_provider for later restoration
- **Disable Restores Settings**: Disabling spicy mode restores the previous model and provider from saved values
- **Persistence Verified**: Settings API correctly saves and retrieves spicy_mode, llm_provider, and openrouter_model

## Test Functions
- `test_enable_spicy_mode_switches_to_grok` — validates provider/model switch on enable
- `test_disable_spicy_mode_restores_previous_model` — validates restoration on disable

## Connections
- [[spicy-mode]] — the feature being tested
- [[openrouter]] — provider used for Grok
- [[grok-model]] — model activated in spicy mode
- [[settings-persistence]] — concept of saving/restoring settings
