---
title: "Schema Echo"
type: concept
tags: [api-bug, error-handling, provider-issues]
sources: []
last_updated: 2026-04-08
---

Provider bug where API returns the response_format schema configuration instead of actual generated content. Common with strict schema enforcement. WorldArchitect.AI handles this via CerebrasSchemaEchoError exception and fallback to non-schema response mode.

**Detection:**
- Response contains {"type": "object"} or schema keywords without actual content
- Specific to providers with response_format handling issues

**Related pages:** [[CerebrasDirectApiProviderImplementation]]
