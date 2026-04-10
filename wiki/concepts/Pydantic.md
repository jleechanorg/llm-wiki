---
title: "Pydantic"
type: concept
tags: [validation, python, library, schema]
sources: [pydantic-validation-entity-tracking-tests]
last_updated: 2026-04-08
---

## Description
Python data validation library using Python type annotations to define schemas. Used in entity_tracking module to validate game state structures.

## Key Features
- Type coercion from strings to typed values
- Validation on model creation
- Default value handling
- Nested model support

## Usage in Wiki
- [[entity_tracking]] uses Pydantic for SceneManifest validation
- VALIDATION_TYPE constant = "Pydantic"

## Related Concepts
- [[DefensiveNumericConverter]] — complementary type handling
- [[SceneManifest]] — Pydantic model using this validation
