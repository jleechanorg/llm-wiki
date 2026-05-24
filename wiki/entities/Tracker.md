---
title: "Tracker"
type: entity
tags: [attractor-pattern, pipeline-runner, go, orchestration, dippin]
date: 2026-05-24
---
## Overview
Tracker is 2389 Research's Go pipeline orchestration engine for multi-agent LLM workflows. It defines pipelines in `.dip` files (Dippin language), executes with parallel agents, and provides a TUI dashboard. A simpler weekend-scale implementation that still converges on the same three-layer architecture.

## Key Properties
- **Type**: Pipeline orchestration engine (Go)
- **Key features**: Dippin language (.dip files), `.dipx` bundles, built-in workflows, interview-mode human gates, manager_loop supervisor, declarative structured output (writes:/reads:), cost accounting, Cloudflare AI Gateway support
- **Source**: https://github.com/2389-research/tracker
- **Node types**: agent, human, tool, parallel, fan_in, subgraph, manager_loop, conditional
- **Built-in workflows**: ask_and_execute, build_product, build_product_with_superspec, deep_review
- **Provider support**: Anthropic, OpenAI, Gemini, OpenAI-compat

## Connections
- [[2389Research]] — 2389 Research built Tracker
- [[Mammoth]] — Mammoth uses Tracker for pipeline execution
- [[AttractorPattern]] — Tracker converges on the attractor architecture
- [[DippinLanguage]] — Tracker pipelines are defined in the Dippin language

## See Also
- [[2389Research]]
- [[Mammoth]]
- [[AttractorPattern]]
