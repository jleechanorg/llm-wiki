---
name: hermes-launchd-meta-pattern
description: "All recurring Hermes gateway failures share a common root: launchd is a hostile environment for daemon assumptions — env isolation, state corruption, signal handling, and resource contention all diverge from shell expectations"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 5e846711-556f-4eab-85b3-0883dbc44f75
---

# Hermes Gateway Meta-Pattern: Launchd as Hostile Daemon Environment

Every recurring Hermes gateway outage from 2026-04 through 2026-05-14 traces back to a single architectural mismatch: **Hermes was built with shell-session assumptions, but runs under launchd which violates every one of them.**

## The 5 assumption mismatches

| Shell assumption | Launchd reality | Failure mode | Incidents |
|---|---|---|---|
| `.bashrc` sourced → env vars available | No shell profile → env vars undefined | 401/403 on LLM calls, missing API keys | 2026-04-30, 2026-05-11 |
| `.env` files augment config | `.env` overrides launchd wrapper tokens | `invalid_auth` from unexpanded `$VAR` | 2026-05-11 |
| Clean process lifecycle (start/stop) | KeepAlive + `--replace` = drain deadlock | Gateway alive but refuses messages | 2026-05-13 |
| No state residue between restarts | Zombie `state.db` sessions survive restart | Gateway blocks on "active agents" that are dead | 2026-05-13 |
| Single plist per service | Migration leaves orphan plists | Port 8642 contention, silent crash | 2026-05-12 |

## Cross-cutting pattern: "Liveness ≠ Functionality"

A recurring diagnostic trap: `curl :8642/health` returning `{"ok":true}` does NOT prove the gateway is working. The health endpoint only proves something is listening on the port. Five outages had healthy endpoints but broken message processing:

1. `--replace` deadlock: health ok, zero messages processed
2. Zombie sessions: health ok, gateway blocked
3. `.env` token override: health ok, `invalid_auth` on Slack API
4. Provider dual registry: health ok, 401 on compression calls
5. RAM exhaustion: health ok, Slack WS ping timeouts

**Required verification:** Always check BOTH health endpoint AND PID-matched port binding AND actual message processing (not just liveness).

## Required guards (currently missing or partial)

| Guard | Status | What it catches |
|---|---|---|
| `doctor.sh` zombie session check | **Missing** | `state.db` ended_at=NULL accumulation |
| `doctor.sh` plist uniqueness check | **Partial** (deploy.sh Stage 0 only) | Orphan plists competing for port |
| `doctor.sh` .env file detection | **Present** (TestNoEnvFiles) | `.env` file override of wrapper tokens |
| `doctor.sh` provider dual-registry | **Missing** | `providers` + `custom_providers` overlap → 401 |
| Monitor: actual message processing | **Missing** | Health ok but zero throughput |
| Monitor: PID matches launchd label | **Present** (CLAUDE.md protocol) | Wrong process on port |

**How to apply:**
- When debugging ANY Hermes gateway issue, run the full diagnostic checklist from [[hermes-gateway-troubleshooting-pattern]] first
- Do NOT trust health endpoint alone — verify PID match AND recent message processing
- After any non-graceful restart, always close zombie sessions in state.db
- Never add `.env` files to HERMES_HOME directories
- Never use `--replace` in plists with KeepAlive
- Verify plist uniqueness before every deploy
- Consolidate providers to single registry (`providers` only, no `custom_providers` overlap)

**Why:** 8+ incidents over 6 weeks all traced to the same architectural mismatch. Individual fixes (delete .env, remove --replace, close zombie sessions) are necessary but insufficient without understanding the meta-pattern: launchd breaks shell assumptions systematically.

**Related:** [[feedback-2026-05-13-hermes-replace-flag]], [[feedback-2026-05-11-env-override-root-cause]], [[feedback-2026-05-12-plist-uniqueness]], [[feedback-2026-05-12-provider-dual-registry]], [[feedback-2026-04-30-launchd-env-isolation]], [[feedback-2026-05-13-staging-disabled]]
