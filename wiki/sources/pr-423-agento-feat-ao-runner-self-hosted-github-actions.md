---
title: "PR #423: [agento] feat(ao-runner): self-hosted GitHub Actions runner PyPI package"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-423.md
sources: []
last_updated: 2026-03-28
---

## Summary
Extracts the Docker-based self-hosted runner setup from worldarchitect.ai into a reusable `ao-runner` PyPI package installable across all jleechanorg repos.

- `ao-runner install --repo owner/repo` — one-command setup with launchd auto-start
- `ao-runner status/start/stop/uninstall` — lifecycle management
- Config at `~/.config/ao-runner/`, logs at `~/Library/Logs/ao-runner/`
- Ephemeral Docker containers via `myoung34/github-runner:ubuntu-noble`

## Metadata
- **PR**: #423
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +2633/-32 in 22 files
- **Labels**: none

## Connections
