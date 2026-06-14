---
title: "Org runner pool expansion + .ci-retrigger empirical audit (2026-06-13)"
type: source
tags: [self-hosted-runners, runner-pool, ci-retrigger, sentinel, audit, 2026-06-13]
date: 2026-06-13
source_file: raw/project_2026-06-13_org_runner_pool_expansion_and_sentinel_audit.md
---

## Summary
On 2026-06-13 the jleechanorg GitHub Actions self-hosted runner pool grew from 6 to **15 online+busy** (2.5× capacity increase) as the launchd supervisor re-spun previously-offline `bare-org-runner-N` instances. Active run pile-up subsided from 50 to 29 as 4 hot PRs settled. An empirical audit confirmed that `.ci-retrigger` is a **write-only memo, not a state machine** — 87 re-trigger commits in 71 days on agent-orchestrator repo, 82/87 (94.3%) empty `git commit --allow-empty`, no code anywhere reads the file. The intended reader is on a different host (likely AO cron on a non-mac runner/VM), out of scope for single-host search.

## Key Claims
- Runner pool: 5× offline `bare-org-runner-N` (IDs 77708-77713) → 9× online+busy (IDs 1, 3, 4, 5, 6, 7, 8, 9, 10); 6 org-runner-mac-N already online+busy; total = **15 (14 busy + 1 idle)**
- The launchd supervisor at `~/Library/LaunchAgents/com.worldarchitect.org-runners.plist` re-spun the offline runners
- 50 → 29 active runs; 4 hot PRs settled: `fix-stale-complete-preserve-fresh-rewards` (10), `fix/7364-level-up-modal-choices-atomic-pair` (10), `fix/banned-names-prompt-injection-7482` (9), `main` (9)
- `.ci-retrigger` empirical audit (3 subagents): NOT FOUND any reader; verdict = **write-only memo, not a state machine**
- 87 re-trigger commits in 71 days; 82/87 (94.3%) empty `git commit --allow-empty`
- File touched only 3 times in 71 days (uncorrelated with commit cadence)
- Inter-arrival times show NO cron signature (11 within-60-sec bursts, human-shaped)
- On `main`, file has been `trigger` continuously since 2026-04-16 while re-trigger commits continue
- Reverted `.ci-retrigger` to HEAD (`trigger`) via `git checkout HEAD -- .ci-retrigger`
- Updated 2026-06-12 memory entry with "Correction (2026-06-13)" section noting the kill recipe's `printf 'idle' > .ci-retrigger` step is cosmetic
- 15-runner effective pool is the real win from this session

## Key Quotes
> "Future agents reading the 2026-06-12 memory entry should not propagate the false claim that 'the AO cron respects `.ci-retrigger`'."

> "The 15-runner effective pool is the real win from this session — that gives worldarchitect.ai meaningful headroom for the next push burst."

## Verified via
- 3 subagent investigations:
  - code search (a4b628fcba93df6e3)
  - launchd/cron audit (af35f4e03535d0788)
  - git log empirical analysis (a544a5665c584c4e2)

## Connections
- [[self-hosted-oss]] — Mac ARM64 runners
- [[self-hosted-bare]] — Linux X64 runners (re-spun by launchd supervisor)
- [[OrgRunnerPool]] — current pool of 15 (14 busy + 1 idle)
- [[CIReSentinel]] — empirical write-only memo (not a state machine)
- [[LaunchdSupervisor]] — `~/Library/LaunchAgents/com.worldarchitect.org-runners.plist` self-healing loop
- [[feedback-2026-06-12-github-org-runner-registration-vs-group-access]] — related 7-effective-runner state from 2026-06-12
- [[feedback-2026-06-12-local-claude-session-can-runaway-push]] — kill recipe updated to remove cosmetic sentinel-flip step
- [[wakebugbot]] — 2026-06-12 instruction-level fix (rewrote to use `gh workflow run`) remains correct
