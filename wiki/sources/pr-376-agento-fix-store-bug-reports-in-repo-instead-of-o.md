---
title: "PR #376: [agento] fix: store bug reports in repo instead of ~/.openclaw/logs"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-376.md
sources: []
last_updated: 2026-03-24
---

## Summary
- Fix bug-hunt-daily.sh to write bug reports to bug_reports/ in the repo instead of ~/.openclaw/logs/bug_reports
- Bug reports were being written outside the git repo, making them invisible to issue #246

## Metadata
- **PR**: #376
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +20/-4 in 3 files
- **Labels**: none

## Connections
