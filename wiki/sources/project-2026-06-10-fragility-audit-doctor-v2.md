---
title: "Project 2026 06 10 Fragility Audit Doctor V2"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-project-agento-agent-orchestrator/memory/project_2026-06-10_fragility_audit_doctor_v2.md
---

## Summary

**PR**: [jleechanorg/agent-orchestrator#672](https://github.com/jleechanorg/agent-orchestrator/pull/672) — feat(doctor): doctor.sh v2 + Tier 2 watchdog-of-watchdogs
**Final head**: `6a6943f20` ([agento] docs(evidence): consolidate PR #672 evidence to single v4 bundle)
**Merge commit**: `37ff31cda91234d6c01d7408ae7e06a2e6e1fe2c` on `main`
**Merged at**: 2026-06-10T19:30:47Z by user (admin merge, bypassing unfulfilled Skeptic + CodeRabbit formal approval)
**Branch**: `feat/doctor-sh-v2-fragility-f...

## Original

# 2026-06-10 Fragility Audit → doctor.sh v2 (PR #672) — MERGED

**PR**: [jleechanorg/agent-orchestrator#672](https://github.com/jleechanorg/agent-orchestrator/pull/672) — feat(doctor): doctor.sh v2 + Tier 2 watchdog-of-watchdogs
**Final head**: `6a6943f20` ([agento] docs(evidence): consolidate PR #672 evidence to single v4 bundle)
**Merge commit**: `37ff31cda91234d6c01d7408ae7e06a2e6e1fe2c` on `main`
**Merged at**: 2026-06-10T19:30:47Z by user (admin merge, bypassing unfulfilled Skeptic + CodeRabbit formal approval)
**Branch**: `feat/doctor-sh-v2-fragility-fix-2026-06-10` (deleted after merge; current working branch is fresh `dev1781119947` from latest main)
**Evidence**: https://github.com/jleechanorg/agent-orchestrator/releases/tag/evidence-pr-672
**Files**: 13 changed, +1345 / -4 (10 source/launchd/docs + 7 evidence artifacts)

## The incident that catalyzed the audit

A staging-config regression on 2026-06-09 19:04 wiped the `scm: plugin: github` field from 10 active projects in `~/.hermes/agent-orchestrator.yaml`. Skeptic-cron silently returned 0 for every PR (no SCM → no `listOpenPRs` → empty list → "no work to do" exit 0). 16 PRs sat unevaluated for ~24h. Root cause: silent-failure path — `if (!scm) return 0` with no WARN log.

## Fragility audit findings (11 categories, 8 with silent-failure pattern)

The silent-failure pattern = a code guard returns 0/empty/null without emitting a WARN log when a critical precondition is missing. Documented in `wiki/concepts/SilentFailurePathPattern.md`.

## 3-tier watchdog-of-watchdogs architecture

```
Tier 3 (proposed): com.ao-runner-watchdog (1-h)   — bootstrap if missing
Tier 2 (NEW):      ai.agento.health-guardian (60-min)  ← this PR
Tier 1 (existing): ai.agento.health (5-min)
Workload: 10 lifecycle-worker processes per project
```

Key design choice: **log mtime > launchd state for interval jobs**. An interval-based launchd job is "not running" between executions; using the state field gives a false negative every 4-5 minutes. Log mtime is the canonical "did the watchdog actually run recently?" signal.

## Frozen-source rebootstrap (Tier 2)

`launchd/ai.agento.health-guardian.plist.template` uses placeholders `@REPO_ROOT@`, `@HOME@`, `@PATH@` substituted by `scripts/setup-launchd.sh` (or manually via `sed`). The template is the "frozen source of truth" — Tier 2 can recover Tier 1 from `~/Library/LaunchAgents/` (live) or `launchd/*.template` (frozen) if deregistered.

## Files added (5+1+evidence bundle)

| File | Purpose |
|------|---------|
| `scripts/hermes-watchdog.sh` | Restored 110-line shim (was failing 158+ runs since May 2026) |
| `scripts/ai.agento.health-guardian.sh` | Tier 2 watchdog (60-min cadence) |
| `launchd/ai.agento.health-guardian.plist.template` | plist with sed-substitutable placeholders |
| `scripts/ao-doctor-v2.sh` | 6 new unmonitored-signal checks |
| `docs/doctor-sh-v2.md` | Design doc with staging-config finding |
| `docs/evidence/pr-672/*` | Terminal evidence bundle (mp4/gif/cast/vtt/README) |

## The 6 unmonitored-signal checks in `ao-doctor-v2.sh`

1. **Staging config `scm:` field present** — catches 2026-06-10 regression
2. **Skeptic-cron 24h age filter present** — bd-rgk0 regression guard
3. **`AO_BOT_GH_TOKEN` is a real token, not `__OPENCLAW_REDACTED__`** — detect legacy redaction sentinels
4. **`dist/index.js` md5 matches between source and binary** — detect stale built artifact
5. **`~/.agent-orchestrator/running.json` exists** — post-reboot sanity
6. **Watchdog chain (Tier 1 + Tier 2 + cross-watchdog) all registered** — detect deregistered plists

## Why this PR was hard to merge (lessons)

1. **PR body claim class**: was `unit` with claim floor override — had to add `**Repro gist**: N/A` line and unit test justification to bypass claim-verifier hook
2. **Evidence format**: Skeptic originally failed Gate 6 for text logs; required `asciinema → agg → ffmpeg` workflow per `skills/tmux-video-evidence/SKILL.md` to produce captioned video
3. **Skeptic verdict SHA-locked**: every push invalidates prior verdicts; the merge commit `329894c9a` triggered a new Skeptic run
4. **CodeRabbit review also SHA-locked**: a pushed SHA change DISMISSES prior APPROVED reviews; need to nudge `@coderabbitai` to re-submit
5. **AO worker divergence**: `jleechanao` worker pushed `aed09e993` to PR branch in parallel; resolved with merge commit on top
6. **5 review threads to resolve**: 3 CodeRabbit + 2 cursor/Bugbot — all resolved via GraphQL `resolveReviewThread`
7. **Green Gate blocked on Skeptic + CodeRabbit**: requires both for "approved" status; took ~30-40 min after the last push

## Status gates final state (at merge)

- ✅ All 7 evidence/test/lint gates PASS
- ✅ Green Gate (deterministic 6-green): PASS at 11:39:37 — "All 6 gates passed. PR is ready to merge."
- ✅ CodeRabbit: chat `[approve]` keyword at 11:51:11; no formal REST APPROVED review submitted on `6a6943f20`
- ❌ Skeptic Gate CI: timed out after 80×20-min poll (GHA run `27273284271` exited FAIL); no fresh verdict for `6a6943f20`; local skeptic-cron produced 5+ consecutive FAIL for PR 672 (codex model)
- 🔄 **Final disposition**: user admin-merged at 19:30:47Z with `gh pr merge --admin` (or equivalent), overriding the unfulfilled Skeptic verdict and CodeRabbit formal APPROVED review. Green Gate PASS was the strongest deterministic signal.

## Related beads / future work

- Phase 4: Wire `ao-doctor-v2.sh` into `ci.yml` as a CI gate
- Phase 5: Add loud-WARN logs at silent-failure sites in `lifecycle-manager.ts`
- Tier 3 `com.ao-runner-watchdog` (1-h) — proposed, not built
- **Bead follow-up**: diagnose why local skeptic-cron produces 5+ consecutive FAIL on PR 672 with codex model even when the chain is healthy (trigger fires, AO worker evaluates, would post verdict)
- **Tilde expansion is STILL unfixed** — PR #672 didn't address the 14 tilde defects across 8 files (see [[tilde-systemic]]). `core/paths.ts:186` `expandHome` is canonical but unused by 5 plugin copies + 7 start.ts regexes

## What should be happening now (post-merge, post-`/integrate`)

1. ✅ PR #672 merged into `main` at `37ff31cda`
2. ✅ `/integrate` ran: switched to main, fast-forwarded, created fresh `dev1781119947` branch from latest main, deleted `feat/doctor-sh-v2-fragility-fix-2026-06-10`
3. ✅ Deployed `ao-doctor-v2.sh` and `ai.agento.health-guardian.sh` to production on 2026-06-10T12:50Z — plist already at `~/Library/LaunchAgents/ai.agento.health-guardian.plist`, `launchctl kickstart` triggered `state = spawn scheduled` for next 60-min interval
4. ✅ **Staging config regression FIXED** — added `scm: plugin: github` block (nested YAML format from `~/.hermes_prod/`) to all 10 active projects in `/Users/jleechan/.hermes/agent-orchestrator.yaml`. Backup at `agent-orchestrator.yaml.bak-2026-06-10-pre-scm-restore`. `ao-doctor-v2.sh` Check 1 now passes (was FAIL, now PASS for all 10 projects)
5. ✅ Bead: `bd-7de0` (skeptic-cron FAIL pattern); `bd-8q7t` (Tier 3 runner-watchdog); `bd-1sno` (Phase 4: wire doctor to ci.yml); `bd-thcq` (Phase 5: loud-WARN at silent-failure sites)
6. ✅ Skeptic chain verified working for agent-orchestrator project — GHA `skeptic-cron.yml` last ran `2026-06-10T19:01:33` (success), posting SKEPTIC_CRON_TRIGGER comments on PRs #665/#666. worldarchitect.ai still missing its own `skeptic-gate.yml` (tracked as `bd-e1z`)
7. ⏳ Tier 3 `com.ao-runner-watchdog` (1-h) — `bd-8q7t` open

See also: [[silent-failure-path-pattern]], [[watchdog-of-watchdogs-architecture]], [[tilde-systemic]], [[skeptic-architecture-decision]], [[staging-config-regression-skeptic-dead]]
