---
title: "AgentBench"
type: concept
tags: [benchmark, agent-evaluation, decision-making, multi-environment]
sources: [agentbench-paper]
last_updated: 2026-04-14
---

Multi-dimensional benchmark with 8 distinct environments for assessing LLM-as-Agent reasoning and decision-making. ICLR 2024. Key finding: commercial LLMs significantly outperform open-source competitors ≤70B.

## Environments

8 evaluation environments covering:
- Operating systems
- Databases
- Knowledge graphs
- And others...

## Key Findings

1. **Commercial models ahead**: GPT-4, Claude significantly ahead of open-source ≤70B
2. **Main obstacles**: poor long-term reasoning, decision-making, instruction following
3. **Code training**: "ambivalent impacts" — helps some agent tasks, not all

## Connections

- Related to [[EvoEval]] — benchmark integrity concerns
- Related to [[OpenHands]] — evaluation platform
- Evidence for coding agent capability gaps
