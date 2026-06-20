---
title: "Hermes Liveness Protocol (6-check parallel battery)"
type: concept
tags: [hermes, verification, liveness, protocol]
last_updated: 2026-06-19
---

# Hermes Liveness Protocol

A 6-check parallel battery that proves a Hermes gateway is functional via **behavioral evidence**, not path-based assumptions. Runs in ~2 seconds when invoked from a single shell with parallel `Bash` tool calls.

## The 6 checks

| # | Check | Pass signal |
|---|---|---|
| 1 | `curl -fsS -m 8 http://127.0.0.1:8643/health` | `{"status":"ok","platform":"hermes-agent"}` |
| 2 | `pgrep -f "hermes gateway" \| wc -l` | exactly `1` (MANDATORY) |
| 3 | `launchctl print gui/$UID/ai.hermes.prod \| grep -E "state\|last exit\|pid"` | `state=running` + non-null PID |
| 4 | `tail -n 30 ~/.hermes_prod/logs/gateway.log` | recent inbound→response pairs with `api_calls > 0` |
| 5 | Synthetic canary ack in C0AKALZ4CKW (12-char `ack-<hex>`) | reply within <30s |
| 6 | `tail -n 30 ~/.hermes_prod/logs/gateway.err.log` | empty |

## Core principle: behavior over path

When `~/.hermes_prod/agents/main/agent/auth-profiles.json` is missing at the canonical path, the gateway is **NOT** automatically broken — auth may live in env vars or a different path in this build. Confirm via behavioral evidence (checks #4 + #5) before declaring broken.

## Mandatory sub-rule

**Single-instance is mandatory.** `pgrep -f "hermes gateway" | wc -l` MUST equal `1` BEFORE declaring operational.

- `>1` = lock storm = WS pong starvation = HTTP 200 with no real work
- Root cause of the 2026-04-05 outage (3 instances competed for `sessions.json.lock`)
- `deploy.sh` Stage 4 now enforces this automatically + `staging-canary.sh` check 9 validates it

## Stable PID is a health signal

A PID unchanged across hours = no restart storm, no memory leak forcing recycle. Example: PID 28443 stable 4+ hours on 2026-06-19 across two liveness checks.

## Sources

- [feedback-2026-06-19-hermes-liveness-and-merge-readiness](../sources/feedback-2026-06-19-hermes-liveness-and-merge-readiness.md) — primary source
- CLAUDE.md "Gateway restart — single-instance mandatory" + "Liveness ≠ Functional (CRITICAL)" caveats

## Connections

- [[HermesGateway]] — the operational surface being verified
- [SingleInstanceDiscipline](SingleInstanceDiscipline.md) — the mandatory sub-rule
- [[LivenessVsFunctionality]] — the underlying principle
- [MergeReadinessGate](MergeReadinessGate.md) — companion protocol for "should we merge" questions
- [[WorktreeIsolation]] — context: editing `~/.hermes/` directly bypasses the canary gate that should run alongside this check
- [[CanaryAck]] — check #5 specifically