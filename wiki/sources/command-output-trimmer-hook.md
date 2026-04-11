---
title: "Command Output Trimmer Hook"
type: source
tags: [claude-code, hooks, compression, output-trimming, context-optimization]
source_file: "raw/command-output-trimmer-hook.md"
sources: []
last_updated: 2026-04-07
---

## Summary
A smart compression system for Claude Code that intercepts verbose slash command outputs and applies intelligent compression rules while preserving essential information. Helps manage context consumption and improves readability.

## Key Claims
- **Smart Command Detection**: Automatically recognizes command type from output patterns and applies tailored compression rules
- **Command-Specific Rules**: Different compression strategies for /test, /pushl, /copilot, /coverage, /execute commands
- **Fallback Support**: Generic compression for unrecognized commands using first 20 + last 10 lines pattern
- **Installation via PostToolUse Hook**: Integrated through `.claude/settings.json` hook configuration

## Key Features
- **/test Commands**: Preserves errors, failures, tracebacks; compresses progress dots and PASSED messages; limits to 3 passed test details
- **/pushl Commands**: Preserves PR links and status; compresses git operation details; limits to 5 git operation lines
- **/copilot Commands**: Preserves phase markers and results; compresses timing calculations
- **/coverage Commands**: Preserves percentage data; compresses detailed file listings
- **/execute Commands**: Preserves TODO states and checklist items; compresses verbose explanations

## Connections
- [[ClaudeCodeHooks]] — this hook system uses Claude Code's PostToolUse hook mechanism
- [[ContextOptimization]] — similar to context window optimization techniques
