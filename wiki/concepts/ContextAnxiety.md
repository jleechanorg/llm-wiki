---
title: "Context Anxiety"
type: concept
tags: [context, compaction, context-reset, anxiety, model-behavior]
date: 2026-03-24
source: [[anthropic-harness-design-long-running-apps]]
---

## Definition
"Context anxiety" is the behavior where models wrap up prematurely as their context window fills — even with compaction active. The model becomes risk-averse and tries to conclude before the work is actually done.

## The Problem with Compaction Alone
Compaction summarizes history in place, preserving continuity. But it doesn't give a clean slate — anxiety persists. The model knows the window is filling and starts wrapping up defensively.

## Solution: Context Resets
A **context reset** clears the context window entirely. The next agent starts with a fresh slate. Cost: token overhead for the handoff artifact. Benefit: no anxiety, no premature wrapping.

| Approach | Behavior | Limitation |
|----------|----------|-------------|
| Compaction | Summarizes history in place | Clean slate unavailable; anxiety persists |
| Context Reset | Clears context window entirely | Requires sufficient handoff artifact |

## When to Reset
- Context window >80% mid-sprint
- Model exhibits premature wrap-up
- Sprint runs >90 minutes without eval

## State Artifact
```json
{
  "sprint": 3,
  "in_progress_files": ["src/handlers/auth.go"],
  "cursor_positions": {"src/handlers/auth.go": "line 247"},
  "next_steps": ["finish auth handler", "write tests"],
  "context_pct": 82
}
```

## Note
Opus 4.6 largely eliminated context anxiety, allowing harness simplification. Check whether current models still require explicit reset triggers.

## Connections
- [[ContextReset]] — the mechanism that solves context anxiety
- [[FileBasedHandoffs]] — how state survives the reset
- [[SprintContract]] — what keeps scope tight during resets
