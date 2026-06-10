---
title: "Agent Orchestrator Fragility Audit (2026-06-10)"
type: source
tags: [agent-orchestrator, fragility, silent-failure-pattern, watchdog, alerting, ao-doctor, skeptic-cron, lifecycle-worker]
date: 2026-06-10
source_file: agent-orchestrator-fragility-2026-06-10.md
---

## Summary

Multi-agent discovery fanout (4 parallel subagents — 3 complete, 1 pending) auditing the Agent Orchestrator (AO) system's fragility. Identified 11 distinct fragility categories, 17 unmonitored signals, 9 missing alerting channels, and a broken chain-of-trust in launchd watchdogs. Proposed 3-tier watchdog architecture (existing `ai.agento.health` + new `ai.agento.health-guardian` + extended `com.ao-runner-watchdog`) and `doctor.sh` v2 with code-path loud-WARN logs and Slack/email/desktop alerting. User intent: stop silently breaking the auto-merge/skeptic-verdict pipeline.

## Key Claims

- 8 of 11 fragility categories share the same root cause class: silent-failure paths in code guards that return early without emitting a WARN/ERROR log when critical preconditions are missing.
- The auto-merge / skeptic-verdict delivery path is the single most fragile pipeline in the system: PR event → `skeptic-gate.yml` GHA polling → lifecycle-worker (local) → `ao skeptic verify` → VERDICT comment posted → GHA gate sees VERDICT → exits PASS/FAIL. Any silent failure in this chain disables fleet-wide PR-merge automation.
- `ai.agento.health` is the sole watchdog for the AO fleet. No watchdog-of-watchdogs. If it dies, fleet-wide blindness for up to 5 minutes (StartInterval=300s). Self-rebootstrap is the only mitigation.
- The original Slack alerter (`ai.hermes-watchdog`) is broken — script `/Users/jleechan/.hermes/scripts/hermes-watchdog.sh` does not exist on disk. Last exit code 127. 158 runs completed before failure. Slack channel C09GRLXF9GR env var set but never delivered.
- 17 unmonitored signals known to operators from memory but not checked by any current script: tmux pane alive but Claude Code process dead; dist loaded in memory but new dist written to disk; orchestrator-prompt cache staleness; pnpm global store version mismatch; git ENOENT inside forked process; running.json absence after reboot; AO_BOT_GH_TOKEN validity; scmFailureCount aggregation; 24h age filter silently dropping /skeptic; paused project opt-out; backfillAllPRs default in new schemas; aging memory files claiming fixes never merged; Vitest OOM empty failed-count handling; ZFC violations in new code; compaction firing on skills/hooks injection; auto-merge race with skeptic-cron; stale background monitor delivering old FAIL after subsequent PASS.
- 9 missing alerting channels: Slack push on silent skeptic returns; desktop notification on "running but broken" workers; tmux status line for prompt/dist staleness; PR auto-comment when memory age > 30d claims a fix; bead auto-creation on fragility pattern detection (would have caught bd-rgk0 automatically); terminal bell on chronic 0% rate automation; Slack/email digest of fragile areas; per-project spawn storm alarm; health-check probe of `ao start` binary version vs worktree dist SHA.

## Key Quotes

> "The auto-merge/skeptic-verdict delivery path is the single most fragile pipeline; lifecycle-worker + skeptic-cron + ai.agento.health form a chain where any one of 3 silent-failure modes disables the entire PR-merge automation fleet-wide." — Discovery agent synthesis (history scan)

> "Suspect external sync script/session wrote yaml at 19:04 — never identified." — Config regression investigation (Jun 10)

> "8 of 11 categories share a common root cause class — guards that return early without emitting a WARN/ERROR log when a critical precondition (scm, action, dist freshness, git on PATH, schema field) is missing." — Top-level pattern finding

## Connections

- [[jleechanorg-agent-orchestrator]] — the project at `/Users/jleechan/project_agento/agent-orchestrator`
- [[WorldArchitect]] — the worldarchitect.ai project that experienced the most skeptic-cron silent failures
- [[Launchd]] — concept page; relevant for the 3-tier watchdog architecture
- [[OrchestrationSystemFragility]] — concept page; the most directly related existing concept
- [[SLOAlerting]] — concept page; relevant for the alerting design
- [[ArtifactPathFragility]] — concept page; related (deploy-related fragility)

## Fragility Categories (11 total)

1. **skeptic_cron_silent_no_verdict** (6 occurrences) — MOST RECURRING
2. **lifecycle_worker_alive_but_broken** (5 occurrences)
3. **config_regression_yaml_clobber** (3 occurrences, structural)
4. **config_missing_required_field_silent** (5 occurrences)
5. **dist_deploy_not_deployed** (4 occurrences)
6. **spawn_path_enoent_paunchy_path** (4 occurrences)
7. **auth_401_minimax_persisted** (3 occurrences)
8. **worktree_ghost_branch_drift** (3 occurrences)
9. **evidence_gate_passes_but_wrong** (2 occurrences)
10. **storm_overspawn** (1 occurrence)
11. **open_browser_unwanted** (1 occurrence, fixed in PR #669)

## Watchdog Architecture Findings

- Active: `ai.agento.health` (StartInterval=300s) — sole watchdog, no alerting, SPOF
- Broken: `ai.hermes-watchdog` (script missing, exit 127, 158 runs lost)
- Broken: `ai.openclaw.startup-check` (0-byte/corrupt plist)
- Broken: `com.jleechan.antigravity-loop` (70+ day stale sentinel)
- Slowest: `com.ao-runner-watchdog` (StartInterval=3600s = 1 hour)
- Replaced: `ai.hermes.gateway` → `ai.hermes.prod` (KeepAlive=true)

## Proposed Architecture: doctor.sh v2

1. Restore `/Users/jleechan/.hermes/scripts/hermes-watchdog.sh` (30-line shim) — re-enable Slack alerting
2. NEW `ai.agento.health-guardian` (60 min) — watchdog-of-watchdogs; checks `ai.agento.health` liveness + log freshness; auto-rebootstrap
3. EXTEND `com.ao-runner-watchdog` (1h) — also re-bootstraps the guardian
4. Add code-path loud-WARN logs at every silent-failure guard identified above
5. Add 17 new `doctor.sh` checks for the unmonitored signals
6. Add 9 new alerting channels (Slack push, desktop notif, tmux status, PR auto-comment, bead auto-creation, etc.)
7. Total worst-case blindness: 60 min (currently: indefinite)
