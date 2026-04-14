---
title: "WS Churn Root Cause"
type: concept
tags: [websocket, ws-churn, ws-pong, event-loop, starvation, maxConcurrent, timeoutSeconds]
last_updated: 2026-04-05
sources: [jleechanclaw-operational-runbook]
---

## Summary
`SlackWebSocket:N > 5` in gateway logs or canary failures (rc=4) despite HTTP 200 indicate event-loop saturation from LLM calls blocking the Node.js gateway thread. The fix is to reduce `maxConcurrent` and `timeoutSeconds` in openclaw.json — restarting alone only clears the counter.

## Root Cause Mechanism

The openclaw-gateway is a Node.js process. When LLM calls take too long or too many run concurrently, they block the Node.js event loop. WebSocket ping/pong heartbeats cannot be processed while the event loop is blocked.

**The formula**: Risk ∝ `timeoutSeconds × maxConcurrent`
- Incident case: `timeoutSeconds=900 × maxConcurrent=20 = 18000`
- Pong starvation threshold (empirically): ~3000-5000
- With `maxConcurrent=3`: `3000/3 = 1000`, use 600 for conservative margin

## The WS Pong Budget

The WebSocket ping/pong mechanism has a budget of 5000ms. If the gateway cannot respond to pings within 5 seconds, the WS connection is considered unhealthy. Event-loop saturation prevents ping responses.

## Symptoms

- `SlackWebSocket:N > 5` in gateway logs (N is the count of missed pongs)
- Canary fails with rc=4 despite HTTP `/health` returning 200
- Gateway appears healthy (HTTP responds) but Slack WS connections degrade

## The Fix (Not Just Restart)

`launchctl restart` clears the counter but sessions re-block immediately. The correct fix:

1. Reduce `timeoutSeconds` to ≤ 600 in openclaw.json
2. Reduce `maxConcurrent` to ≤ 3 in openclaw.json
3. Reduce `subagents.maxConcurrent` to ≤ 3 (same event-loop discipline)
4. THEN restart

## Safe Bounds

| Setting | Safe value | Why |
|---------|-----------|-----|
| `agents.defaults.timeoutSeconds` | ≤ 600 | WS pong budget; higher = event-loop starvation |
| `agents.defaults.maxConcurrent` | ≤ 3 | WS pong budget (safe_timeout = floor(3000/n × 0.65)) |
| `agents.defaults.subagents.maxConcurrent` | ≤ 3 | Same event-loop discipline |

## Why Subagents Have the Same Limit

Even when `maxConcurrent=3` for the main gateway, subagents launched within sessions can have their own concurrency. If a subagent launches with `maxConcurrent=8`, it can saturate the gateway event loop from within — the gateway's own concurrency limit doesn't protect it from its own subprocesses' behavior.

## Related Concepts
- [[GatewayRestartSafety]]
- [[ConfigFirstPrinciple]]