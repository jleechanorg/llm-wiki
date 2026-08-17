---
title: "Systematic Debugging (Phase 1: Build a Feedback Loop)"
type: concept
tags: [debugging, methodology, engineering-discipline]
date: 2026-08-16
---

## Definition

A discipline for hard bugs structured in phases, the first and most important of
which is building a **tight feedback loop** — a fast, deterministic, red-capable
reproduction of the bug — before generating hypotheses or writing a fix. A loop
is tight when it (a) drives the actual bug code path and can catch the specific
symptom, (b) is deterministic (or has a pinned, high reproduction rate for
non-deterministic bugs), (c) is fast (seconds, not minutes), and (d) is
agent-runnable without a human in the loop.

Later phases (reproduce+minimize, hypothesize, instrument, fix+regression-test,
cleanup) all consume this loop rather than substituting for it — bisection,
hypothesis testing, and instrumentation are mechanical once a tight loop exists.

## Applied to live LLM-behavior bugs

For bugs in how a hosted LLM API behaves (wrong finish reason, runaway tool
loop, garbled structured output, model-version-specific regression), Phase 1
means writing a minimal standalone script against the *real* API/SDK — outside
the application — that reproduces the failure on the simplest possible input,
and a comparison script that reproduces the *working* case on the identical
input. Only then should complexity be added one variable at a time until the
exact trigger is isolated.

Crucially, this must happen **before** reaching for external research or
multi-model second-opinion tools when direct API access exists and reproduction
is cheap. Those tools are upper-bounded by what has already been documented
publicly; an undocumented interaction between two SDK config fields on a
specific model version can only be found by running the experiment. See
[[LLM-behavior bugs need direct ablation, not research fan-out]] for a concrete case where a full research
round (6 independent LLM reads, including two real browser-grounded searches)
missed a bug's actual trigger that a 30-line ablation script found in minutes.

## Connections

- [[Root-Cause-First]] — the "why" behind refusing to hypothesize/patch before
  a real reproduction exists
- [[LLM-behavior bugs need direct ablation, not research fan-out]] — the incident that validated this
  method for live model-behavior bugs specifically
- [[Gemini]], [[GeminiAPI]] — the system under investigation in that incident
