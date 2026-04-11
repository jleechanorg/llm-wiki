---
title: "PR #349: [P1] fix: restore register_agent call with agent_name alias (was silently disabled)"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-349.md
sources: []
last_updated: 2026-03-21
---

## Summary
- MCP server (mcp_agent_mail) now accepts agent_name as an alias for name in register_agent, so agents calling it with the natural agent_name parameter (matching fetch_inbox convention) no longer get a Pydantic validation error
- agent-orchestrator.yaml agentRules restored to call register_agent with agent_name before send_message
- The previous workaround (Do NOT call register_agent) was counterproductive: send_message also requires the sender to be a registered agent, so silently skipping regi

## Metadata
- **PR**: #349
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +7/-7 in 1 files
- **Labels**: none

## Connections
