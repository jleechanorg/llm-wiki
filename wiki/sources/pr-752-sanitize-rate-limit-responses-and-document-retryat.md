---
title: "PR #752: Sanitize rate limit responses and document retryAt-only contract"
type: source
tags: [codex]
date: 2025-11-16
source_file: raw/prs-/pr-752.md
sources: []
last_updated: 2025-11-16
---

## Summary
- enforce a `{ retryAt }`-only payload across both ConversationAgent and SecondOpinionAgent (including streaming flows) so rate-limit responses can no longer leak quota metadata
- add dedicated regression suites for each agent to prove that authenticated and anonymous callers, as well as downstream helper failures, always surface only the retry timestamp
- document the minimal response contract (including a change log) and update the standalone validation script so SDK authors can inspect the sa

## Metadata
- **PR**: #752
- **Merged**: 2025-11-16
- **Author**: jleechan2015
- **Stats**: +19/-0 in 1 files
- **Labels**: codex

## Connections
