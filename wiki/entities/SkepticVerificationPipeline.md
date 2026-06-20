---
title: "Skeptic Verification Pipeline"
type: entity
tags: [skeptic, pr-merge-automation, agent-orchestrator, gha, lifecycle-worker, fragility]
date: 2026-06-10
---

## Definition

The **Skeptic Verification Pipeline** is the chain of components that evaluate a pull request and post a verdict (PASS/FAIL) which the GitHub Actions `skeptic-gate.yml` polls for. The pipeline is the single most fragile path in the Agent Orchestrator system, per the 2026-06-10 fragility audit.

## Pipeline Chain (6 stages)

```
PR event → skeptic-gate.yml (GHA) → lifecycle-worker (local) → ao skeptic verify (local LLM) → VERDICT comment → skeptic-gate.yml sees VERDICT → exits PASS/FAIL → auto-merge via skeptic-cron
```

| Stage | Component | Where it runs | Failure mode |
|-------|-----------|---------------|--------------|
| 1 | `skeptic-gate.yml` (GHA) | GHA runner | polling timeout (configurable, default 50 min) |
| 2 | `lifecycle-worker` (per project) | local launchd | silent death (lifecycle-worker not running) |
| 3 | `ao skeptic verify` | local CLI (called by worker) | 401 / 429 / missing API keys |
| 4 | `VERDICT comment` posted to PR | local gh CLI | PATCH 403 for cross-user; CREATE fallback at fca0cc322 |
| 5 | `skeptic-gate.yml` polls for VERDICT | GHA runner | SHA staleness blocks match |
| 6 | `skeptic-cron` auto-merge | local | GitHub merge queue race |

## Why It's Fragile

- **No watchdog-of-watchdogs** — if lifecycle-worker dies, no one re-spawns it without `ai.agento.health` 5-min cycle
- **Silent-failure paths dominate** — 8/11 fragility categories share the silent-return pattern; 6 of those are in this pipeline
- **SHA-locked verdicts** — every push invalidates prior PASS verdicts; re-run required
- **Local LLM dependency** — API key validity (WAFER_API_KEY, ANTHROPIC_API_KEY, etc.) is fragile
- **Stale staging config** — 3rd regression in 30 days (Jun 10 incident: 0 matches for `scm:` in `~/.hermes/agent-orchestrator.yaml`)

## Key Bugs (2026-04 to 2026-06)

- **bd-rgk0** — 24h age filter BEFORE trigger check (PR #654, fixed by PR #661) — silently dropped fresh /skeptic comments
- **fca0cc322** — PATCH 403 → CREATE fallback for cross-user verdict posts
- **PR #516/#517** — Evidence Gate author check fix (was checking `app/skeptic-agent`, actual author is `jleechan2015`)
- **PR #514** — `--trigger-type` flag unsupported (cron passed flag that CLI never defined)
- **2026-06-10 incident** — staging config regression: `scm:`, `skepticModel`, `skepticPostComment` all missing → fleet-wide skeptic blackout

## Monitoring & Detection

Currently NO real-time monitoring of the pipeline. Detection is reactive (operators notice PRs aren't being merged). Proposed in `AgentOrchestratorDoctorShV2`:
- Check 9: 24h age filter presence in skeptic-cron
- Check 8: scmFailureCount fleet aggregation
- Channel 1: Slack push on silent skeptic returns
- Channel 5: bead auto-creation on fragility pattern detection (would have caught bd-rgk0)

## Related

- [jleechanorg-agent-orchestrator](jleechanorg-agent-orchestrator.md) — the project
- [ai-agento-health-guardian](ai-agento-health-guardian.md) — proposed Tier 2 watchdog
- [SilentFailurePathPattern](../concepts/SilentFailurePathPattern.md) — the cross-cutting root cause
- [WatchdogOfWatchdogsArchitecture](../concepts/WatchdogOfWatchdogsArchitecture.md) — the architecture that bounds blindness
- [AgentOrchestratorDoctorShV2](../concepts/AgentOrchestratorDoctorShV2.md) — the doctor.sh design

## Memory

- Source: `~/llm_wiki/raw/agent-orchestrator-fragility-2026-06-10.md`
- Source page: `~/llm_wiki/wiki/sources/agent-orchestrator-fragility-2026-06-10.md`
- Memory entries: `feedback_2026-05-04_worldarchitect_skeptic_missing_scm.md`, `feedback_2026-05-23_skeptic_gate_trigger_markers.md`, `feedback_2026-05-02_skeptic_trigger_type_unsupported.md`, `feedback_2026-06-05_skeptic_reaction_action_notify.md`, `feedback_2026-06-08_skeptic_post_fix_shipped.md`, `project_2026-06-10_staging_config_regression_skeptic_dead.md`
