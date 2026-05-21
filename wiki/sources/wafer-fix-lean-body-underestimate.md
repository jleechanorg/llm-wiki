---
title: "WaferFixPatcher Lean-Body Underestimate"
type: source
tags: [llm-inspector, wafer, GLM-5.1, compaction, proxy, token-estimation]
date: 2026-05-14
raw: raw/feedback_2026-05-14_wafer-fix-lean-body-underestimate.md
---

## Summary

In llm-inspector's proxy, `lean` and `lean,on-demand` modes reassign `forwardBody`
to a stripped version of the request (tool schemas removed) before line 480 where
`WaferFixPatcher` is instantiated. The patcher therefore estimated `input_tokens`
from the smaller lean body — 3–5× lower than the original.

Claude Code's internal context tracker uses the original body. This mismatch caused
Claude Code to believe context was much emptier than it actually was, delaying
auto-compact until the context was completely full. The resulting compact summary
was very large and, combined with the large system prompt, nearly filled the context
immediately after compaction — creating a 3-cycle thrash loop visible only in
`claudew()` (GLM-5.1 via Wafer) sessions.

## Root cause

`src/proxy.ts:480`:

```typescript
// Wrong — forwardBody already reassigned to lean body at this point
const patcher = modes.waferFix
  ? new WaferFixPatcher(estimateInputTokens(forwardBody.length))
  : null;
```

## Fix

```typescript
// Correct — use pre-lean body so estimate matches Claude Code's internal tracking
const patcher = modes.waferFix
  ? new WaferFixPatcher(estimateInputTokens(rawRequestBody.length))
  : null;
```

## References

- Commit: `3fb937fefdaa90377aea6856323f35d0a717cb42` (jleechanorg/llm_inspector main)
- File: `src/proxy.ts:480`
- Related: [[WaferFixPatcher]] concept, [[ClaudeCodeCompaction]] concept
