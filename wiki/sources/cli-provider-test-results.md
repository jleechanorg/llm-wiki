---
title: "CLI Provider Test Results"
type: source
tags: [claude-code, orchestration, cli, testing, providers]
source_file: "raw/cli-provider-test-results.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Test results from 2026-02-16 on branch `chore/pair-orchestration-refactor` evaluating four CLI providers: Claude (opus), Claude (sonnet), MiniMax, and Codex. Claude opus works via orchestration, sonnet is rate-limited, MiniMax and Codex both work.

## Key Claims
- **Claude (opus)**: Works via orchestration with `--model opus` flag
- **Claude (sonnet)**: Rate limited, resets Feb 19 at 12pm
- **MiniMax**: Works via ANTHROPIC_BASE_URL environment variable
- **Codex**: Works via codex CLI
- **Root Cause Fixed**: Claude CLI 401 authentication issue resolved by adding env vars to unset for Claude profile in task_dispatcher.py

## Key Quotes
> "OPUS TEST PASSED\n\nThe orchestration test is successful. I'm the coder agent and I've confirmed the pair programming session launched correctly."

## Connections
- [[Claude]] — CLI provider tested
- [[MiniMax]] — CLI provider tested via ANTHROPIC_BASE_URL
- [[Codex]] — CLI provider tested via codex CLI
- [[Orchestration]] — test framework used for provider validation

## Contradictions
- None identified

## Files Changed
1. `orchestration/task_dispatcher.py` - Added env vars to unset for Claude
2. `orchestration/tests/test_cli_support.py` - Updated test expectations
3. `.claude/pair/pair_execute.py` - Added "minimax" to supported CLIs
