---
title: "Agentic Verification of Software Systems"
type: source
tags: [formal-verification, agentic, Coq, Rocq, theorem-prover, FSE-2026]
sources: []
date: 2025-11-21
source_file: raw/arxiv-2511.17330-agentic-verification.md
---

## Summary

AutoRocq: LLM agent that iteratively communicates with Rocq (Coq) theorem prover for feedback. Unlike prior work requiring extensive proof training, AutoRocq learns on-the-fly. Published at FSE 2026.

## Key Claims

- AI agents can reason about AI-generated code using mathematical/formal methods
- AutoRocq learns and improves **on-the-fly** without extensive proof training
- "Generate and validate loop" integration advances trusted automatic programming

## Technique/Method

- **AutoRocq**: LLM agent communicating with **Rocq (formerly Coq)** theorem prover
- Iterative refinement loop: agent generates, prover validates, agent improves
- Evaluated on **SV-COMP benchmarks** and **Linux kernel modules**

## Connections

- Related to [[CompilerVerification]] — formal verification of code
- [[SelfDebugging]] extends self-correction to correctness verification
- [[AgentMentor]] uses execution logs for corrective instructions
