---
title: "Policy Engine"
type: concept
tags: [policy, authorization, acl, rego, opa]
date: 2026-04-15
---

## Overview

A policy engine decouples policy decisions from application code. Policy engines like OPA (Open Policy Agent) evaluate declarative policies against request context to produce allow/deny decisions.

## Key Systems

| System | Policy Language | Key Use |
|--------|-----------------|---------|
| [[OPA]] | Rego | General-purpose policy engine |
| [[Constitutional AI]] | Constitutional principles | AI safety/alignment |
| [[ConstitutionalClassifiers]] | Principle-based | Output filtering |

## OPA Architecture

OPA uses Rego as its policy language:
- **Rules**: Define virtual documents with heads and bodies
- **Packages**: Namespace grouping for safe sharing
- **References**: Dot-access or bracket notation for nested documents
- **Comprehensions**: Composite values from sub-queries

```rego
package authz
default allow := false
allow if user == "alice"
```

## Policy Engine vs Governance Layer

A policy engine is a runtime *mechanism* for evaluating constraints. The governance layer is the *constitution* — the set of policies that should be enforced. PR #453 proposes a YAML Policy Engine as a component of the governance layer.

## See Also
- [[OPA]]
- [[Rego]]
- [[GovernanceLayer]]
- [[ConstitutionalAI]]
