---
title: "PR #43: fix(agent-base): add vitest, fix @jleechanorg scope imports in tests"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-43.md
sources: []
last_updated: 2026-03-21
---

## Summary
The agent-base plugin was missing a test script and vitest devDependency, and its test file had stale @composio/* import paths after the npm scope rename to @jleechanorg/*.

## Metadata
- **PR**: #43
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +305/-1 in 6 files
- **Labels**: none

## Connections
