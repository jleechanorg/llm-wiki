---
title: "Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code"
type: paper
tags: [security, vibe-coding, benchmark, vulnerability, coding-agent]
date: 2025-12-02
arxiv_url: https://arxiv.org/abs/2512.03262
---

## Summary

Benchmarks vulnerability of agent-generated code in real-world tasks. Created SUSB VIBES benchmark with 200 feature-request tasks from real-world open-source projects. While 61% of SWE-Agent + Claude 4 Sonnet solutions are functionally correct, only 10.5% are secure. Security strategies like vulnerability hints cannot mitigate these issues.

## Key Claims

- **61%** functional correctness for SWE-Agent + Claude 4 Sonnet
- Only **10.5%** are secure
- Security strategies like vulnerability hints "cannot mitigate these security issues"
- Vibe coding: human engineers instruct LLM agents with minimal supervision

## Method

- Created **SUSB VIBES benchmark**: 200 real-world software engineering tasks
- Evaluated multiple widely-used coding agents with frontier models
- Tested preliminary security strategies (vulnerability hints augmentation)

## Results

- Agents perform poorly in software security
- Functional correctness ≠ security
- Security interventions failed to improve outcomes

## Connections

- Evidence for security concerns in [[AgenticMuch]] adoption study
- Related to [[ShadowsInTheCode]] — security risks in multi-agent development
- Relevant to [[ZeroFrameworkCognition]] — safety considerations
