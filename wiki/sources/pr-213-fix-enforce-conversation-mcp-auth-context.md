---
title: "PR #213: fix: enforce conversation MCP auth context"
type: source
tags: [codex]
date: 2025-10-07
source_file: raw/prs-/pr-213.md
sources: []
last_updated: 2025-10-07
---

## Summary
- remove the in-memory conversation storage fallback and require a configured remote conversation MCP service
- document the mandatory conversation MCP environment variables and deployment steps for Cloud Run
- add configuration guardrails and tests to ensure the server fails fast when required settings are missing
- ensure ConversationAgent builds MCP auth contexts so MCP tool executions forward required headers
- validate trimmed MCP service user IDs and extract the token estimation constant f

## Metadata
- **PR**: #213
- **Merged**: 2025-10-07
- **Author**: jleechan2015
- **Stats**: +51/-8 in 3 files
- **Labels**: codex

## Connections
