---
title: "PR #367: [agento] fix(metadata-updater): env-strip regex, sed escaping, git detection refactor"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-367.md
sources: []
last_updated: 2026-04-04
---

## Summary
Fix three bugs in `.claude/metadata-updater.sh` (and sync fixes to embedded plugin copies):

1. **Env-stripping regex bug** — Old param expansion `${clean_command#*=* }` stripped from the first `=` to the last space, mangling embedded `=` values (e.g. `FOO=a=b gh pr create` → bare command became `b` instead of `b gh pr create`). Fixed with a proper regex capture group using `[^[:space:]]*` to allow embedded `=`.

2. **Simplified `escaped_value`** — Replaced two-parameter-expansion lines with a s

## Metadata
- **PR**: #367
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +26/-60 in 4 files
- **Labels**: none

## Connections
