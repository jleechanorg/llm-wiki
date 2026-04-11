---
title: "Workspace Preservation Across Retries"
type: concept
tags: [pair-programming, workspace, retry, tdd, pairv2]
sources: []
last_updated: 2026-04-11
---

## Description
When a pair programming verifier returns FAIL and the workflow retries implementation, the coder's workspace should be preserved — the coder should see prior work, run tests, and make targeted fixes rather than starting from scratch.

## Pattern
The verify-fail-retry loop (pairv2) should:
1. NOT clean the workspace directory between retries
2. Extract verifier's FAIL reasoning and inject as coder prompt suffix
3. Run stale signal files cleanup (IMPLEMENTATION_READY, verification_report.json)
4. Preserve: all source files, contracts, session_info.json, instructions

## Anti-pattern (What to Avoid)
Cleaning the workspace on retry:
```python
# WRONG — loses all prior work
shutil.rmtree(workspace)
os.makedirs(workspace)
```

## Correct Pattern
```python
# Clean only signal files, preserve all code
for sig in ['IMPLEMENTATION_READY', 'verification_report.json']:
    path = os.path.join(session_dir, sig)
    if os.path.exists(path):
        os.remove(path)
# Workspace preserved for next attempt
```

## Retry Prompt Suffix
```
## VERIFIER FEEDBACK (attempt N/M)

Your previous implementation was reviewed and REJECTED:
{extracted_feedback}

The workspace already has your prior work. DO NOT start from scratch.
1. Run tests to see current state: python -m pytest -v
2. Fix the specific issues listed above.
3. Run tests again to verify fixes.
```

## Connections
- [[Nested-Agent-Loops]] — retry loop pattern
- [[Compound-Loops]] — retry + restart = two recovery axes
- [[DeterministicFeedbackLoops]] — feedback must be actionable
