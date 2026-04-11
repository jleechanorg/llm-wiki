---
title: "Fake Services Unit Tests"
type: source
tags: [python, testing, fake-services, firestore, firebase-auth, llm-mocking]
source_file: "raw/test_fake_services.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests verifying fake service implementations (FakeFirebaseAuth, FakeFirestoreClient, create_fake_llm_client) work correctly in isolation without external dependencies. Tests cover basic operations, JSON serialization, and integration between services.

## Key Claims
- **Fake Firestore**: Supports document creation, retrieval, subcollections, and JSON serialization without Mock objects
- **Fake LLM**: Generates realistic JSON responses for campaign creation and story continuation prompts
- **Fake Auth**: Manages users, creates custom tokens, verifies tokens, and produces JSON-serializable user dictionaries
- **Integration**: All fake services work together — user creation, campaign storage, story generation, and story persistence

## Key Quotes
> "Verifies that fakes work correctly in isolation"

## Connections
- [[FakeFirestoreClient]] — core fake database implementation
- [[FakeFirebaseAuth]] — fake authentication service
- [[FakeLLMClient]] — fake LLM for testing
- [[FakeServicesPattern]] — testing methodology

## Contradictions
- None identified
