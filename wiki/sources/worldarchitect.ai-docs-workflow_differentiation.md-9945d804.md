---
title: "Differentiated Linting Workflows"
type: source
tags: [linting, workflow, push, pushl, quality-gate, fast-iteration, worldarchitect]
sources: []
date: 2026-04-07
source_file: workflow differentiation documentation
last_updated: 2026-04-07
---

## Summary
Implements differentiated linting workflows for `/push` and `/pushl` commands to serve different development needs: `/push` enforces a quality gate (lint before push, blocking), while `/pushl` enables fast iteration (push first, non-blocking lint after). Both respect environment variables like `SKIP_LINT` and `ENABLE_LINT_IN_CI`.

## Key Claims
- **Quality Gate (`/push`)**: Runs linting BEFORE push, blocks if issues found — suitable for production branches and team collaboration
- **Fast Iteration (`/pushl`)**: Pushes first, runs linting AFTER (non-blocking), reports issues but continues — suitable for quick fixes and development
- **Environment Controls**: Both workflows respect `SKIP_LINT` and `ENABLE_LINT_IN_CI` for manual override and CI integration
- **Backward Compatible**: Non-destructive changes, clear user feedback, comprehensive documentation

## Key Quotes
> "Choose appropriate tool — Fast iteration: Use `/pushl` for quick changes; Quality assurance: Use `/push` for important work"

## Connections
- [[WorldAI]] — this workflow system was developed for the WorldAI project
- [[ClaudeCode]] — integrates with Claude Code CLI for lint execution

## Contradictions
- None detected

## Feature Matrix

| Feature | `/push` | `/pushl` | `/copilot` |
|---------|--------|----------|------------|
| **Lint Timing** | Before push | After push | Before push |
| **Blocking** | Yes | No | No |
| **Auto-fix** | No | No | Yes |
| **Use Case** | Quality gate | Fast iteration | AI enhancement |
| **Target** | Production | Development | Automation |
