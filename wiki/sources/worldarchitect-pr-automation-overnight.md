---
title: "Overnight PR Merge Loop — Automation Instructions"
type: source
tags: [worldarchitect, pr-automation, overnight-loop, github, cron]
date: 2026-03-16
source_file: /Users/jleechan/Downloads/OVERNIGHT_MERGE_LOOP.md
---

## Summary

An overnight automation loop that drives all open PRs in `jleechanorg/jleechanclaw` to merge while the user sleeps. Runs every 15 minutes via cron, scoring each PR against 6 green criteria (mergeable state, CodeRabbit approval, Bugbot review, evidence PASS). Dispatches Claude Code agents via `/claw` for PRs needing fixes, with escalation rules after 3 consecutive failed iterations.

## 6-Point Green Criteria

| # | Condition | Check |
|---|-----------|-------|
| 1 | `mergeable == true` | `gh api .../pulls/NUM \| jq .mergeable` |
| 2 | `mergeable_state` not dirty/unstable | same API |
| 3 | CodeRabbit approved | reviews API |
| 4 | Bugbot reviewed | reviews API |
| 5 | Bugbot latest review not CHANGES_REQUESTED | reviews API |
| 6 | Evidence review PASS comment | look for `**PASS**` or `evidence.*✅` |

## Scoring Actions

- **Score 6/6**: Merge immediately
- **Score 5/6** (only missing evidence PASS): Post `**PASS** — evidence review: no obvious issues`, then merge
- **CI failing or CR CHANGES_REQUESTED**: Check AO status; if no agent, dispatch `/claw agento fix PR NUM`
- **PR #208** (37 commits, messy): Close and recreate on clean branch
- **Read MCP mail** (project_key=jleechanclaw, agent_name=clawmain): Reply to blocked agents
- **Post Slack summary** to #ai-slack-test

## Escalation Rule

After 3 consecutive iterations with no progress on a PR (same score, same blocker, no new commits or agent activity):
- Merge conflict → rebase the branch myself
- CI flake → re-trigger failing check
- Trivial CR comment → fix inline (read, edit, commit, push)
- Agent dispatched but exited without progress → fix myself

## Key Insight

Firing 10+ `/claw` dispatches in rapid succession causes `openclaw-mcp` Node process leaks — each dispatch spawns new agent process which starts MCP server instances, and when agents exit, the Node MCP server children are orphaned (not cleaned up). Each leaked process consumes ~50-200 MB RSS. A cleanup cron or rate-limiting is needed.

## Connections

- [[Claude]] — uses Claude Code CLI via `/claw`
- [[AgentOrchestration]] — dispatches agents autonomously
- [[GitBranchTracking]] — worktree-based PR processing

## Contradictions

- None identified
