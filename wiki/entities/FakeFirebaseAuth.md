---
title: "FakeFirebaseAuth"
type: entity
tags: [testing, firebase, authentication, fake-service]
sources: [fake-services-unit-tests]
last_updated: 2026-04-08
---

A fake implementation of Firebase Authentication for testing purposes. Provides user management, custom token creation, and token verification.

## Purpose
Enables isolated testing of Firebase Auth-dependent code without connecting to actual Firebase backend.

## Key Capabilities
- Default user retrieval
- User creation with custom UID, email, display name
- Custom token creation and verification
- JSON-serializable user dictionaries

## Connected To
- [[FakeFirestoreClient]] — often used together
- [[FakeLLMClient]] — complete fake backend stack
- [[FirebaseTesting]] — testing patterns
