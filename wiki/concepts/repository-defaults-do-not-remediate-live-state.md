---
title: "Repository defaults do not remediate live state"
type: concept
tags: [deployment, cloud-run, live-state, configuration-drift, verification]
sources: [sources/feedback-2026-08-30-cloud-run-and-mem0-drift-guardrails.md]
last_updated: 2026-08-30
---

## Definition

A corrected repository default governs future configuration generation but does not necessarily mutate already-deployed resources. Configuration correctness and live-state correctness therefore require separate evidence.

## Verification Contract

1. Test the repository policy, including exact allowed names and a fail-safe default for unknown names.
2. Apply explicit remediation to existing resources that violate the policy.
3. Enumerate the complete live resource set after remediation and compare every item with the intended invariant.

For WorldArchitect.AI Cloud Run capacity, only `mvp-site-app-dev` and `mvp-site-app-stable` may default to `min-instances=1`; every preview, staging, experiment, ad-hoc, and unknown service defaults to zero. PR #9586 fixed the repository policy, while `mvp-site-app-s1`, `s3`, `s4`, and `s5` still required live updates before all 22 preview services enumerated at zero.

## Connections

- [[CloudRun]] — the deployment platform where repository and live revision state diverged.
- [[WorldArchitectAI]] — the affected application and policy owner.
- [[EndStateLayerPrinciple]] — tool/configuration success and user-visible end state are distinct proof layers.
- [[ExecutableDependencyHealthChecks]] — the same two-layer principle applied to dependency readiness.
