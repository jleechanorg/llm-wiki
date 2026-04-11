---
title: "PR #5686: fix(integrate): harden against SIGPIPE exits and beads daemon hook failures"
type: source
tags: []
date: 2026-02-21
source_file: raw/prs-worldarchitect-ai/pr-5686.md
sources: []
last_updated: 2026-02-21
---

## Summary
- Fix `integrate.sh` crashing under `set -euo pipefail` when `git log/diff | head` pipelines emit SIGPIPE (exit 141)
- Bypass Husky hooks for scripted branch checkouts to prevent beads daemon failures from blocking integration
- Skip O(n) squash-merge scan in FORCE_MODE for large histories (>1000 commits)
- Add `.claude/skills/beads-issue-tracking.md` with beads usage guide and DB recovery instructions

## Metadata
- **PR**: #5686
- **Merged**: 2026-02-21
- **Author**: jleechan2015
- **Stats**: +118/-14 in 2 files
- **Labels**: none

## Connections
