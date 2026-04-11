---
title: "CLI Provider Test Results"
type: source
tags: [worldarchitect, testing, cli, orchestration, claude, minimax, codex]
sources: []
source_file: docs/cli_provider_test_results.md
date: 2026-02-16
last_updated: 2026-04-07
---

## Summary

Test results from chore/pair-orchestration-refactor branch validating four LLM providers: Claude (opus), Claude (sonnet), MiniMax, and Codex. Claude opus and MiniMax, Codex work via orchestration; Claude sonnet is rate-limited. The key fix was adding env var cleanup to prevent MiniMax credentials from being inherited by Claude CLI.

## Key Claims

- **Claude (opus)**: ✅ WORKS via orchestration with proper env cleanup
- **Claude (sonnet)**: ⚠️ RATE LIMITED — resets Feb 19 at 12pm
- **MiniMax**: ✅ WORKS via ANTHROPIC_BASE_URL with direct CLI
- **Codex**: ✅ WORKS via codex CLI

## Root Cause Analysis

### Issue: Claude CLI 401 Authentication via Orchestration

**Problem:** When running Claude via orchestration, MiniMax-specific env vars were inherited:
- `ANTHROPIC_AUTH_TOKEN=sk-cp-...` (MiniMax token)
- `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic`
- `ANTHROPIC_MODEL=MiniMax-M2.5`

**Fix:** Added to `orchestration/task_dispatcher.py` — Claude profile `env_unset`:
```python
"env_unset": [
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_SMALL_FAST_MODEL",
],
```

## Files Changed

1. `orchestration/task_dispatcher.py` — Added env vars to unset for Claude
2. `orchestration/tests/test_cli_support.py` — Updated test expectations
3. `.claude/pair/pair_execute.py` — Added "minimax" to supported CLIs