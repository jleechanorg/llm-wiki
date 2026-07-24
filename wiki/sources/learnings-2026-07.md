---
title: "Consolidated /learn recap — ez-gh-actions fleet rollout: 12 things that went wrong (2026-07-06)"
type: source
tags: [ezgha, fleet, runners, infra, lessons-learned, worldarchitect.ai]
date: 2026-07-06
source_file: roadmap/learnings-2026-07.md (appended section)
---

## Summary
Single session on 2026-07-06 exposed every gap in the ezgha-binary-rollout → operational-tooling → merge-ready chain. 12 distinct failures categorized into 3 underlying ezgha binary bugs, 4 deceptive failure modes (silent degradation), and 5 procedural gaps (agent-side). External `/ezgha-watchdog` masks most; only upstream fixes in `jleechanorg/ez-gh-actions` (issues #14, #15) will eliminate them. Companion source already exists for the post-recovery incident recap (2026-07-07).

## Key Claims
- **Meta-pattern**: gap between "binary works in dev" and "fleet stays healthy in prod" is dominated by daemon lifecycle mismatch, configuration drift, and operational-tooling blind spots.
- 3 underlying ezgha binary bugs require code fixes: slot-top-up gap, missing sd-notify heartbeats, install.sh not refreshing systemd unit
- 4 deceptive failure modes silently degraded: colima VM Stopped while hostagent alive, stale GitHub runner busy=true, limactl JSON dict-vs-list shape, head -n 1 wrong-VM pick
- 5 procedural gaps: claims without checking both hosts, static 22/22 verdict, run-status artifacts, MacBook SSH default-off, Codex symlink required
- Operational rule: write `/learn` recap after first production week of any new infra tool

## Key Quotes
> "When adopting a new infrastructure tool (binary + systemd + Docker + launchd + GitHub runners + CI gates), the gap between 'binary works in dev' and 'fleet stays healthy in prod' is dominated by 3 classes of failure: daemon lifecycle mismatch, configuration drift, operational-tooling blind spots."

## Connections
- [[EzGhaDaemon]] — the binary whose gaps this document captures
- [[FleetWatchdogScript]] — the external watchdog that masks binary bugs
- [[MacColimaRuntime]] — silent VM-down failure mode documented here
- [[LinuxSystemdUnit]] — stale-unit-after-upgrade failure mode
- [[CodexSkillMirroring]] — symlink-required mirror pattern
- [[RunnerHealthSkill]] — per-arch verdict pattern (replaces static 22/22)
- [[JeffUbuntuHost]] — the host where the Linux fleet runs
- [[GitHubAPIRateLimit]] — secondary blocker during cross-PR correlation

## Key Artifacts
- PR #8193 on jleechanorg/worldarchitect.ai (carrier)
- jleechanorg/ez-gh-actions issues #14, #15 (upstream fixes)
- Bead `rev-a8sby` (cross-cutting audit)
- 8 Claude memory entries in `~/.claude/projects/.../memory/feedback_2026-07-06_*`
- `/Users/jleechan/roadmap/nextsteps-2026-07-06-runner-fleet-hardening-pr8193.md`
- `.claude/skills/ezgha-watchdog/`, `.claude/skills/mac-remote/`, `.claude/skills/runner-health/`
- `.claude/commands/mac.md`