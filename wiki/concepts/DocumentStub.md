---
title: "Document Stub"
type: concept
tags: [testing, mock-object, dom-simulation, test-doubles]
sources: [settings-context-test-utilities]
last_updated: 2026-04-08
---

## Definition
Partial JavaScript document implementation for test environments that provides minimal DOM query capabilities without a full browser.

## Implemented Methods
- **getElementById(id)** — Returns element by ID from elements map
- **querySelector(selector)** — Returns first matching element (supports radio button checked query)
- **querySelectorAll(selector)** — Returns array of matching elements
- **addEventListener(event, handler)** — Registers document-level event handlers
- **visibilityState** — Property for page visibility simulation

## Usage Context
Used in [[SettingsContextTestUtilities]] to simulate the document object when testing settings page interactions in Node.js test environment.
