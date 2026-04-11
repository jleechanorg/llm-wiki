---
title: "WorldArchitect.AI AGENTS.md — Repository Guidelines"
type: source
tags: [worldarchitect, agents, rules, github, testing]
date: 2026-04-06
source_file: /Users/jleechan/worldarchitect.ai/AGENTS.md
---

## Summary

The AGENTS.md is the compact core contract for agents working in the WorldArchitect.AI repository. It prioritizes structured JSON schemas over prose, mandates a GOAL/MODIFICATION/NECESSITY/INTEGRATION PROOF file protocol before editing, preserves crontab `GITHUB_TOKEN` lines, and maintains `.beads/` as version-controlled. It defines a strict integration hierarchy for new file creation and enforces that `.beads/` changes are included in all PRs.

## Key Claims

- JSON input/output schemas preferred over prose templates for LLM communication
- File protocol (required before any edit): GOAL, MODIFICATION, NECESSITY, INTEGRATION PROOF
- Integration order: existing file → utility → `__init__.py` → test → class method → config → NEW
- `.beads/` MUST be version controlled; never gitignore it; always include in PRs
- Use `gh` for all GitHub operations (PRs/issues/checks/releases)
- Never delete/remove the active worktree unless explicitly asked
- At session end: quality checks + push branch updates; work not complete until push succeeds
- Testing: `testing_mcp/` and `testing_ui/` must run with real services only (no mock mode)
- tmux sessions with dynamic task agents; never execute orchestration tasks personally
- Modal routing priority: God mode → character creation → level-up → campaign upgrade → character creation state → combat state → semantic intent classifier → explicit override → story fallback
- Stale-flag guards required for level-up: `level_up_in_progress=False` and `level_up_pending=False` block stale reactivation
- Pre-rebase checklist: conflict markers, lint/type-check, staged files verification
- Beads integration: `bd ready --json`, `bd create`, `bd update`, `bd close`

## Key Quotes

> "Default to integrating into existing files. New file creation is last resort." — file creation philosophy

> "Keep `.beads/` tracked and include beads changes in PRs." — non-negotiable

> "At session end: quality checks + push branch updates; work is not complete until push succeeds." — session completion rule

> "LLM decides, server executes." — core architectural principle

## Connections

- [[Claude]] — extends Claude Code CLI conventions
- [[ClaudeCode]] — governs Claude Code CLI behavior
- [[Beads]] — beads issue tracking is core to agent workflow
- [[AgentOrchestration]] — tmux-based dynamic task agents

## Contradictions

- None identified
