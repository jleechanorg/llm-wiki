---
title: "OpenClaw Orchestration System Design"
type: source
tags: [openclaw, orchestration, agent-orchestrator, autonomous-loop, memory, escalation]
date: 2026-03-15
source_file: /home/jleechan/project_jleechanclaw/jleechanclaw/docs/ORCHESTRATION_SYSTEM_DESIGN.md
---

## Summary
The OpenClaw Orchestration System replaces manual developer intervention in the PR lifecycle by layering deterministic AO reactions with LLM-powered OpenClaw judgment. The system handles CI failures, review comments, and merge readiness autonomously — the developer only sees work that genuinely requires human judgment.

## Key Claims
- **Replace Yourself**: The north star is that Jeffrey only sees work requiring genuine judgment; everything else is automated (CI fixes, review comment handling, merge gates)
- **Memory makes the system smarter**: Three memory tiers (project, feedback, outcome ledger) compound across sessions so each CI failure isn't the "first ever"
- **Deterministic first, LLM for judgment**: 80% of PR reactions are deterministic rules; LLM only called for ambiguous cases (vague reviews, strategy decisions, risk assessment)
- **Fail closed, escalate explicitly**: Budget exhaustion always triggers Slack notification; sessions never silently loop
- **Config-first**: Before writing Python, check if openclaw config (SOUL.md, TOOLS.md, cron/) can achieve the goal

## Key Quotes
> "A stateless agent is permanently dumb. This system has three memory tiers that compound across every task." — ORCHESTRATION_SYSTEM_DESIGN.md
> "The LLM is expensive, slow, and occasionally wrong. Deterministic code is cheap, fast, and predictable." — ORCHESTRATION_SYSTEM_DESIGN.md
> "Jeffrey reviews a Slack message that says 'PR #173 is merge-ready' and hits merge. The 2 hours of CI debugging never touched his attention." — ORCHESTRATION_SYSTEM_DESIGN.md

## Connections
- [[AgentOrchestrator]] — session lifecycle manager (spawn/kill tmux worktrees), monitors CI, auto-remediates deterministically
- [[OpenClaw]] — LLM brain with persistent memory, makes judgment calls above the AO reaction layer
- [[MergeReadinessContract]] — the five-gate contract that defines when a PR is truly merge-ready
- [[HarnessEngineering]] — the broader philosophy of building environments and feedback loops that make agents reliable
- [[DailyBugHunt]] — a 9am Pacific daily cron job that spawns 4 parallel agents to scan recently merged PRs for bugs

## Architecture Overview

```
Developer opens PR → GitHub webhook → webhook_daemon → pr_lifecycle
  → ao_spawn (tmux worktree, headless agent)
  → CI runs → AO detects result
  → CI green → OpenClaw LLM review → Slack "ready to merge"
  → CI failed → escalation_router routes deterministically
    → retry budget ≥ 2 + parseable error → parallel fix (2-3 worktrees)
    → retry budget remaining → single retry via ao send
    → budget exhausted → Slack escalation to developer
```

## Memory Flow

```
Agent session completes
  → outcome_recorder.record_outcome(error_class, strategy, result)
  → outcomes.jsonl
  → pattern_synthesizer.py (cron, nightly)
    → "for ImportError on Django models, strategy-B wins 78%"
  → generate_fix_strategies() seeds next retry with winning strategies
```

## Merge-Readiness Gates (all five required)
1. CI green (GitHub Actions, all checks success)
2. No conflicts (GitHub API, mergeable == "MERGEABLE")
3. No serious comments (CodeRabbit/Copilot/Cursor Bugbot no REQUEST_CHANGES)
4. Evidence reviewed (CodeRabbit/Codex via /er, PASS or WARN)
5. OpenClaw approved (pr_reviewer.py LLM, ReviewDecision.approve)

## Implementation Status
- Ingress (webhook_ingress.py:19888, HMAC) ✅ Live
- AO spawn dispatch (webhook_worker.py) ✅ E2E proven
- Escalation router ✅ Implemented
- Failure budgets ✅ Implemented
- Parallel retry ✅ Implemented
- PR reviewer (LLM) ✅ Wired to Claude API
- CodeRabbit gate ✅ Implemented
- Evidence review gate ✅ Implemented
- Outcome recorder ✅ Implemented
- Pattern synthesizer (cron) ✅ Implemented
- Daily bug hunt ✅ Implemented
- Self-improving prompts 🔴 Not started
- Auto-triage notifications 🔴 Not started
- Convergence Intelligence Layer 🔴 Not started

## Related Concepts
- [[AutonomousAgentLoop]]
- [[MemoryTierArchitecture]]
- [[EscalationRouter]]
- [[MergeReadinessContract]]