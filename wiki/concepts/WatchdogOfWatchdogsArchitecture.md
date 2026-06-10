---
title: "Watchdog-of-Watchdogs Architecture"
type: concept
tags: [watchdog, launchd, alerting, reliability, agent-orchestrator, ai-agento-health]
date: 2026-06-10
---

## Definition

A **watchdog-of-watchdogs** (or **meta-watchdog**) is a supervisory process that monitors the health of other watchdogs in a system, rather than (or in addition to) monitoring the primary workload. It is the second tier in a multi-tier watchdog chain designed to bound the maximum blindness window of any single point of failure in the monitoring layer itself.

## The Problem It Solves

A single watchdog (e.g., `ai.agento.health` running every 5 minutes) has a critical gap: if the watchdog itself fails or gets deregistered, the entire fleet becomes invisible. Self-rebootstrap is one mitigation, but it requires the watchdog to be alive to detect its own absence — a chicken-and-egg problem.

## Three-Tier Watchdog Chain (Proposed for Agent Orchestrator)

```
Tier 1: ai.agento.health         (5 min)  — Watches workers; primary remediation
Tier 2: ai.agento.health-guardian (60 min) — Watches Tier 1; auto-rebootstrap if missing
Tier 3: com.ao-runner-watchdog    (1 hour) — Watches Tier 2; broader rebootstrap capability
```

**Detection-to-recovery SLA:** worst-case 60 minutes (Tier 3 cadence). Currently: indefinite if Tier 1 dies without self-rebootstrap.

## Design Principles

1. **Each tier must be SIMPLER than the tier below** — Tier 2 has fewer checks than Tier 1; Tier 3 has fewer than Tier 2
2. **No tier self-heals from a tier above its own check** — Tier 1 cannot fix Tier 2; Tier 2 cannot fix Tier 3
3. **Alert on tier missing, not just on tier failing** — bootstrap-tier logs "Tier X plist not loaded" + Slack-alert
4. **Frozenscript of bootstrap plist in repo** — Tier 2/3 can re-bootstrap Tier 1 from `scripts/frozen/ai.agento.health.plist`
5. **Cross-tier alerting channel** — all tiers post to the same Slack channel with severity emoji

## Implementation Pattern (Bash + launchd)

```bash
#!/bin/bash
# ai.agento.health-guardian — Tier 2 watchdog
# Cadence: 60 min via launchd StartInterval=3600
set -euo pipefail

LABEL="ai.agento.health"
LOG_PATH="$HOME/.openclaw/logs/ao-health.log"
FROZEN_PLIST="$REPO_ROOT/launchd/frozen/ai.agento.health.plist"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"

# Check 1: is Tier 1 plist loaded?
if ! launchctl print "gui/$(id -u)/$LABEL" 2>/dev/null | grep -q "state = running"; then
  echo "WARN: $LABEL plist not loaded — bootstrapping from frozen copy"
  cp "$FROZEN_PLIST" "$LAUNCH_AGENT_DIR/$LABEL.plist"
  launchctl bootstrap "gui/$(id -u)" "$LAUNCH_AGENT_DIR/$LABEL.plist"
  post_slack_alert ":rotating_light: $LABEL was missing, auto-bootstrapped"
fi

# Check 2: is Tier 1 log fresh (< 10 min old)?
if [ -f "$LOG_PATH" ]; then
  age_seconds=$(( $(date +%s) - $(stat -f %m "$LOG_PATH") ))
  if [ "$age_seconds" -gt 600 ]; then
    echo "WARN: $LABEL log stale ($age_seconds s) — kickstart to force re-run"
    launchctl kickstart -kp "gui/$(id -u)/$LABEL"
    post_slack_alert ":warning: $LABEL log stale, kickstart triggered"
  fi
else
  echo "WARN: $LABEL log missing — kickstart"
  launchctl kickstart -kp "gui/$(id -u)/$LABEL" || true
  post_slack_alert ":warning: $LABEL log missing, kickstart triggered"
fi
```

## Why launchd (not systemd, not cron)

- **launchd is the OS scheduler on macOS** — runs even when no user is logged in
- **StartInterval guarantees cadence** — not subject to drift like cron
- **ThrottleInterval prevents crash loops** — useful when the script has bugs
- **StandardOutPath captures logs** — no need for separate log rotation
- **Plist is plutil-linted at install** — syntactically validated before launchd loads

## Related Concepts

- [[Launchd]] (the underlying mechanism)
- [[AgentOrchestratorDoctorShV2]] (the doctor.sh design that complements this)
- [[SilentFailurePathPattern]]
- [[SLOAlerting]] (SLA/SLO-driven alerting pattern)
- [[lifecycle-worker]] (the workload being watched)

## Failure Mode: Watchdog-of-Watchdogs Itself Dies

If Tier 2 (health-guardian) dies, the chain relies on Tier 3 (1-hour cadence) to detect and rebootstrap Tier 2. This is the trade-off: each tier reduces SPOF risk but increases the maximum blindness window.

For **critical systems**, an external pager (PagerDuty, Opsgenie, etc.) is the only way to escape this hierarchy — but the user-scope setup does not need that for development work.

## Memory

- Source: `~/llm_wiki/raw/agent-orchestrator-fragility-2026-06-10.md`
- Source page: `~/llm_wiki/wiki/sources/agent-orchestrator-fragility-2026-06-10.md`
- Related memory: `project_2026-06-09_lifecycle_workers_running_broken.md`
