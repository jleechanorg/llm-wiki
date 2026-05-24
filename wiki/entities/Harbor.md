---
title: "Harbor"
type: entity
tags: [attractor-pattern, benchmark-runner, ai-evaluation]
date: 2026-05-24
---
## Overview
Harbor is a concurrent benchmark runner for AI coding agents. It is the execution infrastructure used by AttractorBench to run agents in Docker or cloud environments (Daytona), producing ATIF-format trajectories for reproducibility.

## Key Properties
- **Type**: Benchmark runner for coding agents
- **Key features**: Concurrent execution, Docker/Daytona environments, ATIF trajectory format, multi-agent head-to-head comparison, cost-aware metrics
- **Supported agents**: claude-code, codex, gemini-cli, opencode, openhands, aider
- **Usage in AttractorBench**: `harbor run --path ./tasks --agent claude-code --model anthropic/claude-sonnet-4-6 --env docker`

## Connections
- [[AttractorBench]] — Harbor runs AttractorBench evaluations
- [[StrongDM]] — Harbor is the execution layer for AttractorBench
- [[ATIF]] — Harbor produces ATIF-format agent trajectories

## See Also
- [[AttractorBench]]
- [[StrongDM]]
