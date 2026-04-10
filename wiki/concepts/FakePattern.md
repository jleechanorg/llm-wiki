---
title: "Fake Pattern"
type: concept
tags: [testing, test-doubles, mock-vs-fake]
sources: ["fake-firestore-testing.md", "fake-firebase-auth-service-for-testing.md", "fake-llm-service-for-testing.md"]
last_updated: 2026-04-08
---

## Definition
The Fake pattern is a testing approach where test doubles behave like real objects rather than merely verifying call assertions. Unlike Mocks, Fakes are stateful and return realistic data structures.

## Key Characteristics
- **Stateful**: Maintains internal state across method calls
- **Realistic responses**: Returns fully-populated objects matching real interfaces
- **Behavioral simulation**: Behaves like the real implementation, not just stubbed responses
- **Deep copy semantics**: Data is independent after "persistence" to catch post-write mutations

## Applications in WorldArchitect.AI
- [[Fake Firestore Implementation]] — FakeFirestoreDocument with deep copy semantics
- [[Realistic Firebase Auth test doubles]] — FakeUserRecord, FakeDecodedToken, FakeFirebaseAuth
- [[Fake LLM Service for Testing]] — FakeLLMResponse, FakeModelAdapter with response templates
- [[Service Provider Factory for Tests]] — factory for switching between fake/real/capture modes

## Why Fake Over Mock
Mock objects can pass tests but fail in production due to JSON serialization differences. Fakes return the exact data structures the application expects, catching bugs that mocks miss.
