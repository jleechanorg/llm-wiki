---
title: "Mock Mode Testing"
type: concept
tags: [testing, mock, development-mode]
sources: []
last_updated: 2026-04-08
---

Testing pattern where MOCK_SERVICES_MODE environment variable enables deterministic responses for testing without external API calls. Used to validate response schemas and API structure.

## Connections
- [[LLMService]] — module being tested
- [[Constants]] — environment variable configuration
