---
title: "JSDOM"
type: entity
tags: [library, testing, javascript, dom]
sources: [sophisticated-wizard-test-jsdom]
last_updated: 2026-04-08
---

## Summary
JavaScript library that provides a DOM implementation for Node.js, enabling browser environment simulation in server-side tests. Used by the sophisticated wizard test to create a realistic browser context without requiring a real browser.

## Key Features
- Pure JavaScript DOM implementation
- Simulates browser APIs (window, document, navigator)
- Supports CSS selector queries
- Enables headless DOM manipulation testing

## Connections
- [[SophisticatedWizardTestJsdom]] — uses JSDOM for browser simulation
- [[RedGreenTDD]] — methodology for the test using JSDOM
