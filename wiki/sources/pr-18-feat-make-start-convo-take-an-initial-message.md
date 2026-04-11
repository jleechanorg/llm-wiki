---
title: "PR #18: feat: make start convo take an initial message"
type: source
tags: [codex]
date: 2025-10-07
source_file: raw/prs-/pr-18.md
sources: []
last_updated: 2025-10-07
---

## Summary
- allow `start-conversation` to accept an initial message and seed the legacy flow
- refresh the smoke tests/docs to cover legacy + unified APIs and resolve the base URL from CI (SERVICE_URL fallback + gcloud)
- make the conversation server boot logic Jest-friendly and add shared global mocks so unit tests run under CommonJS

## Metadata
- **PR**: #18
- **Merged**: 2025-10-07
- **Author**: jleechan2015
- **Stats**: +1193/-157 in 14 files
- **Labels**: codex

## Connections
