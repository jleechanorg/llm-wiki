---
title: "Codex `--full-auto` Flag Broken (Use `--dangerously-bypass-approvals-and-sandbox`)"
type: source
tags: ["codex", "agent-orchestrator", "plugin-fix", "feedback"]
date: 2026-06-05
source_file: feedback_2026-06-05_codex_full_auto_flag_broken.md
---

## Summary
Codex CLI no longer accepts `--full-auto`; `packages/plugins/agent-codex/src/index.ts` must use `--dangerously-bypass-approvals-and-sandbox` instead. The plugin dist was not updated post-CLI change.

## Key Claims
- `ao spawn --agent codex` exits immediately with `error: unexpected argument '--full-auto' found`
- Fix: `packages/plugins/agent-codex/src/index.ts:840` replace with `--dangerously-bypass-approvals-and-sandbox`
- Rebuild required: `pnpm --filter @jleechanorg/ao-plugin-agent-codex build && pnpm --filter @jleechanorg/ao-cli build`

## Key Quotes
> Codex CLI introduced `--dangerously-bypass-approvals-and-sandbox` as the replacement for `--full-auto` at some point post-plugin authorship

## Connections
- [[AgentOrchestrator]] — plugin config
