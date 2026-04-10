---
title: "End-to-End Testing"
type: concept
tags: [testing, methodology, integration]
sources: []
last_updated: 2026-04-08
---

## Description
Testing methodology that validates the entire application stack from user interface through backend services to database. End-to-end tests verify complete workflows by testing through all layers rather than isolated units.

## Characteristics
- Tests full request/response cycle
- Uses mocking for external dependencies (Firestore, auth)
- Requires TESTING_AUTH_BYPASS for auth-free testing
- Uses unittest framework with patch decorators

## Related
- [[FakeFirestoreClient]] - mocking strategy
- [[TestVisitCampaignEnd2End]] - example test
- [[IntegrationTesting]] - related concept
