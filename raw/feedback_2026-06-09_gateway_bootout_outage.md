---
name: hermes-gateway-bootout-outage-root-cause
description: hermes gateway stop calls bootout which permanently evicts the service from launchd — KeepAlive cannot restart after bootout; correct restart is kickstart -k via hermes gateway restart
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-26bt
  originSessionId: 0045c60d-afe5-4e07-84a6-54dde9b7d8b0
---

# Hermes Gateway: bootout = Permanent Eviction (2026-06-09 Outage Root Cause)

## Context

On 2026-06-09, the `ai.hermes.prod` gateway was found dead. Gateway had not been running
for an unknown duration despite `KeepAlive = true` in the plist.

## Root Cause (CRITICAL)

`hermes gateway stop` internally calls `launchctl bootout gui/$UID/ai.hermes.prod`.

**bootout removes the service PERMANENTLY from the bootstrap domain.** KeepAlive
only restarts processes that crash while STILL REGISTERED in the domain. A bootout
removes the registration entirely — KeepAlive has nothing left to watch.

The 2026-06-09 outage: something called `hermes gateway stop` (bootout) but the
follow-up `hermes gateway start` (bootstrap + kickstart) never ran. Gateway was
permanently evicted.

Source confirmed in gateway.py:
- `launchd_stop()` line ~2935: deliberately calls bootout — comment: "bootout unloads
  the service definition so KeepAlive doesn't respawn"
- `launchd_restart()` line ~2990: uses `kickstart -k`, falls back to
  bootstrap+kickstart only if job is already unloaded (correct)

## Rule

**NEVER call `hermes gateway stop` without immediately calling `hermes gateway start`.**

If you just need to restart (config unchanged): use `hermes gateway restart` instead.
This calls `kickstart -k` which kills+restarts while preserving bootstrap domain
registration. KeepAlive remains active.

## Recovery Procedure

When gateway is not in `launchctl list`:
```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.prod.plist
launchctl kickstart gui/$(id -u)/ai.hermes.prod
sleep 3
curl -s http://127.0.0.1:8642/health
```

Or use the safe restart script:
```bash
bash ~/.hermes/scripts/hermes-safe-restart.sh
```

## Correct Restart Decision Tree

| Situation | Command |
|-----------|---------|
| Normal restart (plist unchanged) | `hermes gateway restart` (kickstart -k) |
| Plist file changed | `launchctl bootout gui/$UID/ai.hermes.prod && launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.hermes.prod.plist` |
| Gateway evicted from domain | Recovery procedure above |
| NEVER use | `hermes gateway stop` without follow-up start |

## Related Changes (2026-06-09 session)

- `ai.hermes.prod.plist`: ThrottleInterval changed 30→10 (faster recovery), KeepAlive set to `SuccessfulExit: false`
- `~/.hermes/scripts/hermes-safe-restart.sh`: new script, handles both kickstart and re-bootstrap fallback
- `~/.hermes/CLAUDE.md`: gateway section updated — points to port 8642 (was 8643), added WARNING about stop without start
- qdrant moved to Docker `--restart=always` (more reliable crash recovery than launchd KeepAlive for non-gateway services)
- ollama kept native (macOS Apple Silicon has no Metal GPU passthrough in Docker)

## Why: bootout vs kickstart

**Why bootout:** Used only when plist changes (updates the service definition). Removes
and re-registers. Side effect: removes from domain = KeepAlive can't restart.

**Why kickstart -k:** Kills and restarts while staying registered. KeepAlive active.
This is what `hermes gateway restart` calls internally. Correct for normal restarts.

**Jetsam note:** macOS OOM governor (Jetsam) sends SIGTERM to background processes under
memory pressure. This looks like a crash — KeepAlive WILL restart after Jetsam kill because
the process crashes while still registered. KeepAlive only fails to restart after bootout.

## References

- Session: 2026-06-09, branch `dev1781128746`
- PR: [#473](https://github.com/jleechanorg/jleechanclaw/pull/473) (fix(gateway): enforce kickstart-k restart pattern), committed `473b7b76eb`
- File: `/Users/jleechan/projects_other/hermes-agent/hermes_cli/gateway.py` lines ~2935, ~2990
- Script: `~/.hermes/scripts/hermes-safe-restart.sh`

**Why:** [[feedback_2026-05-14_hermes_launchd_meta_pattern]] covers launchd env isolation;
this entry covers the specific stop-without-start bootout trap and the kickstart-k rule.
