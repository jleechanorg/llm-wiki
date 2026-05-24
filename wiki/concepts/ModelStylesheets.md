---
title: "Model Stylesheets"
type: concept
tags: [attractor-pattern, css, model-routing, configuration]
date: 2026-05-24
---
## Overview
Model stylesheets are a CSS-like configuration system that maps node classes to LLM providers and models in DOT pipeline files. They allow declarative, per-node model selection without hardcoding backend choices in the pipeline logic.

## Key Properties
- **What**: CSS-like selectors embedded in DOT graph attributes that route nodes to specific LLM providers/models
- **Why matters**: Separates model selection from pipeline logic; changes model routing without modifying pipeline structure; enables cost optimization (cheap model for planning, expensive model for code)
- **Syntax**: `* { llm_model: claude-sonnet-4-5; llm_provider: anthropic; } .code { llm_model: claude-opus-4-6; }`
- **Origin**: Mammoth's build_pong.dot example introduced the pattern; Tracker's Dippin language uses `model:` and `provider:` per-node attributes

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[Mammoth]] | Runner | Introduced model stylesheets in build_pong.dot |
| [[Kilroy]] | Runner | Uses run.yaml provider config with per-node model attributes |
| [[AttractorPattern]] | Pattern | Backends are swappable per run; never hardcode in .dot |

## Connection to Attractor Pattern
Model stylesheets embody the Attractor pattern's principle that backends must be swappable per run and never hardcoded in DOT files or handlers. The stylesheet is configuration, not logic — separation of concerns at the model selection level.

## See Also
- [[DOTAsArtifact]]
- [[AttractorPattern]]
- [[Mammoth]]
