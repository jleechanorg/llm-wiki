---
title: "jleechanclaw-pr-review-decision"
type: source
tags: [jleechanclaw, pr-review, llm, autonomous]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/pr_review_decision.py
---

## Summary
Pure LLM PR review decision engine. The LLM receives the full ReviewContext and makes all decisions through inference — no hardcoded rules, no deterministic gating, no keyword matching. Posts review via gh CLI for approve/request_changes and sends Slack DM to Jeffrey for escalations. Falls back to subprocess `claude -p` if Anthropic SDK is unavailable.

## Key Claims
- Zero-framework cognition: all decisions delegated to LLM inference over full context
- Action set: approve, request_changes, escalate_to_jeffrey, skip
- Confidence score clamped to [0, 1]
- Comments parsed as path/line/body for inline review suggestions
- LLM call uses claude-sonnet-4-6 via Anthropic SDK or claude CLI fallback
- Slack escalation sends to JEFFREY_DM_CHANNEL (D0AFTLEJGJU)

## Connections
- [[jleechanclaw-pr-reviewer]] — provides ReviewContext consumed here
- [[jleechanclaw-canary]] — different Slack notification pattern (canary/heartbeat)

## Contradictions
- None identified