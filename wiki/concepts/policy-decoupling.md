---
title: "Policy Decoupling"
type: concept
tags: [opa, architecture, policy-engine, separation-of-concerns]
sources: [https://www.openpolicyagent.org/docs/latest/]
last_updated: 2026-04-19
---

## Overview
Policy decoupling is the architectural pattern of separating policy decision-making from policy enforcement — the policy engine (OPA) provides answers to "what should happen?" while the application or infrastructure layer decides whether to act on them. This is the OPA-core insight: input comes in as JSON, policy evaluates, structured decision comes out, application enforces.

## Key Properties
- **Decision/Enforcement split**: Policy engine decides; application enforces
- **JSON query API**: Policy evaluated by sending structured input; result is structured output
- **Fail-closed default**: `default allow := false` — unknown states default to denial
- **Hot reload**: Policies loaded on the fly without service restart

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| OPA | Policy engine | Canonical implementation of policy decoupling |
| Envoy/Istio | Service mesh | Enforces OPA decisions at proxy layer |
| Kubernetes admission | Enforcement point | OPA Gatekeeper enforces at K8s API layer |

## Connection to ZFC Level-Up Architecture
ZFC Level-Up Architecture applies the same principle: the model (LLM) decides level-up facts; `rewards_engine.py` validates and formats. The backend formats like OPA evaluates — purely mechanical transformation of structured input to structured output, no semantic judgment.

## See Also
- [[OPA]]
- [[Rego]]
- [[Fail-Closed]]
- [[ZFC-Level-Up-Architecture]]