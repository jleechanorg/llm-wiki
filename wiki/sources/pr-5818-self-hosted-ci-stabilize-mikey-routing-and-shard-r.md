---
title: "PR #5818: Self-hosted CI: stabilize mikey routing and shard regressions"
type: source
tags: []
date: 2026-03-03
source_file: raw/prs-worldarchitect-ai/pr-5818.md
sources: []
last_updated: 2026-03-03
---

## Summary
- Stabilize self-hosted mikey runner routing with label fallback via `SELF_HOSTED_RUNNER_LABELS`
- Fix shard workflow checkout: SHA-pinned `actions/checkout`, deterministic ref, removed `persist-credentials: false` (caused auth-loss on retry)
- Start 2 isolated runner containers by default (`RUNNER_COUNT=2`) with per-container workdirs to prevent shared `_actions` corruption
- Set `EPHEMERAL=true` as default: persistent mode causes `tar` permission errors on macOS colima bind-mounts when re-extr

## Metadata
- **PR**: #5818
- **Merged**: 2026-03-03
- **Author**: jleechan2015
- **Stats**: +482/-873 in 33 files
- **Labels**: none

## Connections
