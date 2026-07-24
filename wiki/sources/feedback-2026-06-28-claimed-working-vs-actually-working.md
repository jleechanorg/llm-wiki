---
title: "Claimed Working vs Actually Working — Runner Fleet Verification Probes"
type: source
tags: [runners, infrastructure, verification, silent-divergence, end-state-layer]
date: 2026-06-28
source_file: feedback_2026-06-28_claimed_working_vs_actually_working.md
---

## Summary

After 4 runner-fleet hardening PRs merged (#7851, #8024, #8026, #8027), the agent claimed "runners healthy" based on tool-status output (merge success, Green Gate passed, container Up). The `/advice` reviewer caught this as MEDIUM confidence — "claimed working ≠ actually working." Probes revealed 5 silent-divergence patterns: bind-mount vs COPY trap, hook content md5 mismatch, GITHUB_REPOSITORY env propagation, GitHub-side runner registration state ≠ container state, and gh CLI silent skip in check_github_session_state. The general principle: tool-status reports the implementation layer (did the tool do its part), but the end-state layer is what users experience — verify both.

## Key Claims

- Bind-mount source on Lima VM must match deployed file path; verify via `docker inspect .Mounts[] | select(.Destination)`
- Hook content md5 inside running container must equal deployed file md5
- GITHUB_REPOSITORY must be set by runner before ACTIONS_RUNNER_HOOK_JOB_STARTED fires
- Container Up + GitHub offline = session-conflict class (Runner.Listener retries forever on `Error: Conflict`)
- gh api failure in check_github_session_state must NOT return 0 silently — silent skip = meta-divergence
- After merging any PR that touches runner infra, run all 5 probes before claiming success

## Key Quotes

> "The 4-PR hardening set was largely a no-op on running workloads if bind-mount didn't reach containers."

> "Returning 0 on auth failure creates a meta-divergence (can't see divergence because the divergence detector is offline)."

## Connections

- [[LimaVM]] — Lima is where bind-mount and runner containers live
- [[SelfHostedRunners]] — the fleet that all 5 probes verify
- [[RunnerSessionConflict]] — sibling memory on the specific session-conflict class caught by Probe 4
- [[RuntimeMirrorInstall]] — install.sh pattern that ensures the deployed path matches the bind-mount source
- [[EndStateLayerPrinciple]] — the general principle captured in ~/.claude/CLAUDE.md
- [[RunnerHealthMonitor]] — ubuntu-runner-health.sh where check_github_session_state lives
