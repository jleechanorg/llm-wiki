---
title: "WaferFixSSEPatcher"
type: concept
tags: [wafer, sse, proxy, streaming, autocompact, llm-inspector]
sources: [wafer-sse-input-tokens-zero-fix-2026-05-14]
last_updated: 2026-05-14
---

A composable proxy-layer SSE transformer that patches `"input_tokens":0` in the `message_start` event with an estimated token count derived from the request body size.

## Problem

Some LLM providers (GLM-5.1 / wafer at `pass.wafer.ai`) return `"input_tokens":0` in every `message_start` SSE event. Claude Code uses this value to track context window fill level. Zero causes autocompact to thrash: Claude Code thinks context was just cleared after every response, so the real context (~70K tokens) refills within 3 turns, triggering autocompact again — infinitely.

## Implementation (`src/filters.ts` in llm-inspector)

```typescript
export class WaferFixPatcher {
  private buffer = "";
  private patched = false;

  constructor(private estimatedTokens: number) {}

  process(chunk: Buffer): Buffer[] {
    if (this.patched) return [chunk];  // pass-through after first event
    this.buffer += chunk.toString("utf-8");
    const boundary = this.buffer.indexOf("\n\n");
    if (boundary !== -1) {
      const firstEvent = this.buffer.slice(0, boundary + 2);
      const remainder = this.buffer.slice(boundary + 2);
      const patchedEvent = firstEvent.replace(
        /"input_tokens"\s*:\s*0\b/,
        `"input_tokens":${this.estimatedTokens}`,
      );
      this.patched = true;
      this.buffer = "";
      return [Buffer.from(patchedEvent + remainder, "utf-8")];
    }
    return [];  // still buffering
  }

  flush(): Buffer[] { /* returns remaining buffer if stream ends prematurely */ }
}
```

## Token Estimation

`Math.round(bodyBytes / 4)` — ~4 bytes per token is a reasonable approximation for JSON-heavy API payloads. Actual payloads of ~155K bytes → ~38K tokens estimated.

## Safety

The regex `/"input_tokens"\s*:\s*0\b/` only fires when the value is **literally `0`**. When the provider returns a real count (e.g. `42000`), the regex does not match and the chunk passes through unmodified. Safe to enable for all sessions.

## Deployment

Enabled via `--tool-mode lean,wafer-fix` in the wafer launchd plist. Part of the composable mode system where `parseModeFeatures("lean,wafer-fix")` returns `{lean: true, waferFix: true}`.

## Related

- [[SSEStreaming]] — SSE event boundary structure
- [[Compaction]] — autocompact thrash mechanism
- [[TokenEstimation]] — byte/4 approximation pattern
- [[wafer-sse-input-tokens-zero-fix-2026-05-14]] — source / full context
