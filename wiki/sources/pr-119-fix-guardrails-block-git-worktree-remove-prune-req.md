---
title: "PR #119: fix(guardrails): block git worktree remove/prune — require manual human approval"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-119.md
sources: []
last_updated: 2026-03-23
---

## Summary
During a monitoring session (2026-03-22), a bulk worktree cleanup script iterated all registered git worktrees in the agent-orchestrator repo without scoping to AO session names. It deleted `worktree_worker5`, `worktree_worker2`, `worktree_agentog2`, `worktree_pr82`, and `worktree_pr98` — all active Claude Code session directories. All shell commands in the affected sessions broke instantly (`CWD no longer exists`). The session was unrecoverable without manual intervention.

## Metadata
- **PR**: #119
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +268/-0 in 3 files
- **Labels**: none

## Connections
