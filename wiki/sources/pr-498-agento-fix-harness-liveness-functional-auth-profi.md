---
title: "PR #498: [agento] fix(harness): liveness≠functional — auth-profiles probe, deploy seeding, doctor STATE_DIR check"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldai_claw/pr-498.md
sources: []
last_updated: 2026-04-05
---

## Summary
Silent Slack failure (2026-04-04): OpenClaw bot stopped responding to Jeffrey's messages. Root cause: `auth-profiles.json` was missing from `~/.openclaw_prod/agents/main/agent/` (the prod state dir). HTTP `/health` returned `{"ok":true,"status":"live"}` throughout — every diagnostic check looked green while every LLM call silently failed with "No API key found for provider anthropic".

The plist had also been using `~/.openclaw-production/` (wrong dir) instead of `~/.openclaw_prod/` (the deploy.

## Metadata
- **PR**: #498
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +978/-2251 in 7 files
- **Labels**: none

## Connections
