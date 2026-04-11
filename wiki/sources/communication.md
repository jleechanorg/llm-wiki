# Communication Wiki

This file documents communication systems, mail coordination, and messaging infrastructure in the user's environment.

---

## Component: mcp_mail (main repository)
- **Path**: /Users/jleechan/mcp_mail/
- **Type**: mail/mcp-mail
- **Purpose**: Primary MCP Agent Mail coordination server - provides message routing, coordination tooling, and project context to cooperating agents
- **Modified**: 2026-03-25

---

## Component: mcp_mail (Go library)
- **Path**: /Users/jleechan/projects/mcp_mail/
- **Type**: mail/library
- **Purpose**: Go implementation of mail system with mailbox, routing, delivery, and resolve logic
- **Modified**: 2026-02-23

---

## Component: mcp_mail Backups
- **Path**: /Users/jleechan/.mcp_agent_mail_backups/
- **Type**: mail/backup
- **Purpose**: Backup snapshots of mcp_mail repository with SQLite storage for messages
- **Modified**: 2025-12-17

---

## Component: gastown Mail (Slack integration)
- **Path**: /Users/jleechan/projects/gastown/internal/mail/
- **Type**: slack/bot-token
- **Purpose**: Slack bot authentication for gastown agent coordination system
- **Modified**: 2026-02-01

---

## Component: gastown Message Templates
- **Path**: /Users/jleechan/projects/gastown/internal/templates/messages/
- **Type**: mail/templates
- **Purpose**: Message templates for agent handoff, escalation, nudge, and spawn communications
- **Modified**: 2026-02-23

---

## Component: openclaw-config Slack Credentials
- **Path**: /Users/jleechan/openclaw-repo/openclaw-config/credentials/slack/
- **Type**: slack/credentials
- **Purpose**: Slack integration credentials and configuration for openclaw agent system
- **Modified**: 2026-02-13

---

## Component: cron-gateway Slack Credentials
- **Path**: /Users/jleechan/worktrees/jleechanclaw-cron-gateway/openclaw-config/credentials/slack/
- **Type**: slack/credentials
- **Purpose**: Slack credentials for scheduled agent cron gateway system
- **Modified**: 2026-02-01

---

## Component: mcp_mail Agent Config
- **Path**: /Users/jleechan/mcp_mail/.mcp.json
- **Type**: mail/mcp-config
- **Purpose**: MCP server configuration for agent mail coordination
- **Modified**: 2026-01-31

---

## Component: agent-bridge Slack Source
- **Path**: /Users/jleechan/worktrees/beads_prs_20260309_020425/jleechanorg__agent_bridge/src/slack
- **Type**: slack/source
- **Purpose**: Slack integration source code for agent bridge project
- **Modified**: various

---

## Component: agent-mail Project Data
- **Path**: /Users/jleechan/.mcp_agent_mail_backups/mcp_mail_repo_dot_mcp_mail_20251218_000804/projects/
- **Type**: mail/project-data
- **Purpose**: Project-specific message data stored in agent mail backups
- **Modified**: 2025-12-17

---

## Component: openclaw-docs Slack Documentation
- **Path**: /Users/jleechan/projects/openclaw-docs/skills/slack
- **Type**: slack/docs
- **Purpose**: Slack integration documentation and skills for openclaw
- **Modified**: various

---

## Component: worldarchitect-automation Mail History
- **Path**: /Users/jleechan/Library/Logs/worldarchitect-automation/pr_history/mcp_mail
- **Type**: mail/history
- **Purpose**: Automation system mail/PR history logs
- **Modified**: various