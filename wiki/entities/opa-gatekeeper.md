---
title: "OPA Gatekeeper"
type: entity
tags: [opa, kubernetes, admission-control, policy-engine]
sources: [https://open-policy-agent.github.io/gatekeeper/]
last_updated: 2026-04-19
---

## Overview
OPA Gatekeeper is a CNCF project that integrates OPA with Kubernetes admission control. It enables Kubernetes to enforce OPA policies on pod creation and resource modifications through a webhook admission controller. Gatekeeper adds constraint templates — parameterized Rego policies that can be instantiated per namespace or cluster — to OPA's basic API-server query model.

## Key Properties
- **CNCF project**: Graduated under CNCF alongside OPA
- **Constraint templates**: Parameterized Rego policies reusable across namespaces
- **Admission controller**: Webhook intercepts Kubernetes API requests before mutation
- **Audit**: Periodically evaluates existing resources against policies (not just mutation-time)

## Connections
- [[OPA]] — Gatekeeper is a specialized OPA deployment targeting Kubernetes
- [[Kubernetes-RBAC]] — Gatekeeper complements RBAC with policy-level enforcement beyond identity
- [[OPA-Constraint-Templates]] — the constraint template pattern Gatekeeper enables
- [[Policy-as-Code]] — constraint templates are policy-as-code for K8s workloads

## See Also
- [[OPA]]
- [[Kubernetes-RBAC]]
- [[OPA-Constraint-Templates]]
- [[Policy-as-Code]]
