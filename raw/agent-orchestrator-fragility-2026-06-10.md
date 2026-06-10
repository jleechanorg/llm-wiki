# Agent Orchestrator Fragility Audit — 2026-06-10

**Source:** Multi-agent discovery fanout (4 parallel subagents, 3 complete + 1 pending)
**Date:** 2026-06-10
**Trigger:** User observation "the system seems so fragile" + need for `doctor.sh` / alerting
**Project:** `/Users/jleechan/project_agento/agent-orchestrator` (fork of ComposioHQ/agent-orchestrator, hosted at jleechanorg)

## Background

The Agent Orchestrator (AO) is a local LLM-based automation system managing 10+ project worktrees via tmux sessions, launchd plists, and lifecycle-workers. It runs PR-merge automation (skeptic gate, auto-merge), orchestrates workers (claude-code, codex, antigravity/agy, minimax, wafer), and persists state in `~/.agent-orchestrator/`. The system has been in production for ~6 months with multiple fragility incidents.

**The merge pipeline chain:** PR event → `skeptic-gate.yml` GHA polling → lifecycle-worker (local) → `ao skeptic verify` (local LLM) → VERDICT comment posted → `skeptic-gate.yml` sees VERDICT → exits PASS/FAIL → auto-merge via `skeptic-cron.yml`.

## Top 11 Fragility Categories (30-day window)

Ranked by operator pain and recurrence:

### 1. skeptic_cron_silent_no_verdict (6 occurrences, MOST RECURRING)

Silent return paths in `skeptic-cron-local.ts` when preconditions fail. Six distinct root causes:

- **Missing `scm: plugin: github`** in project config — `if (!scm?.listOpenPRs) return 0` returns silently (worldarchitect, May 4)
- **`--trigger-type` flag unsupported** — cron passed flag that CLI never defined; every cycle silently failed (May 2)
- **Worker reaction `action: notify`** instead of `skeptic-review` — silently disabled skeptic (Jun 5)
- **24h age filter BEFORE trigger check** — drops PRs by pr.updatedAt > 24h even when fresh `/skeptic` exists; PR 654 bug, fixed by PR 661 (Jun 9)
- **PATCH 403 silent failure** for cross-user verdict posts (Jun 8, fixed in fca0cc322)
- **Stale staging config** (Jun 10) — `~/.hermes/agent-orchestrator.yaml` overwritten with stale snapshot at 19:04 PT Jun 9; `scm:`, `skepticModel`, `skepticPostComment` all missing; fleet-wide skeptic blackout

### 2. lifecycle_worker_alive_but_broken (5 occurrences)

- 517 sessions spawned on "take it all the way" → loadavg 205, DNS starved, gateway down 2h (May 15)
- 135+ spawn `git ENOENT` in `ao-health.log`; workers up 14+ min but broken; `ai.agento.health` pgrep sees alive → never restarts (Jun 9)
- `execFile('git', ...)` at `packages/core/src/backfill-extensions.ts:451+` inherits process.env.PATH; launchd-nohup chain drops PATH on fork
- 5+ projects have `ai.agento.health` liveness check that cannot distinguish "running" from "running-but-failing"
- Beads: bd-85r, bd-9lxx, bd-7gdr (open)

### 3. config_regression_yaml_clobber (3 occurrences, structural)

- 3rd regression in 30 days (Jun 5, Jun 5, Jun 9)
- Staging `~/.hermes/agent-orchestrator.yaml` and prod `~/.hermes_prod/agent-orchestrator.yaml` don't auto-sync
- `ao_find_config_path` resolution order: staging-before-prod in `scripts/lib/ao-config-topology.sh:85`
- Unknown external writer at 19:04 Jun 9 — never identified
- No diff detection, no checksum, no backup-before-write
- Last verdicts 18:40-18:45 PT, config clobbered 19:04, workers reloaded at 22:22

### 4. config_missing_required_field_silent (5 occurrences)

No JSON schema validation. Silent no-op when:
- `scm: plugin: github` missing (worldarchitect, May 4)
- `worker-signals-completion.action: notify` instead of `skeptic-review` (Jun 5)
- `running.json` absent after reboot — only `ao start` writes it, not lifecycle-worker
- `backfillAllPRs: true` default — mctrl_test 30 PRs spawned 100+ workers, load 104+
- Multiple field absences stacked: scm, action, skepticModel (Jun 10)

### 5. dist_deploy_not_deployed (4 occurrences)

`/Users/jleechan/bin/ao` is a symlink → `main repo dist/index.js`. Running `ao start` holds compiled dist in memory.

- M3 model switch wrote config files but skipped gateway restart — process ran M2.7 in memory 4 days (May 11)
- Skeptic bug fix in commits but not deployed for hours (Jun 2)
- PR #669 committed but localhost:3000 STILL auto-opening (Jun 9)
- Three-step manual sequence required: rebuild worktree dist → copy to main dist → kill PID
- No CI deploys dist automatically

