---
title: "End2EndBaseTestCase"
type: entity
tags: [testing, base-class, unittest]
sources: []
last_updated: 2026-04-08
---

## Description
Base test case class in tests.test_end2end module providing common setup for end-to-end integration tests including app creation, authentication mocking, and test client configuration.

## Usage
Inherited by specific test classes like TestVisitCampaignEnd2End to provide consistent test infrastructure.

## Related
- [TestVisitCampaignEnd2End](TestVisitCampaignEnd2End.md) - test class inheriting from this
- [FakeFirestoreClient](FakeFirestoreClient.md) - mock Firestore client used in tests
