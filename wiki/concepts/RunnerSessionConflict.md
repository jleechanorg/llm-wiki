---
title: "RunnerSessionConflict"
type: concept
tags: [github-actions, self-hosted-runners, ops, silent-failure]
sources: [sources/feedback-2026-06-28-runner-session-conflict.md]
last_updated: 2026-06-28
---

## Summary
A silent failure mode for self-hosted GitHub Actions runners where a container is `Up` and logs `Listening for Jobs` while GitHub-side reports the runner as `offline` and never dispatches jobs to it. Root cause: when a runner container is killed (docker rm -f, system shutdown, OOM) WHILE GitHub has allocated a job to it (`busy=true`), the GitHub-side record stays `busy=true` for the entire job timeout window (~30+ min). On restart, GitHub rejects fresh registration with "A session for this runner already exists"; Runner.Listener retries forever instead of giving up and re-registering.

## Why It Matters
- Container-side health checks (`docker ps`, `docker logs` showing "Listening for Jobs") are misleading — they show process state, not dispatch eligibility
- `heal-runners.sh` does NOT reconcile GitHub-side runner state; it only manages containers
- CI degrades silently: zero errors surface to operators, jobs simply never start
- All 16 Linux runners may show `Up` while only 15 receive jobs — silent capacity loss

## Detection Signature
Three signals must be observed together:
1. `gh api orgs/jleechanorg/actions/runners --jq '.runners[] | select(.name=="X") | .status'` = `offline`
2. `docker ps --filter name=X` = `Up X minutes`
3. `docker logs X | tail -5` shows:
   ```
   √ Connected to GitHub
   A session for this runner already exists.
   YYYY-MM-DDTHH:MM:SSZ: Runner connect error: Error: Conflict. Retrying until reconnected.
   ```

## Heal Procedure
```bash
# 1. Get the runner ID from GitHub
RUNNER_ID=$(gh api orgs/jleechanorg/actions/runners --jq '.runners[] | select(.name=="X") | .id')

# 2. Delete the stale GitHub-side registration (only works if busy=false;
#    if busy=true, wait for the job to time out or cancel the job first)
gh api -X DELETE orgs/jleechanorg/actions/runners/$RUNNER_ID

# 3. Restart the container to re-register fresh
docker restart X

# 4. Verify (give it ~15s)
gh api orgs/jleechanorg/actions/runners --jq '.runners[] | select(.name=="X") | {status, busy}'
# Expect: { "status": "online", "busy": false }
```

## Verification Layer Hierarchy
For "runner X is healthy" claims, use the most-authoritative signal you can obtain:
1. Container Up? (local, fast, **misleading**)
2. GitHub `status:"online"`? (**authoritative for dispatch eligibility**)
3. Runner actually receiving jobs in the last 5 min? (end-to-end proof)

Required minimum for health claims: (2). For "runners are healthy overall" claims: (3) sampled across the fleet.

## Prevention
- Never kill a runner container mid-job without cancelling the GitHub-side allocation first (`gh api -X POST .../runs/<id>/cancel`)
- Wrap container lifecycle in a single script that: cancels running jobs → waits for `busy=false` → `docker rm -f` → DELETE stale record → start fresh container
- Add a periodic fleet probe that compares `docker ps` (Up count) vs `gh api .../runners --jq '[.runners[] | select(.status=="online")] | length'` — divergence = session conflict(s)

## Related Concepts
- [[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]] — broader pattern of distinguishing infra flakes from real failures
- [[ZeroRunnersCIStuck]] — total fleet outage (related but distinct: all runners offline, not silent single-runner divergence)
- [[LimaVMCommunicationPattern]] — two-stage SSH hop to jeff-ubuntu / Lima QEMU (probe before diagnosing)
- [[VerifyBeforeUpstreamClaim]] — verify before reporting (extends to runner health claims)

## Source
- [Runner session conflict (2026-06-28)](sources/feedback-2026-06-28-runner-session-conflict.md) — first observed on org-runner-mac-6 (runner ID 111582); surfaced after PR #7851/#8026/#8027 runner-fleet hardening