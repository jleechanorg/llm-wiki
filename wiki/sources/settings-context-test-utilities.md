---
title: "Settings Context Test Utilities"
type: source
tags: [testing, javascript, mock-objects, dom-simulation, settings-page, api-keys, model-selection]
source_file: "raw/settings-context-test-utilities.md"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript test utilities providing mock DOM element factories for settings page testing. Creates simulated HTML elements (inputs, buttons, selects) with event handling, classList manipulation, and element state for automated testing without a real browser.

## Key Claims
- **makeElement Factory** — Creates mock DOM elements with id, handlers, value, textContent, type, checked, disabled, style, dataset properties
- **classList Mock** — Implements add, remove, toggle, contains methods for CSS class manipulation on mock elements
- **Event Simulation** — addEventListener, removeEventListener, dispatchEvent, click, focus, blur methods for user interaction simulation
- **buildSettingsContext** — Constructs comprehensive test context with all settings page elements (API keys, model selectors, provider radios, status indicators)
- **Document Stub** — Partial document implementation with getElementById, querySelector, querySelectorAll for test isolation

## Key Elements Created
- API Key inputs: geminiApiKey, openrouterApiKey, cerebrasApiKey
- Model selectors: geminiModel, openrouterModel, cerebrasModel, openclawGatewayUrl/Port/Token
- Provider radios: providerGemini, providerOpenrouter, providerOpenclaw
- Status indicators: gemini-key-status, openrouter-key-status, cerebras-key-status
- Action buttons: testOpenclawConnection, save-message, error-message

## Connections
- [[SessionHeaderUtilities]] — Related testing utilities for game state handling
- [[TestServiceProviderAbstractBaseClass]] — Python test infrastructure pattern
- [[PytestConfiguration]] — Testing framework configuration

## Contradictions
- []
