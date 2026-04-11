---
title: "jeffrey-oracle-cost"
type: synthesis
tags: [jeffrey, oracle, cost, model-selection, optimization]
sources: [jeffrey-oracle, JeffreyTechStack, ModelRouting]
last_updated: 2026-04-11
---

# Jeffrey Oracle: Cost Optimization

Specialized oracle for cost consciousness: model selection, API spending, token budgets, and cost-competent automation.

## When Jeffrey Evaluates Cost

| Situation | Jeffrey's Response |
|-----------|-------------------|
| Model choice: routine task | Minimax — cheap, appropriate for volume work |
| Model choice: complex task | Anthropic/Claude — worth the cost for quality |
| Model choice: structured JSON | Gemini Flash — cheap + good JSON adherence |
| New API call in hot path | Token budget impact? Context compaction needed? |
| New automation script | Minimax for the script invocation itself |
| Anthropic call without justification | "Is this necessary? Can minimax handle it?" |
| Preview model to production set | Conditional — [[Preview-Model-Risk]] — flag medium risk |
| Budget-based feature decision | Budget allocation before adding features |
| Cost spike without explanation | Investigate: which model? which task? |

## Model Selection Principles (from wiki)

- **Minimax for volume/routine** — M2.5 at $40/month vs Anthropic at $200/month (ModelRouting)
- **Anthropic for quality** — Code review, evidence verification, complex reasoning
- **Claude team pattern** — Loop with cheap model, fix with smart model (ModelRouting)
- **Cost is a feature** — Minimax integrated as default for cost-conscious tasks (JeffreyTechStack)

## Jeffrey's Cost Triggers

- `minimax` not considered for bulk operations → "minimax for this"
- Anthropic used for tasks Minimax could handle → "unnecessary spend"
- Preview model added to security-critical sets → conditional, require risk acknowledgment
- New API endpoint with unbounded token usage → token budget enforcement required
- Automation without cost accounting → "what's the monthly cost?"
- High token consumption without compaction strategy → Context-Bloat investigation

## Cost Decision Tree

1. Is this a routine/volume task? → Minimax
2. Does it require quality review or complex reasoning? → Anthropic/Claude
3. Does it need structured JSON output? → Gemini Flash
4. Is it a creative/uncensored task? → Grok
5. Does it touch security-critical paths? → Conditional + risk acknowledgment
6. Can existing context budget handle it? → Check TokenBudgeting

## Parent Oracle
[[jeffrey-oracle]] — the full decision framework
