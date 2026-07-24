---
title: "Go AO factory dispatch + claudem MiniMax sync --all (2026-07-06)"
type: source
tags: [dark-factory, agent-orchestrator, go-ao, claudem, minimax]
date: 2026-07-06
source_file: raw/feedback_2026-07-06_go_ao_factory_claudem_setup.md
---

## Summary

dark-factory `/af` dispatch switched from TypeScript AO (`ao-ts`) to the Go mirror binary (`ao-go`) with headless `ao daemon` on port 3001. MiniMax/claudem routing cannot use harness name `claudem` without mirror code; instead `factory-ao-minimax-sync.sh --all` applies claudem-equivalent env to every registered Go AO project. Global `~/bin/claudem` executable added for non-interactive shells.

## Key Claims

- Go AO validates harness names; `claudem` is rejected — use `claude-code` + project env.
- `ao start` opens Electron app; factory uses `ao-go daemon` headless.
- TS `wa-*` and Go `worldarchitect-*` sessions are separate namespaces.
- MiniMax sync must run per project (`--all` loop); no global agent env in Go AO without code change.

## Connections

- [[DarkFactory]] — `/af` tick and factory-ao-remediate.sh
- [[AgentOrchestrator]] — Go mirror at agent-orchestrator-mirror
