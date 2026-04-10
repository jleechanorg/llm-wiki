---
title: "Mocking (Software Testing)"
type: concept
tags: [testing, mocking, test-doubles, unittest]
sources: ["world-logic-module-structure-tests"]
last_updated: 2026-04-08
---

## Definition
Mocking is a technique in software testing where real objects are replaced with test doubles that simulate the behavior of real dependencies. This enables isolated testing without external services.

## Application in This Source
The test file demonstrates comprehensive mocking of:
- firebase_admin and its submodules (firestore, auth)
- pydantic (BaseModel, Field, ValidationError)
- cachetools (TTLCache, cached)
- google.genai (Client)
- docx, fpdf, flask

This allows testing world_logic.py without requiring actual Firebase or external service connections.

## Related Concepts
- [[UnitTesting]] — testing methodology
- [[TestDrivenDevelopment]] — development approach
- [[Firebase]] — mocked service
