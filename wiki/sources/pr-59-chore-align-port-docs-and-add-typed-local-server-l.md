---
title: "PR #59: chore: align port docs and add typed local server launcher"
type: source
tags: []
date: 2025-11-04
source_file: raw/prs-/pr-59.md
sources: []
last_updated: 2025-11-04
---

## Summary
- document the new Conversation MCP port allocations (6000/6001 dev, 6100/6101 test) in AGENTS.md and ~/.bashrc so the server stays out of the 2000–3000 range
- replace the legacy bash-heavy run_local_server.sh with a TypeScript launcher that prefers port 6000, falls back to random ports when busy, and runs npm run dev without spawning new terminal tabs
- wire the backend package.json to expose npm run run-local-server (tsx watch) so hot reload remains intact

## Metadata
- **PR**: #59
- **Merged**: 2025-11-04
- **Author**: jleechan2015
- **Stats**: +168/-285 in 5 files
- **Labels**: none

## Connections
