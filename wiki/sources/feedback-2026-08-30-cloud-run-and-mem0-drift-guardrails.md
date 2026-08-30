---
title: "Cloud Run and Mem0 drift require executable and live-state guardrails"
type: source
tags: [cloud-run, mem0, sdk-drift, live-state, fail-closed]
date: 2026-08-30
source_file: raw/feedback_2026-08-30_cloud_run_and_mem0_drift_guardrails.md
bead: rev-67fm6
---

## Summary

WorldArchitect.AI's repository policy correctly restored minimum-instance defaults, but four already-deployed preview services remained warm until live Cloud Run remediation. In the same session, Mem0's dependencies appeared healthy while a stale SDK call failed behind a blanket exception handler, then an invalid configured Groq credential silently discarded inferred writes. The combined lesson is that configuration changes require live-state enumeration, dependency health checks must execute the real operation, and extraction-auth failures need a bounded `infer=False` preservation path.

## Key Claims

- Cloud Run capacity changes need both an exact-name repository enforcement test and a post-change enumeration of live services.
- Only `mvp-site-app-dev` and `mvp-site-app-stable` may default to one minimum instance; preview, staging, experiment, ad-hoc, and unknown services must default to zero.
- Mem0 health requires a real semantic search using the installed SDK signature, not imports, Qdrant readiness, or `Memory.from_config()` alone.
- Every Mem0 client boundary needs a compatibility test for its SDK call shape, and fail-open hooks must expose bounded diagnostics instead of swallowing exceptions.
- `/ms` is a file-backed recovery path and does not prove Mem0 recall works.
- Credential presence does not prove credential health; `401 invalid_api_key` must be surfaced, and an extraction-auth failure must preserve a bounded direct memory with `infer=False` rather than silently dropping the write.
- jleechanclaw PR #841, commit `e614e005d2ad9fe640f31a21881739a452799aab`, implemented the bounded authentication fallback; two tests and a real add/search canary verified it.

## Key Quotes

> "A merged default does not prove existing revisions were remediated."

> "Fail-open hooks may not fail silently. Preserve prompt execution, but emit the exception type and message to stderr or a bounded diagnostic log."

> "Credential presence is not credential health."

## Connections

- [[WorldArchitectAI]] — PR #9586 restored the repository's exact-name minimum-instance policy.
- [[CloudRun]] — the four warm preview services required live remediation after the policy merged.
- [[RepositoryDefaultsDoNotRemediateLiveState]] — configuration correctness and deployed-state correctness are independent proofs.
- [[Mem0HelperFiles]] — the recall hook used a stale `search()` call shape and swallowed the resulting error.
- [[Mem0QdrantDeployment]] — infrastructure readiness is necessary but insufficient for recall health.
- [[ExecutableDependencyHealthChecks]] — health probes must exercise the actual read-only capability.
- [[SilentFailurePathPattern]] — blanket exception suppression hid the SDK incompatibility.
