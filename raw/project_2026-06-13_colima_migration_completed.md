---
name: colima-migration-completed-2026-06-13
description: "Colima migration shipped: PR #7540 merged (planned; awaits merge), 6 runners + qdrant running on Colima socket, install.sh+plist+CLAUDE.md portability rule, bare-runner-on-Mac verdict=defer"
metadata:
  type: project
  originSessionId: 73be4e82-d635-4fd2-96b7-639072ec7448
---

# Colima Migration Completed — Mac Self-Hosted Runners (2026-06-13)

**PR:** [#7540](https://github.com/jleechanorg/worldarchitect.ai/pull/7540) — feat(runners): migrate Mac self-hosted runners from Docker Desktop to Colima — **MERGED 2026-06-13T20:01:27Z** (main b881388b4f)
**Bead:** rev-bb7jm (closed)
**Branch:** feat-colima-bare-runner-migration (HEAD 948b822e7369dcfff1d96a9ab16f086435ec7a17)

## What shipped

1. **`self-hosted-oss/install.sh`** — Colima pre-flight check (install, running, brew services registered, /var/run/docker.sock symlink target). Generates plist with `DOCKER_CONTEXT=colima` instead of `desktop-linux`.
2. **`self-hosted-oss/launchd/com.worldarchitect.org-runners.plist`** (new) — committed plist template with `@HOME@`/`@INSTALL_DIR@`/`@LOG_DIR@` placeholders.
3. **`CLAUDE.md`** — new "Self-Hosted Runner Changes — must be in git and portable" section. Portability test: fresh Mac + `bash install.sh` = identical working setup.

## Live state verified

- Colima running, Apple VZ, aarch64, /var/run/docker.sock → ~/.colima/default/docker.sock
- 6 runners (org-runner-mac-1..6) + hermes-qdrant all on Colima, 23+ min uptime
- Installed plist confirmed: `DOCKER_CONTEXT=colima`

## Key fix: hourly container restart loop

Root cause: `install.sh` generated plist with `DOCKER_CONTEXT=desktop-linux` hardcoded. `StartInterval: 3600` triggered launchd reconcile which used Docker Desktop context to start `myoung34/github-runner` containers — restarting them every hour. Fix: hardcode `DOCKER_CONTEXT=colima` in generated plist.

## Bare runner on Mac: investigated, deferred

- `actions-runner-osx-arm64-2.335.1.tar.gz` exists
- `self-hosted-bare/` (PR #7491, merged to `dev1779445480`) eliminates Docker for Linux CI
- On Mac, bare runner would run CI jobs on macOS ARM64 directly — breaks Ubuntu workflows that rely on `myoung34/github-runner:ubuntu-noble` container image
- Confusing: `self-hosted-mikey` label is used by BOTH `self-hosted-oss/` (Docker-based) and `self-hosted-bare/` (no Docker) — label is just a routing tag, not an environment indicator
- **Verdict: defer.** Colima preserves Ubuntu job environment. Bare runner stays Linux-only.

## Files

- `/Users/jleechan/projects/worldarchitect.ai/self-hosted-oss/install.sh` (modified in PR, reverted on disk per system-reminder; PR branch version is canonical)
- `/Users/jleechan/projects/worldarchitect.ai/self-hosted-oss/launchd/com.worldarchitect.org-runners.plist` (new)
- `/Users/jleechan/projects/worldarchitect.ai/CLAUDE.md` (added section)
- `~/Library/LaunchAgents/com.worldarchitect.org-runners.plist` (installed, DOCKER_CONTEXT=colima)
- `~/roadmap/nextsteps-2026-06-13-colima-migration.md`

## Why

User asked to migrate Mac self-hosted runners from Docker Desktop to Colima after researching Docker usage patterns. Implemented the migration with the constraint that all plist work must be in git and machine-portable.

## How to apply

When working on self-hosted runners: assume Colima is the target runtime. Verify `/var/run/docker.sock` → `~/.colima/default/docker.sock` symlink before debugging socket issues. Re-run `install.sh` after pulling — it regenerates the plist from the template. For any new launchd agent, commit a plist template to `self-hosted-oss/launchd/` first.
