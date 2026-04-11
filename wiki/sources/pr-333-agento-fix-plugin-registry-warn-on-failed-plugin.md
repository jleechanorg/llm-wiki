---
title: "PR #333: [agento] fix(plugin-registry): warn on failed plugin loads + add monorepo-relative fallback"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-333.md
sources: []
last_updated: 2026-04-03
---

## Summary
- `loadBuiltins()` now logs a warning when a builtin plugin import fails (no longer silently swallows `ERR_MODULE_NOT_FOUND`)
- Adds `tryMonorepoFallback()` that resolves `@jleechanorg/ao-plugin-*` packages via a path relative to the CLI binary location (`packages/plugins/<name>/dist/index.js`)
- `loadBuiltins()` accepts an optional `fallbackImportFn` parameter for testability
- Replaces the "silently skips unavailable packages" test with 4 new TDD tests

## Metadata
- **PR**: #333
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +322/-55 in 5 files
- **Labels**: none

## Connections
