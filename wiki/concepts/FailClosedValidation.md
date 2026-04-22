---
title: "Fail-Closed Validation"
type: concept
tags: [fail-closed, validation, schema-registry, batch-discard]
date: 2026-04-15
---

## Overview

Fail-Closed Validation is a validation semantics where the entire batch is discarded if any message is invalid. Confluent Schema Registry implements this: "If a batch of messages is sent, and at least one is invalid, then the entire batch is discarded."

## Key Properties

- **Fail-closed**: Invalid content causes rejection, not just warning
- **Batch-level**: Entire batch is rejected together
- **vs fail-open**: Fail-open allows partial processing of invalid data
- **Consistency**: Guarantees all-or-nothing semantics

## Connection to Governance

Fail-closed validation is the model for PR #453's fail-closed merge semantics — if evidence is missing or Skeptic is SKIPPED, the PR fails closed (not merged with a warning). The validation gate rejects the entire PR, not just the failing check.

## See Also
- [[Confluent]]
- [[SchemaIDValidation]]
- [[SkepticGate]]