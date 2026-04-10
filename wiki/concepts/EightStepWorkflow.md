---
title: "Eight-Step Workflow"
type: concept
tags: [workflow, process, orchestration]
sources: ["zoe-openclaw-agent-swarm-reference"]
last_updated: 2026-04-07
---

The complete workflow from customer request to merged PR.

## Steps

### Step 1: Scope with Orchestrator
Customer request → discuss with Zoe → Zoe pulls context (Obsidian vault, CRM, prod DB), writes precise prompt

### Step 2: Spawn Agent
Each agent gets own git worktree, tmux session, detailed prompt with full context

### Step 3: Monitor (Cron Every 10 Min)
Check-agents.sh checks liveness, PRs, CI status, auto-respawns (max 3 attempts)

### Step 4: Agent Creates PR
`gh pr create --fill` — PR alone doesn't trigger notification

### Step 5: Automated Code Review (3 Models)
Codex (edge cases), Gemini (security), Claude Code (validation)

### Step 6: Automated Testing
Lint + TypeScript + Unit + E2E + Playwright against preview env. UI changes require screenshot in PR (CI enforced)

### Step 7: Human Review
Telegram notification: "PR #341 ready for review." 5-10 min review, often merge without reading code

### Step 8: Merge
Daily cron cleans up orphaned worktrees and task registry

## Connections
- [[ZOE]] — orchestrator for steps 1-3, 7
- [[AgentSpawning]] — step 2
- [[CronMonitoring]] — step 3
- [[AutomatedCodeReview]] — step 5
- [[AutomatedTesting]] — step 6
