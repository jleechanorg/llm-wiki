---
title: "Data Integrity Validation"
type: concept
tags: [testing, data-validation, corruption-detection, firestore]
sources: [data-integrity-test-suite]
last_updated: 2026-04-08
---

## Definition

Data integrity validation is the practice of verifying that data structures maintain their expected form and type throughout application operations. It catches corruption bugs where objects are unexpectedly converted to strings, lists become dicts, or nested structures are flattened incorrectly.

## Key Principles

1. **Type Enforcement**: Data fields must maintain their documented type (dict, list, string)
2. **Runtime Validation**: Validate data after each transformation or update operation
3. **Fail-Fast on Corruption**: Detect corruption immediately rather than allowing it to propagate


## Application in World AI

In the World AI system, data integrity validation is critical for:
- **NPC Data**: NPCs must always be dictionaries with expected fields (name, type, relationship, hp)
- **State Updates**: The `update_state_with_changes` function must preserve nested structure
- **Game State**: GameState objects must maintain consistent schema across saves

## Related Concepts

- [[FirestoreService]] — handles state persistence where integrity matters
- [[GameState]] — domain object requiring integrity guarantees
- [[RegressionTesting]] — catching integrity bugs before they reach production
