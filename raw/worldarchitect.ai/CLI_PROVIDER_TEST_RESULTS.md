# CLI Provider Test Results

**Date:** 2026-02-16
**Branch:** chore/pair-orchestration-refactor

## Test Results Summary

| Provider | Status | Notes |
|----------|--------|-------|
| Claude (opus) | ✅ WORKS | Via orchestration |
| Claude (sonnet) | ⚠️ RATE LIMITED | Resets Feb 19 at 12pm |
| MiniMax | ✅ WORKS | Via ANTHROPIC_BASE_URL |
| Codex | ✅ WORKS | Via codex CLI |

## Evidence

### Claude (opus) - ✅ WORKING

**Test:** Orchestration with `--model opus` flag

**Log Evidence** (`/tmp/orchestration_logs/chorepairorchestrationrefactor80c01adecoder_1771282825289-24310.log`):
```
{"type":"assistant","message":{"model":"claude-opus-4-6",...,"content":[{"type":"text","text":"**OPUS TEST PASSED**\n\nThe orchestration test is successful. I'm the coder agent and I've confirmed the pair programming session launched correctly."}]}}
```

**Direct CLI Test:**
```bash
$ /Users/jleechan/.local/bin/claude -p "Say 'TEST PASSED'" --model opus --dangerously-skip-permissions
TEST PASSED
```

### Claude (sonnet) - ⚠️ RATE LIMITED

**Error:**
```
{"type":"assistant","message":{...,"content":[{"type":"text","text":"You've hit your limit · resets Feb 19 at 12pm (America/Los_Angeles)"}]}}
```

### MiniMax - ✅ WORKS

**Direct Test:**
```bash
$ ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic ANTHROPIC_MODEL=MiniMax-M2.5 /Users/jleechan/.local/bin/claude -p "Say 'test'" --model MiniMax-M2.5 --dangerously-skip-permissions
Genesis Coder, Prime Mover,

test
```

**Orchestration:** MiniMax CLI profile exists but validation script has issues (works when called directly)

### Codex - ✅ WORKS

Previously verified in pair sessions. Codex launches successfully via orchestration.

## Root Cause Analysis & Fix

### Issue: Claude CLI 401 Authentication via Orchestration

**Problem:** When running Claude via orchestration, the environment had MiniMax-specific env vars:
- `ANTHROPIC_AUTH_TOKEN=sk-cp-...` (MiniMax token)
- `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic`
- `ANTHROPIC_MODEL=MiniMax-M2.5`

These were inherited by Claude CLI, causing it to route through MiniMax API with invalid credentials.

**Fix:** Added to `orchestration/task_dispatcher.py` - Claude profile `env_unset`:
```python
"env_unset": [
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",  # MiniMax token
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_SMALL_FAST_MODEL",
],
```

Also added `ANTHROPIC_AUTH_TOKEN` to `env_cleanup_vars` for fallback cleanup between CLI attempts.

### Issue: MCP Mail `to` Parameter

**Error:** `to: Input should be a valid list [type=list_type, input_value='...', input_type=str]`

**Fix:** Already addressed - agents now pass `to` as a list: `["agent-name"]`

## Files Changed

1. `orchestration/task_dispatcher.py` - Added env vars to unset for Claude
2. `orchestration/tests/test_cli_support.py` - Updated test expectations
3. `.claude/pair/pair_execute.py` - Added "minimax" to supported CLIs
