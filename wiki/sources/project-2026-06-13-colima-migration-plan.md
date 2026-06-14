---
title: "Colima migration plan for Mac self-hosted runners (2026-06-13)"
type: source
tags: [colima, docker-desktop, self-hosted-runners, planning, 2026-06-13]
date: 2026-06-13
source_file: raw/project_2026-06-13_colima_migration_plan.md
---

## Summary
Research and plan for migrating jleechanorg's Mac self-hosted runners from Docker Desktop to Colima. Two friction points identified (both one-liners): `/var/run/docker.sock` hardcoded symlink + launchd startup ordering. Five benefits noted (no Docker Desktop commercial license, ~1-2GB less RAM per host, no menubar GUI overhead, proper launchd service via `brew services start colima`, faster container finalization). Plan verified against codebase before execution; bead rev-bb7jm.

## Key Claims
- Two friction points: (1) `/var/run/docker.sock` hardcoded (HIGH, easy) — fix with `sudo ln -sf ~/.colima/default/docker.sock /var/run/docker.sock`; (2) launchd startup ordering (MEDIUM) — fix with `brew services start colima`
- Five benefits: no Docker Desktop commercial license, ~1-2GB less RAM per Mac, no menubar GUI process (~150-300MB overhead), proper launchd service, faster container finalization
- Closes beads rev-y31a (Docker Desktop GUI quit) and rev-b69i (runner interruption)
- Docker usage verified from codebase: `start-runner.sh` (docker pull/run/ps/rm), `docker-compose.yml` (myoung34/github-runner:ubuntu-noble), `docker-compose.docker-sock.yml` (mounts /var/run/docker.sock), `defaults.sh` (`docker_rm_force_with_timeout` race fix)
- App build (`mvp_site/Dockerfile`) + deploy done via Cloud Build, NOT local Docker

## Key Quotes
> "Two friction points are both one-liners."

> "App build (`mvp_site/Dockerfile`) + deploy — done via Cloud Build (remote, NOT local Docker)"

## Migration steps
```bash
# On each Mac runner host:
brew install colima docker docker-compose
colima start --cpu 4 --memory 8 --vm-type vz --arch aarch64
sudo ln -sf ~/.colima/default/docker.sock /var/run/docker.sock
brew services start colima

# Test one slot
RUNNER_COUNT=1 ./start-runner.sh
# Watch one CI job complete, then flip all 6
```

## Connections
- [[Colima]] — target runtime
- [[ColimaMigrationCompleted]] — execution result (PR #7540)
- [[BeadRev-bb7jm]] — closed tracking bead
- [[BeadRev-y31a]] — Docker Desktop GUI quit (closed by migration)
- [[BeadRev-b69i]] — runner interruption (closed by migration)
- [[myoung34-github-runner]] — base image (`ubuntu-noble`)
- [[CloudBuild]] — remote build/deploy, not local Docker
