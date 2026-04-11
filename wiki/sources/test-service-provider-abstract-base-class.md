---
title: "Test Service Provider Abstract Base Class"
type: source
tags: [testing, abstract-base-class, service-abstraction, mock-services, real-services, firestore, gemini, authentication]
source_file: "raw/test-service-provider-abstract-base-class.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python abstract base class defining the interface for switching between mock and real service implementations. Enables test isolation while supporting both mocked and live service backends for Firestore, Gemini AI, and authentication.

## Key Claims
- **ABC Interface Pattern** — TestServiceProvider defines abstract methods for service client access
- **Dual-Mode Testing** — supports both mock and real service backends via the same interface
- **Three Service Types** — Firestore (database), Gemini (LLM), and Auth (authentication)
- **Cleanup Lifecycle** — abstract cleanup() method ensures test isolation
- **Runtime Detection** — is_real_service property indicates current backend mode

## Interface Methods

| Method | Return Type | Purpose |
|--------|------------|----------|
| get_firestore() | Any | Firestore client (mock or real) |
| get_gemini() | Any | Gemini client (mock or real) |
| get_auth() | Any | Auth service (mock or real) |
| cleanup() | None | Clean up resources after test |
| is_real_service | bool | Runtime backend mode detection |

## Connections
- [[Real Service Provider Implementation]] — concrete implementation using actual Firestore/Gemini APIs
- [[Integration Tests with Real API Calls]] — uses real services for end-to-end testing
- [[Pytest Integration for Real-Mode Testing Framework]] — pytest fixtures leveraging this pattern

## Contradictions
- None identified
