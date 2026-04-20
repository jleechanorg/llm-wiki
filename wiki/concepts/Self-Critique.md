---
title: "Self-Critique"
type: concept
tags: [ai-self-improvement, alignment, constitutional-ai, model-reasoning, zfc]
sources: [Constitutional AI (Anthropic, 2022)]
last_updated: 2026-04-19
---

## Overview

Self-critique is the mechanism where an AI model evaluates its own outputs against a set of principles or criteria, identifies flaws or gaps, and revises the output before returning it. Constitutional AI (CAI) is the canonical implementation: the model generates both the response and a self-critique against a constitutional set of principles, then revises based on the critique. The result is a model that flags its own uncertainty rather than presenting every output as confident truth.

## Key Properties

- **Model critiques its own output**: Not a separate critique model — the same model evaluates against principles
- **Constitutional principles as criteria**: A written constitution of rules the model checks itself against
- **Chain-of-thought for transparency**: Critique reasoning is explicit, making failures traceable
- **Revision pass**: Model revises the initial output based on what the critique identified
- **Structured output option**: Self-critique can be structured (a `caveats` field) rather than free text

## Related Systems

| System | Type | Relevance |
|--------|------|-----------|
| Constitutional AI | Anthropic implementation | Self-critique against constitutional principles |
| RLAIF | AI feedback technique | AI preference model as critic — structural self-critique |
| Debate | Alignment technique | Adversarial critique as truth-seeking mechanism |
| Model-as-Judge | Architecture | Self-critique as the "why" behind a model's decision |
| Recursive Reward Modeling | Scalable oversight | AI assists in evaluating AI — recursive self-critique |

## Connection to ZFC Level-Up Architecture

In the ZFC Level-Up design, the `caveats` field in `level_up_signal` is a structured self-critique:

```json
{
  "level_up_signal": {
    "level_up": true,
    "new_level": 5,
    "caveats": "ASI choice competitive with Extra Attack; player is Fighter 3/Sorcerer 2 — treating as class_feature per prompt priority, but spell slot progression may outweigh melee at level 5."
  }
}
```

The `caveats` field serves three purposes:

1. **Explicit uncertainty**: The model surfaces what it wasn't sure about rather than hiding behind a confident boolean
2. **Audit trail**: When a level-up decision goes wrong, `caveats` explains the model's reasoning path
3. **Stricter validation signal**: The formatter uses non-empty `caveats` with `level_up=true` as a signal to apply stricter validation or log for human review

## Key Quote

> "The only human oversight is provided through a list of rules or principles" while the model itself generates "self-critiques and revisions." — Constitutional AI (Anthropic, 2022)

## Canonical Pattern: CAI Two-Phase

**Phase 1 (Critique)**: Model receives initial response + constitutional principles → generates critique identifying violations
**Phase 2 (Revision)**: Model revises response based on critique → revised output is returned

The two phases can be:
- **Explicit** (two separate model calls): Initial response → critique → revision
- **Implicit** (single call): Model generates response with critique embedded in structured fields like `caveats`

WorldArchitect.AI's `caveats` field uses the implicit pattern: the model produces `level_up_signal` with an embedded `caveats` explanation in a single response, rather than a separate critique pass.

## Why Self-Critique Matters for AI Safety

1. **Transparency**: Chain-of-thought critique makes reasoning explicit and auditable
2. **Scalable oversight**: Model flags its own issues — reduces human review burden
3. **Corrigibility**: Self-critical model accepts corrections rather than presenting every output as confident
4. **Uncertainty surfacing**: Model explicitly marks what it was unsure about rather than defaulting to false confidence

## See Also

- [[Constitutional-AI]] — the canonical self-critique implementation
- [[RLAIF]] — AI feedback as critique mechanism
- [[Debate]] — adversarial critique as truth-seeking
- [[Model-as-Judge]] — where self-critique fits in the decision architecture
- [[Corrigibility]] — alignment property enabled by self-critique
- [[ZFC-Level-Up-Architecture]] — WorldArchitect's specific self-critique application via `caveats` field
