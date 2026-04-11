---
title: "Agent Orchestrator Fork — Summary"
type: source
tags: [agent-orchestrator, fork, jleechanorg, autonomous, zero-touch, skeptic, zfc, beads, evolve-loop, llm-inspector]
date_added: 2026-04-11
---

## Overview

`jleechanorg/agent-orchestrator` is a fork of `ComposioHQ/agent-orchestrator`. The upstream is a general-purpose tool for spawning AI coding agents in parallel git worktrees. The fork builds an **autonomous, zero-touch PR merging pipeline** on top of it — AO workers drive PRs from open to merged with zero operator intervention.

## Repository Facts

- Fork of: `ComposioHQ/agent-orchestrator`
- Fork repo: `jleechanorg/agent-orchestrator`
- Working directory: `/Users/jleechan/project_agento/`
- Package name: `@composio/ao`
- Install: `npm install -g @composio/ao`
- Language: TypeScript (strict), pnpm monorepo
- Key dirs: `packages/core/src/`, `packages/plugins/`, `roadmap/`, `.beads/`

## What the Fork Adds

| Feature | Upstream | Fork |
|---|---|---|
| Auto-merge | None | AO orchestrator + evolve loop |
| Skeptic gate | None | 7th merge gate (LLM verifier) |
| Evidence gate | None | CI validates PR evidence bundle + claim class |
| CodeRabbit reviews | None | Per-PR on every PR |
| Cursor Bugbot | Skipped | Runs on every PR |
| REST rate-limit fallback | None | GH rate limit → REST fallback |
| OpenClaw notifier | None | Wired for Slack notifications |
| Self-hosted runners | No | Yes |
| CI workflows | 5 | 6 (+ `skeptic-cron.yml`) |

## Core Design Principles

### AO Workers as Default Execution Model

When given a task, default to dispatching an AO worker (`ao spawn`) rather than running `claude -p` directly. Workers can:
- Claim a PR: `ao spawn --project agent-orchestrator --claim-pr <N>`
- Claim a bead: `ao spawn --bead <id>`
- Run arbitrary tasks: `ao spawn "fix the rate limit handler"`
- Run background/monitoring loops: `ao spawn --no-worktree "run the evolve loop"`

### Zero-Framework Cognition (ZFC)

No keyword routing, heuristic scoring, or semantic classification in application code. All such judgment must be delegated to model API calls. Forbidden patterns include `if task.includes("fix")`, regex-based intent routing, hardcoded keyword lists, and hand-tuned scoring functions. Correct pattern: pass text to the model with a clear prompt and act on the model's response.

### Development Hierarchy

1. Config (`agent-orchestrator.yaml`) — reactions, agentRules, routing
2. New plugin in an existing slot
3. New plugin type (new slot in plugin-registry)
4. Core code change — only when 1–3 are insufficient

### Plugin Architecture

Agent plugins: cursor, codex, gemini, aider, opencode.
Runtime plugins: tmux, process.
SCM plugins: github (with REST fallback), gitlab.
Tracker plugins: linear, beads.
Notifier plugins: openclaw (Slack).

## Skeptic Gate

The 7th merge gate. An LLM-based PR verifier that runs via AO worker with local API keys — never in GHA.

**Chain:** PR event → `skeptic-gate.yml` starts polling → lifecycle-worker detects PR → `ao skeptic verify` runs LLM locally → posts `VERDICT:PASS/FAIL` comment → `skeptic-gate.yml` exits.

All LLM evaluation routes through `packages/cli/src/lib/llm-eval.ts` (Codex primary → Claude fallback). `ao skeptic verify` runs from `/tmp` to avoid project `CLAUDE.md` hooks skewing evaluation.

Known bug fixed: Codex echoed prompt template containing `VERDICT:PASS` as an example, causing false-PASS matches. Fixed by tightening VERDICT parsing.

## 7-Green Merge Gates

All seven must hold: CI green; mergeable; CodeRabbit APPROVED; Bugbot clean; inline threads resolved; evidence bundle present (when required); Skeptic PASS (not SKIPPED).

## Beads Issue Tracker

Issues live in `.beads/issues.jsonl`. The `br` CLI creates, updates, and closes beads. IDs follow `bd-XXXX`. Timestamps must be RFC3339 with `Z` or `+00:00` (never `+00:00Z`).

## Evolve Loop

A continuous loop that drives open PRs toward merge. Triggered via `ao evolve` or the `projects.agent-orchestrator.evolveLoop` config key. Phases include CI triage, review-comment response, skeptic-gate polling, and healthy-cycle fast path. Phase history documented in `roadmap/evolve-loop-findings.md`.

## llm_inspector

A proxy tool (`llm_inspector/`) that measures per-turn token overhead by sitting between Claude Code and the Anthropic API. Key findings (v2.1.30–v2.1.98):
- Tool definitions: ~49% of overhead (~24K tokens/turn)
- CLAUDE.md: ~16%
- System prompt: ~15%
- MCP definitions: ~15%
- `--tool-mode lean` strips 17 heavy built-ins (~20K tokens/turn savings)
- `--tool-mode on-demand` replaces heavy schemas with stubs; buffers all SSE from byte 1; detects stubbed tool_use in `content_block_start`; re-issues with full schemas. 4 safeguards: buffer ALL SSE, per-request-id isolation, graceful fallback, accept KV-cache invalidation.

## Context Compaction Work

- `DISABLE_AUTO_COMPACT=1` + `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` disables auto-compaction
- PreCompact hook fires on v2.1.77 but only catches ~2% of compactions (1/54)
- Most compactions bypass the hook
- Compaction destroys PR context — always re-verify PR numbers with `gh` after compaction
- GrowthBook experiment `tengu_amber_redwood` caps context to 400K by default; env var overrides it

## Key Source Files

- `/Users/jleechan/project_agento/worktree_compaction/CLAUDE.md` — fork guidelines, ZFC, dev hierarchy, skeptic architecture
- `/Users/jleechan/project_agento/worktree_compaction/README.md` — fork vs upstream table, quick start
- `/Users/jleechan/project_agento/worktree_compaction/roadmap/README.md` — rolling activity log, bead index, roadmap docs
- `/Users/jleechan/project_agento/worktree_compaction/roadmap/evolve-loop-findings.md` — evolve loop phase history
- `/Users/jleechan/project_agento/worktree_compaction/roadmap/skeptic-ao-worker-architecture.md` — skeptic architecture deep dive
- `/Users/jleechan/project_agento/worktree_compaction/.beads/issues.jsonl` — canonical issue list
- `/Users/jleechan/llm_inspector/` — context overhead proxy tool
