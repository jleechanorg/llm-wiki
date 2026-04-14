---
title: "Gateway Restart Safety"
type: concept
tags: [openclaw, gateway, launchd, single-instance, lock-storm, ws-pong, deployment]
last_updated: 2026-04-05
sources: [jleechanclaw-operational-runbook]
---

## Summary
OpenClaw gateway requires exactly one running instance. Multiple instances competing for session locks causes lock storms and WS pong starvation, making the gateway completely unresponsive despite HTTP `/health` returning 200. Any restart (deploy, manual, launchd bounce) must be preceded by orphan process cleanup.

## Single-Instance Enforcement

After ANY gateway restart, verify:
```bash
pgrep -x openclaw-gateway | wc -l   # must be 1
```

If count > 1: fix with:
```bash
pkill -x openclaw-gateway           # kill all
launchctl start gui/$(id -u)/com.openclaw.gateway
sleep 20 && pgrep -x openclaw-gateway | wc -l   # verify == 1
```

`deploy.sh` now enforces this automatically (Stage 4 orphan kill + single-instance assertion). `staging-canary.sh` check 9 also validates it.

## Root Cause: Lock Storm

When multiple `openclaw-gateway` processes run:
1. They compete for `sessions.json.lock`
2. Lock contention causes event-loop blocking
3. WS pong budget (5000ms) gets exhausted
4. Gateway becomes HTTP-unresponsive but `/health` still returns 200 (health check doesn't test lock acquisition)

**Root cause incident 2026-04-05**: deploy.sh Stage 4 used `launchctl stop` + `launchctl start` without killing orphaned processes first. Three instances spawned.

## Gateway Upgrade Protocol

1. Run pre-flight: `bash ~/.openclaw/scripts/gateway-preflight.sh --fix`
2. Backup: `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.pre-upgrade-$(date +%s)`
3. Verify `meta.lastTouchedVersion` in `~/.openclaw-consensus/openclaw.json` matches running binary version (mismatch causes `RangeError: Maximum call stack size exceeded` from AJV recursion — incident 2026-03-30)
4. Perform upgrade
5. Restart and verify single-instance again

## Staging Bootstrap Broken State

If `launchctl bootstrap` fails with "Bootstrap failed: 5: Input/output error":
1. `launchctl unload -w ~/Library/LaunchAgents/ai.openclaw.staging.plist`
2. Verify disabled: `launchctl print-disabled gui/$UID | grep staging`
3. Re-bootstrap: `launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.staging.plist`
4. Start: `launchctl start gui/$UID/ai.openclaw.staging`

If still fails, run `bash ~/.openclaw/scripts/install-launchagents.sh` to regenerate the plist.

## Related Concepts
- [[WSChurnRootCause]]
- [[ConfigFirstPrinciple]]
- [[ProactiveSessionRecovery]]