---
title: "Rego"
type: entity
tags: [opa, policy-language, rego, cloud-native]
sources: [https://www.openpolicyagent.org/docs/latest/]
last_updated: 2026-04-19
---

## Overview
Rego (pronounced "ray-go") is OPA's purpose-built policy language for expressing policies over complex hierarchical data structures including JSON. It supports both boolean allow/deny decisions and arbitrary structured output — not just yes/no, but generates the full response payload. This makes it directly analogous to structured level-up JSON output in game logic.

## Key Properties
- **High-level declarative**: Rego policies read like business rules, not algorithm
- **Structured output**: Unlike boolean-only languages, Rego generates arbitrary data structures
- **Iteration**: `some ... in ...` for existential quantification over collections
- **Universal quantification**: `every` keyword for all-quantified policy expressions
- **Fail-closed default**: `default allow := false` is the canonical deny-by-default pattern

## Connections
- [[OPA]] — Rego is the policy language of the OPA engine
- [[OPA-Rego-Policy-Language]] — the concept page for Rego's policy semantics
- [[Policy-Decoupling]] — Rego separates policy from application code
- [[OPA-Bundle-Signing]] — Rego policies can be signed and verified via OPA bundles

## See Also
- [[OPA]]
- [[Policy-Decoupling]]
- [[OPA-Rego-Policy-Language]]
