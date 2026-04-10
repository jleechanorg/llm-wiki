---
title: "JeffreyTechStack"
type: concept
tags: [jeffrey, tools, tech-stack, automation]
sources: [github-patterns, ai-coding]
last_updated: 2026-04-09
---

# Jeffrey's Tech Stack

## Claude Code + OpenClaw
Core IDE with cmux session management and model steering.

## Minimax Integration
- MINIMAX_API_KEY env var
- ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
- Default model: MiniMax-M2.5
- Cost-conscious alternative to Anthropic

## gh CLI — Non-Negotiable
All GitHub operations via gh — PRs, issues, checks, releases.
No GitHub web UI for operational tasks.

## Self-Hosted Runners
Private repos use self-hosted runners, not GitHub-hosted.

## beads / br (Rust)
Workflow automation — recent migration from Python .beads.

## Python + asyncio
Primary automation language.
asyncio.run() for async tests.
Flask for HTTP test servers.

## Cron + Launchd
Persistent background automation.
- Every 10 minutes for PR automation
- automation_safety_manager.py tracks limits
- run_automation_cron_one_minute.sh for debug/catch-up

## CodeRabbit
Automated PR review — all CHANGES_REQUESTED resolved before merge.

## Skeptic Gates
Evidence/citation verification in CI — fail-closed.

## mem0
Persistent memory/recall — USER_ID=jleechan in mem0_config.py.

## MCP Agent Mail
Agent-to-agent coordination for orchestrator pattern.

## Testing Infrastructure
- pytest -q for concise output
- WAHttpTest base class with gunicorn
- Real-mode enforcement in core tests

## Not Used (Notably)

- No sparse checkout (prefers full clones)
- No docstrings unless needed
- No README for README's sake
- No verbose logging
