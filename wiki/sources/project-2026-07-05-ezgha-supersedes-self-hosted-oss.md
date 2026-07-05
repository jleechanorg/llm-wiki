---
title: "ez-gh-actions supersedes worldarchitect.ai self-hosted-oss/* (2026-07-05)"
type: source
tags: [ez-gh-actions, runner-migration, jit-registration, vm-within-vm, jleechanorg, deletion-deferred]
date: 2026-07-05
source_file: raw/project_2026-07-05_ezgha_supersedes_self_hosted_oss.md
---

## Summary

`jleechanorg/ez-gh-actions` (Rust ezgha daemon with JIT registration and VM-within-VM isolation) is the new sole GitHub Actions runner. The legacy `worldarchitect.ai/self-hosted-oss/*` shell-script fleet is slated for deletion. As of 2026-07-05 the Mac fleet is producing `ez-mac-runner-b-*` (5-6 active) and the Linux fleet on jeff-ubuntu is producing `ez-org-runner-*` + `ez-runner-b-*` (15 active). Both are handling real `jleechanorg/worldarchitect.ai` jobs.

## Key Claims

- ezgha daemon supersedes self-hosted-oss/* because it has daemon-managed reconcile (vs. cron-managed), JIT registration (no RUNNER_TOKEN expiry), VM-within-VM isolation (vs. process isolation), and a single source of truth for slot state
- Deletion is deferred ("someone else will do it later") per explicit user direction on 2026-07-05
- The legacy runner-health skill in worldarchitect.ai (PR #8140, 2026-07-03) is partially redundant with the new `ezgha-doctor` skill that ships in ez-gh-actions

## Key Quotes

> "note that ez gh actiosn runner repo is the new sole gh actions and we should delete all hte self hosted oss code from this repo later lets /learn to remember this and someone else will do it"

## Connections

- [[EzGhaDaemon]] — the new Rust daemon
- [[JeffUbuntu]] — Linux fleet host (15 ezgha runners active)
- [[MacColimaVm]] — Mac fleet host (5-6 ezgha runners active)
- [[JitRegistrationPattern]] — the auth-flow that avoids RUNNER_TOKEN expiry
- [[VmWithinVmIsolation]] — the architectural pattern ezgha uses
- [[SelfHostedOssLegacy]] — the scripts slated for deletion
- [[RunnerHealthSkill]] — partially redundant with ezgha-doctor