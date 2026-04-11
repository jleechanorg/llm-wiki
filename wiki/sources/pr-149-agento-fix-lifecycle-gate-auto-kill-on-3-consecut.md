---
title: "PR #149: [agento] fix(lifecycle): gate auto-kill on 3 consecutive SCM failures (bd-6jc)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-149.md
sources: []
last_updated: 2026-03-24
---

## Summary
When agentDead=true and SCM check throws, the catch block fell through and immediately returned killed, destroying worktrees on a single transient blip. Fix: require 3 consecutive SCM failures before auto-kill.

## Metadata
- **PR**: #149
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +81/-13 in 2 files
- **Labels**: none

## Connections
