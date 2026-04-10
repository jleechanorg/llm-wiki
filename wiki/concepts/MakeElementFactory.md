---
title: "MakeElement Factory"
type: concept
tags: [testing, mock-object, dom-simulation, factory-pattern]
sources: [settings-context-test-utilities]
last_updated: 2026-04-08
---

## Definition
JavaScript factory function that creates mock DOM elements with standardized properties and methods for automated testing.

## Key Properties
- **id** — Element identifier
- **handlers** — Event handler storage object
- **value** — Input value property
- **textContent** — Text content property
- **type** — Input type (text, checkbox, etc.)
- **checked** — Checkbox/radio selection state
- **disabled** — Disabled state
- **style** — CSS style object
- **dataset** — Data attribute storage

## Key Methods
- **addEventListener(event, handler)** — Register event handler
- **removeEventListener(event)** — Unregister event handler
- **dispatchEvent(event)** — Trigger event handler
- **click()** — Simulate click event
- **focus()** — Simulate focus event
- **blur()** — Simulate blur event

## Usage Context
Used in [[SettingsContextTestUtilities]] to build test contexts for settings page UI testing without requiring a real browser environment.
