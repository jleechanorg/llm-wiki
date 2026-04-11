---
title: "PR #212: Containerize Claude CLI tooling with SDK runner, auth reuse, and self-hosted CI"
type: source
tags: [codex]
date: 2025-10-07
source_file: raw/prs-/pr-212.md
sources: []
last_updated: 2025-10-07
---

## Summary
- replace the legacy claude-cli wrapper with a Docker-driven SDK image that mounts host auth state, forwards slash commands, and orchestrates `/testllm`
- add a Node-based Claude Code SDK runner plus pinned dependency versions shared by both local installs and the container build
- introduce a self-hosted "Claude Copilot Verification" workflow that runs the Docker wrapper, along with README documentation covering automation, runner setup, and PR guidance

## Metadata
- **PR**: #212
- **Merged**: 2025-10-07
- **Author**: jleechan2015
- **Stats**: +1107/-8 in 7 files
- **Labels**: codex

## Connections
