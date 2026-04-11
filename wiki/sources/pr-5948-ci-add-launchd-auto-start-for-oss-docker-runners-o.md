---
title: "PR #5948: ci: add launchd auto-start for OSS Docker runners on macOS"
type: source
tags: []
date: 2026-03-13
source_file: raw/prs-worldarchitect-ai/pr-5948.md
sources: []
last_updated: 2026-03-13
---

## Summary
- Add `self-hosted-oss/install.sh` — installs a launchd agent that auto-starts runners after Mac reboot
- Add `self-hosted-oss/launchd-start.sh` — wrapper that waits up to 150s for Docker, then runs `start-runner.sh`
- Remove old bare-metal runner plists (handled separately on the machine)

## Metadata
- **PR**: #5948
- **Merged**: 2026-03-13
- **Author**: jleechan2015
- **Stats**: +73/-0 in 2 files
- **Labels**: none

## Connections
