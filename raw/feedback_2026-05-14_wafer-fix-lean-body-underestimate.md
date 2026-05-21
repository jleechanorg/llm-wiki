---
name: wafer-fix-lean-body-underestimate
description: WaferFixPatcher estimated input_tokens from lean body (post-strip) causing 3-5x undercount and claudew() auto-compact thrash loop
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 6a211e84-47d6-4aef-8b98-46bf0d862321
---

## Learning

WaferFixPatcher uses `rawRequestBody.length` to estimate input_tokens to patch
GLM-5.1's `input_tokens: 0` bug. But when `lean` or `lean,on-demand` mode is
active, `forwardBody` is reassigned to the stripped body (tool schemas removed)
BEFORE line 480 where the patcher is created. This meant the estimate was based
on the lean body — 3–5× smaller than the original.

## Why it caused thrashing

- Claude Code's internal context tracker counts the **original** messages
  (including full tool schemas)
- WaferFixPatcher reported e.g. **12,500 tokens** (lean body) when Claude Code
  tracked ~50,000 tokens internally
- Claude Code saw artificially low context usage → delayed compaction until
  context was truly full
- Late compaction → very long conversation to summarize → oversized compact
  summary
- Compact summary + large system prompt (CLAUDE.md files) already filled most
  of GLM-5.1's context immediately after compact
- Within 3 turns → threshold hit again → compact → repeat (3× thrash warning)

## Why /clear didn't help

`/clear` resets conversation but not the proxy mode. Every fresh session hits
the same late-compaction pattern because the underlying estimate is always wrong.

## Fix

`src/proxy.ts:480` — use `rawRequestBody.length` (pre-lean) instead of
`forwardBody.length` (post-lean):

```typescript
// Before (wrong):
const patcher = modes.waferFix
  ? new WaferFixPatcher(estimateInputTokens(forwardBody.length))
  : null;

// After (correct):
const patcher = modes.waferFix
  ? new WaferFixPatcher(estimateInputTokens(rawRequestBody.length))
  : null;
```

**Why rawRequestBody**: The estimate should match Claude Code's internal belief
about context size (what it thinks it sent), not what was forwarded to the model.
This aligns compaction timing with what Claude Code expects.

## Verification

- Commit: `3fb937fefdaa90377aea6856323f35d0a717cb42` on main
- Build: `npm run build` — success
- Proxy restarted: PID 50494, same `lean,on-demand,wafer-fix` args, new build

## Pattern

Whenever a body is transformed **before** an estimator that consumes body size,
the estimator must reference the **pre-transform** body to remain calibrated
with the caller's expectations. The transform is an optimization for the
downstream model; the estimate is feedback to the upstream client.

**Why**: [[feedback_2026-05-14_wafer-sse-input-tokens-zero]] — original fix
that added WaferFixPatcher; this fixes a secondary error in its estimation path.
