---
title: "Age Field Validation in Character Classes"
type: source
tags: [python, testing, unittest, pydantic, validation, character-schemas]
source_file: "raw/age-field-validation-character-classes.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file validating age field functionality in NPC and PlayerCharacter Pydantic schemas. Tests cover optional age field, boundary validation (0-50000), fantasy age support, and type enforcement.

## Key Claims
- **Optional Field**: age field defaults to None when not specified, allowing age-less characters
- **Boundary Validation**: Rejects negative ages and ages over 50,000 with ValidationError
- **Fantasy Ages**: Supports ages up to 50,000 for fantasy beings (elves, dragons, etc.)
- **Type Enforcement**: Only accepts integer values, rejects floats and strings

## Key Quotes
> "Test that negative ages are rejected" — validates lower boundary
> "Test that unreasonably high ages are rejected" — validates upper boundary of 50000

## Connections
- [[NPC]] — entity class being tested
- [[PlayerCharacter]] — entity class being tested
- [[Pydantic Validation]] — validation mechanism used

## Contradictions
- None identified
