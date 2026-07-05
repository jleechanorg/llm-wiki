---
title: "SelfHostedOssLegacy"
type: entity
tags: [legacy, worldarchitect-ai, shell-script, runner, deletion-deferred]
date: 2026-07-05
---

## Definition

The shell-script-based self-hosted runner fleet that lives in
`jleechanorg/worldarchitect.ai/self-hosted-oss/`. Includes:

- `heal-runners.sh` — reconciliation entry point (with flock hardening from PR #8143)
- `mac-runner-health.sh`, `ubuntu-runner-health.sh` — health probes
- `runner-capacity-failover.sh` — hybrid failover to GitHub-hosted (PR #8142)
- `cache-integrity.sh` — runner cache validation
- `install.sh` — runtime-mirror installer to `~/.local/share/worldarchitect-runners/`

## Status

Slated for deletion per user direction on 2026-07-05: "we should delete all
hte self hosted oss code from this repo later lets /learn to remember this
and someone else will do it."

## Why it's still load-bearing

The worldarchitect.ai CI workflows pin to labels `self-hosted,self-hosted-mikey`
which the legacy scripts register. The new ezgha daemon adds `ezgha`, `Linux`/
`macOS`, `X64`/`ARM64` labels but also inherits the legacy labels (configurable).
Full deletion requires:

1. Audit all `.github/workflows/*.yml` for self-hosted-oss script deps
2. Update worldarchitect.ai CLAUDE.md to remove self-hosted-oss/ sections
3. Delete `self-hosted-oss/` directory
4. Update `.claude/skills/runner-health/` (most redundant with ezgha-doctor)
5. Update `runtime-mirror-sync` install paths

## References

- [[Project2026-07-05-ezgha-supersedes-self-hosted-oss]]
- [[EzGhaDaemon]]
