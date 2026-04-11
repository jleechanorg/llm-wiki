---
title: "PR #563: fix: stop exposing convo tools via FastMCP proxy"
type: source
tags: [codex]
date: 2025-11-05
source_file: raw/prs-/pr-563.md
sources: []
last_updated: 2025-11-05
---

## Summary
- block convo.* tool invocations at the HTTP proxy and strip them from tools/list responses
- update the conversation configuration integration check to expect only conversation.* tools
- document that the backend no longer exposes convo.* helpers directly

## Metadata
- **PR**: #563
- **Merged**: 2025-11-05
- **Author**: jleechan2015
- **Stats**: +247/-34 in 3 files
- **Labels**: codex

## Connections
