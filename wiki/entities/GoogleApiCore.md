---
title: "GoogleApiCore"
type: entity
tags: [library, google-cloud, exceptions]
sources: [firestore-service-database-error-handling-tests]
last_updated: 2026-04-08
---

GoogleApiCore is Google's Python library for API error handling. Provides exception classes like DeadlineExceeded, ServiceUnavailable, and Unauthenticated used in the Firestore error handling tests.

## Exception Types Used
- `DeadlineExceeded` — connection timeout
- `ServiceUnavailable` — connection refused
- `Unauthenticated` — token expiry
- `Aborted` — transaction conflict
