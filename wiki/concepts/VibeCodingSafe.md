---
title: "VibeCodingSafe"
type: concept
tags: [security, vibe-coding, benchmark, vulnerability]
sources: [vibe-coding-safe-paper]
last_updated: 2026-04-14
---

Security benchmark for vibe coding: human engineers instruct LLM agents with minimal supervision. Key finding: only 10.5% of functionally correct agent solutions are secure.

## Key Numbers

| Metric | Value |
|--------|-------|
| Functional Correctness | 61% |
| Security | 10.5% |
| Gap | 50.5 percentage points |

## The Problem

Vibe coding = human engineers instruct LLM agents to complete coding tasks with minimal supervision. Security strategies like vulnerability hints **cannot mitigate** these issues.

## SUSB VIBES Benchmark

- 200 real-world feature-request tasks from open-source projects
- Tests widely-used coding agents with frontier models
- Evaluates functional correctness AND security

## Connections

- Evidence for [[AgenticMuch]] adoption concerns — 22-28% using agents but only 10.5% secure
- [[ShadowsInTheCode]] — multi-agent security vulnerabilities
- [[ZeroFrameworkCognition]] — safety implications
