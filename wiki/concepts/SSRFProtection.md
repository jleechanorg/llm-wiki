---
title: "SSRF Protection"
type: concept
tags: [security, ssrf, web]
sources: [openai-compatible-inference-proxy]
last_updated: 2026-04-08
---

Server-Side Request Forgery protection mechanism that detects and rejects redirect responses. Prevents attackers from bypassing URL validation by tricking the server into following redirects to internal or unauthorized endpoints. The proxy checks `response.is_redirect` and `response.history` to block such attempts.