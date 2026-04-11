---
title: "PR #4957: feat(automation): add --codex-update-api flag to pr-monitor"
type: source
tags: []
date: 2026-02-08
source_file: raw/prs-worldarchitect-ai/pr-4957.md
sources: []
last_updated: 2026-02-08
---

## Summary
- Adds `--codex-update-api` flag to `jleechanorg-pr-monitor` CLI
- Lists and inspects Codex cloud tasks via `codex cloud` CLI API (no browser, no Cloudflare)
- Depends on PR #4956 (CodexCloudAPI wrapper)

**Key themes:**
- Cloudflare bypass via official API
- New CLI flag alongside existing `--codex-update`

## Metadata
- **PR**: #4957
- **Merged**: 2026-02-08
- **Author**: jleechan2015
- **Stats**: +1359/-24 in 9 files
- **Labels**: none

## Connections
