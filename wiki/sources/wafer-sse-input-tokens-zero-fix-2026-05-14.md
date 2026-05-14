---
title: "Wafer SSE input_tokens:0 Autocompact Thrashing Fix"
type: source
tags: [wafer, sse, streaming, autocompact, proxy, llm-inspector]
raw: raw/feedback_2026-05-14_wafer-sse-input-tokens-zero.md
date: 2026-05-14
---

## Summary

GLM-5.1 (wafer) always returns `"input_tokens":0` in the SSE `message_start` event, causing Claude Code autocompact to thrash: it believes context was just cleared after every response, so it refills within 3 turns and fires autocompact again — infinitely.

Fix: `WaferFixPatcher` in llm-inspector's `src/filters.ts` buffers SSE chunks until the first `\n\n` boundary (end of `message_start`), then replaces `"input_tokens":0` with `Math.round(requestBodyBytes / 4)` before streaming the remainder.

## Root Cause

```
event: message_start
data: {"type":"message_start","message":{...,"usage":{"input_tokens":0,"output_tokens":0}}}
```

Claude Code uses `input_tokens` from the SSE `message_start` to track context window usage. `0` → thinks context was just cleared → context refills within 3 turns → autocompact → `0` again → infinite loop.

Anthropic returns real token counts so autocompact paces correctly.

## Implementation

### `WaferFixPatcher` (`src/filters.ts`)

Stateful transformer:
- Buffers incoming SSE chunks until first `\n\n` (first event boundary)
- Applies `/"input_tokens"\s*:\s*0\b/` regex — only fires when value is literally `0`
- Replaces with estimated token count (`bodyBytes / 4`)
- All subsequent chunks pass through with zero buffering

### Composable mode system (`parseModeFeatures`)

`--tool-mode` now accepts comma-separated features:
- `lean` — strips LEAN_REMOVE_LIST (~29KB chrome/drive tools)
- `on-demand` — stubs heavy tool schemas
- `wafer-fix` — patches `input_tokens:0` in SSE stream

Wafer launchd plist updated to `lean,wafer-fix`.

## Verification

- `npm test`: 23/23 tests pass (14 new tests)
- Proxy log: `[lean: stripped 1 tools] [wafer-fix: est 38747 tokens]`
- Request body shrunk from 158699B → 154989B (lean stripping)

### JSONL Proof (2026-05-14)

Line 1259 of `c03c7cd8-ad2a-4107-b27b-6ef0a5fd4635.jsonl` (worktree-location-freeze project) confirmed both root causes firing simultaneously:

- `model: GLM-5.1`
- `Read {"file_path": ".../.beads/issues.jsonl"}` — no offset, no limit
- `usage: {input_tokens: 0}` — provider returned zero in same event

Both root causes are required independently to stop thrashing. The unguarded read caused genuine context overflow; `input_tokens:0` caused blind tracking regardless of actual fill level.

## Key Files

- `src/filters.ts` — `WaferFixPatcher`, `parseModeFeatures`, `estimateInputTokens`
- `src/proxy.ts` — mode feature dispatch, patcher wired into normal-SSE and on-demand-SSE paths
- `src/filters.test.ts` — 23 tests
- `~/Library/LaunchAgents/com.jleechan.llm-inspector-wafer.plist` — `lean,wafer-fix`

## Reusable Pattern

`input_tokens:0` is not specific to wafer — apply `WaferFixPatcher` to any upstream that returns zero token counts. The regex only fires when the value is literally `0`, so enabling it broadly is safe.

## Related Concepts

- [[SSEStreaming]] — SSE event boundary structure
- [[Compaction]] — Claude Code autocompact mechanism
- [[WaferFixSSEPatcher]] — the patcher pattern itself
- [[TokenEstimation]] — byte/4 approximation
