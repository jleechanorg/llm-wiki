# Hermes Launchd Meta-Pattern: Hostile Daemon Environment

**Source**: `~/.claude/projects/-Users-jleechan--hermes/memory/feedback_2026-05-14_hermes_launchd_meta_pattern.md`
**Bead**: orch-5pf0
**Date**: 2026-05-14

## Summary

Every recurring Hermes gateway outage from 2026-04 through 2026-05-14 traces back to a single architectural mismatch: Hermes was built with shell-session assumptions, but runs under launchd which violates every one of them.

## The 5 Assumption Mismatches

| Shell assumption | Launchd reality | Failure mode | Incidents |
|---|---|---|---|
| `.bashrc` sourced → env vars available | No shell profile → env vars undefined | 401/403 on LLM calls, missing API keys | 2026-04-30, 2026-05-11 |
| `.env` files augment config | `.env` overrides launchd wrapper tokens | `invalid_auth` from unexpanded `$VAR` | 2026-05-11 |
| Clean process lifecycle (start/stop) | KeepAlive + `--replace` = drain deadlock | Gateway alive but refuses messages | 2026-05-13 |
| No state residue between restarts | Zombie `state.db` sessions survive restart | Gateway blocks on "active agents" that are dead | 2026-05-13 |
| Single plist per service | Migration leaves orphan plists | Port 8642 contention, silent crash | 2026-05-12 |

## Cross-cutting Pattern: Liveness ≠ Functionality

`curl :8642/health` returning `{"ok":true}` does NOT prove the gateway is working. Five outages had healthy endpoints but broken message processing:

1. `--replace` deadlock: health ok, zero messages processed
2. Zombie sessions: health ok, gateway blocked
3. `.env` token override: health ok, `invalid_auth` on Slack API
4. Provider dual registry: health ok, 401 on compression calls
5. RAM exhaustion: health ok, Slack WS ping timeouts

## Required Guards

| Guard | Status | What it catches |
|---|---|---|
| `doctor.sh` zombie session check | Missing | `state.db` ended_at=NULL accumulation |
| `doctor.sh` plist uniqueness check | Partial (deploy.sh Stage 0 only) | Orphan plists competing for port |
| `doctor.sh` .env file detection | Present (TestNoEnvFiles) | `.env` file override of wrapper tokens |
| `doctor.sh` provider dual-registry | Missing | `providers` + `custom_providers` overlap → 401 |
| Monitor: actual message processing | Missing | Health ok but zero throughput |
| Monitor: PID matches launchd label | Present (CLAUDE.md protocol) | Wrong process on port |

## Application Rules

- Never trust health endpoint alone — verify PID match AND recent message processing
- After any non-graceful restart, always close zombie sessions in state.db
- Never add `.env` files to HERMES_HOME directories
- Never use `--replace` in plists with KeepAlive
- Verify plist uniqueness before every deploy
- Consolidate providers to single registry (`providers` only, no `custom_providers` overlap)

## Related

- [[hermes-gateway-troubleshooting-pattern]]
- [[hermes-replace-flag]]
- [[env-override-root-cause]]
- [[plist-uniqueness]]
- [[provider-dual-registry]]
- [[launchd-env-isolation]]
