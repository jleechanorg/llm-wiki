---
title: "Single-Instance Discipline (mandatory pgrep == 1)"
type: concept
tags: [hermes, gateway, launchd, discipline, mandatory]
last_updated: 2026-06-19
---

# Single-Instance Discipline

**Mandatory rule**: `pgrep -f "hermes gateway" | wc -l` MUST equal `1` BEFORE declaring a Hermes gateway operational.

## Why it's mandatory

- `>1` = multiple instances competing for session locks → lock storm → WS pong starvation → total HTTP unresponsiveness despite `curl /health` returning 200
- Root cause of the **2026-04-05 outage**: `deploy.sh` Stage 4 used `launchctl stop` + `launchctl start` without killing orphaned processes first; 3 instances spawned, competed for `sessions.json.lock`, and the gateway became completely unresponsive

## Enforcement points

- `deploy.sh` Stage 4 — orphan kill + single-instance assertion (added after 2026-04-05 incident)
- `staging-canary.sh` check 9 — validates single-instance
- `~/.hermes/scripts/gateway-preflight.sh --fix` — auto-repair
- `HermesLivenessProtocol` check #2 — must equal 1 in every liveness sweep

## Recovery procedure when violated

```bash
# 1. Kill all instances
pkill -f "hermes gateway"

# 2. Clear stale locks (handles plain-PID and JSON {"pid":N} formats)
find ~/.hermes/agents/main/sessions/ -name "*.lock" | while read f; do
  raw=$(cat "$f" 2>/dev/null)
  pid=$(echo "$raw" | python3 -c "import sys,json; print(json.load(sys.stdin)['pid'])" 2>/dev/null || echo "$raw" | tr -d '[:space:]')
  [[ "$pid" =~ ^[0-9]+$ ]] && ! kill -0 "$pid" 2>/dev/null && rm -f "$f" && echo "removed: $f"
done

# 3. Restart cleanly
launchctl start gui/$(id -u)/ai.hermes.prod

# 4. Verify single-instance
sleep 20 && pgrep -f "hermes gateway" | wc -l   # must be 1
```

## Relationship to other concepts

- **Restart Is NOT the Fix**: WS Churn Root Cause per CLAUDE.md — when `SlackWebSocket:N > 5` appears, restart alone only clears the counter; sessions re-block immediately. The fix is reducing `timeoutSeconds × maxConcurrent` (not adding more instances).
- **Liveness ≠ Functionality**: HTTP 200 doesn't prove the gateway is functional; pgrep == 1 is a separate, mandatory check.

## Sources

- CLAUDE.md "Gateway restart — single-instance mandatory" section
- [feedback-2026-06-19-hermes-liveness-and-merge-readiness](../sources/feedback-2026-06-19-hermes-liveness-and-merge-readiness.md) — verified PID 28443 stable 4h+ across two liveness checks (single instance confirmed)
- 2026-04-05 outage postmortem (incident reference)

## Connections

- [[HermesGateway]] — the operational surface this rule protects
- [HermesLivenessProtocol](HermesLivenessProtocol.md) — check #2 in the 6-check protocol
- [[LivenessVsFunctionality]] — related concept (HTTP 200 != functional)
- [WSChurnRootCause](WSChurnRootCause.md) — restart alone doesn't fix; reducing concurrency does