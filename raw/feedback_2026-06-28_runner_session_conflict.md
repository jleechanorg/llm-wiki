---
name: runner-session-conflict
description: When GitHub shows a runner offline but the container is Up + Listening, it's a session conflict — Runner.Listener retries forever; manual heal required
type: feedback
bead: none
---

## Context

After PR #7851 + #8026 + #8027 (Lima VM watchdog + generic pre-job-hook + dual-VM install),
verified Lima VM healthy, all 16 Linux runners Up, watchdog running. But mac-6 was
showing offline on GitHub even though the container was `Up 4 minutes` and logs showed
`Listening for Jobs`. This is a silent divergence: container-side vs GitHub-side
runner registration state are independent, and `heal-runners.sh` does NOT reconcile them.

## The pattern

**Symptoms:**
- `gh api orgs/jleechanorg/actions/runners` shows `org-runner-X: status=offline`
- `docker ps --filter name=org-runner-X` shows `Up X minutes`
- `docker logs org-runner-X | tail -5` shows:
  ```
  √ Connected to GitHub
  A session for this runner already exists.
  2026-06-28T20:03:12Z: Runner connect error: Error: Conflict. Retrying until reconnected.
  ```

**Root cause:**
When a runner container is killed (docker rm -f, system shutdown, OOM kill) WHILE
GitHub has allocated a job to it (busy=true), the GitHub-side record stays in
`busy=true` for the entire job timeout window (~30+ min). When the container
restarts and tries to register fresh, GitHub rejects with "A session already exists"
because the old (busy=true) record is still there. Runner.Listener is designed to
retry forever on conflict, not give up and re-register with a new agent ID.

This is a **silent failure mode**: the runner appears healthy from container-side
inspection (Up, Listening) but receives ZERO jobs from GitHub. CI degrades silently
without any error to operators.

## The fix

```bash
# 1. Get the runner ID from GitHub
RUNNER_ID=$(gh api orgs/jleechanorg/actions/runners --jq '.runners[] | select(.name=="org-runner-X") | .id')

# 2. Delete the stale GitHub-side registration (only works if busy=false; if busy=true,
#    wait for the job to time out or cancel the job first)
gh api -X DELETE orgs/jleechanorg/actions/runners/$RUNNER_ID

# 3. Restart the container to re-register fresh
docker restart org-runner-X

# 4. Verify
sleep 15
gh api orgs/jleechanorg/actions/runners --jq '.runners[] | select(.name=="org-runner-X") | {status, busy}'
# Expect: { "status": "online", "busy": false }
```

## How to apply

Any time you observe runner status divergence:
1. Check container-side: `docker ps --filter name=org-runner-X`
2. Check GitHub-side: `gh api orgs/jleechanorg/actions/runners --jq '.runners[] | select(.name=="org-runner-X") | {status, busy}'`
3. If container up + GitHub offline → session conflict → apply the heal above
4. NEVER claim "runners healthy" from container-side alone — always check GitHub API

**Verification layer hierarchy** (most-authoritative last):
1. Container Up? (local, fast, can be misleading)
2. GitHub `status:"online"`? (authoritative for job dispatch eligibility)
3. Runner actually receiving jobs in the last 5 min? (end-to-end proof)

For "X is healthy" claims, you need at least (2).

## Related memories

- [[verify-lima-vm-before-runner-ops]] — SSH-probe Lima BEFORE diagnosing runners
- [[lima-vm-walkthrough]] — full Lima communication pattern
- [[lima-vm-watchdog-gap]] — June 18-23 5-day outage context

## References

- Session: 2026-06-28 (post PR #7851 merge)
- Affected runner: org-runner-mac-6 (runner ID 111582)
- See PR #7851, #8024, #8026, #8027 for the runner-fleet hardening work