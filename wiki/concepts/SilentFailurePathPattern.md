---
title: "Silent Failure Path Pattern"
type: concept
tags: [fragility, root-cause, agent-orchestrator, skeptic-cron, lifecycle-worker, doctor-sh-v2]
date: 2026-06-10
---

## Definition

A **silent failure path** is a code guard or condition check that returns early (often with a falsy return value, an empty array, or a "0" status) without emitting a WARN or ERROR log when a critical precondition is missing or fails. The function appears to "succeed" from the caller's perspective, but the actual work did not happen.

## Mechanism

```typescript
// ANTI-PATTERN — silent failure path
async function evaluateProject(project: Project) {
  const scm = registry.get<SCM>("scm", project.scm?.plugin);
  if (!scm?.listOpenPRs) return 0;  // ← SILENT RETURN, NO LOG
  // ...rest of evaluation
}

// DURATION FIX — loud WARN at the silent guard
async function evaluateProject(project: Project) {
  const scm = registry.get<SCM>("scm", project.scm?.plugin);
  if (!scm?.listOpenPRs) {
    console.warn(`[skeptic-cron] ${project.name}: missing scm config (project.scm=${project.scm}); skipping. Add 'scm: plugin: github' to enable.`);
    return 0;
  }
  // ...rest of evaluation
}
```

## Why It Persists

1. **Defensive programming gone wrong** — "if (!x) return" feels safe but hides config/environment problems
2. **Unit tests pass** — mocking the missing dependency returns the falsy branch, test passes
3. **No observability gap** — until users notice "skeptic didn't run for project X," no one looks
4. **Easy to write** — the alternative (loud WARN + structured logging) requires explicit design

## Occurrence in Agent Orchestrator

8 of 11 fragility categories identified in the 2026-06-10 audit share this root cause:

| Category | Silent guard | Real impact |
|----------|--------------|-------------|
| skeptic_cron_silent_no_verdict | `if (!scm?.listOpenPRs) return 0` | 16 PRs unevaluated fleet-wide |
| config_missing_required_field_silent | `if (!action) return` | Skeptic silently disabled |
| lifecycle_worker_alive_but_broken | `pgrep` returns 0 only on missing process | "Running but broken" never detected |
| skeptic age filter before trigger | `if (pr.updatedAt < cutoff) continue` | Fresh /skeptic comments silently dropped |
| running.json absence | `getRunning()` returns null | "AO is not running" error in spawn |
| orchestrator-prompt cache staleness | no comparison check | New features never reach running workers |
| dist deploy desync | process holds old dist in memory | PR merged ≠ fix deployed |
| AO_BOT_GH_TOKEN validity | token may be `__OPENCLAW_REDACTED__` | Workers auth 401 silently |

## DDetection Patterns

Static analysis (lint) can flag suspicious `if (!x) return` patterns in:
- Cron / scheduled task entry points
- Worker initialization
- SCM / GitHub / SCM plugin calls
- Process spawning (`execFile`, `spawnSync`)
- Configuration loaders

But the most durable defense is the **doctor.sh loud-WARN pattern** — add `console.warn` at the silent guard with enough context for an operator to diagnose without code archaeology.

## Related Concepts

- [OrchestrationSystemFragility](OrchestrationSystemFragility.md)
- [WatchdogOfWatchdogsArchitecture](WatchdogOfWatchdogsArchitecture.md)
- [AgentOrchestratorDoctorShV2](AgentOrchestratorDoctorShV2.md)
- [[LoudFailFastPattern]] (proposed counter-pattern)
- [[StructuredLoggingContract]]

## Memory

- Project memory: `~/.claude/projects/-Users-jleechan-project-agento-agent-orchestrator/memory/MEMORY.md` — multiple fragility entries
- Source: `~/llm_wiki/raw/agent-orchestrator-fragility-2026-06-10.md`
- Source page: `~/llm_wiki/wiki/sources/agent-orchestrator-fragility-2026-06-10.md`

## Beads

- bd-rgk0 (skeptic-cron 24h filter, fixed by PR #661)
- bd-85r, bd-9lxx, bd-7gdr (lifecycle workers running but broken)
- bd-a7mq (session-manager merged reuse)
