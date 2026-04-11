---
title: "PR #328: [P1] fix: delete retired test files, fix stuck threshold, fix dashboard"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-328.md
sources: []
last_updated: 2026-03-21
---

## Summary
After PR #323 retired 19 Python orchestration modules, 14 test files and 2 test classes were left behind — all failing on import. The agent-stuck threshold (10m) was too aggressive, causing jc-434 to be killed mid-green-loop on PR #326 before it could see CR approval. The AO dashboard plist was broken (wrong node path, dev mode crash).

## Metadata
- **PR**: #328
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +15/-5421 in 18 files
- **Labels**: none

## Connections
