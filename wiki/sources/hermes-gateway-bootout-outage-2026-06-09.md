# Hermes Gateway: bootout Outage Root Cause (2026-06-09)

**Source**: `~/.claude/projects/-Users-jleechan--hermes/memory/feedback_2026-06-09_gateway_bootout_outage.md`
**Date**: 2026-06-09
**Type**: feedback (Critical)
**Bead**: jleechan-26bt (closed)

## Summary

`hermes gateway stop` calls `launchctl bootout` which permanently removes the service from
the macOS launchd bootstrap domain. `KeepAlive` cannot restart a service that has been
evicted from the domain. This was the root cause of the 2026-06-09 `ai.hermes.prod` outage.

## Key Rule

**NEVER call `hermes gateway stop` without immediately calling `hermes gateway start`.**

For normal restarts: `hermes gateway restart` (uses `kickstart -k`, KeepAlive preserved).

## Restart Decision Tree

| Situation | Command |
|-----------|---------|
| Normal restart (plist unchanged) | `hermes gateway restart` |
| Plist file changed | `bootout` + `bootstrap` |
| Gateway evicted from domain | `launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.hermes.prod.plist && launchctl kickstart gui/$UID/ai.hermes.prod` |

## Related Changes

- `ai.hermes.prod.plist`: ThrottleInterval 30→10, KeepAlive SuccessfulExit:false
- `~/.hermes/scripts/hermes-safe-restart.sh`: new safe restart script
- qdrant moved to Docker `--restart=always`
- ollama kept native (Metal GPU, no Docker passthrough on Apple Silicon)

**References**: PR [#473](https://github.com/jleechanorg/jleechanclaw/pull/473), commit `473b7b76eb`
