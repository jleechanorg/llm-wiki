---
title: "PR #917: Add abort-aware streaming retries for Cerebras"
type: source
tags: [codex]
date: 2025-12-06
source_file: raw/prs-/pr-917.md
sources: []
last_updated: 2025-12-06
---

## Summary
- propagate AbortSignal from Cerebras streaming options into the retry loop so rate-limit/network backoff can be cancelled
- pass the signal to httpClient.fetch and delayWithAbort for streaming calls to align behavior with non-streaming requests

## Metadata
- **PR**: #917
- **Merged**: 2025-12-06
- **Author**: jleechan2015
- **Stats**: +8/-3 in 1 files
- **Labels**: codex

## Connections
