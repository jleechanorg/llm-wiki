---
title: "Hermes gateway bootout = permanent eviction (2026-06-09)"
type: source
tags: [feedback, hermes, gateway, launchd, bootout, kickstart, KeepAlive, outage]
date: 2026-06-09
source_file: raw/feedback_2026-06-09_gateway_bootout_outage.md
---

## Summary
On 2026-06-09 the `ai.hermes.prod` gateway was found dead despite `KeepAlive=true`. Root cause: `hermes gateway stop` internally calls `launchctl bootout` which **permanently evicts** the service from the launchd bootstrap domain. KeepAlive only restarts processes that crash while still registered; a bootout removes the registration entirely, so KeepAlive has nothing left to watch. The follow-up `hermes gateway start` never ran, leaving the gateway evicted indefinitely.

## Key Claims
- `hermes gateway stop` → `launchctl bootout gui/$UID/ai.hermes.prod` (intentional, line ~2935 of `gateway.py` — comment: "bootout unloads the service definition so KeepAlive doesn't respawn").
- `hermes gateway restart` → `launchctl kickstart -k` (line ~2990) — kills + restarts while preserving bootstrap-domain registration. KeepAlive stays active. **This is the correct restart command.**
- NEVER call `hermes gateway stop` without immediately calling `hermes gateway start`. The 2026-06-09 outage was a `stop` with no follow-up `start`.
- For plist file changes, the correct pair is `bootout` + `bootstrap` (then `kickstart`) — not `stop` + `start` because the latter relies on the same bootout trap.

## Recovery Procedure
When gateway is missing from `launchctl list`:
```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.prod.plist
launchctl kickstart gui/$(id -u)/ai.hermes.prod
sleep 3
curl -s http://127.0.0.1:8642/health
```
Or use `bash ~/.hermes/scripts/hermes-safe-restart.sh`.

## Restart Decision Tree
| Situation | Command |
|---|---|
| Normal restart (plist unchanged) | `hermes gateway restart` (kickstart -k) |
| Plist file changed | `launchctl bootout gui/$UID/ai.hermes.prod && launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.hermes.prod.plist` |
| Gateway evicted from domain | Recovery procedure above |
| NEVER use | `hermes gateway stop` without follow-up start |

## Key Quotes
> bootout removes the service PERMANENTLY from the bootstrap domain. KeepAlive only restarts processes that crash while STILL REGISTERED in the domain. A bootout removes the registration entirely — KeepAlive has nothing left to watch.

> macOS OOM governor (Jetsam) sends SIGTERM to background processes under memory pressure. This looks like a crash — KeepAlive WILL restart after Jetsam kill because the process crashes while still registered. KeepAlive only fails to restart after bootout.

## Related Changes (2026-06-09 session)
- `ai.hermes.prod.plist`: ThrottleInterval 30→10 (faster recovery), `KeepAlive.SuccessfulExit: false`
- `~/.hermes/scripts/hermes-safe-restart.sh`: new script (handles both kickstart and re-bootstrap fallback)
- `~/.hermes/CLAUDE.md`: gateway section points to port 8642 (was 8643), added WARNING about stop without start
- qdrant moved to Docker `--restart=always` (more reliable than launchd KeepAlive for non-gateway services)
- ollama kept native (macOS Apple Silicon has no Metal GPU passthrough in Docker)

## Connections
- [[Launchd]] — launchd lifecycle: bootstrap/kickstart/bootout semantics
- [[Gateway]] — the `ai.hermes.prod` gateway in particular
- [[GatewayRestartSafety]] — restart decision tree and stop-without-start trap
- [[GatewayURLResolution]] — port 8642 health endpoint
- [[hermes-launchd-meta-pattern]] — launchd env isolation; this entry covers the bootout/kickstart-k distinction
