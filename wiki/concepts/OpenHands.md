---
title: "OpenHands"
type: concept
tags: [open-source, coding-agent, platform, evaluation, SWE-bench]
sources: [openhands-paper]
last_updated: 2026-04-14
---

Open-source platform for AI-powered software development. Enables reproducible research and evaluation of coding agents with standardized environment and benchmark integration (SWE-bench, HumanEval).

## Key Features

- Containerized evaluation environments
- Standardized agent interface definition
- Benchmark integration framework
- Action space specification for coding agents
- Sandboxed execution for safety

## Architecture

OpenHands provides:
1. **Environment**: containerized SE environment (code editing, git, shell)
2. **Agent Interface**: standardized action space (edit, run, test, commit)
3. **Evaluation Harness**: benchmark runners for SWE-bench, HumanEval, etc.

## Connections

- Core platform for [[AgentBench]]-style evaluation
- Alternative to [[SWE-Agent]] single-agent approach
- Used in [[PRWatchdog]] for automated agent evaluation
