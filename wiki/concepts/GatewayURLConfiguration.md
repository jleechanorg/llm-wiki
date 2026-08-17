---
title: "Gateway URL Configuration"
type: concept
tags: [configuration, networking, environment-variables]
sources: []
last_updated: 2026-04-08
---

Pattern for configuring HTTP client gateway URLs with fallback chain:

1. Check for explicit full URL env var (trusted, no validation)
2. Fall back to host:port construction
3. Default to localhost (127.0.0.1:18789)

Used by OpenClawHTTPClient, inference proxies, and similar patterns.
