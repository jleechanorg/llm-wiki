---
title: "ai.agento.health-guardian"
type: entity
tags: [watchdog, launchd, agent-orchestrator, ai-agento-health, tier-2-watchdog, proposed]
date: 2026-06-10
---

## Definition

**`ai.agento.health-guardian`** is a proposed Tier 2 watchdog (launchd plist + shell script) that supervises the existing `ai.agento.health` watchdog. It is the middle tier of a 3-tier watchdog-of-watchdogs chain designed to bound the maximum blindness window for the Agent Orchestrator fleet to 60 minutes.

## Status

**PROPOSED (2026-06-10)** — design complete, not yet implemented. Implementation ETA: 1-2 days.

## Architecture

```
Tier 3: com.ao-runner-watchdog (1h)  [EXISTING, will be extended]
   ↓ bootstraps if missing
Tier 2: ai.agento.health-guardian (60 min)  [PROPOSED — this entity]
   ↓ bootstraps if missing
Tier 1: ai.agento.health (5 min)  [EXISTING]
   ↓ monitors lifecycle workers
Workload: 10+ lifecycle-worker processes per project
```

## Responsibilities

1. **Plist liveness check** — `launchctl print gui/$(id -u)/ai.agento.health | grep "state = running"` every 60 minutes
2. **Log freshness check** — `stat -f %m` on `~/.openclaw/logs/ao-health.log`; stale > 10 min = kickstart
3. **Auto-rebootstrap** — if plist missing or deregistered, copy from `scripts/frozen/ai.agento.health.plist` and `launchctl bootstrap`
4. **Slack alerting** — post to channel C09GRLXF9GR via direct curl (bypassing broken `ai.hermes-watchdog` script) with severity emoji
5. **Self-rebootstrap** — re-bootstrap own plist if deregistered (mirrors Tier 1's self-heal)

## Implementation Sketch

```bash
#!/bin/bash
# scripts/ao-health-guardian.sh — Tier 2 watchdog
# Cadence: 60 min via launchd StartInterval=3600
set -euo pipefail

LABEL="ai.agento.health"
LOG_PATH="$HOME/.openclaw/logs/ao-health.log"
FROZEN_PLIST="$HOME/project_agento/agent-orchestrator/launchd/frozen/ai.agento.health.plist"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"

post_slack() {
  local emoji="$1" msg="$2"
  curl -sS -X POST -H "Content-Type: application/json" \
    -d "{\"text\": \"$emoji $LABEL-guardian: $msg\"}" \
    "$SLACK_WEBHOOK_URL" || true
}

# Check 1: is Tier 1 plist loaded?
if ! launchctl print "gui/$(id -u)/$LABEL" 2>/dev/null | grep -q "state = running"; then
  echo "WARN: $LABEL plist not loaded — bootstrapping from frozen copy"
  cp "$FROZEN_PLIST" "$LAUNCH_AGENT_DIR/$LABEL.plist"
  launchctl bootstrap "gui/$(id -u)" "$LAUNCH_AGENT_DIR/$LABEL.plist"
  post_slack ":rotating_light:" "plist missing, auto-bootstrapped from frozen copy"
fi

# Check 2: is Tier 1 log fresh (< 10 min old)?
if [ -f "$LOG_PATH" ]; then
  age_seconds=$(( $(date +%s) - $(stat -f %m "$LOG_PATH") ))
  if [ "$age_seconds" -gt 600 ]; then
    echo "WARN: $LABEL log stale ($age_seconds s) — kickstart"
    launchctl kickstart -kp "gui/$(id -u)/$LABEL" || true
    post_slack ":warning:" "log stale (${age_seconds}s), kickstart triggered"
  fi
fi
```

## Why This Matters

The 2026-06-10 fragility audit identified that `ai.agento.health` is the SOLE watchdog for the AO fleet. If it dies, fleet-wide blindness persists for up to 5 minutes per StartInterval cycle, with no automatic recovery. The proposed Tier 2 guardian reduces the maximum blindness window to 60 minutes AND ensures the Tier 1 watchdog is re-bootstrapped if deregistered.

## Related

- [SkepticVerificationPipeline](SkepticVerificationPipeline.md) — the workload being protected
- [[ai-agento-health]] — the Tier 1 watchdog
- [[com-ao-runner-watchdog]] — the Tier 3 watchdog
- [WatchdogOfWatchdogsArchitecture](../concepts/WatchdogOfWatchdogsArchitecture.md) — concept page
- [AgentOrchestratorDoctorShV2](../concepts/AgentOrchestratorDoctorShV2.md) — the broader design
- [Launchd](../concepts/Launchd.md) — the underlying mechanism
