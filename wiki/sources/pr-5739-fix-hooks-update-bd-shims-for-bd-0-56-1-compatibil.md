---
title: "PR #5739: fix(hooks): update bd shims for bd 0.56.1 compatibility"
type: source
tags: []
date: 2026-02-23
source_file: raw/prs-worldarchitect-ai/pr-5739.md
sources: []
last_updated: 2026-02-23
---

## Summary
- 3 of 5 `.husky/_/` shims called `bd hook <name>` (bd 0.55.4 API)
- bd 0.56.1 renamed the command to `bd hooks run <name>`
- Self-hosted runner `claude-drift-runner` (Mac) has bd 0.56.1, causing git checkout to fail

## Metadata
- **PR**: #5739
- **Merged**: 2026-02-23
- **Author**: jleechan2015
- **Stats**: +6/-6 in 3 files
- **Labels**: none

## Connections
