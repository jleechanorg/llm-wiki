---
title: "PR #52: fix: resolve pre-existing test failures + update stale doc constants"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-52.md
sources: []
last_updated: 2026-03-05
---

## Summary
- Fix `db_path.test.ts` — used cwd with legacy `worldai_claw.db` file, triggering fallback path. Now uses clean temp dirs for proper cwd-independence testing.
- Update `docs/design-react-native-ai-integration.md` — unified `EMBER_ALPHA_MULTIPLIER_WEB/MOBILE` → `EMBER_ALPHA_MULTIPLIER` (and star equivalent) to match PR #51 changes.
- Note: `npm rebuild better-sqlite3` required locally for Node version mismatch (not a code change).

## Metadata
- **PR**: #52
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +24/-12 in 3 files
- **Labels**: none

## Connections
