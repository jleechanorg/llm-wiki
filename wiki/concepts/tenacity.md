---
title: "Tenacity"
type: concept
tags: [python, retry, reliability, llm-api, multi-agent-systems]
date: 2026-04-21
---

## Overview

Tenacity is an Apache 2.0 Python retry library with configurable wait strategies (fixed, exponential, jitter), stop conditions, and async support. Used in multi-agent systems for LLM API reliability.

## Key Properties

- **Stop conditions**: `stop_after_attempt(N)`, `stop_after_delay(S)`
- **Wait strategies**: `wait_fixed(S)`, `wait_exponential(min, max)`, `wait_random_exponential`, `wait_chain`
- **Retry on**: any exception type or return-value based condition
- **Async**: full support for `async def`

## Relevance to Chimera

Chimera benchmark had 33-93% error rates on MiniMax API. Tenacity-style exponential backoff (1s→2s→4s with jitter) would improve reliability. Currently Chimera uses manual retry in `call_minimax`.

## See Also

- [[MultiAgentOrchestration]] — coordination patterns that need retry logic
- [[ProjectChimera]] — benchmark with retry implementation
- [[AgentBench]] — multi-agent evaluation framework
