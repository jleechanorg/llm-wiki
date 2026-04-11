---
title: "Agent Orchestrator Fork (jleechanorg)"
type: entity
tags: [agent-orchestrator, fork, autonomous, zero-touch, skeptic, beads, zfc]
sources: [agent-orchestrator-fork-summary.md]
last_updated: 2026-04-11
---

## Summary

`jleechanorg/agent-orchestrator` is a fork of ComposioHQ/agent-orchestrator that transforms the upstream CI tool into an **autonomous, zero-touch PR merging pipeline**. The fork's goal: AO workers drive PRs from open to merged with zero operator intervention. The upstream is a general-purpose orchestration tool; the fork adds skeptic verification, evidence gates, evolve-loop, and beads issue tracking on top.

## Fork vs Upstream

| Feature | ComposioHQ (upstream) | jleechanorg (fork) |
|---|---|---|
| Auto-merge | None | AO orchestrator + evolve loop |
| Skeptic agent | None | 7th merge gate (LLM verifier) |
| Evidence gate | None | CI validates PR evidence bundle |
| CodeRabbit reviews | None | Per-PR reviews |
| Cursor Bugbot | Skipped | Runs on every PR |
| REST fallback | None | GH rate limit → REST fallback |
| OpenClaw notifier | None | Wired for Slack notifications |
| Self-hosted runners | No | Yes |
| CI workflows | 5 | 6 (+ skeptic-cron.yml) |

## Skeptic Architecture

The Skeptic gate runs via AO worker with local API keys — never in GHA. Adding API keys to CI is explicitly forbidden.

**Chain:** PR event → `skeptic-gate.yml` starts polling → lifecycle-worker detects PR → runs `ao skeptic verify` locally → posts VERDICT comment → `skeptic-gate.yml` sees VERDICT → exits PASS/FAIL.

| Component | Role | Runs where |
|---|---|---|
| `skeptic-gate.yml` | GHA check that polls for VERDICT comment | GHA (no API keys) |
| `skeptic-cron.yml` | Cron that evaluates open PRs | GHA — calls `ao skeptic verify` |
| `ao skeptic verify` | CLI that runs LLM evaluation | Local machine (has API keys) |
| lifecycle-worker | Detects trigger comments, dispatches verify | Local machine (launchd plist) |

See [[SkepticGate]] for full detail.

## 7-Green Merge Gates

All seven must hold: CI green; mergeable; CodeRabbit APPROVED; Bugbot clean; inline threads resolved; evidence when required; Skeptic PASS (not SKIPPED). Check merge status first with `gh api`.

## Zero-Framework Cognition (ZFC)

No keyword routing, heuristic scoring, or semantic classification in application code. All such judgment must be delegated to model API calls.

Forbidden AO-specific patterns:
- `if task.includes("fix")` to detect bug-fix tasks
- `detectActivity()` using handcrafted regex routing
- Hardcoded lists of "coding task keywords" in routing logic
- Config classifiers using keyword heuristics instead of model calls

## llm-eval.ts Shared Utility

All LLM evaluation (skeptic, verifier, exit-criteria checks) must route through `packages/cli/src/lib/llm-eval.ts`. Never hard-code binary paths (`codex`, `claude`) or raw `execSync` calls in command handlers.

Re-use chain:
- `llmEval(prompt, {model?})` — full fallback chain (Codex primary → Claude fallback)
- `tryCodexPrint(prompt)` — codex `exec -` only
- `tryClaudePrint(prompt)` — claude `--dangerously-skip-permissions --print` only
- `resolveCodexBinary()` — imported from `@jleechanorg/ao-plugin-agent-codex`

## Evolve Loop

A continuous loop that drives open PRs toward merge. Phases include: CI triage, review-comment response, skeptic-gate polling, and healthy-cycle fast path. The loop is triggered via `ao evolve` or the builtin `evolveLoop` config key. See `roadmap/evolve-loop-findings.md` for phase history.

## Beads Issue Tracker

Issues live in `.beads/issues.jsonl`. The `br` CLI creates, updates, and closes beads. IDs follow `bd-XXXX`. Bead timestamps must use RFC3339 with `Z` or `+00:00` (never `+00:00Z`).

Active/notable beads:
- bd-h5ye — on-demand tool profiles design
- bd-hoyn — llm-inspector on-demand mode (shipped)
- bd-cx06 — context compaction master fix (closed)
- bd-pwku — skill restoration

## llm_inspector Context Overhead Tool

A proxy tool (`llm_inspector/`) that sits between Claude Code and the Anthropic API to measure per-turn token overhead. Key findings:
- Tool definitions: ~49% of overhead
- CLAUDE.md: ~16%
- System prompt: ~15%
- MCP definitions: ~15%
- `--tool-mode lean` strips 17 heavy built-ins (~20K tokens/turn savings)
- `--tool-mode on-demand` replaces heavy schemas with stubs, buffers SSE, re-issues with full schemas on demand

## Context Compaction Work

The fork has investigated Claude Code's context compaction behavior extensively:
- `DISABLE_AUTO_COMPACT=1` + `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` disables auto-compaction
- PreCompact hook fires on v2.1.77 but only catches ~2% of compactions
- Most compactions bypass the hook
- Compaction destroys PR context; always re-verify with `gh` after compaction

## Fork Isolation Rules

- New files for new features; additive upstream edits
- Plugin-first; minimal core diff (use `*-extensions.ts`)
- Fork exports grouped in `index.ts`
- Risky files: `lifecycle-manager.ts`, `types.ts`, `config.ts`, `spawn.ts`
- Safe: `packages/plugins/**`, `roadmap/`

## Connections

- [[AgentOrchestrator]] — base system this fork extends
- [[SkepticGate]] — 7th merge gate owned by this fork
- [[WorldArchitectAI]] — primary target repository for dogfooding
- [[BeadsTracker]] — `.beads/issues.jsonl` issue system
