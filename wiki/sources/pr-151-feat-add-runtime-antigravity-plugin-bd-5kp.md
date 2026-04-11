---
title: "PR #151: feat: add runtime-antigravity plugin (bd-5kp)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-151.md
sources: []
last_updated: 2026-03-24
---

## Summary
The AO (Agent Orchestrator) currently supports tmux-based runtimes for spawning coding agents. This PR adds a new runtime plugin that uses Google's Antigravity IDE as a worker runtime via Peekaboo macOS accessibility API. Antigravity runs Gemini/Opus autonomously once a conversation is started, leveraging Google's model quota.

Design spec: `docs/design/antigravity-orchestrator.md`
Epic: bd-5kp

## Metadata
- **PR**: #151
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +3880/-132 in 29 files
- **Labels**: none

## Connections
