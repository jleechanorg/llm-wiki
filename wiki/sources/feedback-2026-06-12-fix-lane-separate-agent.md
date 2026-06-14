---
title: "Fix-lane as separate agent pattern (2026-06-12)"
type: source
tags: [fix-lane, separate-agent, parallel-fanout, review-response, bugbot-stale, argparse-greedy, exec-defeats-trap, test-pollution]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_fix_lane_separate_agent.md
---

## Summary
When a 2-lane parallel fanout lands a PR pair and BOTH come back from review with actionable findings, spawn a fresh fix-lane subagent — not a continuation of the original lane agents. One subagent can handle both branches (read-only on what shipped, then push targeted fix commits per PR). The original agents were tuned for "build green from spec," not "respond to 5-comment review thread with surgical fixes."

## Key Claims
- Fresh fix-lane agent reads the diff + the review, writes a fix list, and pushes 1-2 commits per PR — cleaner than extending the original
- Bugbot stale-comment trap: `CHANGES_REQUESTED` from a pre-fix review does NOT auto-dismiss when fix commits land; treat as stale when actionable items = 0, CI green, CodeRabbit skipped/approved; admin-merge is fine
- Argparse `--bash-argv` lesson: any boolean-style flag followed by a positional argv is greedy and steals tokens; pass complex payloads as JSON-encoded strings (single argument, no ambiguity)
- `exec python` defeats bash traps: `exec` replaces the shell so the EXIT trap never fires on Python's non-zero exit; either remove `exec` or use a subshell wrapper; trade-off: one extra bash process per invocation
- Test pollution to `~/.dark-factory/panics/` is the failure mode the v9 perf-log lesson warned about; make the panic dir an explicit `--panic-dir` flag and the test pass a tmp_path

## Key Quotes
> "One subagent can handle both branches (read-only on what shipped, then push targeted fix commits per PR). Cleaner than extending the original."

> "`exec python` defeats bash traps: `exec` replaces the shell, so the EXIT trap never fires on Python's non-zero exit. Either remove `exec` (bash stays alive, trap fires) OR use a subshell wrapper."

## Connections
- [[FixLanePattern]] — separate subagent for review-response work
- [[BugbotStaleComments]] — CHANGES_REQUESTED does not auto-dismiss
- [[FileDisjointLanes]] — file-disjoint pattern that produced the PRs
- [[ArgparseGreedyFlag]] — JSON-encoded payload pattern
- [[TestPollution]] — `--panic-dir` flag + tmp_path pattern
