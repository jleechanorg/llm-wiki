---
title: "Firebase Credentials"
type: concept
tags: [firebase, testing, authentication, credentials]
sources: ["common-test-utilities"]
last_updated: 2026-04-08
---

## Definition
Firebase credentials are authentication keys and configuration that grant access to Firebase services (Firestore, Authentication, Storage, etc.).

## Role in Testing
In test environments, Firebase credentials should be unavailable to ensure tests use mocked services rather than making real API calls. The `has_firebase_credentials()` utility enforces this by returning `False`.

## Related Concepts
- [[MockedServices]] — Test doubles that replace real Firebase interactions
- [[FirebaseAuthentication]] — Firebase Auth service
- [[Firestore]] — Firebase NoSQL database

## Sources
- [[CommonTestUtilities]]
