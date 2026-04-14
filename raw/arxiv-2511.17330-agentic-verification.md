---
title: "Agentic Verification of Software Systems"
type: paper
tags: [formal-verification, agentic, Coq, Rocq, theorem-prover, FSE-2026]
date: 2025-11-21
arxiv_url: https://arxiv.org/abs/2511.17330
---

## Summary

AI agents can reason about AI-generated code using mathematical/formal methods. AutoRocq is an LLM agent that iteratively communicates with the Rocq (Coq) theorem prover for feedback and context. Unlike prior work requiring extensive LLM training on proof examples, AutoRocq learns and improves on-the-fly. Published at FSE 2026.

## Key Claims

- AI agents can reason about large volumes of AI-generated code using mathematical/formal methods
- Unlike prior work, AutoRocq learns and improves **on-the-fly** without extensive proof training
- "Generate and validate loop" integration with coding agents could advance trusted automatic programming

## Technique/Method

- **AutoRocq**: LLM agent communicating with **Rocq (formerly Coq)** theorem prover
- Iterative refinement loop: agent generates, prover validates, agent improves
- Autonomous collaboration between proof agent and theorem prover

## Results

- Evaluated on **SV-COMP benchmarks** and **Linux kernel modules**
- "Promising efficacy in achieving automated program verification"
- FSE 2026 publication

## Connections

- Related to [[CompilerVerification]] — formal verification of code
- [[SelfDebugging]] extends self-correction to correctness verification
- [[AgentMentor]] uses execution logs for corrective instructions
