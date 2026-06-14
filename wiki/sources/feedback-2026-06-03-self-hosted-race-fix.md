---
title: "Self-hosted Mac runner race condition fix (2026-06-03)"
type: source
tags: [feedback, self-hosted-runner, docker, macos, race-condition, worldarchitect-ai]
date: 2026-06-03
source_file: raw/feedback_2026-06-03_self_hosted_race_fix.md
---

## Summary
The `docker_rm_force_with_timeout` helper on macOS (no GNU `timeout`) was returning before the Docker daemon finalized the container removal, producing a `removal of container ... is already in progress` loop. The fix runs `docker rm -f` synchronously and polls `docker ps -a` until the container actually disappears. This is the underlying Docker cleanup primitive that the 2026-06-09 supervisor / RC sourcing ops file builds on.

## Key Claims
- `docker rm -f &` + `wait $pid` on macOS returns as soon as `wait` completes (often 0 because the subshell swallowed the real exit), but the daemon is still finalizing the removal.
- The next iteration of the loop then issues `docker rm -f` on the same name → `Error response from daemon: removal of container ... is already in progress`.
- Correct invariant: "Wait for the daemon to finalize" — poll `docker ps -a` until the named container is actually gone, returning non-zero only if the container is still present after the deadline.
- "Already in progress" errors during the poll are silently tolerated — the container will disappear in a few seconds.
- The patched `defaults.sh` must be cp'd to both the worktree and `~/.local/share/worldarchitect-runners/defaults.sh` (the stable install path launchd runs from).
- Same pattern (synchronous call + poll for actual disappearance) applies to `docker network rm`, `docker volume rm`, and any other async-finishing Docker operation.

## Key Quotes
> "Synchronous `docker rm -f` returns when the daemon accepts the request, not when the container is fully removed. Without polling, concurrent or sequential removal of the same name races against the daemon's own state machine."

## Connections
- [[feedback-2026-06-09-runner-supervisor-and-ops]] — companion file; this one is the underlying `docker_rm_force_with_timeout` primitive, that one is the supervisor + RC sourcing + busy=true layer around it
- [[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]] — adds the `docker_rm_force_with_timeout` race condition to the self-hosted-runner failure catalogue
- [[Launchd]] — adds the stable-install-path cp discipline (the same fix has to be re-cp'd to `~/.local/share/worldarchitect-runners/` after worktree edits)
- [[SelfHostedRunnerNaming]] — companion ops rule about the two-scripts-two-locations pattern

## Bead / PR / Roadmap

- Bead: not yet filed (memory file has `Bead rev-xxxxx` placeholder)
- PR: not directly linked; the fix was deployed through the 2026-06-09 supervisor rollout ([#7271](https://github.com/jleechanorg/worldarchitect.ai/pull/7271))
- Origin session: `73be4e82-d635-4fd2-96b7-639072ec7448`

## [[jeffrey-oracle]]

Not affected. This is a self-hosted-runner Docker cleanup primitive specific to the macOS fleet.
