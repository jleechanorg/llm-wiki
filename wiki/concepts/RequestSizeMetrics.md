---
title: "Request Size Metrics"
type: concept
tags: [logging, monitoring, metrics, token-counting]
sources: [gemini-request-size-logging-tests]
last_updated: 2026-04-08
---

## Description
Metrics tracked for LLM API requests: character count (ch), token count (tk), and byte count (b). Logged before API calls to monitor request sizes and prevent token limit issues.

## Formula
```
Total = Contents + System Instruction
Metrics: characters, tokens, bytes
```

## Connections
- [[GeminiProvider]] — logs these metrics
- [[TokenLimit]] — related to max token monitoring
- [[RequestLogging]] — broader logging concept
