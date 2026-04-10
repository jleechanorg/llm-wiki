---
title: "FakeLLMResponse"
type: entity
tags: [testing, mock, llm]
sources: [timeline-log-budget-end2end-tests]
last_updated: 2026-04-08
---

Mock LLM response generator for end-to-end testing. Located at mvp_site.tests.fake_llm. Provides synthetic LLM responses for testing prompt handling and response parsing without calling real LLM APIs.

## Used In
- [[Timeline Log Budget End-to-End Tests]] — for narrative/entities response mocking
- [[Think Mode End-to-End Tests]] — for think mode response handling
- [[Spicy Mode Toggle E2E Tests]] — for model switching validation

## Connections
- [[FakeFirestoreClient]] — paired mock for Firestore
- [[End2EndBaseTestCase]] — base class using this mock
