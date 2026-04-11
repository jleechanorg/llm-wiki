---
title: "PR #44: feat(config): wire openclaw notifier plugin — ORCH-6ae"
type: source
tags: []
date: 2026-03-20
source_file: raw/prs-worldai_claw/pr-44.md
sources: []
last_updated: 2026-03-20
---

## Summary
ORCH-6ae: The notifier-openclaw plugin exists but was never wired into the canonical config example or tested as a config-to-plugin path. AO escalation events (agent-stuck, ci-failed) could not reach OpenClaw without manually editing the yaml.

## Metadata
- **PR**: #44
- **Merged**: 2026-03-20
- **Author**: jleechan2015
- **Stats**: +19/-5 in 1 files
- **Labels**: none

## Connections
