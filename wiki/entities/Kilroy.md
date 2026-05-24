---
title: "Kilroy"
type: entity
tags: [attractor-pattern, pipeline-runner, go, dark-factory]
date: 2026-05-24
---
## Overview
Kilroy is a local-first Go CLI for running StrongDM-style Attractor pipelines, built by Dan Shapiro. It supports English-to-DOT ingestion, graph validation, isolated worktree execution, and CXDB-based checkpoint recovery.

## Key Properties
- **Type**: Attractor pipeline runner (Go)
- **Key features**: English-to-DOT ingestion, graph validation, worktree isolation, CXDB checkpoints, multi-provider (OpenAI/Anthropic/Google/Kimi/ZAI/Minimax/Cerebras)
- **Source**: https://github.com/danshapiro/kilroy
- **Stars**: 201
- **Commands**: `attractor ingest`, `attractor validate`, `attractor run`, `attractor resume`, `attractor status`, `attractor stop`
- **HTTP mode**: Experimental REST API with SSE for real-time progress

## Connections
- [[DanShapiro]] — Shapiro built Kilroy
- [[CXDB]] — Kilroy uses CXDB for run history and checkpoint recovery
- [[AttractorPattern]] — Kilroy implements the Attractor spec
- [[DarkFactory]] — Kilroy is a dark factory implementation

## See Also
- [[DanShapiro]]
- [[Mammoth]]
- [[Tracker]]
- [[AttractorPattern]]
