---
title: "PR #5756: ci: extend self-hosted runner control-plane to coverage workflow"
type: source
tags: []
date: 2026-02-26
source_file: raw/prs-worldarchitect-ai/pr-5756.md
sources: []
last_updated: 2026-02-26
---

## Summary
- harden `.github/workflows/coverage.yml` with self-hosted runner control-plane primitives
- remove `venv` restore from `actions/cache` and force deterministic fresh virtualenv bootstrap
- add runner preflight + quarantine gate + health score update and artifact export
- update `docs/ci/runner-hosting-strategy.md` status/implementation notes
- record bead tracking update in `.beads/issues.jsonl`

## Metadata
- **PR**: #5756
- **Merged**: 2026-02-26
- **Author**: jleechan2015
- **Stats**: +238/-25 in 12 files
- **Labels**: none

## Connections
