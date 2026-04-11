---
title: "PR #2472: Force OAuth auth by unsetting API keys in CLI agents"
type: source
tags: []
date: 2025-12-18
source_file: raw/prs-worldarchitect-ai/pr-2472.md
sources: []
last_updated: 2025-12-18
---

## Summary
- Add `env_unset` config to CLI_PROFILES to unset API keys before launching agents
- This forces CLIs to use OAuth authentication instead of API keys
- OAuth typically has higher rate limits (especially with Google AI Pro/Ultra subscriptions)

## Metadata
- **PR**: #2472
- **Merged**: 2025-12-18
- **Author**: jleechan2015
- **Stats**: +42/-0 in 2 files
- **Labels**: none

## Connections
