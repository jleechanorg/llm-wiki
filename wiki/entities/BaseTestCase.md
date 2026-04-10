---
title: "BaseTestCase"
type: entity
tags: [python, testing, unittest]
sources: ["real-mode-testing-framework-integration-validation"]
last_updated: 2026-04-08
---

Base test case class providing standardized fixtures for both mock and real mode testing. Provides access to firestore, gemini, auth services and is_real mode indicator.

## Attributes
- **firestore**: Firestore service instance (mock or real)
- **gemini**: Gemini service instance (mock or real)
- **auth**: Auth service instance (mock or real)
- **is_real**: Boolean indicating current test mode
- **test_firestore**: Legacy compatibility attribute
- **test_gemini**: Legacy compatibility attribute
- **test_auth**: Legacy compatibility attribute
- **is_real_mode**: Legacy compatibility attribute
