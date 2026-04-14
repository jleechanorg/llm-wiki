---
title: "Autonomous Agent Loop"
type: concept
tags: [autonomous-loop, pr-lifecycle, ci-fix, openclaw, ao, replacement-self]
last_updated: 2026-03-15
sources: [jleechanclaw-orchestration-system-design]
---

## Summary
The Autonomous Agent Loop is the core operational pattern where a headless agent (claude-code, codex, or gemini) runs inside an AO worktree, handles a PR fix or review task, and the system automatically handles CI failures and retry without developer intervention. The developer only intervenes for genuine judgment calls.

## How It Works

```
Developer opens PR
  → GitHub webhook POST /webhook (pull_request.opened)
  → webhook_daemon HMAC validates + stores in webhook_deliveries
  → pr_lifecycle normalizes + routes
  → ao_spawn (project, issue) → spawns headless agent in tmux worktree
  → Agent reads PR, implements fix, pushes commit → CI starts
  → CI runs → AO detects result via scm-github plugin
  → CI green → merge.ready → OpenClaw LLM review
  → CI failed → reaction.escalated → escalation_router routes
    → retry remaining → ao send enriched fix prompt
    → budget exhausted → Slack DM to developer
```

## Key Properties

**Replace Yourself (North Star)**
A PR opened Monday should be merged Monday. CI failures auto-fixed, review comments auto-addressed, CodeRabbit approval obtained, merge-readiness gates passed. Developer's GitHub notification feed becomes near-empty.

**Memory Compounds**
Without memory, every CI failure is the first CI failure the system has ever seen. With the outcome ledger, a `ModuleNotFoundError` on a Django project triggers a known-good fix strategy instead of random exploration.

**Parallel Retry**
Instead of 3 sequential retries (30 minutes), the system can run 3 parallel strategies (10 minutes) — first green wins.

## The Five Gates of Merge-Readiness

| Gate | Source | Check |
|------|--------|-------|
| CI green | GitHub Actions | All required checks `conclusion == success` |
| No conflicts | GitHub API | `mergeable == "MERGEABLE"` |
| No serious comments | CodeRabbit, Copilot, Cursor Bugbot | No `REQUEST_CHANGES` verdict |
| Evidence reviewed | CodeRabbit / Codex via `/er` | Evidence review PASS or WARN |
| OpenClaw approved | pr_reviewer.py LLM | `ReviewDecision.approve` |

## Failure Modes

| Failure Mode | System Response |
|---|---|
| CI failed, budget >= 2, parseable error | ParallelRetryAction (2-3 worktrees) |
| CI failed, budget remaining | RetryAction (single ao send) |
| Budget exhausted | NotifyJeffreyAction (Slack DM) |
| Session stuck (idle > threshold) | KillAndRespawnAction |
| Vague review comment | OpenClaw LLM interprets + dispatches |
| Risky change in sensitive path | OpenClaw LLM escalates with warning |

## Contrast with Manual Workflow

Manual: Write code → open PR → wait for CI → fix CI → wait for review → fix review → merge = hours of attention across multiple days.

Autonomous: Developer opens PR → system handles everything until "ready to merge" Slack → developer hits merge. The debugging never touches developer attention.

## Related Concepts
- [[HarnessEngineering]]
- [[MemoryTierArchitecture]]
- [[EscalationRouter]]
- [[MergeReadinessContract]]
- [[DailyBugHunt]]