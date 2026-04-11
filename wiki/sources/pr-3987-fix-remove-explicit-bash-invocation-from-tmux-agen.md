---
title: "PR #3987: fix: Remove explicit bash invocation from tmux agent spawn"
type: source
tags: []
date: 2026-01-24
source_file: raw/prs-worldarchitect-ai/pr-3987.md
sources: []
last_updated: 2026-01-24
---

## Summary
Fixes recurring macOS permission dialog by removing explicit "bash" from tmux new-session commands. Agent scripts now execute directly via their shebang (`#!/usr/bin/env bash`), avoiding macOS security prompts for bash to "access data from other apps."

## Metadata
- **PR**: #3987
- **Merged**: 2026-01-24
- **Author**: jleechan2015
- **Stats**: +180/-3 in 3 files
- **Labels**: none

## Connections
