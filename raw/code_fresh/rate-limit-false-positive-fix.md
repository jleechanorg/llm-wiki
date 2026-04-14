# Bead: Fix False Positive Rate Limit Detection in CLI Fallback Logic

## Problem

The CLI fallback logic in task_dispatcher.py incorrectly detects "rate limit" text in agent output as an actual API rate limit failure. This causes unnecessary fallback to other CLIs even when the task completed successfully.

### Root Cause
- Pattern matching: `grep -Eqi "{rate_limit_pattern}"` detects ANY occurrence of "rate limit" in output
- False positives from:
  - CodeRabbit bot comments mentioning "rate limit" (informational, not API failure)
  - Agent output quoting other sources that mention rate limits
  - Log messages about other services' rate limits

### Evidence
- PR #5566 MiniMax fixcomment completed successfully (exit=0)
- But log contained "Rate limit exceeded" from CodeRabbit comments
- Fallback triggered unnecessarily to Gemini and Cursor

## Brainstorm Solutions

### Option 1: Exit Code + Specific Error Patterns (Recommended)
Only trigger fallback when BOTH conditions met:
1. Non-zero exit code AND
2. Specific API error patterns (not general mentions)

```bash
# Only detect actual API failures, not informational messages
API_RATE_LIMIT_PATTERNS=(
  "error.*rate.*limit.*exceeded"      # API quota exhausted
  "429.*Too.*Many.*Requests"          # HTTP 429
  "rate.*limit.*during.*request"       # During API call
  "exceeded.*daily.*quota.*model"      # Model-specific quota
)
```

### Option 2: Context-Aware Detection
Check if "rate limit" appears in:
- stderr vs stdout (API errors in stderr)
- Near actual API call timestamps
- Not in quoted blocks/agent summaries

### Option 3: Require Multiple Confirmations
Must see rate limit 2+ times or in specific contexts before triggering fallback

### Option 4: Separate Informational vs Critical
- "informational" rate limits → ignore
- "critical" rate limits (API failure) → trigger fallback

## Recommended Fix

Use Option 1: Check exit code first, then specific API error patterns. The current logic triggers on ANY rate limit mention regardless of exit code.

### Files to Modify
- `orchestration/task_dispatcher.py` - around line 2417
