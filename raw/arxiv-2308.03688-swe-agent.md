---
title: "Agentless: Demystifying LLM-based Software Engineering Tasks"
type: paper
tags: [coding-agent, SWE-bench, no-code-agent, benchmark]
date: 2024-03-14
arxiv_url: https://arxiv.org/abs/2403.19114
---

## Summary
Agentless is a paper that challenges the assumption that sophisticated multi-agent architectures are necessary for software engineering tasks. It demonstrates that simple, "agentless" approaches — often just single-prompt or two-stage methods — can achieve competitive or superior results on SWE-bench and similar benchmarks. The work questions the complexity being added by multi-agent frameworks.

## Key Claims
- Simple approaches match or exceed complex multi-agent systems on SWE-bench
- "Agentless" (single-prompt) methods can be surprisingly effective for code repair
- Multi-agent overhead may not justify the complexity for many SE tasks
- Challenge to the prevailing assumption that more agent complexity = better results

## Technique/Method
- Single-prompt or two-stage approaches vs. multi-agent chains
- Direct prompt engineering with sufficient context
- Simple retrieval-augmented approaches
- Minimal tool use compared to sophisticated agent frameworks

## Results
- Competitive performance on SWE-bench compared to multi-agent approaches
- Lower compute cost and simpler infrastructure
- Faster execution due to reduced round-trips

## Limitations
- May not generalize to more complex, open-ended SE tasks
- Benchmark performance ≠ real-world software engineering capability
- Single-prompt approaches may struggle with multi-file understanding

## Connections
- Challenges [[Voyager]] and [[MetaGPT]] complexity assumptions
- Relevant to harness cost/benefit analysis
- Evidence for simplicity preference in coding agent design
- Connects to [[Harness5LayerModel]] L3 (Execution) decisions
