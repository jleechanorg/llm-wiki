---
title: "Model-as-Judge"
type: concept
tags: [zfc, model-computes, ai-judgment, alignment, scalable-oversight]
sources: [Constitutional AI (Anthropic), RLHF/RLAIF scalable oversight literature]
last_updated: 2026-04-19
---

## Overview

Model-as-Judge is the architectural pattern where an AI model makes semantic decisions — what something means, whether it applies, which option to choose — and a downstream system enforces those decisions fail-closed. The judge model outputs structured decisions; the enforcer (backend) validates format and applies policy, but does not re-decide the semantic question. This is the core ZFC pattern: model computes, backend formats.

## Key Properties

- **Semantic decisions delegated to model**: The model decides intent, classification, truthfulness, level-up availability — anything requiring judgment of meaning or context.
- **Structured decision output**: Model outputs machine-readable structured data (not free text that needs parsing), e.g., `{level_up: true, new_level: 5, choices: [...]}`.
- **Backend is pure formatter/enforcer**: Backend validates format, applies fail-closed rules, renders UI — does not re-evaluate the semantic decision.
- **Fail-closed enforcement**: When model output is malformed, the formatter rejects it — not even a "reasonable default" is substituted.
- **Self-critique as structured output**: Model explains its own reasoning gaps via a `caveats` field — what it couldn't do, what confused it, what judgment calls it made.

## Related Systems

| System | Type | Relevance |
|--------|------|-----------|
| Constitutional AI | Anthropic method | Model self-critique against principles — Model-as-Judge precursor |
| RLAIF | Technique | AI preference model judges outputs — structural Model-as-Judge |
| OPA/Rego | Policy engine | Policy decides; application enforces — identical architectural pattern |
| NVIDIA Fail-Safe Guardrails | Production pattern | Out-of-band action interception — enforcer fail-closed on model's decisions |
| CIRL | Mathematical framework | Machine uncertain over human reward — Model-as-Judge alignment rationale |

## Canonical Examples from WorldArchitect.AI

### Level-Up Signal (ZFC)
```json
{
  "level_up_signal": {
    "level_up": true,
    "new_level": 5,
    "previous_turn_exp": 6200,
    "current_turn_exp": 6500,
    "choices": [{"type": "class_feature", "description": "Extra Attack"}],
    "caveats": "ASI choice competitive with Extra Attack; player is Fighter 3/Sorcerer 2 — spell slot progression may outweigh melee option at level 5."
  }
}
```
Model computes level-up decision + self-critique; `rewards_engine.format_model_level_up_signal()` validates and formats only.

### OPA Rego (Infrastructure Parallel)
```rego
default allow := false
allow if {
    count(violation) == 0
    somekv := input.key
    violation[kv.key]
}
```
OPA decides "allow"; Kubernetes enforces. OPA may also generate structured remediation data, not just boolean.

## Why Model-as-Judge Works

1. **Brittleness of keyword/heuristic judgment**: Hardcoded rules miss edge cases; model handles context
2. **Drift of developer assumptions**: What "level-up available" means evolves; model adapts
3. **Scalable oversight**: Model evaluates more game state per turn than backend threshold math could
4. **Auditability**: Structured output is traceable; keyword checks are not
5. **Corrigibility at data level**: Backend fail-closed rules can reject bad model output — the system corrigibly rejects malformed decisions

## ZFC Invariant

> **Model-as-Judge does not mean Model-as-Authority-without-checks.** The backend's fail-closed formatter is the corrector. When the model outputs `{level_up: true}` without `new_level`, the formatter returns `(None, None)` — it corrects the model, not blindly accepts it.

## See Also

- [[ZFC-Level-Up-Architecture]] — the WorldArchitect implementation of Model-as-Judge for level-up
- [[Constitutional-AI]] — self-critique as the mechanism for Model-as-Judge alignment
- [[RLAIF]] — AI preference model as judge in the RLAIF/RLAIF framework
- [[Fail-Closed]] — formatter enforcement as the "corrector" in Model-as-Judge
- [[Corrigibility]] — alignment property that allows the system to correct model output
- [[Self-Critique]] — the mechanism (model critiques its own reasoning)
- [[OPA]] — infrastructure-level Model-as-Judge: OPA decides, application enforces
