---
title: "OPA Partial Rules"
type: concept
tags: [opa, rego, policy-evaluation, query]
sources: [https://www.openpolicyagent.org/docs/latest/]
last_updated: 2026-04-19
---

## Overview
OPA Rego supports both complete rules (fully evaluated when all variables are bound) and partial rules (evaluated when some variables remain unbound, returning a set of bindings that satisfy the rule). Partial evaluation generates policy templates — the policy engine produces the rule structure with unbound variables; runtime inputs instantiate the concrete values.

## Key Properties
- **Complete rules**: Fully evaluated; all variables bound
- **Partial rules**: Some variables unbound; returns bindings set
- **Template generation**: Partial eval produces reusable policy templates
- **Runtime instantiation**: Input data fills unbound variables at query time
- **Structural output**: Not just boolean — partial rules can return structured data

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| OPA | Policy engine | Partial eval is a core Rego feature |
| OPA Gatekeeper | K8s admission | Uses partial rules to generate constraint templates |
| Regal | Rego linter | Checks partial rule correctness |

## Connection to ZFC Level-Up Architecture
OPA's partial rules returning unbound templates that instantiate at runtime is directly analogous to the ZFC model-output schema: the schema defines the structure (`level_up`, `new_level`, `previous_turn_exp`), the model provides the concrete values at response time. The backend (formatter) performs the instantiation.

## See Also
- [[Rego]]
- [[OPA]]
- [[OPA-Constraint-Templates]]
- [[ZFC-Level-Up-Architecture]]