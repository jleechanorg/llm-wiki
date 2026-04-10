---
title: "HTTP Proxy"
type: concept
tags: [networking, interception, capture]
sources: []
last_updated: 2026-04-07
---

Method of intercepting API requests by routing traffic through a custom proxy server. Used to capture Claude Code's system prompt in structured JSON format.

## Setup
1. Run custom Python proxy server
2. Set `ANTHROPIC_BASE_URL=http://localhost:8000`
3. Invoke Claude Code normally

## Related Sources
- [[Claude Code System Prompt Capture - Method Comparison]]

## See Also
- [[SystemPrompt]]
- [[DebugMode]]
