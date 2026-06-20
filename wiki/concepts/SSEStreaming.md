---
title: "SSE Streaming"
type: concept
tags: [streaming, http, server-sent-events]
sources: [openrouter-provider-tests]
last_updated: 2026-06-05
---

Server-Sent Events (SSE) streaming is a server-push technology where the server sends data to the client over HTTP using the text/event-stream content type.

## Usage in LLM Providers
- Providers stream token-by-token responses via SSE
- Each chunk is prefixed with "data: " and suffixed with newlines
- Stream terminates with "data: [DONE]"
- Client iterates over iter_lines() to parse delta.content fields

## message_start Event and Token Tracking

The first SSE event from Anthropic's API is always `message_start`, containing `usage: {input_tokens, output_tokens}`. Claude Code uses `input_tokens` from this event to track context window fill level.

**Critical**: providers that return `input_tokens: 0` (e.g. GLM-5.1/wafer) cause Claude Code autocompact to thrash — it believes context was just cleared after every response. Fix: buffer until `\n\n` boundary, patch `"input_tokens":0` with estimated value. See [WaferFixSSEPatcher](WaferFixSSEPatcher.md) and [wafer-sse-input-tokens-zero-fix-2026-05-14](../sources/wafer-sse-input-tokens-zero-fix-2026-05-14.md).

## Related Pages
- [[OpenRouterProviderTests]] — validates SSE parsing in openrouter_provider
- [[StreamingSync]] — generate_content_stream_sync function concept
- [WaferFixSSEPatcher](WaferFixSSEPatcher.md) — proxy-level patcher for `input_tokens:0` in message_start
- [Compaction](Compaction.md) — autocompact thrash caused by zero token counts

## ⚠️ iter_lines(decode_unicode=True) is a UTF-8 footgun (PR #7249)

**Added 2026-06-05** — see `pr7249-utf8-mojibake-streaming-fix-2026-06-05.md`

`requests.Response.iter_lines(decode_unicode=True)` decodes SSE bytes using
`self.encoding`, which **defaults to ISO-8859-1** when the upstream
Content-Type lacks a `charset=` directive. This silently corrupts multi-byte
UTF-8 (em-dash, curly quotes, curly apostrophe) when SSE chunks cross a
line boundary. Affects OpenRouter and OpenAI proxy providers. Bug is
non-deterministic per turn (depends on chunk boundaries).

**Safe pattern (OpenClaw already does this)**:
```python
for line in response.iter_lines():  # NO decode_unicode=True
    text = line.decode("utf-8", errors="replace")  # explicit decode
```

**Less safe alternative**:
```python
response.encoding = "utf-8"  # force BEFORE iter_lines
for line in response.iter_lines(decode_unicode=True):
    ...
```

Regression test pattern: use a `FakeSSEResponse` whose `iter_lines` is the
**real** method with `encoding=ISO-8859-1` (mimics `requests` default).
Build raw SSE bytes with `ensure_ascii=False` so em-dash is actual
`0xE2 0x80 0x94` bytes (not `\\u2014` escape).
