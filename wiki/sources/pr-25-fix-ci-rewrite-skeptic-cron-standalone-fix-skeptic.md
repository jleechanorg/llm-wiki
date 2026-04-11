---
title: "PR #25: fix(ci): rewrite skeptic-cron standalone + fix skeptic-gate polling"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-25.md
sources: []
last_updated: 2026-03-29
---

## Summary
Skeptic workflows were broken in two ways:
1. **skeptic-cron.yml** referenced `.github/actions/skeptic-setup` (doesn't exist in this repo) and `packages/cli/dist/index.js` (agent-orchestrator CLI, not present here) — causing every run to fail with "Can't find action.yml under .github/actions/skeptic-setup"
2. **skeptic-gate.yml** used `--slurpfile /dev/null` which is an invalid `gh api` flag, causing immediate API failure and rapid exit. Also polled for verdicts from `jleechan2015` but cron post

## Metadata
- **PR**: #25
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +106/-208 in 2 files
- **Labels**: none

## Connections
