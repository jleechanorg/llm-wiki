---
title: "Interface Testing"
type: concept
tags: [testing, unit-tests, interface]
sources: ["real-service-provider-tests"]
last_updated: 2026-04-08
---

Unit testing approach verifying a class implements a specific interface contract. Tests check that RealServiceProvider is an instance of TestServiceProvider and implements all required methods.

## Test Patterns
- isinstance() checks for interface compliance
- Method existence verification
- Return type validation
- Exception handling for missing dependencies

## Related
- [[TestServiceProvider]] — interface being tested
- [[RealServiceProvider]] — class under test
