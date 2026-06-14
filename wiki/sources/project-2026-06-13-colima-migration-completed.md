---
title: "Colima migration completed for Mac self-hosted runners (2026-06-13)"
type: source
tags: [colima, docker-desktop, self-hosted-runners, launchd, migration, 2026-06-13]
date: 2026-06-13
source_file: raw/project_2026-06-13_colima_migration_completed.md
---

## Summary
Colima migration shipped in [PR #7540](https://github.com/jleechanorg/worldarchitect.ai/pull/7540) on 2026-06-13: Mac self-hosted runners moved from Docker Desktop to Colima. The migration included a Colima pre-flight check in `install.sh`, a committed plist template with `DOCKER_CONTEXT=colima` (fixes an hourly container restart loop), and a CLAUDE.md portability rule. Bare runner on Mac was investigated and **deferred** — the `self-hosted-mikey` label is shared by both `self-hosted-oss/` (Docker) and `self-hosted-bare/` (host OS), so preserving Colima keeps the Ubuntu job environment stable.

## Key Claims
- PR #7540 merged 2026-06-13T20:01:27Z (main b881388b4f); bead rev-bb7jm closed
- `self-hosted-oss/install.sh` now generates plist with `DOCKER_CONTEXT=colima` (fixes hourly restart loop)
- `self-hosted-oss/launchd/com.worldarchitect.org-runners.plist` is a new committed template with `@HOME@`/`@INSTALL_DIR@`/`@LOG_DIR@` placeholders
- CLAUDE.md gained a "Self-Hosted Runner Changes — must be in git and portable" section
- 6 runners (org-runner-mac-1..6) + hermes-qdrant all on Colima, 23+ min uptime at write time
- Bare runner on Mac verdict = **defer**; Colima preserves Ubuntu job environment
- Root cause of hourly restart: hardcoded `DOCKER_CONTEXT=desktop-linux` in plist triggered `StartInterval: 3600` launchd reconcile that used Docker Desktop context

## Key Quotes
> "The migration is verified complete. `DOCKER_CONTEXT=colima` is now hardcoded in the plist template, eliminating the hourly container restart loop caused by Docker Desktop context resolution."

> "Verdict: defer. Colima preserves Ubuntu job environment. Bare runner stays Linux-only."

## Files
- `/Users/jleechan/projects/worldarchitect.ai/self-hosted-oss/install.sh` (modified in PR; reverted on disk per system-reminder; PR branch version is canonical)
- `/Users/jleechan/projects/worldarchitect.ai/self-hosted-oss/launchd/com.worldarchitect.org-runners.plist` (new)
- `/Users/jleechan/projects/worldarchitect.ai/CLAUDE.md` (added section)
- `~/Library/LaunchAgents/com.worldarchitect.org-runners.plist` (installed, DOCKER_CONTEXT=colima)

## Connections
- [[Colima]] — runtime (Apple VZ, aarch64, /var/run/docker.sock → ~/.colima/default/docker.sock)
- [[DockerDesktop]] — superseded runtime
- [[self-hosted-oss]] — Docker+Ubuntu runner fleet
- [[self-hosted-bare]] — bare host-OS runner fleet (PR #7491, Linux-only)
- [[self-hosted-mikey-label-routing]] — label shared by OSS and bare; not an environment indicator
- [[LaunchdTemplateOrphanPrevention]] — committed plist template rule
- [[BeadRev-bb7jm]] — closed tracking bead
- [[ColimaMigrationPlan]] — research and friction-point analysis
