---
name: wafer-sse-input-tokens-zero
description: "GLM-5.1 (wafer) always returns input_tokens:0 in SSE message_start, causing Claude Code autocompact thrashing — fixed by WaferFixPatcher in llm-inspector proxy"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: f6c08ed2-9a66-45b2-9ecb-2784de0ecba6
---

## Context

Claude Code sessions routed through wafer (GLM-5.1 via pass.wafer.ai) repeatedly hit the autocompact thrashing warning:

> "Autocompact is thrashing: the context refilled to the limit within 3 turns of the previous compact, 3 times in a row."

This did not occur with normal Anthropic (claude-sonnet-4-6) sessions through the same proxy.

## Root Cause

Wafer/GLM-5.1 returns `"input_tokens": 0` in the SSE `message_start` event on every response:

```
event: message_start
data: {"type":"message_start","message":{...,"usage":{"input_tokens":0,"output_tokens":0,...}}}
```

Claude Code uses `input_tokens` from the API response to track context window usage. When it receives `0`, it believes the context was just cleared. The actual request body is ~285KB (~70K tokens), so the context refills within 3 turns, triggering autocompact, which reports `0` again — infinite cycle.

Anthropic returns real token counts, so its autocompact paces correctly.

**Contributing factor**: Tool schemas are enormous (~200KB of the 285KB body):
- `builtin_tools`: ~101KB
- `mcp_tools`: ~98KB (chrome automation tools alone ~29KB)

## Solution

Added composable proxy mode system to llm-inspector:

### 1. `WaferFixPatcher` (`src/filters.ts`)

Buffers SSE chunks until the first `\n\n` boundary (end of `message_start`), replaces `"input_tokens":0` with `Math.round(requestBodyBytes / 4)`, then streams the rest through immediately.

Safe for non-wafer sessions: regex only fires when `input_tokens` is literally `0`.

### 2. Composable modes (`parseModeFeatures`)

`--tool-mode` now accepts comma-separated features:
- `lean` — strips LEAN_REMOVE_LIST tools (~29KB chrome/drive tools)
- `on-demand` — stubs heavy tool schemas, re-issues on use
- `wafer-fix` — patches `input_tokens:0` in SSE stream

Legacy `lean-on-demand` still works as before.

### 3. Wafer launchd plist updated to `lean,wafer-fix`

File: `~/Library/LaunchAgents/com.jleechan.llm-inspector-wafer.plist`

## Verification

- `npm test`: 23/23 tests pass (14 new tests covering `WaferFixPatcher`, `parseModeFeatures`, `estimateInputTokens`)
- Proxy log after reload shows: `[lean: stripped 1 tools] [wafer-fix: est 38747 tokens]`
- Request body shrunk from 158699B → 154989B (lean stripping)

## References

- `src/filters.ts` — `WaferFixPatcher`, `parseModeFeatures`, `estimateInputTokens`
- `src/proxy.ts` — mode feature dispatch, patcher wired into normal-SSE and on-demand-SSE paths
- `src/filters.test.ts` — tests for all new code
- `~/Library/LaunchAgents/com.jleechan.llm-inspector-wafer.plist` — updated to `lean,wafer-fix`
- `~/.llm-inspector/captures/*.summary.json` — showed builtin_tools ~101KB, mcp_tools ~98KB per request

## Reusable Pattern

**Why** — `input_tokens:0` is not specific to wafer. Apply this pattern to any proxy upstream that returns zero token counts. The patcher is safe to enable broadly: when the actual token count is non-zero, the regex does not match and the chunk passes through unmodified.
