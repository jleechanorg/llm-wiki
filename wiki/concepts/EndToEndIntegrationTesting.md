---
title: "End-to-End Integration Testing"
type: concept
tags: [testing, integration, e2e, python, unittest]
sources: [npc-death-state-persistence-e2e-tests]
last_updated: 2026-04-08
---

## Description
Testing methodology that validates the complete application stack from API endpoints through all service layers, testing the full flow of requests and responses without mocking internal components.

## Key Characteristics
- Tests complete request/response cycle
- Only mocks external services (LLM providers, Firestore DB) at lowest level
- Uses Flask test client for HTTP request simulation
- Verifies end-to-end behavior across all layers

## Connection to E2E Tests
- [[NPC Death State Persistence E2E Tests]] — end-to-end test for death state persistence
- [[End2EndBaseTestCase]] — base class providing test infrastructure
- [[FakeFirestoreClient]], [[FakeLLMResponse]] — external service mocks
