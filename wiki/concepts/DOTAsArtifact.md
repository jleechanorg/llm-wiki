---
title: "DOT as Artifact"
type: concept
tags: [attractor-pattern, graphviz, dot, pipeline, workflow-definition]
date: 2026-05-24
---
## Overview
The DOT-as-artifact pattern treats Graphviz DOT pipeline files as the durable, versionable, shareable product of a dark factory. The runner code is dorodango — polish, discard, rebuild from spec — but the .dot files encode the development process and are worth versioning and reviewing.

## Key Properties
- **What**: Standard Graphviz DOT syntax used to define LLM agent pipelines — which steps need an LLM, which need human gates, where to fork, what verification commands to run
- **Why matters**: DOT files are the blueprints; the factory implementations are the engines. Everyone shares the engine and hides the blueprints — but the pipelines are more interesting than the runners
- **Two styles**: (1) Tool-node pipelines (all shell commands, deterministic, zero token cost) vs (2) LLM-node pipelines (every step uses a model, expensive, nondeterministic). Best practice: combine both — deterministic tools for setup/validation, LLM nodes only where reasoning is needed
- **Model stylesheets**: CSS-like selectors that map node classes to LLM providers/models (e.g. `* { llm_model: claude-sonnet-4-5; } .code { llm_model: claude-opus-4-6; }`)

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[Kilroy]] | Runner | Generates DOT from English via `attractor ingest` |
| [[Mammoth]] | Runner | 21-rule DOT linter, 5-phase lifecycle |
| [[Tracker]] | Runner | Uses Dippin language (.dip) instead of raw DOT |
| [[DarkFactory]] | Repo | dark-factory runner parses DOT via pydot |

## Connection to Attractor Pattern
DOT files are the Attractor pattern's primary artifact. The question isn't how to build the factory anymore — it's what to build with it. Share your .dot files: "What does your 'audit a Rails app' pipeline look like?"

## See Also
- [[AttractorPattern]]
- [[Dorodango]]
- [[WorkflowEngine]]
