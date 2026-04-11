---
title: "PR #750: Only return retryAt payloads vs ratelimit full info"
type: source
tags: [codex]
date: 2025-11-16
source_file: raw/prs-/pr-750.md
sources: []
last_updated: 2025-11-16
---

## Summary
- sanitize ConversationAgent and SecondOpinionAgent so both streaming and non-streaming flows now emit only the retryAt timestamp when their rate limit trips
- document the minimal rate limit response contract and add dedicated regression tests to cover both agents
- align the standalone rate-limit response validation script with the new policy by logging only the retryAt payload

## Metadata
- **PR**: #750
- **Merged**: 2025-11-16
- **Author**: jleechan2015
- **Stats**: +227/-301 in 7 files
- **Labels**: codex

## Connections
