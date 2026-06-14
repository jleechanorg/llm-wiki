---
name: self-hosted-mac-runner-race-condition-fix
description: "docker_rm_force_with_timeout on macOS returned before daemon finalized, causing \"removal already in progress\" loop; fix is to fire foreground rm + poll docker ps -a until container actually disappears"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 73be4e82-d635-4fd2-96b7-639072ec7448
---

# Self-hosted Mac runner race condition (2026-06-03)

Bead rev-xxxxx (add bead ID once filed)

## Symptom

`heal-runners.sh` and `start-runner.sh` on Mac (no GNU `timeout`) spun forever with:
```
WARN: Force-removing stale runner containers: org-runner-mac-1
...
Error response from daemon: removal of container org-runner-mac-3 is already in progress
WARN: Could not remove stale container org-runner-mac-3; continuing.
WARN: Removing existing runner container org-runner-mac-3 (force remove).
```

The launchd agent (`com.worldarchitect.org-runners`) ended up `state = not running` after enough of these errors piled up. 0 / 6 Mac runners were running, while 10 Linux org-runners on a different host were still online.

## Root cause

`docker_rm_force_with_timeout` in `self-hosted-oss/defaults.sh` used a backgrounded `docker rm -f &` + `wait $pid` on macOS:

```bash
( docker rm -f "$container_name" >/dev/null & \
  pid=$! ; \
  ( sleep "$timeout_secs" ; kill -9 $pid 2>/dev/null || true ) & \
  wait $pid 2>/dev/null )
```

The function returned as soon as `wait` completed (often 0 because the subshell swallowed the real exit). The Docker daemon was still finalizing the removal. The next script iteration called `docker rm -f` on the same name → "already in progress". `start_one_runner` line 350 also retries the same container, so the loop never terminated.

## Fix

Patched `docker_rm_force_with_timeout` to (1) run `docker rm -f` synchronously and (2) **poll `docker ps -a` until the container actually disappears** before returning. Returns non-zero only if the container is still present after the deadline. Tolerates "already in progress" silently during the poll.

Also synced the patched `defaults.sh` to:
- `~/.local/share/worldarchitect-runners/defaults.sh` (stable install)
- `~/projects/worldarchitect.ai/self-hosted-oss/defaults.sh` (main worktree)

## Why

`Wait for the daemon to finalize` is the invariant the script was violating. Synchronous `docker rm -f` returns when the daemon accepts the request, not when the container is fully removed. Without polling, concurrent or sequential removal of the same name races against the daemon's own state machine.

**How to apply:** Any future Docker cleanup helper in this repo (and in any self-hosted runner fork) must poll for actual disappearance, not just return on the rm exit code. Same pattern applies to `docker network rm`, `docker volume rm`, and any other async-finishing Docker operation.
