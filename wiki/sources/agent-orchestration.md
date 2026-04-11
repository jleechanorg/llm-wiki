---
name: agent-orchestration
type: system
provenance:
  source: /Users/jleechan/.antigravity-loop
  ingested: 2026-04-07
  last_seen: 2026-04-07
---

# Agent Orchestration System

Multi-agent coordination system spanning multiple projects including agent-orchestrator, ai_universe_living_blog, jleechanclaw, mctrl_test, org-runners, and worldai_claw.

## Components

### Antigravity Loop

- **Path**: `/Users/jleechan/.antigravity-loop`
- **Type**: component (orchestrator)
- **Purpose**: Self-running agent orchestration loop with watchdog functionality
- **Status**: Active

### AO Runner

- **Path**: `/Users/jleechan/.ao-runner.d`
- **Type**: component (orchestrator)
- **Purpose**: Runner data for orchestrator sessions
- **Projects**: agent-orchestrator, ai_universe_living_blog, jleechanclaw, mctrl_test, org-runners, worldai_claw
- **Status**: Active

### Orchestrator Sessions

- **Path**: `/Users/jleechan/.ai_orch_sessions.json`
- **Type**: component (agent data)
- **Purpose**: Tracks active Claude/Codex/Minimax/Gemini/Cursor sessions across worktrees and projects
- **Entry Count**: ~253

### AI Universe Memory Sync

- **Path**: `/Users/jleechan/.ai-universe`
- **Type**: component (memory sync)
- **Purpose**: Authentication tokens and scripts for AI Universe service integration, includes Firebase service account keys
- **Status**: Active

## Related

- [index](index.md) - Full catalog
- [code-projects](code-projects.md) - Code project references