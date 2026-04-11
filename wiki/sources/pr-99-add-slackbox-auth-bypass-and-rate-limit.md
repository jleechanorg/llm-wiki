---
title: "PR #99: Add slackbox auth bypass and rate limit"
type: source
tags: [codex]
date: 2025-12-10
source_file: raw/prs-/pr-99.md
sources: []
last_updated: 2025-12-10
---

## Summary
- exempt the Slackbox webhook from bearer/JWT middleware while applying dedicated Slack-style rate limiting
- keep Slack webhook tests from clobbering any previously initialized Slack client fixture

## Metadata
- **PR**: #99
- **Merged**: 2025-12-10
- **Author**: jleechan2015
- **Stats**: +189/-9 in 7 files
- **Labels**: codex

## Connections
