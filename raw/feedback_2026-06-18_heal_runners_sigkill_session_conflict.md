---
name: heal-runners-sigkill-session-conflict-loop
description: "docker rm -f in heal-runners.sh SIGKILLs myoung34/github-runner before it can call actions/runner/remove; orphaned GitHub session causes new container to loop on \"Runner connect error: Error: Conflict. Retrying until reconnected.\" Fix: docker stop --time=30 + docker rm."
metadata: 
  node_type: memory
  type: feedback
  bead: rev-dsny5
  originSessionId: cddd86d9-cb68-4482-b37b-9b08aeaf6d2c
---

# heal-runners SIGKILL → GitHub session conflict loop (PR #7666, 2026-06-18)

PR: [jleechanorg/worldarchitect.ai#7666](https://github.com/jleechanorg/worldarchitect.ai/pull/7666) — commit `15c2652cfe` on branch `monitor-ubuntu-runners-alerts`. Targets `self-hosted-oss/heal-runners.sh:204`.

Companion to [[runner-supervisor-loop-and-rc-sourcing]] — that covers the broader supervisor loop + `.runner` volume recreation workaround; this one captures the **causal** fix at the recycle site.

## Root cause

`heal-runners.sh:204` was `docker rm -f "$name"` — SIGKILL, immediate teardown. The `myoung34/github-runner` entrypoint's SIGTERM handler is the one that calls `actions/runner/remove` against GitHub. SIGKILL skips it.

GitHub's session table does not always notice the orphaned session immediately. When the new container registers with the same name, GitHub sees the old session still alive and returns 409 Conflict on session start. The runner retries forever:

```
√ Connected to GitHub
A session for this runner already exists.
2026-06-18 22:27:42Z: Runner connect error: Error: Conflict. Retrying until reconnected.
[repeats forever]
```

## Evidence

2026-06-18 15:27:20Z heal-runners cycle recycled 3 Mac runners simultaneously (mac-1, -2, -4). All three ended up with **byte-identical conflict-loop logs**. mac-3 (44m up), mac-5 (12m up), mac-6 (7m up) survived — busy at the moment of the cycle (skipped by `RUNNER_SELF_HEAL_REQUIRE_GH_BUSY_CHECK` guard at `heal-runners.sh:150-156`).

The survivors were NOT actually healthier than the recycled ones — they only escaped because their old sessions happened to clear before the new container tried to start its session. Pure timing luck.

## Fix

`self-hosted-oss/heal-runners.sh:204`:

```bash
# before — SIGKILL, entrypoint never cleans up session
if docker rm -f "$name" >/dev/null 2>&1; then

# after — SIGTERM with grace window, then remove
if docker stop --time=30 "$name" >/dev/null 2>&1 \
   && docker rm "$name" >/dev/null 2>&1; then
```

30-second grace gives the entrypoint enough time to deregister and close its WebSocket cleanly. No conflict on next registration.

## Why not just clear sessions pre-recycle via `gh api`?

Tempting but wrong. The session table is server-side; you can't `DELETE` a session row directly via API. The only way to clear a stale session is either (a) wait for GitHub's timeout, or (b) `actions/runner/remove` from inside the runner process — which is exactly what `docker stop` lets the SIGTERM handler do.

## Why not skip the recycle entirely on `state=running, restarts=0`?

The current trigger is `RUNNER_SELF_HEAL_ERROR_PATTERNS` matched against the last N log lines. Tempting to require `restarts > 0` as a precondition, but that would miss real cases where the runner is "running" but the listener is wedged. `docker stop --time=30` is the structurally correct fix; pattern tuning is a band-aid.

## Runtime copy sync

Per [[runner-supervisor-loop-and-rc-sourcing]] §"Stable install path sync", the live `heal-runners.sh` is at `~/.local/share/worldarchitect-runners/heal-runners.sh`. install.sh's RUNTIME_SCRIPTS array copies it from the worktree. After editing the worktree copy:

```bash
cp self-hosted-oss/heal-runners.sh ~/.local/share/worldarchitect-runners/heal-runners.sh
```

launchd's running `launchd-start.sh` will pick up the change on its next 5-min tick.

## Verification after merge

After #7666 merges + this Mac's runtime copy is synced, the next forced recycle should produce **no** conflict-loop logs in any of the 6 runners. The "Runner connect error: Conflict" string should disappear from `docker logs <container>` output entirely.

If it reappears: the image's STOPSIGNAL was overridden somewhere (it currently defaults to SIGTERM, which is what we want), OR the 30-second grace is shorter than the entrypoint's cleanup time and needs to grow.

**How to apply:** Any future containerized GitHub Actions runner using a graceful-shutdown entrypoint (myoung34/github-runner, actions/runner, custom images) must NOT be SIGKILL'd on recycle. Always `docker stop --time=<grace>` first, then `docker rm`. Same pattern applies to any container that holds a long-poll connection to an upstream control plane (buildkite-agent, circleci runner, drone-agent, etc.).
