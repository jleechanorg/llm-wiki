---
title: "PR #62: fix: tighten CodeRabbit ping policy — push-triggered only, no timer"
type: source
tags: []
date: 2026-03-07
source_file: raw/prs-worldai_claw/pr-62.md
sources: []
last_updated: 2026-03-07
---

## Summary
- Removed blind 10-minute cron (`pr-review-watchdog.sh`) that was pinging `@coderabbit-ai review` on every open non-approved PR unconditionally
- Clarified CodeRabbit Review Protocol in `CLAUDE.md` and `AGENTS.md`: only trigger after a fresh push lands on the PR branch

## Metadata
- **PR**: #62
- **Merged**: 2026-03-07
- **Author**: jleechan2015
- **Stats**: +4/-0 in 2 files
- **Labels**: none

## Connections
