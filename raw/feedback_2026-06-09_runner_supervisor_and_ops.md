---
name: runner-supervisor-loop-and-rc-sourcing
description: Self-healing launchd supervisor wrapping heal-runners.sh in `while true; sleep 300` avoids 3600s StartInterval stall; sourcing ~/.bashrc requires `set +u` AND `set +e` to absorb cmux $PROMPT_COMMAND access and user rc errexit leak
metadata:
  type: feedback
  originSessionId: 73be4e82-d635-4fd2-96b7-639072ec7448
  bead: rev-5ysuv
---

# Runner supervisor loop + RC sourcing (PR #7271, 2026-06-09)

PR: [jleechanorg/worldarchitect.ai#7271](https://github.com/jleechanorg/worldarchitect.ai/pull/7271) — merged 2026-06-07T22:06:25Z by jleechan2015, merge commit `bdaadff0f5f156f23639a44e6e0fc7d01ff95307`.

Companion to [[self-hosted-mac-runner-race-condition-fix]] — that captures the `docker_rm_force_with_timeout` race fix; this one captures everything around the supervisor wrapper.

## Why the supervisor is a `while true; ...; sleep 300` loop, not `KeepAlive`

The previous `launchd-start.sh` exited after one `heal-runners.sh` cycle. With `StartInterval=3600`, a single bad cycle → 1-hour gap with no reconciliation. launchd's `KeepAlive` would work but obscures the failure mode (you can't tell from a stuck agent vs a cycling one).

The fix wraps the cycle in `while true; do bash heal-runners.sh; sleep 300; done`. Each cycle is independent. A failed cycle logs the exit code and the loop continues — this is the design intent. **The script uses `set -uo pipefail`, NOT `set -e` — the loop must survive `heal-runners.sh` non-zero exits.**

## Why bashrc sourcing needs `set +u` AND `set +e` (not just `set +u`)

`launchd` runs jobs with a minimal env — no `.bashrc`/`.zprofile` is sourced. We must inherit login/interactive env so `DOCKER_HOST`, `PATH`, `NVM`, etc. survive into `heal-runners.sh` and its descendants.

But user rc files can blow up the supervisor in two ways:

