---
title: "JIT Registration Pattern"
type: concept
tags: [github-actions, registration, runner, ezgha]
date: 2026-07-05
---

## Definition

Instead of registering a long-lived runner with a registration token that
expires (typically 1 hour), the runner calls `gh api .../generate-jitconfig`
to mint a single-use JIT config. The runner registers itself, accepts ONE job,
deregisters, and exits. No token to manage, no expiry race.

## Failure mode this avoids

The classic self-hosted runner setup uses a registration token derived from
`gh api orgs/.../actions/runners/registration-token`, which has a 1-hour TTL.
If the container takes > 1 hour to start (slow docker pull, host under load),
the token expires before registration completes, and the daemon enters a
restart loop. The `AO per-repo runners stuck Restarting (1) with 404`
incident (memory 2026-06-28) was exactly this class.

## How ez-gh-actions does it

```rust
// src/github.rs:177
pub fn generate_jitconfig(...) -> Result<...>
```

Each `start_one()` calls `generate_jitconfig` for a fresh runner name, embeds
the encoded config in the container's `ACTIONS_RUNNER_INPUT_JITCONFIG` env,
and lets the upstream `actions/runner` binary do the rest. When the job
completes, the runner self-deregisters.

## Tradeoffs

- (+) No token expiry race.
- (+) No manual cleanup of stale registrations (the runner deregisters
  itself).
- (-) Requires `repo admin` or `org owner` scope on the token used by `gh`.
  Self-hosted runner setup needs that anyway.
- (-) One job per container: if you have 100 queued jobs, you need 100
  containers (or a queue).

## References

- [[Project2026-07-05-ezgha-supersedes-self-hosted-oss]]
- [[EzGhaDaemon]]
