---
title: "2026-06-13 Agy Trust Prompt Inner Workspaces"
type: source
tags: ["project", "agent-orchestrator"]
date: 2026-06-13
source_file: raw/project_2026-06-13_agy_trust_prompt_inner_workspaces.md
---

## Summary
agy trust prompt (\

## Key Claims
- | `~/.gemini/trustedFolders.json` (outer) | legacy / some internal commands (NOT session-startup) |
- | `~/.gemini/antigravity-cli/settings.json` `trustedWorkspaces` (inner) | agy session-startup code (THIS is what fires the trust prompt) |
- - killed at 98s, `killConfirmed=stuck-probe`
- - Log: `~/.ao-sessions/ao-6353/.gemini/antigravity-cli/log/cli-20260613_032803.log` shows trust prompt 30s after spawn, then waiting for input
- - Outer trustedFolders.json was correctly populated with the worktree path
- - Inner antigravity-cli/settings.json trustedWorkspaces was NOT populated

## Connections
- [[AgentOrchestrator]] — AO worker dispatch memory
- Source: `raw/project_2026-06-13_agy_trust_prompt_inner_workspaces.md`
