---
title: "PR #64: [agento][bd-awq] feat: poll GitHub PRs by CodeRabbit changes-requested"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-64.md
sources: []
last_updated: 2026-03-21
---

## Summary
- update `poller-github-pr` to target only PRs whose latest decisive CodeRabbit review is `CHANGES_REQUESTED`
- keep CI signal in metadata/priority (`ci-failing` -> higher priority)
- include `latestReviews` in `gh pr list` query and derive CodeRabbit state from reviewer login `coderabbitai[bot]`
- rely on poller-manager for active-session dedupe and respawn-cap enforcement (configure `respawnCap: { max: 3, window: "12h" }`)

## Metadata
- **PR**: #64
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +106/-247 in 2 files
- **Labels**: none

## Connections
