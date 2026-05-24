---
title: "Model Stylesheet"
type: concept
tags: [attractor, kilroy, model-routing, css]
date: 2026-05-24
---

## Overview

A CSS-like model routing system for DOT pipeline files, implemented in [[Kilroy]]. Allows per-node LLM provider and model configuration using CSS specificity rules, replacing hardcoded backend selection with declarative routing.

## Syntax

```dot
* { llm_provider: openai; }
.code { llm_model: claude-opus-4-6; }
#review { reasoning_effort: high; }
box { llm_provider: anthropic; }
```

## Specificity Rules

| Selector | Specificity | Example | Matches |
|---|---|---|---|
| Universal `*` | 0 | `* { llm_provider: openai; }` | All nodes |
| Shape | 1 | `box { ... }` | Nodes with `shape=box` |
| Class `.` | 2 | `.code { ... }` | Nodes with `class="code"` |
| ID `#` | 3 | `#review { ... }` | Node named `review` |

Higher specificity wins. Ties resolved by last declaration (cascade order).

## Properties

- `llm_provider` — which LLM service to call (openai, anthropic, gemini)
- `llm_model` — which model within the provider (claude-opus-4-6, gpt-5.4)
- `reasoning_effort` — reasoning depth (low, medium, high)
- `temperature` — sampling temperature
- `max_tokens` — output token limit

## vs Alternatives

| Approach | Used By | Flexibility |
|---|---|---|
| Model stylesheet (CSS-like) | [[Kilroy]] | Per-node, specificity-based, cascade |
| `--backend` flag | dark-factory | Per-run only, single backend |
| Provider catalog | [[Smasher]] | Per-pipeline, programmatic selection |

## Connections

- [[Kilroy]] — Implementation
- [[AttractorPattern]] — The pattern that uses model routing