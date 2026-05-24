---
title: "Failure Dossier"
type: concept
tags: [attractor, kilroy, failure-analysis, retry]
date: 2026-05-24
---

## Overview

Per-stage structured failure analysis system implemented in [[Kilroy]]. Classifies every node failure into one of 6 categories, each with distinct retry and escalation semantics. Provides the taxonomy that dark-factory's Healer approximates via unsupervised clustering.

## 6-Class Failure Taxonomy

| Class | Description | Retryable | Escalation |
|---|---|---|---|
| `transient_infra` | Network timeout, rate limit, service unavailable | Yes (default) | No — retry same model |
| `budget_exhausted` | Token/cost budget exceeded for node or pipeline | No | Yes — escalate to cheaper/faster model |
| `compilation_loop` | Agent repeatedly produces same broken code | No | Yes — escalate to stronger model |
| `deterministic` | Same input always produces same wrong output | No | No — retrying won't help |
| `canceled` | Human or system explicitly canceled execution | No | No |
| `structural` | Pipeline graph is invalid (missing edges, unreachable nodes) | No | No — requires DOT fix |

## Retry Gating

Only `transient_infra` is retryable by default. This is a critical design decision: naive retry of `budget_exhausted` or `compilation_loop` wastes tokens and time. Instead, these trigger model escalation.

## Model Escalation

When a node fails with `budget_exhausted` or `compilation_loop`:

```dot
fix [escalation_models="anthropic:claude-opus-4-6,openai:gpt-5.4"]
```

The node escalates through the chain on each failure, trying progressively different (or stronger) models.

## vs dark-factory Healer

| Feature | Failure Dossier (Kilroy) | Healer (dark-factory) |
|---|---|---|
| Classification | 6 predefined classes | Unsupervised clustering by (node, outcome, output_hash) |
| Retry gating | Only transient_infra retryable | max_retries/max_visits on all failures |
| Model escalation | Built-in per-node | No equivalent |
| Timing | Synchronous, per-failure | Asynchronous, post-hoc |
| Prescription | Class-based rules | LLM-generated from cluster patterns |

The Healer is more flexible (discovers novel failure patterns) but less actionable (no automatic retry gating or model escalation).

## Connections

- [[Kilroy]] — Implementation
- [[AttractorPattern]] — The pattern that uses failure classification