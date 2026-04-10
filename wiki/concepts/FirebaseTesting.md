---
title: "Firebase Testing"
type: concept
tags: [firebase, testing, firestore, authentication, google-cloud]
sources: [fake-services-unit-tests]
last_updated: 2026-04-08
---

Testing strategies for Firebase-based applications, specifically using fake implementations of Firestore and Firebase Authentication.

## Components
- **Firestore**: NoSQL database with document/collection hierarchy
- **Authentication**: User management, custom tokens, ID token verification

## Testing Approaches
1. **Fake services**: In-memory implementations matching API surface
2. **Firebase Emulator**: Official Firebase local emulation
3. **Mock objects**: Test-specific mocking frameworks

## Best Practices
- Use fake services for unit tests (fast, isolated)
- Use emulator for integration tests (closer to production)
- Ensure JSON-serializable output for downstream compatibility

## Connected To
- [[FakeFirestoreClient]] — test implementation
- [[FakeFirebaseAuth]] — test implementation
- [[GoogleCloudPlatform]] — underlying cloud provider
