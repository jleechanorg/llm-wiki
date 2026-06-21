---
title: "jeff-ubuntu: Runner containers live inside Lima VM (colima), not host Docker"
type: source
tags: [runners, jeff-ubuntu, lima, colima, docker, infrastructure, reference]
date: 2026-06-21
source_file: raw/reference_jeff_ubuntu_docker_lima.md
bead: rev-p4l2f
---

## Summary

The GitHub Actions self-hosted runners on jeff-ubuntu run inside a Lima VM (colima), NOT directly on the host Docker. Running bare `docker ps` on jeff-ubuntu connects to the host Docker socket and shows wrong containers. All runner operations require the Lima VM docker context.

## Key Claims

- Runners are at `~/projects/worktree_runner/self-hosted-colima/` (NOT `self-hosted-oss/`)
- Lima VM docker socket: `unix:///home/jleechan/.lima/colima/sock/docker.sock`
- 16 EPHEMERAL runner services (`runner-1`…`runner-16`), containers `org-runner-1`…`org-runner-16`
- Monitor runs via `colima-runners.service` systemd + cron every 15 minutes
- Container overlay disk can fill from CI job artifacts (grew to 62GB before fix); force-recreate frees it
- EXPECTED_RUNNERS=10 was stale; compose defines 16 — bumped via PR #7757

## Key Claims — Docker context

```bash
# Wrong — host Docker:
docker ps

# Right — Lima VM:
DOCKER_HOST=unix:///home/jleechan/.lima/colima/sock/docker.sock docker ps
# Or:
docker --context lima-colima ps
```

## Connections

- [[CronMinimalEnv]] — monitor.sh needs bashrc source for ACCESS_TOKEN
- [[SelfHostedColima]] — the docker-compose stack managing the 16 runners
- [[JeffUbuntuSSH]] — SSH access: `ssh jeff-ubuntu`

## References

- PR [#7757](https://github.com/jleechanorg/worldarchitect.ai/pull/7757) — monitor.sh ACCESS_TOKEN fix + EXPECTED_RUNNERS=16
- Memory: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/reference_jeff_ubuntu_docker_lima.md`
- Bead: `rev-p4l2f`
