---
title: "PR #565: refactor: consolidate conversation persistence on sendMessage"
type: source
tags: [codex]
date: 2025-11-05
source_file: raw/prs-/pr-565.md
sources: []
last_updated: 2025-11-05
---

## Summary
- route all conversation persistence through ConversationMCPTool.sendMessage and remove the redundant addMessage helper
- update ConversationAgent, SecondOpinionAgent, and SingleModelChatService to send both user and assistant messages via sendMessage
- refresh mocks and Jest suites to reflect the unified API surface

## Metadata
- **PR**: #565
- **Merged**: 2025-11-05
- **Author**: jleechan2015
- **Stats**: +355/-232 in 9 files
- **Labels**: codex

## Connections
