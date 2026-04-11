---
title: "PR #6027: fix(claw): source .bashrc via interactive shell for env var inheritance"
type: source
tags: []
date: 2026-03-19
source_file: raw/prs-worldarchitect-ai/pr-6027.md
sources: []
last_updated: 2026-03-19
---

## Summary
The /claw command dispatches tasks to OpenClaw via nohup openclaw agent. However, nohup subprocesses do not inherit shell env vars defined in ~/.bashrc, causing openclaw plugins (e.g. openclaw-mem0) to fail with errors like GROQ_API_KEY is not set.

Two prior commits on feature branches (b958515255 and dc906cd5a4) attempted fixes but were never merged to main.

## Metadata
- **PR**: #6027
- **Merged**: 2026-03-19
- **Author**: jleechan2015
- **Stats**: +7/-4 in 1 files
- **Labels**: none

## Connections
