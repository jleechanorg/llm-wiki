---
title: "Runner session conflict — silent GitHub-side offline when container is Up"
type: source
tags: [feedback, runners, self-hosted, github-actions, ops]
date: 2026-06-28
source_file: feedback_2026-06-28_runner_session_conflict.md
---

## Summary
When a self-hosted runner container is killed mid-job, GitHub keeps the runner record in `busy=true` for the job timeout window. On restart, GitHub rejects fresh registration with "A session for this runner already exists"; Runner.Listener retries forever instead of giving up — so the container appears `Up`/`Listening for Jobs` while receiving zero jobs. This is a silent divergence between container-side and GitHub-side runner state that `heal-runners.sh` does NOT reconcile.

## Key Claims
- `gh api orgs/jleechanorg/actions/runners` status=offline + `docker ps` Up + logs "A session for this runner already exists" + "Runner connect error: Error: Conflict. Retrying until reconnected." = session conflict (not a healthy runner)
- The conflict root cause is container killed WHILE GitHub had `busy=true`; old record blocks fresh registration
- Runner.Listener is designed to retry forever on conflict — there is no automatic re-register path
- Heal = `gh api -X DELETE` the stale GitHub-side runner ID, then `docker restart` to re-register fresh; verify `status:"online"` afterwards
- Verification layer hierarchy (most-authoritative last): (1) Container Up? (can be misleading) → (2) GitHub `status:"online"`? (authoritative for dispatch eligibility) → (3) actually receiving jobs in last 5 min? (end-to-end proof)
- For "X is healthy" claims you need at least (2); never claim health from container-side alone

## Key Quotes
> "A session for this runner already exists.
> 2026-06-28T20:03:12Z: Runner connect error: Error: Conflict. Retrying until reconnected."

> "This is a silent failure mode: the runner appears healthy from container-side inspection (Up, Listening) but receives ZERO jobs from GitHub."

> "NEVER claim 'runners healthy' from container-side alone — always check GitHub API"

## Connections
- [[LimaVMCommunicationPattern]] — Lima QEMU SSH-probe before diagnosing runners
- [[LimaVMWatchdogGap]] — June 18-23 5-day silent hang context (related class: silent divergence between control plane and observable state)
- [[LimaVMWalkthrough]] — full Lima comms pattern for jeff-ubuntu
- [[VerifyBeforeUpstreamClaim]] — generalized "verify before reporting" pattern
- [[OrgRunnerFleet]] — jleechanorg self-hosted runner fleet (org-runner-X, org-runner-mac-N)
- PR #7851, #8024, #8026, #8027 — runner-fleet hardening work
- org-runner-mac-6 (runner ID 111582) — first observed instance

## Heal Procedure
```bash
# 1. Get the runner ID from GitHub
RUNNER_ID=$(gh api orgs/jleechanorg/actions/runners --jq '.runners[] | select(.name=="org-runner-X") | .id')

# 2. Delete the stale GitHub-side registration (only works if busy=false;
#    if busy=true, wait for the job to time out or cancel the job first)
gh api -X DELETE orgs/jleechanorg/actions/runners/$RUNNER_ID

# 3. Restart the container to re-register fresh
docker restart org-runner-X

# 4. Verify
sleep 15
gh api orgs/jleechanorg/actions/runners --jq '.runners[] | select(.name=="org-runner-X") | {status, busy}'
# Expect: { "status": "online", "busy": false }
```

## Related memories
- [[verify-lima-vm-before-runner-ops]] — SSH-probe Lima BEFORE diagnosing runners
- [[lima-vm-walkthrough]] — full Lima communication pattern
- [[lima-vm-watchdog-gap]] — June 18-23 5-day outage context

## References
- Session: 2026-06-28 (post PR #7851 merge)
- Affected runner: org-runner-mac-6 (runner ID 111582)
- See PR #7851, #8024, #8026, #8027 for the runner-fleet hardening work