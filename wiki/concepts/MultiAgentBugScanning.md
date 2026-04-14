---
title: "Multi-Agent Bug Scanning"
type: concept
tags: [multi-agent, parallel, bug-scanning, codex, cursor, minimax, gemini, fresh-context]
last_updated: 2026-03-26
sources: [jleechanclaw-bug-hunt-20260326]
---

## Summary
Multi-agent bug scanning is the pattern of running multiple AI agents in parallel against the same or overlapping sets of PRs/code to maximize bug detection coverage. Each agent uses a different model family (Codex/OpenAI, Cursor, Minimax, Gemini), and results are deduplicated and aggregated into a unified report with severity rankings and suggested fixes.

## Why Parallel Different-Model Agents

Different model families have different coding patterns and training data, which means:
- Different bug detection strengths (some catch logic errors better, others catch edge cases)
- Different false positive rates
- Different coverage of language-specific vs. architecture-level issues

Running 4 agents in parallel over the same 2-day window of merged PRs gives coverage that a single agent cannot match in the same time.

## Agent Roster

| Agent | Model family | Role in bug scan |
|---|---|---|
| Codex | OpenAI | Primary coding agent, strong on logic bugs |
| Cursor | Cursor AI | Primary coding agent, strong on idiom/style bugs |
| Minimax | MiniMax | Primary coding agent, different training corpus |
| Gemini | Google | Primary coding agent, different code understanding |

## Fresh Context per Agent

Each agent scan operates with fresh context:
- The agent receives the PR diff and relevant code, not accumulated session context
- This avoids context bloat that degrades bug detection quality
- Follows the Harness Engineering principle: "Fresh Context, Not Accumulated Context"

## Aggregation and Dedup

Results from all 4 agents are:
1. Collected into `bug_reports/` directory
2. Deduplicated (same file+line from multiple agents → single report)
3. Severity-ranked (1-5 scale)
4. Critical bugs → beads created for tracking
5. Summary posted to Slack #bug-hunt

## Bug Report Schema

Each bug report includes:
- `repo`: repository name
- `pr`: PR number
- `file`: file path
- `line`: line number (when determinable)
- `description`: what the bug is
- `severity`: 1-5
- `suggested_fix`: how to fix it

## Limitations

- Agents scan PRs that have already been merged — bugs found mean a follow-up PR is needed
- No live CI context during scan (agents review the diff, not the running system)
- Severity scoring is subjective to each agent's judgment
- False positives are possible and require human triage

## Related Concepts
- [[DailyBugHunt]]
- [[AutonomousAgentLoop]]
- [[IndependentVerification]]