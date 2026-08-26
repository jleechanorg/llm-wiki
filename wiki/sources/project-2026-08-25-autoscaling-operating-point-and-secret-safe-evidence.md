---
title: "Autoscaling operating points need stochastic evidence and secret-safe publication"
type: source
tags: [worldarchitect-ai, cloud-run, autoscaling, concurrency, evidence, security]
date: 2026-08-25
source_file: raw/project_2026-08-25_autoscaling-operating-point-and-secret-safe-evidence.md
---

## Summary

WorldArchitect Cloud Run trials established that concurrency-driven
autoscaling works, while falsifying the stronger claim that one scalar
concurrency deterministically triggers it. The operational result is a
dev-only CPU8/concurrency180/Gunicorn180 learning profile, backed by a
sanitized claim-scoped evidence bundle rather than credential-bearing Git
history.

## Key Claims

- A clean target-171 trial scaled 1 to 2 with 2,185/2,185 successful terminals,
  concurrency recommendation 2, and CPU recommendation 1.
- Five comparable authenticated target-180 trials all reached two instances;
  pooled load-driver terminal error was 27/10,066 (0.268%).
- Identical 165/171 target loads produced different outcomes, so a
  deterministic scalar threshold was not proven.
- Fleet-wide concurrency and per-instance concurrency are different claims.
- Aggressive capacity settings should remain environment-scoped until
  memory-heavy request classes are tested.
- Evidence should be republished from primary data with explicit provenance
  and redaction when the source branch history contains credentials.

## Connections

- [[cloud-run-autoscaling]] — the platform behavior and operating-point rule.
- [[EvidenceBundles]] — sanitized claim-scoped publication and integrity.
- [[EmpiricalConcurrencyVerification]] — primary data over naming or offered load.
- [[worldarchitect.ai]] — affected system.

## Oracle impact

This technical workflow learning does not affect [[jeffrey-oracle]].

