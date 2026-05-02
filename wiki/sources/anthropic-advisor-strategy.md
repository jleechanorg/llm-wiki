---
title: "The Advisor Strategy: Give Agents an Intelligence Boost"
type: source
tags: [advisor-strategy, multi-agent, opus, sonnet, executor-advisor, anthropic, cost-optimization]
date: 2026-04-01
source_file: https://claude.com/blog/the-advisor-strategy
---

## Summary
Anthropic's advisor tool pairs Opus as a server-side advisor alongside Sonnet or Haiku as the executor. Sonnet handles most tasks independently, calling on Opus only when it hits a decision it cannot resolve. This inverts the sub-agent pattern — no decomposition, no worker pool, no orchestration. Results: +2.7pp on SWE-bench Multilingual at 11.9% lower cost per task.

## Key Claims
- **Executor decides when to invoke advisor** — no orchestration logic required; the executor calls Opus only when it "hits a decision it can't reasonably solve"
- **Advisor inverts sub-agent pattern**: no decomposition, no worker pool, no orchestration — a smaller cost-effective model drives and escalates only when frontier-level reasoning is needed
- **Opus acts as server-side advisor**: never calls tools, never produces user-facing output, returns plans/corrections/stop signals
- **Advisor tokens are 400–700 text tokens**, keeping overall cost well below running Opus end-to-end
- **Sonnet + Opus advisor**: +2.7pp on SWE-bench, 11.9% lower cost per task vs Sonnet alone
- **Haiku + Opus advisor**: 41.2% on BrowseComp (more than double Haiku solo's 19.7%), trailing Sonnet solo by 29% in score but costing 85% less per task
- Eric Simmons (Bolt CEO): *"It makes better architectural decisions on complex tasks while adding no overhead on simple ones."*

## Key Quotes
> "Sonnet or Haiku runs the task end-to-end as the executor, calling tools, reading results, and iterating toward a solution. When the executor hits a decision it can't reasonably solve, it consults Opus for guidance as the advisor. Opus accesses the shared context and returns a plan, a correction, or a stop signal, and the executor resumes."

## Implementation Details
- Beta header: `anthropic-beta: advisor-tool-2026-03-01`
- Declare `advisor_20260301` in the tools array alongside other tools
- Set `max_uses` to cap advisor calls per request
- Executor tokens billed at executor rates; advisor tokens at Opus rates

## Connections
- [[ExecutorAdvisorPattern]] — the architectural pattern from this source
- [[AdvisorStrategy]] — the specific Anthropic implementation
- [[OpusAsAdvisor]] — Opus as the advisor model
- [[CostOptimization]] — cost benefits of advisor over running Opus end-to-end