### 6. spawn_path_enoent_paunchy_path (4 occurrences)

- 14 tilde defects across 8 files; canonical `expandHome` in `core/paths.ts:186` not used by 5 plugin copies + 7 `start.ts` regexes
- 9 sites in `backfill-extensions.ts` use bare `git` (not `/usr/bin/git`) — PR #671 fix
- `execFile()` resolution depends on `process.env.PATH` at runtime, not just plist env
- AO_CLI_PATH plist env works for `ao` binary but not for bare system binaries

### 7. auth_401_minimax_persisted (3 occurrences)

- `__OPENCLAW_REDACTED__` sentinels exported as real tokens
- 5 PRs stuck with 401 (Apr 15): #454, #453, #452, #450, #444
- PR #510 approved but never merged; `setup-launchd.sh` sed substitutions missing

### 8. worktree_ghost_branch_drift (3 occurrences)

- AO workers leave main clones in detached HEAD after checking out `origin/main`
- Stale Claude conversation state in reused worktree path JSONL contaminates fresh PR workers
- `pruneStaleWorktrees` + `worktreeDir==path` from May 29 root cause

### 9. evidence_gate_passes_but_wrong (2 occurrences)

- Evidence Gate checked `app/skeptic-agent` for verdicts but actual author is `jleechan2015`/`github-actions[bot]`
- Used oldest verdict `.[0]` instead of newest
- `gh api --paginate` exits 1 on rate-limit under `set -e`

### 10. storm_overspawn (1 occurrence)

- "Take it all the way" spawned 517 sessions, loadavg 205
- `kanban.max_spawn=8` (config) + 20-worker hard cap (discipline)

### 11. open_browser_unwanted (1 occurrence, fixed)

- `waitForPortAndOpen` always fired `open()` on dashboard URL
- PR #669 landed 3-layer suppression (YAML `openBrowser:false` / `AO_NO_OPEN_BROWSER` env / `--no-open-browser` CLI)

## Cross-Cutting Pattern: Silent Failure Paths

**8 of 11 categories share the same root cause class:** guards that return early without emitting a WARN/ERROR log when a critical precondition is missing. The merge pipeline (lifecycle-worker + skeptic-cron + ai.agento.health) is a chain where any one of 3 silent-failure modes disables the entire PR-merge automation fleet-wide.

**The auto-merge/skeptic-verdict delivery path is the single most fragile pipeline in the system.**

## Launchd / Watchdog Architecture Survey

### Active watchdogs (1)

**`ai.agento.health`** — StartInterval=300s (5 min)
- Watches: lifecycle-worker process presence per project (pgrep), main repo branch invariant, WAFER_API_KEY auth validity, stale launchd registrations
- Remediates: starts missing workers, kills stale/orphan workers, SIGTERM→SIGKILL escalation, re-bootstraps its own launchd service if deregistered
- **Self-heals: yes** | **Alerting: NONE — log-only** | **SPOF: yes**

### Broken/disabled watchdogs

- **`ai.hermes-watchdog`** — last exit code 127. Script `/Users/jleechan/.hermes/scripts/hermes-watchdog.sh` does not exist on disk. 158 runs completed before failure. Slack alerting channel `C09GRLXF9GR` set but never delivered. **Single source of truth for AO prod/system alerting is gone.**
- **`ai.openclaw.startup-check`** — 0-byte/corrupt plist. launchd cannot load it.
- **`com.jleechan.antigravity-loop`** — sentinel watchdog-start is 70+ days old; 8h self-unload never fires. Watchdog.sh unloads itself, but not via the broken sentinel. Effective: either dead or keeps re-arming `antigravity-orch` indefinitely.

### Replaced

- **`ai.hermes.gateway`** — "Could not find service in domain"; replaced by `ai.hermes.prod` (KeepAlive=true, prod-grade)

### Slowest pollers (longest detection-to-alert)

- **`ai.openclaw.monitor-agent`** (StartInterval 1800s = 30 min) — has Slack alerting to C0AKYEY48GM, C0AKALZ4CKW, C0AJ3SD5C79 — but 30-min detection gap
- **`com.ao-runner-watchdog`** (StartInterval 3600s = 1 hour) — runs `ao doctor --fix` for self-hosted runners

### Chain-of-trust gap

**NO CHAIN.** `ai.agento.health` is the sole watchdog for the AO fleet. Nothing watches `ai.agento.health` except itself (self-rebootstrap) and Hermes (theoretically, via broken `ai.hermes-watchdog`).

## Current Script Inventory

