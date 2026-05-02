---
title: Process Reward Models
type: concept
tags: [prm, reward-model, process-supervision, outcome-supervision]
date: 2026-04-23
sources: [chimera-p13-findings]
---

## Definition
Process Reward Models (PRMs) reward the quality of reasoning steps, not just the final output. Contrast with Outcome Reward Models (ORMs) which score only the result regardless of how it was derived.

## ORM vs PRM Distinction
- **ORMs:** Reward outcomes regardless of reasoning quality. For tasks where output quality is determinable without inspecting reasoning (factual recall, simple classification), ORMs are sufficient.
- **PRMs:** Reward step-by-step reasoning quality. For multi-step tasks (mathematical reasoning, logical deduction), PRMs outperform because correct reasoning steps are necessary for correct output.

## Key Research
Lightman et al., "Let the Modeling Fit the Job," BAIR, 2023 — https://arxiv.org/abs/2308.12538

## Chimera Connection
Extended Thinking (auto-research Cycle B) outperformed Single by +16-29 points on medium/complex tasks — consistent with PRM research showing process supervision helps on multi-step tasks.

Mode selection should be based on query complexity:
- Low complexity (single-step, factual) → Single (ORM-style)
- Medium complexity (multi-step, verifiable) → Fixed (single critic, PRM-light)
- High complexity (multi-perspective domain) → GNN 3-perspective (full PRM-style)

## Rubric Implication
Current 20-anchor rubric is outcome-focused. Adding process anchors that track reasoning step quality would help PRM-style modes demonstrate their advantage more clearly.