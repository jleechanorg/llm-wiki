---
title: "PR #5768: CI: centralize self-hosted selector"
type: source
tags: []
date: 2026-02-25
source_file: raw/prs-worldarchitect-ai/pr-5768.md
sources: []
last_updated: 2026-02-25
---

## Summary
- Centralize self-hosted runner selection across workflows via a single expression:
  - `runs-on: ${{ fromJson(vars.SELF_HOSTED_RUNNER_LABELS || '["self-hosted"]') }}`
- Keep fallback behavior unchanged (`ubuntu-latest` fallback jobs unchanged).
- Update self-hosted workflow docs to document the shared selector and optional repo variable.

## Metadata
- **PR**: #5768
- **Merged**: 2026-02-25
- **Author**: jleechan2015
- **Stats**: +19/-15 in 9 files
- **Labels**: none

## Connections