| Script | Checks | Auto-fix | Alerting | Schedule |
|--------|--------|----------|----------|----------|
| `scripts/ao-doctor.sh` | Node, git, pnpm, ao launcher, tmux, gh, config dirs, dist, version, worker count, non-canonical binaries | `--fix` kills non-canonical workers, refreshes launcher, creates missing dirs, deletes stale temp files | NONE | Manual |
| `scripts/ao-doctor-monitor.sh` | Wraps `ao doctor`, namespace alignment, rogue configs, rate limits, session sprawl, zombie sessions, CHANGES_REQUESTED gaps, stray worktrees, PR age | NO (warn only) | Slack (webhook or user token to #openclaw-health) | Manual |
| `scripts/ao-health.sh` | Config discovery, main repo branch, per-project worker start, orphan kill, wafer API canary, self-rebootstrap | YES (force main, kill orphans, start missing) | NONE (file log only) | launchd StartInterval=300s |
| `scripts/ao-update.sh` | Requires: node, git, pnpm, npm, clean tree, on main. Rebuild: pnpm install + pnpm -r build + pnpm install -g . (3x retry). Restart: ao_bin lifecycle-worker per project. Smoke: --version, doctor --help | YES (kill + restart) | NONE | Manual |

## Memory Gaps (signals that should be monitored but aren't)

From 50+ memory entries, 17 unmonitored signals:

1. tmux pane alive but Claude Code process dead
2. dist loaded in memory but new dist written to disk
3. orchestrator-prompt cache staleness
4. pnpm global store version mismatch
5. git ENOENT inside forked process
6. running.json absence after reboot
7. AO_BOT_GH_TOKEN validity in env
8. scmFailureCount aggregation (per-PR not fleet)
9. 24h age filter silently dropping /skeptic
10. paused project opt-out (ao stop ralph respawns in 5 min)
11. backfillAllPRs default in new schemas
12. Aging memory files claiming fixes never merged (self-confirmation trap)
13. Vitest OOM empty failed-count handling
14. ZFC violations in new code
15. Compaction firing on skills/hooks injection
16. Auto-merge race with skeptic-cron
17. Stale background monitor delivering old FAIL after subsequent PASS

## Missing Alerting Channels

1. Slack push notification on silent skeptic returns
2. Desktop notification on "running but broken" workers
3. tmux status line for prompt/dist staleness
4. PR auto-comment when memory age > 30d claims a fix
5. **bead auto-creation on fragility pattern detection** (would have caught bd-rgk0 automatically)
6. Terminal bell on chronic 0% rate automation
7. Slack/email digest of fragile areas (currently manual grep)
8. Per-project spawn storm alarm
9. Health-check probe of `ao start` binary version vs worktree binary version

## Proposed Architecture: doctor.sh v2 with Alerting

### Three-tier watchdog chain

1. **`ai.agento.health`** (5 min) — current primary, retains self-rebootstrap
2. **NEW `ai.agento.health-guardian`** (60 min) — checks ONLY: is health loaded? Is its log < 10 min old? If not, bootstrap from frozen copy. Slack-alerts via direct curl to channel C09GRLXF9GR (bypassing broken `ai.hermes-watchdog`).
3. **EXTEND `com.ao-runner-watchdog`** (1h) — also re-bootstraps the guardian.

Total worst-case blindness: 60 min. Currently: indefinite.

### Restored Slack alerting path

Recreate `/Users/jleechan/.hermes/scripts/hermes-watchdog.sh` as a 30-line shim that posts to channel C09GRLXF9GR via `HERMES_WATCHDOG_ALERT_CHANNEL` env var. ~1 hour of effort.

### doctor.sh loud-WARN-at-code-path pattern

For each of the 17 unmonitored signals, add a loud `console.warn` at the code path where the guard currently returns silently. This is the durable fix — detect fragility patterns at the code level, not just in watchdog scripts.

### doctor.sh checks for new monitoring

- Config drift between `~/.hermes/` (staging) and `~/.hermes_prod/` (prod) yamls
- pnpm global store version match
- All 10 lifecycle-workers alive (with pgrep + actual functionality probe, not just process liveness)
- All 5 launchd plists loaded
- Both `~/.hermes/` and `~/.hermes_prod/` yaml files validate against schema
- `running.json` exists
- `ao start` binary SHA matches worktree dist SHA
- `ao skeptic verify` smoke test on a known PR
- WAFER_API_KEY + ANTHROPIC_API_KEY + OPENAI_API_KEY validity
- Hermes gateway (`ai.hermes.prod`) alive
- agent-mail MCP server alive

## Connections

- [[AgentOrchestrator]] — the project at `/Users/jleechan/project_agento/agent-orchestrator`
- [[SkepticArchitecture]] — local LLM evaluation, not GHA API keys
- [[WatchdogArchitecture]] — launchd-based supervision
- [[SilentFailurePathPattern]] — cross-cutting root cause
- [[DoctorShAlertingV2]] — proposed design

## Beads

- bd-85r, bd-9lxx, bd-7gdr (lifecycle workers broken, open)
- bd-rgk0 (skeptic-cron 24h filter, closed by PR #661)
- bd-a7mq (session-manager reuse, P1)
- bd-q3tt (P1)
- bd-3m1t (tilde expansion, proposed)
- bd-cx08 (context hygiene audit, every 2 weeks)
