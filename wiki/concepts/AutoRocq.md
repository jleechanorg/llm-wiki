---
title: "AutoRocq"
type: concept
tags: [formal-verification, agentic, Coq, Rocq, theorem-prover]
sources: [agentic-verification-paper]
last_updated: 2026-04-14
---

LLM agent for automated program verification that iteratively communicates with Rocq (Coq) theorem prover. FSE 2026.

## Key Insight

> Unlike prior work requiring extensive LLM training on proof examples, AutoRocq learns and improves **on-the-fly**.

## The Verify Loop

```
LLM Agent → Rocq Prover → Feedback → LLM Agent → ...
```

## Connections

- Related to [[CompilerVerification]] — CompCert, CakeML proofs
- [[SelfDebugging]] — extends self-correction to correctness
- [[AgentMentor]] — execution feedback for improvement
