---
title: "PR #36: fix(doctor): support renamed ao package in runtime sanity check"
type: source
tags: []
date: 2026-03-20
source_file: raw/prs-worldai_claw/pr-36.md
sources: []
last_updated: 2026-03-20
---

## Summary
The ao package was renamed from packages/agent-orchestrator to packages/ao, but ao-doctor.sh check_runtime_sanity() still hardcoded the old path. This caused ao doctor to always report launcher entrypoint is missing, which cascaded into the health monitor reporting false RED status.

## Metadata
- **PR**: #36
- **Merged**: 2026-03-20
- **Author**: jleechan2015
- **Stats**: +22/-2 in 2 files
- **Labels**: none

## Connections
