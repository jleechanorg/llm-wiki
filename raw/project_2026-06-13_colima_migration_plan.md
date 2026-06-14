---
name: colima-migration-plan-2026-06-13
description: "Colima migration research for Mac self-hosted runners: 2 friction points (socket symlink + launchd), 5 benefits, bead rev-bb7jm, steps verified against codebase"
metadata: 
  node_type: memory
  type: project
  originSessionId: 73be4e82-d635-4fd2-96b7-639072ec7448
---

# Colima Migration Plan — Mac Self-Hosted Runners (2026-06-13)

**Bead:** rev-bb7jm — "Migrate self-hosted Mac runners from Docker Desktop to Colima"
**Nextsteps doc:** `~/roadmap/nextsteps-2026-06-13-colima-migration.md`

## How Docker is used in this project (verified from codebase)

1. `self-hosted-oss/start-runner.sh` — `docker pull`, `docker run --name org-runner-mac-N`, `docker ps -a`, `docker rm -f` lifecycle loop
2. `self-hosted-oss/docker-compose.yml` — runs `myoung34/github-runner:ubuntu-noble` containers
3. `self-hosted-oss/docker-compose.docker-sock.yml` — mounts `/var/run/docker.sock:/var/run/docker.sock` into runner containers
4. `self-hosted-oss/defaults.sh` — `docker_rm_force_with_timeout()` polls `docker ps -a` after rm (macOS race condition fix)
5. App build (`mvp_site/Dockerfile`) + deploy — done via Cloud Build (remote, NOT local Docker)

## Friction points

**FRICTION 1 — `/var/run/docker.sock` hardcoded (HIGH, easy)**
- Colima socket is at `~/.colima/default/docker.sock`
- Fix: `sudo ln -sf ~/.colima/default/docker.sock /var/run/docker.sock`
- Eliminates need to change any script or compose file

**FRICTION 2 — launchd startup ordering (MEDIUM)**
- Docker Desktop auto-starts on login; runners plist assumes Docker available
- Fix: `brew services start colima` installs Colima as launchd service
- Optionally add `colima start || true` at top of `start-runner.sh` as belt-and-suspenders

## Benefits

1. No Docker Desktop commercial license (MIT-licensed Colima)
2. ~1-2GB less RAM per Mac host (Apple VZ backend vs Docker Desktop VM)
3. No menubar GUI process (~150-300MB overhead)
4. `brew services start colima` = proper launchd service, no manual restarts
5. Faster container finalization → `docker_rm_force_with_timeout` race condition less likely
6. Closes beads rev-y31a (Docker Desktop GUI quit) and rev-b69i (runner interruption)

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

**Why:** [rev-bb7jm] User approved Colima migration direction on 2026-06-13. Two friction points are both one-liners.

**How to apply:** When making any changes to `self-hosted-oss/` or the runner launchd plist, assume Colima (not Docker Desktop) as the target runtime. Verify the `/var/run/docker.sock` symlink exists before debugging runner socket issues.
