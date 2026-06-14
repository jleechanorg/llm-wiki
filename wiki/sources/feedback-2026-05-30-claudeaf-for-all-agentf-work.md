---
title: "Feedback 2026-05-30 Claudeaf-For-All-Agentf-Work"
type: source
tags: [feedback, project, memory-file]
date: 2026-05-30
source_file: raw/memory_backfill_2026_06_13/feedback_2026-05-30_claudeaf-for-all-agentf-work.md
---

## Summary

For work under (the Agnt-F org repos), coding must run through — the Agent-F enterprise Claude account (, ), never the bare personal . See [[claude-multi-account-setup]]. the Agnt-F org repos are enterprise work and must be authored/committed under the enterprise identity, not personal .

## Key Claims

- `claudeaf` is now a **function** (not an alias) in `~/.bashrc` (~line 635), so it works in non-interactive shells — the Bash tool, scripts, hooks, and the dark-factory `claude` backend. `export -f claudeaf claudeafc` propagates it to child shells.
- Deterministic enforcement: PreToolUse(Bash) hook `~/.claude/hooks/enforce-claudeaf-agentf.sh` (registered in `~/.claude/settings.json` Bash matcher group) **blocks (exit 2)** any bare `claude`/`clauded*` spawn whose cwd or command references `/Users/jleechan/agent-f`, unless it carries `CLAUDE_CONFIG_DIR=*.claude-agent-f` or uses `claudeaf`/`claudeafc`. Non-claude commands (git, gh, python, the `python -m runner` factory launch) pass through.
- Dark-factory wiring: `runner/handlers.py` `_sanitized_env()` copies the full env (only stripping `*HOLDOUT*`), so launching the factory with `CLAUDE_CONFIG_DIR=~/.claude-agent-f` exported makes every `claude`-backend node use the Agent-F account. The binary is chosen by PATH; the *account* by config dir.

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
