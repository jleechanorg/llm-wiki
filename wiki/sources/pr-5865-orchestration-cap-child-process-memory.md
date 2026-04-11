---
title: "PR #5865: Orchestration: cap child process memory"
type: source
tags: []
date: 2026-03-06
source_file: raw/prs-worldarchitect-ai/pr-5865.md
sources: []
last_updated: 2026-03-06
---

## Summary
- add a shared child-process virtual memory cap constant for orchestration runner scripts
- wrap generated CLI executions with a `ulimit -v` guard before launching the actual child command
- add regression coverage to verify generated runner scripts include the memory cap wrapper

## Metadata
- **PR**: #5865
- **Merged**: 2026-03-06
- **Author**: jleechan2015
- **Stats**: +141/-2 in 3 files
- **Labels**: none

## Connections
