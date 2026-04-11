---
title: "PR #260: fix: enforce conversation MCP configuration"
type: source
tags: []
date: 2025-10-11
source_file: raw/prs-/pr-260.md
sources: []
last_updated: 2025-10-11
---

## Summary
- register `convo.send-message` and route through ConversationMCPTool.sendMessage so single-message flows auto-create conversations
- document and enforce `CONVERSATION_MCP_SERVER_URL` via deployment docs and scripts, including Express typings for the HTTP proxy
- harden `conversation_config_test.sh` to probe `convo.send-message` against a local server and fail fast when the conversation MCP URL is missing

## Metadata
- **PR**: #260
- **Merged**: 2025-10-11
- **Author**: jleechan2015
- **Stats**: +423/-56 in 17 files
- **Labels**: none

## Connections
