---
title: "PR #49: Mission Control: add feature-flagged cmux bridge dispatch"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-49.md
sources: []
last_updated: 2026-03-05
---

## Summary
- add `orchestration.cmux_bridge` with command wrappers for ping/list/send/read/new workspace/split/close
- integrate cmux path into task poller behind feature flag (default off)
- add docs/env examples for `CMUX_SOCKET_PATH` and `CMUX_SOCKET_PASSWORD`
- add TDD coverage for cmux bridge and task poller integration behavior

## Metadata
- **PR**: #49
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +0/-0 in 0 files
- **Labels**: none

## Connections
