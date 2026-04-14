---
title: "New Machine Setup Guide"
type: source
tags: [setup, macos, ubuntu, automation, dotfiles]
sources: []
last_updated: 2026-04-14
---

## Summary

Full restore guide for macOS and Ubuntu. Start with OOM guard to prevent memory-pressure panics during rest of setup. Covers dotfiles, runtimes, git, Claude/Codex config, cron/launchd automation.

## Key Claims

- OOM Guard (launchd/systemd): prevents memory-pressure panics during setup from runaway user-space tools
- rgignore + rg-safe wrapper: memory-limited ripgrep
- nvm (Node 22/20), pyenv (Python 3.12), Rust/cargo, bun, uv
- GitHub: gh auth login, git lfs install
- Ghostty terminal config
- Claude/Codex MCP config with real tokens
- Home backup via launchd/cron (every 4 hours)
- Disk usage alert via launchd/cron
- Verify OOM guard is working before continuing

## File Index

- ~/.rgignore, ~/.bash_profile, ~/.zshrc, ~/.zshenv, ~/.gitconfig
- ~/.cerebras_model, ~/.npmrc
- ~/.config/ghostty/config
- ~/.codex/AGENTS.md, ~/.codex/config.toml
- ~/.claude/mcp.json
- ~/bin/mem-watchdog.sh, ~/bin/rg-safe, ~/bin/gh-create-repo-auto

## Connections

- [[BackupStrategy]] — Backup before system rebuild

## Contradictions

- None identified
