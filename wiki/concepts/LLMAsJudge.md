---
title: "LLM-as-Judge"
type: concept
tags: [evaluation, llm-as-judge, rubric, quality-scoring]
sources: [project-chimera-neural-network-llm-agents-2026-04-19]
last_updated: 2026-04-19
---

## Definition

Using a separate LLM to evaluate and score outputs from other systems or agents. In Project Chimera, a dedicated GPT-5.4 instance serves as judge using a 5-dimension rubric.

## Chimera's 5-Dimension Rubric

| Dimension | Weight |
|-----------|--------|
| Factual Accuracy | 30% |
| Comprehensiveness & Depth | 25% |
| Clarity & Structure | 20% |
| Usefulness | 15% |
| Efficiency | 10% |

## Connections

- [[ProjectChimera]] uses LLM-as-Judge as its evaluation layer
- Related to [[CanonicalCodeScorer]] which applies similar rubric-based evaluation in the auto-research context
- Quality Gate in Chimera is a specific instantiation
