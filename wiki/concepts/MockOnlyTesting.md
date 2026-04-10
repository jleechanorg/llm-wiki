---
title: "Mock-Only Testing"
type: concept
tags: [testing, mocks, unit-testing]
sources: []
last_updated: 2026-04-08
---

## Definition
Traditional unit testing approach where all external dependencies are mocked via unittest.mock.patch. Tests only validate code behavior against mock responses without verifying real service integration.

## Limitations
- Cannot detect drift between mock implementation and actual API behavior
- No integration validation against real external services
- Requires manual maintenance as APIs evolve

## Migration Path
Upgrade to [[DualModeTesting]] using [[ServiceProviderPattern]] to enable both mock and real service testing from same test code.
