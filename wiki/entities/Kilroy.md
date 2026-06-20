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
- [DanShapiro](DanShapiro.md) — Shapiro built Kilroy
- [CXDB](../concepts/CXDB.md) — Kilroy uses CXDB for run history and checkpoint recovery
- [AttractorPattern](../concepts/AttractorPattern.md) — Kilroy implements the Attractor spec
- [DarkFactory](../concepts/DarkFactory.md) — Kilroy is a dark factory implementation

## See Also
- [DanShapiro](DanShapiro.md)
- [Mammoth](Mammoth.md)
- [Tracker](Tracker.md)
- [AttractorPattern](../concepts/AttractorPattern.md)
