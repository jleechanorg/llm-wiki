---
title: "Cron env missing ACCESS_TOKEN — silent zombie recreation failures"
type: source
tags: [runners, cron, docker, ubuntu, jeff-ubuntu, self-hosted, anti-pattern]
date: 2026-06-21
source_file: raw/feedback_cron_env_access_token.md
bead: rev-p4l2f
---

## Summary

Scripts dispatched by cron lack `ACCESS_TOKEN` and other shell-profile env vars. When `monitor.sh` on jeff-ubuntu tried to recreate zombie GitHub Actions runner containers via `docker compose up --force-recreate`, it silently failed because `ACCESS_TOKEN="${ACCESS_TOKEN:-}"` expanded to empty string in cron's minimal environment. This caused 9/16 ubuntu runners to stay as permanently-offline zombies for multiple cron cycles.

## Key Claims

- Cron's minimal environment has no `ACCESS_TOKEN`, `ORG_NAME`, or `LABELS` — only bare `PATH`, `HOME`, and a few system vars
- `docker compose` treats env vars used via `${VAR}` substitution as required; empty string → fatal error "required variable X is missing a value"
- The companion script `start.sh` already sourced `~/.bashrc`, but `monitor.sh` did not inherit this pattern when `zombie_check` was added later
- Fix: conditional `source ~/.bashrc` block (with `set +u` guard) at the top of `monitor.sh`
- Test: `env -i HOME=$HOME PATH=/usr/bin:/bin bash monitor.sh` should exit clean

## Key Quotes

> "ACCESS_TOKEN is missing a value: export ACCESS_TOKEN in ~/.bashrc"

## Connections

- [[JeffUbuntuLimaVMRunners]] — the machine and stack this applies to
- [[CronMinimalEnv]] — pattern: cron env = `HOME`, `PATH`, no shell exports
- [[DockerComposeEnvSubstitution]] — compose treats `${VAR}` as required by default

## Rule

Any shell script invoked from cron or launchd that calls `docker compose` with variable substitution MUST have near the top:
```bash
if [[ -z "${ACCESS_TOKEN:-}" ]]; then
  set +u
  source "${HOME}/.bashrc" 2>/dev/null || true
  set -u
fi
```

## References

- PR [#7757](https://github.com/jleechanorg/worldarchitect.ai/pull/7757) — merged `57055943ef`, fix in `self-hosted-colima/scripts/monitor.sh:36-44`
- Memory: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_cron_env_access_token.md`
- Bead: `rev-p4l2f`
