---
title: "OpenClaw Operational Runbook"
type: source
tags: [openclaw, runbook, gateway, deployment, ws-churn, launchd, ao-backfill, slack]
date: 2026-04-05
source_file: /home/jleechan/project_jleechanclaw/jleechanclaw/docs/operational-runbook.md
---

## Summary
The OpenClaw Operational Runbook consolidates operational procedures that agents rarely need but must follow correctly. Key topics include: gateway restart safety (single-instance mandatory), WS churn root cause and correct fix, openclaw.json mutation safety (surgical updates only), gateway upgrade pre-flight, staging bootstrap repair, worktree isolation rules, and Slack threading/reply protocol.

## Key Claims

### Gateway Restart — Single-Instance Mandatory
After ANY gateway restart, verify exactly **one** `openclaw-gateway` process is running:
```bash
pgrep -x openclaw-gateway | wc -l   # must be 1
```
Multiple instances compete for session locks → lock storm → WS pong starvation → total HTTP unresponsiveness (even though `/health` returns 200).

**Root cause 2026-04-05**: deploy.sh Stage 4 used `launchctl stop` + `start` without killing orphaned processes first. Three instances spawned, competed for `sessions.json.lock`, gateway became completely unresponsive.

### WS Churn Root Cause — Restart Is NOT the Fix
`SlackWebSocket:N > 5` in logs or canary fails (rc=4) despite HTTP 200 → root cause is event-loop saturation from LLM calls blocking the Node.js thread.

- `timeoutSeconds > 600` combined with `maxConcurrent > 3` = WS pong starvation (pong budget = 5000ms)
- Subagents `maxConcurrent` must also stay ≤ 3 — values like 8 can saturate the gateway event loop
- **Correct fix**: reduce both in openclaw.json, then restart. Restart alone only clears the counter.
- Safe bounds: `timeoutSeconds ≤ 600`, `maxConcurrent ≤ 3`, `subagents.maxConcurrent ≤ 3`
- Derivation: Risk ∝ `timeoutSeconds × maxConcurrent`. Incident: 900×20=18000. Pong starvation threshold ~3000-5000. With maxConcurrent=3: `3000/3 = 1000`, use 600 for margin.

### openclaw.json Mutation Safety
**NEVER rewrite the entire file.** Always surgical: `d['some']['nested']['key'] = new_value`. Full rewrites silently drop config sections not in the Python scope (e.g. `agents.defaults.heartbeat` disappeared on 2026-03-23 when model was updated via full rewrite).

### Protected Keys (never change without explicit Jeffrey authorization)

| Key | Required value | Why |
|-----|---------------|-----|
| `agents.defaults.heartbeat.every` | `"5m"` | Doctor enforces 5m |
| `agents.defaults.heartbeat.target` | `"last"` | Doctor enforces this |
| `agents.defaults.timeoutSeconds` | `≤ 600` | WS pong budget |
| `agents.defaults.maxConcurrent` | `≤ 3` | WS pong budget |
| `agents.defaults.subagents.maxConcurrent` | `≤ 3` | Same event-loop discipline |
| `plugins.slots.memory` | `"openclaw-mem0"` | Without this, gateway silently uses builtin `memory-core`, mem0 plugin disabled |

### Gateway Upgrade Safety
MANDATORY before ANY gateway version change or `openclaw doctor --fix`:
```bash
bash ~/.openclaw/scripts/gateway-preflight.sh        # check only
bash ~/.openclaw/scripts/gateway-preflight.sh --fix   # check and auto-repair
```
Key rules:
- Never run `openclaw doctor --fix` without checking for existing plists first
- ThrottleInterval in gateway plist must be >= 10 (preferably 30)
- Backup `openclaw.json` before upgrade
- MANDATORY: verify `meta.lastTouchedVersion` matches running binary version (mismatch causes `RangeError: Maximum call stack size exceeded` crash from AJV recursion — incident 2026-03-30)

### Worktree Isolation Rule
`~/.openclaw/` is staging. `~/.openclaw_prod/` is production. Direct edits to `~/.openclaw/` bypass staging canary gate and code review.

**Permitted exceptions (three only):**
1. `openclaw.json` — surgical key updates only
2. `cron/jobs.json` — live job management
3. Emergency hot-fixes explicitly authorized by user in current session

Correct flow: edit in worktree → commit → PR → merge → `git pull` in `~/.openclaw/` → `scripts/deploy.sh`

### Config-First Principle
Before writing Python, check if openclaw config can achieve the goal. New Python in `src/orchestration/` only justified for capabilities that genuinely don't exist in the config surface.

## Related Concepts
- [[GatewayRestartSafety]]
- [[ConfigFirstPrinciple]]
- [[WSChurnRootCause]]