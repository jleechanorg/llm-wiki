---
title: "PR #1632: refactor: consolidate CRDT validation harness"
type: source
tags: [codex]
date: 2025-09-19
source_file: raw/prs-worldarchitect-ai/pr-1632.md
sources: []
last_updated: 2025-09-19
---

## Summary
- move the CRDT validation harness under `scripts/tests/` so it can be executed with `python -m scripts.tests.crdt_validation` and referenced from tooling docs
- add a pytest wrapper that exercises each scenario group and skips cleanly when the optional `memory_backup_crdt` module is unavailable
- refresh CRDT documentation and maintenance scripts to point at the new consolidated entry point

## Metadata
- **PR**: #1632
- **Merged**: 2025-09-19
- **Author**: jleechan2015
- **Stats**: +660/-2956 in 14 files
- **Labels**: codex

## Connections
