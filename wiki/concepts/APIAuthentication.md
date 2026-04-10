---
title: "API Key Authentication"
type: concept
tags: [auth, api, security]
sources: [openai-compatible-inference-proxy]
last_updated: 2026-04-08
---

Authentication pattern using personal API keys (worldai_) that are resolved to user identifiers via database lookup. The proxy uses the same authentication mechanism as the /mcp endpoint, resolving API keys to user_id through Firestore to determine which user's gateway to forward requests to.