---
title: "Fake Firebase Auth Service for Testing"
type: source
tags: [python, testing, firebase, authentication, mock, fake-objects]
source_file: "raw/fake-firebase-auth-service-for-testing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing realistic Firebase Authentication responses for testing environments. Implements the "Fake" pattern (stateful test double) versus traditional "Mock" pattern, returning fully-populated user records and decoded tokens instead of mock objects.

## Key Claims
- **Fake Pattern**: Stateful test doubles that behave like real objects, not just verifying call assertions
- **Complete Token Lifecycle**: FakeDecodedToken implements full token interface with claims, expiry, and dictionary-style access
- **User Management API**: Mirrors Firebase Admin SDK methods (get_user, get_user_by_email, create_user, update_user)
- **Error Handling**: FakeAuthError with Firebase-like error codes (user-not-found, uid-already-exists)

## Key Classes
- **FakeUserRecord**: UID, email, display_name, metadata (creationTime, lastSignInTime), customClaims, providerData
- **FakeDecodedToken**: Token claims including aud, iss, iat, exp, auth_time, sub + custom claims
- **FakeAuthError**: Firebase-style error codes and messages
- **FakeFirebaseAuth**: In-memory user and token storage with CRUD operations

## Connections
- [[ServiceProviderFactory]] — likely integration point for test provider selection
- [[EntityValidatorShim]] — similar pattern of providing backward compatibility

## Contradictions
- None identified
