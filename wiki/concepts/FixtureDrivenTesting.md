---
title: "Fixture-Driven Testing"
type: concept
tags: [tdd, testing, fixtures]
sources: ["modal-routing-fixtures", "modal-state-management-test-utilities"]
last_updated: 2026-04-08
---

## Definition
A testing approach where test scenarios are defined in external data files (JSON) rather than hardcoded in test methods.

## Benefits
- Non-developers can add test scenarios by editing JSON
- Scenarios are machine-checkable and version-controllable
- Enables declarative specification of test cases
- Separates test data from test logic

## Implementation
- Test loads scenarios from JSON file (e.g., `modal_routing_fixtures.json`)
- Each scenario includes: name, description, state, user_input, expect
- Test iterates over scenarios, applying each to validate behavior

## Related Concepts
- [[TDD]] — Test-Driven Development
- [[InvariantTesting]] — testing system invariants rather than implementation details
