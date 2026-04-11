---
title: "PR #374: [agento] fix(metadata-updater): use BASH_REMATCH[2] not [1] in env-strip regex"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-374.md
sources: []
last_updated: 2026-04-04
---

## Summary
- Adds 11 integration tests covering env-prefix stripping when the env value contains embedded `=` characters (e.g. `FOO=a=b gh pr create`).
- These cases were raised by all 5 reviewers in the prior commit attempt and are now covered.
- The script itself is unchanged from origin/main.

## Metadata
- **PR**: #374
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +58/-0 in 1 files
- **Labels**: none

## Connections
