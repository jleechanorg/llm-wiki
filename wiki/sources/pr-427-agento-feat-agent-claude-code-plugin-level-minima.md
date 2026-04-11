---
title: "PR #427: [agento] feat(agent-claude-code): plugin-level MiniMax routing via model prefix"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-427.md
sources: []
last_updated: 2026-04-11
---

## Summary
- Detects MiniMax models by `MiniMax-` prefix in `AgentLaunchConfig.model`
- For MiniMax models: sets `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic` and `ANTHROPIC_AUTH_TOKEN=$MINIMAX_API_KEY` / `ANTHROPIC_API_KEY=$MINIMAX_API_KEY` in worker env, omits `env -u ANTHROPIC_BASE_URL` from launch command
- For all other models: clears `ANTHROPIC_BASE_URL` (unchanged behavior â†’ Anthropic OAuth)
- Removes dead `~/.bashrc` AO-session conditional (was always overridden by the plugin)

**Net effe

## Metadata
- **PR**: #427
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +82/-13 in 2 files
- **Labels**: none

## Connections
