---
title: "OPA Constraint Templates"
type: concept
tags: [opa, kubernetes, gatekeeper, policy-template]
sources: [https://open-policy-agent.github.io/gatekeeper/]
last_updated: 2026-04-19
---

## Overview
OPA Gatekeeper's constraint templates are parameterized Rego policies that can be instantiated with different inputs at runtime — reusable policy schemas where the namespace or cluster name fills in the parameters. Templates enable one policy definition to produce different enforcement outcomes across multiple targets without code changes: write once, instantiate per namespace.

## Key Properties
- **Parameterized Rego**: Template defines structure; runtime inputs fill parameters
- **Namespace-scoped**: Same template, different values per namespace or cluster
- **Audit mode**: Constraint templates can evaluate existing resources not just admission mutations
- **CRD-based**: Gatekeeper uses Kubernetes Custom Resource Definitions to define templates
- **Partial evaluation**: Gatekeeper uses OPA partial rules to generate the constraint template

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| OPA Gatekeeper | K8s admission | Constraint templates are Gatekeeper's defining feature |
| Partial-Rules | Rego feature | Gatekeeper uses partial rule evaluation to generate templates |
| Kubernetes RBAC | Identity enforcement | Gatekeeper complements identity with policy enforcement |
| OPA Constraint Templates | Concept | The parameterized policy pattern |

## Connection to ZFC Level-Up Architecture
Constraint templates' pattern — write policy once, instantiate with different runtime data — maps to the ZFC `level_up_signal` schema: define the structure (`level_up`, `new_level`, `previous_turn_exp`, `current_turn_exp`) once; the model provides values per response. The formatter is the constraint template engine that instantiates the policy with the model's provided values.

## See Also
- [[OPA-Gatekeeper]]
- [[Partial-Rules]]
- [[OPA]]
- [[ZFC-Level-Up-Architecture]]
