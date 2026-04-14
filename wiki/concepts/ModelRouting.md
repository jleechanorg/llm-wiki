---
title: "Model Routing"
type: concept
tags: [AI-models, cost-optimization, task-matching]
sources: [agent-loop-demo, openclaw-workshop-notes]
last_updated: 2026-04-08
---

## Definition

The practice of using different AI models for different tasks based on cost, capability, and token limits. No single LLM is suitable for every task.

## Model Selection Matrix

| Model | Strengths | Weaknesses | Best For |
|-------|-----------|------------|----------|
| [[Codex]] 5.3/5.4 | Highest intelligence, excellent reasoning | Expensive, rapid token consumption | Complex code reviews, architectural decisions |
| [[Claude]] | Quality review, evidence checking | Expensive | Review and quality assurance |
| [[Gemini]] Flash | Structured JSON, game state | Safety filters on creative | RPG mechanics, data extraction |
| [[Minimax]] | Cheap, repetitive tasks | Poor JSON adherence, drops fields | Volume work, initial drafts |
| [[Grok]] | Virtually uncensored | Less capable at pure coding | Creative narratives, unrestricted content |

## Cost Management Strategy

Monthly spend typically:
- Anthropic: ~$200
- Cursor: ~$60
- Minimax: ~$40
- Total: ~$300/month

## Smart Routing Rules

1. **Out of Credits?** Switch to cheaper model for non-critical tasks
2. **Complex Task?** Use Codex/Claude with evidence review
3. **Volume Work?** Use Minimax for initial drafts
4. **Creative/RPG?** Use Grok for uncensored creativity
5. **Structured Data?** Use Gemini Flash for JSON

## The Claude Team Pattern

Use Claude team with Minimax model:
- Gets volume done fast and cheap
- Loop with dumb model, fix with smart model
- Evidence review uses smarter model

## Connections

- [[EvidenceReview]] — Secondary review step
- [[Parallelization]] — Multiple agents, multiple models
- [[ReasoningBudget]] — model routing and reasoning budget are complementary adaptive allocation strategies: routing selects which model, budget controls how much compute that model uses
- [[HarnessEngineering]] — a harness implements model routing as part of its dispatch logic
- [[AgenticCoding]] — agentic coding systems benefit from routing tasks to appropriate models
- [[AdaptiveComputation]] — model routing is a form of adaptive computation at the model-selection level
