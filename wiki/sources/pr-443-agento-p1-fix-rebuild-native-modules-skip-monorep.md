---
title: "PR #443: [agento] [P1] fix(rebuild-native-modules): skip monorepo container packages without entry point"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-443.md
sources: []
last_updated: 2026-03-30
---

## Summary
- Guard the require check in `rebuild-native-modules.sh` to skip packages without a `package.json`
- Fixes the infinite rebuild loop triggered by `@rolldown`, a monorepo container package that has platform-specific sub-packages but no root entry point

## Metadata
- **PR**: #443
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +28/-4 in 3 files
- **Labels**: none

## Connections
