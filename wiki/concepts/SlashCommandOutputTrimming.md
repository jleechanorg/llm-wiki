---
title: "Slash Command Output Trimming"
type: concept
tags: [token-reduction, hooks, optimization, slash-commands]
sources: ["context-optimization-implementation-plan"]
last_updated: 2026-04-08
---

## Summary
Technique for reducing token consumption from Claude Code slash commands by intercepting outputs and applying compression rules before display. Targets 50-70% reduction in command output tokens.

## Key Details
- **Max line limits**: 10-25 lines per command type
- **Preserve patterns**: Critical indicators (FAILED, ERROR, passed, PR URLs, ✅/❌)
- **Compress patterns**: Progress dots, git operations, dependency installation
- **Implementation**: `.claude/hooks/command_output_trimmer.py`

## Applicable Commands
- `/test`: max 20 lines, preserve FAILED/ERROR/passed
- `/pushl`: max 15 lines, preserve PR URLs and git status
- `/build`: max 10 lines, preserve Success/Error indicators
- `/coverage`: max 25 lines, preserve percentages and TOTAL
