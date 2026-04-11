---
title: "PR #5746: CI Reliability: Runner control plane + self-hosted bootstrap hardening"
type: source
tags: []
date: 2026-02-24
source_file: raw/prs-worldarchitect-ai/pr-5746.md
sources: []
last_updated: 2026-02-24
---

## Summary
- Hardened self-hosted runner control plane in `test.yml` for reliable infra-classification, retries, and health scoring.
- Added/extended writable tool-cache bootstrap coverage so `actions/setup-python` on constrained self-hosted runners uses writable directories instead of `/Users/runner`.
- Fixed preflight JSON parsing and interpreter selection to avoid infra-classify loss on hosts without a legacy `python` binary.
- Corrected runner health scoring for gated/skipped paths so quarantine/missin

## Metadata
- **PR**: #5746
- **Merged**: 2026-02-24
- **Author**: jleechan2015
- **Stats**: +1014/-106 in 17 files
- **Labels**: none

## Connections
