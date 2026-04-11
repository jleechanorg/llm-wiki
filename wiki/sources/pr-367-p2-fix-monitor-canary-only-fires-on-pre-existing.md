---
title: "PR #367: [P2] fix(monitor): canary only fires on pre-existing probe failures"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-367.md
sources: []
last_updated: 2026-03-23
---

## Summary
The monitor-e2e-canary Slack post fired on every monitor run, including healthy ones. This created noise in `#ai-slack-test` on every successful run, making it impossible to distinguish a deliberate failure-triggered canary from routine monitoring.

## Metadata
- **PR**: #367
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +10/-3 in 1 files
- **Labels**: none

## Connections