1. **Unset vars (`set -u` abort)**: `cmux-bash-integration.bash` touches `$PROMPT_COMMAND` (a var the launchd shell doesn't have). Result: `set -u` parent aborts on first access inside the rc. **Fix: `set +u` around the rc-sourcing block**, restore `set -u` after.
2. **errexit leak (`set -e` propagation)**: many shared dotfiles run `set -o errexit`. A `set -e` parent then turns the *next* transient heal-cycle failure into a fatal script exit — the very thing the loop is designed to absorb. **Fix: `set +e` around the rc-sourcing block**, do not restore `set -e` for the rest of the script. (The script's intent IS that heal-runners failures are logged, not fatal — this matches the `set -uo pipefail` choice above.)

Source order matters: `.bash_profile` → `.zprofile` → `.bashrc` → `.zshrc`. Each is `.`-sourced with `> /dev/null 2>&1 || true` so a failing rc never aborts the supervisor.

## Docker start-up race — bound the wait, not retry forever

The supervisor waits up to `DOCKER_WAIT_SEC=150` (30 × 5s) for Docker. If unavailable, it logs and `exit 1` so launchd can respawn the whole script at the next `StartInterval`. **Do NOT loop here**: Docker won't come up faster than that, and infinite spin is hostile to other launchd agents on the same user context.

## GitHub-side `busy=true` corruption — local actions cannot clear it

Symptom: all 16 self-hosted runners on `jleechanorg` stuck `busy=true` on GitHub's side, even though the local `actions.runner.*` processes are stopped and containers removed. No local command clears it.

Cause: prior cancellation of orphan GitHub Actions runs left all runners in a `Busy` registration state that the API blocks new work for.

Recovery: it took ~1 hour for GitHub's session-timeout to clear, OR explicit `gh api -X DELETE` against the runner registration after the runner is fully offline. We confirmed the local Docker side is healthy *before* assuming GH-side is the problem — a stuck busy state with 0 in-flight runs is a strong signal.

## Hard-reset gotcha — container → volume removal ordering

`docker volume rm <runner-work-vol>` fails with `volume is in use` if the container is still attached. Correct order:

```bash
docker stop  <container>   # or `docker kill` if stop times out
docker rm -f <container>
docker volume rm <work-vol> # only now is the volume releasable
```

The `docker_rm_force_with_timeout` poll pattern (see companion memory) covers the rm step but the **stop must happen first** — `docker rm -f` does NOT stop a running container on some Docker versions.

## "Session already exists" loop — orphan `.runner` credentials

If a container's `.runner` file holds credentials for a session that GitHub still considers active (e.g. from a cancelled run), every restart hits `Error: A session for this runner already exists.` The fix is full container recreation:

1. `docker rm -f` (stops + removes, but `.runner` persists in the named volume)
2. `docker volume rm` on the work volume (drops `.runner`)
3. Re-create the container with `start-runner.sh` — it generates a fresh `.runner`

**Do NOT** try to clear the stale session from `~/.runner` files alone; the daemon-side state is what matters.

## PR cancellation collateral damage — protect the in-flight /green PR

When fanout subagents cancel orphan CI runs, the protected set MUST include the PR currently being driven to /green. Otherwise the cancellation subagent kills the CI runs the /green subagent just pushed for, and the /green subagent loops on missing checks.

**Rule**: pass the same protected-PR list to BOTH the cancellation subagent AND the /green subagent. The /green subagent already knows which PRs it owns; the cancellation subagent does not. The safe default is the union: protected PRs + the PR the /green subagent is working on.

## Stable install path sync — `~/.local/share/worldarchitect-runners/`

Scripts live in two places: the main worktree (`/Users/jleechan/projects/worldarchitect.ai/self-hosted-oss/`) AND the stable install (`~/.local/share/worldarchitect-runners/`). launchd runs the stable install, NOT the worktree copy. After editing any of `defaults.sh`, `launchd-start.sh`, `heal-runners.sh`, `start-runner.sh` in the worktree:

```bash
cp self-hosted-oss/{defaults,launchd-start,heal-runners,start-runner}.sh \
   ~/.local/share/worldarchitect-runners/
```

If you forget this, `heal-runners.sh` exits with `exit=127` (command not found) on the next reconcile, the supervisor logs the error, and you lose the fix in a 5-minute cycle.

## Verification protocol after supervisor deploy

1. `launchctl print gui/$(id -u)/com.worldarchitect.org-runners` — confirm `state = running`, `last exit code = 0`.
2. Tail `~/.local/share/worldarchitect-runners/supervisor.log` for at least one full cycle (5 min). Look for `Reconciling runner pool...` → `Cycle OK. Sleeping 300s.`
3. `docker ps | grep org-runner` — confirm at least `RUNNER_COUNT` containers running and `Running` (not `Restarting`).
4. Trigger a real CI run on a non-protected PR; verify the runner picks it up within 60s.

## Why this matters

`jleechanorg` runs org-level self-hosted runners on Mac (and Linux) for cost and capacity reasons. Without the supervisor loop + race fix, the fleet is one Docker hiccup away from being fully offline, and launchd's 1-hour `StartInterval` means a recovery that should take 5 minutes takes an hour. With the supervisor: any transient failure is logged and the next 5-minute cycle re-converges.

**How to apply:** Any future `launchd`-managed, container-pool supervisor on macOS should follow the same pattern: `while true` loop with `set -uo pipefail` (NOT -e), rc-sourcing with `set +u` AND `set +e`, bounded Docker wait that defers to launchd respawn, stable install path sync, and GH-side `busy=true` as a known-recoverable failure mode that local actions cannot clear alone.
