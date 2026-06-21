---
name: reference-jeff-ubuntu-docker-lima
description: "jeff-ubuntu runner containers live inside a Lima VM, not the host Docker — always use lima-colima context"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1b83ecc8-6dc7-4dc3-9c53-0197133eccce
---

# jeff-ubuntu: Runner containers are inside a Lima VM

The GitHub Actions self-hosted runners on jeff-ubuntu run inside a **Lima VM** (colima), NOT directly on the host Docker.

## Critical: always use the Lima VM Docker context

```bash
# Wrong — queries host Docker (/var/run/docker.sock), wrong containers:
ssh jeff-ubuntu 'docker ps'

# Right — queries Lima VM Docker:
ssh jeff-ubuntu 'DOCKER_HOST=unix:///home/jleechan/.lima/colima/sock/docker.sock docker ps'

# Or use context name:
ssh jeff-ubuntu 'docker --context lima-colima ps'
```

## Key paths on jeff-ubuntu

| Resource | Path |
|---|---|
| Lima VM socket | `~/.lima/colima/sock/docker.sock` |
| Compose file | `~/projects/worktree_runner/self-hosted-colima/docker-compose.yml` |
| Monitor script | `~/projects/worktree_runner/self-hosted-colima/scripts/monitor.sh` |
| Start script | `~/projects/worktree_runner/self-hosted-colima/scripts/start.sh` |
| Monitor log | `~/.worldarchitect-runner/work/monitor.log` |
| Systemd unit | `colima-runners.service` (user-mode) |
| Cron | `*/15 * * * *` runs `monitor.sh` |

## Runner topology

- **16 runner services** defined in docker-compose.yml (`runner-1` … `runner-16`)
- Container names: `org-runner-1` … `org-runner-16` (inside Lima VM)
- `EPHEMERAL=true` — each container de-registers after one job, then Docker restarts it
- `restart: unless-stopped` — container auto-restarts after ephemeral exit
- Lima VM disk can fill from job artifacts; monitor alerts at 80% and prunes

## Common docker commands (run on jeff-ubuntu)

```bash
# Check all runner containers:
DOCKER_HOST=unix:///home/jleechan/.lima/colima/sock/docker.sock docker ps -a | grep org-runner

# Force-recreate all (frees disk + re-registers all runners):
source ~/.bashrc
export PATH="$HOME/.local/bin:/usr/lib/go-1.23/bin:$PATH"
cd ~/projects/worktree_runner/self-hosted-colima
limactl shell colima -- env ORG_NAME="$ORG_NAME" RUNNER_NAME_PREFIX="${RUNNER_NAME_PREFIX:-org-runner}" LABELS="$LABELS" ACCESS_TOKEN="$ACCESS_TOKEN" docker compose -f docker-compose.yml -p jleechanorg-colima-runners up -d --force-recreate

# Disk usage inside Lima VM:
DOCKER_HOST=unix:///home/jleechan/.lima/colima/sock/docker.sock docker system df
```

## monitor.sh cron requirements

`monitor.sh` must have `ACCESS_TOKEN` to recreate zombie containers via `docker compose`.
It sources `~/.bashrc` at the top — if that ever stops working, zombie recreation will silently fail
with `ACCESS_TOKEN is missing a value`. Check `~/.worldarchitect-runner/work/monitor.log` for FAILED lines.

**Why:** Discovered 2026-06-21: 9/16 runners were zombies (completed jobs, de-registered, containers stuck).
monitor.sh had `ACCESS_TOKEN="${ACCESS_TOKEN:-}"` (empty from cron), so recreations silently failed.
Fix: added `source ~/.bashrc` to monitor.sh; bumped `EXPECTED_RUNNERS` 10→16.
