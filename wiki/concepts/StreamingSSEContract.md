---
title: "Streaming SSE Contract"
type: concept
tags: [streaming, sse, http, api, contract]
sources: []
last_updated: 2026-04-08
---

The specification for how Server-Sent Events are streamed from /interaction/stream endpoint. Each mode (character/think/god) must return correct SSE done payloads with mode-specific response structures.

**Key requirement**: Done payload must include god_mode_response field even when empty string, to satisfy validator checking for field presence.

**Mentioned in**: [[StreamingSSEContractE2ETests]]
