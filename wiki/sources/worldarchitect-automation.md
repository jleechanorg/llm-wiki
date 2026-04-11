---
title: "WorldArchitect.AI Cross-Organization PR Automation System"
type: source
tags: [worldarchitect, automation, pr-workflow, github, ai-agents, cron]
date: 2026-04-01
source_file: /Users/jleechan/worldarchitect.ai/automation/
---

## Summary

The WorldArchitect.AI automation system monitors and processes PRs across the entire `jleechanorg` GitHub organization using isolated git worktrees, multi-CLI AI agents (Claude/Codex/Gemini/MiniMax), and layered safety limits. It runs three core workflows: PR monitoring (posts Codex instruction comments), FixPR (autonomously fixes conflicts/failing CI), and Codex GitHub Mentions (browser automation for branch updates). Safety limits (50 runs/day, 10 attempts/PR) and launchd/cron scheduling keep operations bounded.

## Key Claims

- Monitors ALL repositories in `jleechanorg` organization (ai_universe, worldarchitect.ai, claude-commands, etc.)
- Each PR processed in isolated git worktree: `~/tmp/jleechanorg-pr-workspaces/{repo}-pr-{num}/`
- Worktree isolation: creates fresh workspace per processing cycle, prunes after completion
- Three AI CLI backends: Claude, Codex, Gemini (configurable via `--agent-cli`)
- Safety dual-limits: per-PR max 10 attempts + global max 50 runs/day (resets at midnight)
- Workflow-specific comment limits: PR automation, Fix-comment, Codex Update, FixPR each have 10-comment budgets
- 6-point green criteria for merging: mergeable + not dirty + CodeRabbit approved + Bugbot reviewed + no CHANGES_REQUESTED + evidence PASS
- Comment markers prevent duplicate processing: `codex-automation-commit`, `fix-comment-automation-run`, `fixpr-automation-run`
- Scheduled via launchd/native schedulers (migrated from crontab), offset schedules prevent thundering herd
- Codex GitHub Mentions: Playwright + Chrome CDP for browser automation; auth state persists across runs
- `testing_mcp/` and `testing_ui/` run with real services only — no mock mode
- Install via PyPI or git+https for reproducible cron deployments (editable installs break in multi-worktree setups)

## Key Quotes

> "Safety limits are hardcoded in the automation package; override via CLI flags (not environment variables)" — configuration philosophy

> "EDitable installs break in multi-worktree setups — DO NOT use pip install -e . for cron jobs" — critical operational insight

> "Codex GitHub Mentions automation connects to existing Chrome via CDP to bypass Cloudflare" — auth persistence strategy

## Automation Architecture

| Component | Technology | Purpose |
|-----------|-----------|---------|
| PR Discovery | GitHub GraphQL/REST API | Organization-wide PR search |
| Worktree Isolation | `git worktree add/remove` | Isolated per-PR workspaces |
| AI Agent Dispatch | Claude/Codex/Gemini/MiniMax | Autonomous fix implementation |
| Safety Manager | File-based rate limiting | Per-PR + global limits |
| Browser Automation | Playwright + Chrome CDP | Codex GitHub mentions |
| Scheduling | launchd/cron | Every 10-30 min intervals |

## 6-Point Green Merge Criteria

1. `mergeable == true` (GitHub API)
2. `mergeable_state` not `dirty` or `unstable`
3. CodeRabbit (`coderabbitai[bot]`) has APPROVED
4. Bugbot (`cursor[bot]`) has reviewed
5. Bugbot's latest review is NOT `CHANGES_REQUESTED`
6. Evidence review PASS comment present (`**PASS**` or `evidence.*✅`)

## Connections

- [[Claude]] — Claude CLI as one of the AI agent backends
- [[Codex]] — Codex CLI as AI agent backend
- [[AgentOrchestration]] — orchestration system dispatching agents
- [[GitBranchTracking]] — worktree-based isolation for PR processing
- [[Beads]] — beads track automation progress and blockers
- [[MiniMax]] — MiniMax CLI as additional agent backend

## Contradictions

- None identified
