---
title: "PR #204: fix(doctor): correct non-canonical lifecycle-worker detection"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-204.md
sources: []
last_updated: 2026-03-26
---

## Summary
Fixes two bugs in `ao doctor` lifecycle-worker detection in `packages/cli/scripts/ao-doctor.sh`:

1. **Field index bug**: `\$11` was used to extract the binary path, but for `node /path/ao lifecycle-worker` the command path is at `$12` (since `$11` = `/path/ao`). Changed to iterate fields and find the one matching `/ao$` (the binary path).

2. **Grep pattern too broad**: `grep 'lifecycle-worker'` matched file names like `ao-lifecycle-triage.md` in truncated `ps aux` output. Changed to require tr

## Metadata
- **PR**: #204
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +11/-8 in 2 files
- **Labels**: none

## Connections
