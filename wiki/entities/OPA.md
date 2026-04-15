---
title: "OPA"
type: entity
tags: [policy-engine, rego, authorization, acl]
date: 2026-04-15
---

## Overview

OPA (Open Policy Agent) is a policy engine streamlining policy management across the stack. It uses Rego as its declarative policy language and decouples policy decisions from application code.

## Key Properties

- **License**: Apache 2.0
- **Policy language**: Rego (declarative, inspired by Datalog)
- **Key concepts**:
  - Rules: Define virtual documents with heads and bodies
  - Packages: Namespace grouping for safe sharing
  - Existentially quantified variables (serve as input AND output)
  - References: Dot-access or bracket notation for nested documents
  - Comprehensions: Composite values from sub-queries
  - Keywords: `some`, `every`, `with`, `default`, `in`
- **ACL example**:
  ```rego
  package authz
  default allow := false
  allow if user == "alice"
  ```
- **Decouples policy decisions from application code**

## Connections

- [[PolicyEngine]] — OPA is a policy engine using Rego
- [[Rego]] — OPA's policy language
- [[GovernanceLayer]] — OPA could serve as the policy engine for governance constraints

## See Also
- [[PolicyEngine]]
- [[Rego]]
- [[GovernanceLayer]]
