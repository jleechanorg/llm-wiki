---
title: "Tmux Session Management"
type: concept
tags: [execution-model, monitoring, sessions]
sources: []
last_updated: 2026-04-07
---

Tmux session management is the execution model used by Genesis for running agent tasks. It provides interactive, observable, and resumable sessions.

## Characteristics
- **Interactive**: Sessions can be attached and monitored manually
- **Observable**: Real-time output visible in terminal
- **Resumable**: Sessions persist and can be reattached after disconnect

## Comparison to Alternative
- Genesis uses tmux sessions (interactive)
- Ralph uses background processes (daemon-style)
- Different monitoring approaches required for each model
