---
title: "Integration Command (/integrate)"
type: source
tags: [git, integration, branch, automation, test-server]
sources: []
last_updated: 2026-04-14
---

## Summary

Creates fresh branch from main and cleanup test servers. Enhanced with auto-learning to capture patterns from previous branch work.

## Key Claims

- Creates dev{timestamp} branch by default or custom branch name
- Auto-Learning: automatically triggers /learn to capture insights
- Stops test server for current branch before integration
- Removes branch-specific PID and log files
- Ensures no orphaned server processes
- New branch starts with clean server state

## Usage

- /integrate — Creates dev1752251680 branch
- /integrate [branch-name] — Creates custom named branch
- /integrate --force — Override safety checks

## Connections

- [[CommandSystemDocumentation]] — Git workflow commands
- [[EvolveLoop]] — Learning from integration patterns

## Contradictions

- None identified
