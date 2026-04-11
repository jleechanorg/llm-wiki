---
title: "PR #281: fix: prevent claude wrapper from masking failures"
type: source
tags: [codex]
date: 2025-10-14
source_file: raw/prs-/pr-281.md
sources: []
last_updated: 2025-10-14
---

## Summary
- ensure the Claude CLI Docker wrapper forces CI_SIMULATION to false by default
- allow callers to explicitly re-enable simulation mode via the CI_SIMULATION environment variable
- configure the Codex git setup script to embed the PAT using the x-access-token username so git pull works without prompting

## Metadata
- **PR**: #281
- **Merged**: 2025-10-14
- **Author**: jleechan2015
- **Stats**: +67/-8 in 1 files
- **Labels**: codex

## Connections
