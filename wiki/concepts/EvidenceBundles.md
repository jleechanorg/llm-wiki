---
title: "Evidence Bundles"
type: concept
tags: [evidence, testing, standards, provenance]
sources: [campaign-pagination-mcp-integration-test]
last_updated: 2026-04-08
---

## Summary
Evidence capture standard requiring request/response pairs with timestamps and provenance data per evidence-standards.md. Used in integration testing to verify API behavior.


## Key Characteristics
- Captures request/response pairs
- Includes timestamps for temporal tracking
- Provenance data for source identification
- Standards-compliant format per evidence-standards.md

## Related Concepts
- [MCProtocol](MCProtocol.md) — tool invocation
- [Firestore](Firestore.md) — backend storage

## Update 2026-06-27 — Dark Factory evidence envelopes

Dark Factory now treats evidence envelopes as the durable run proof, not as optional after-the-fact notes. Each run should expose command echo, events JSONL, CXDB source/extract hashes, `node_io.jsonl`, pipeline copy, per-node input/output refs, and transcript refs under `evidence/<run-id>/`.

Important distinction: bounded previews are acceptable for logs and indexes, but previews must not become the downstream LLM handoff. Coder/fix/reviewer nodes need either the full free-form output or complete file refs they can read.

Source: [Dark Factory reviewer/output/evidence contract and deterministic install smoke](../sources/project-2026-06-27-dark-factory-reviewer-output-evidence-contract.md).

## Update 2026-08-25 — secret-safe claim-scoped publication

When source evidence history contains credentials or identities, tip redaction
alone does not make direct historical blob links safe. Rebuild a canonical
claim-scoped publication from primary data, retain only required fields, label
raw versus derived versus authored artifacts, add a claim-to-artifact map and
explicit non-claims, bind every file with SHA-256, and secret-scan the hosted
copy. The PR should link one canonical head-bound evidence marker.

Source: [Autoscaling operating points need stochastic evidence and secret-safe publication](../sources/project-2026-08-25-autoscaling-operating-point-and-secret-safe-evidence.md).
