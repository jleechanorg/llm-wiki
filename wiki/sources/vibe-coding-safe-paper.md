---
title: "Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code"
type: source
tags: [security, vibe-coding, benchmark, vulnerability, coding-agent]
sources: []
date: 2025-12-02
source_file: raw/arxiv-2512.03262-vibe-coding-safe.md
---

## Summary

Benchmarks vulnerability of agent-generated code. Created SUSB VIBES benchmark with 200 real-world tasks. While 61% of SWE-Agent + Claude 4 Sonnet solutions are functionally correct, only 10.5% are secure. Security strategies like vulnerability hints cannot mitigate these issues.

## Key Claims

- **61%** functional correctness for SWE-Agent + Claude 4 Sonnet
- Only **10.5%** are secure
- Security strategies like vulnerability hints "cannot mitigate these security issues"

## Method

- Created **SUSB VIBES benchmark**: 200 real-world software engineering tasks
- Evaluated multiple widely-used coding agents with frontier models
- Tested preliminary security strategies (vulnerability hints augmentation)

## Connections

- Evidence for security concerns in [[AgenticMuch]] adoption study
- Related to [[ShadowsInTheCode]] — security risks in multi-agent development
- Relevant to [[ZeroFrameworkCognition]]
