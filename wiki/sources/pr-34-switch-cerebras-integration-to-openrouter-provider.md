---
title: "PR #34: Switch Cerebras integration to OpenRouter provider"
type: source
tags: [codex]
date: 2025-09-23
source_file: raw/prs-/pr-34.md
sources: []
last_updated: 2025-09-23
---

## Summary
- point the Cerebras configuration at the OpenRouter endpoint and update API key validation to the new sk-or- prefix
- ensure all Cerebras requests (Node and Python tooling) send the OpenRouter X-Title header and reference the aggregated base URL
- refresh scripts, docs, and tests to reflect the OpenRouter provider and updated example credentials

## Metadata
- **PR**: #34
- **Merged**: 2025-09-23
- **Author**: jleechan2015
- **Stats**: +43/-32 in 11 files
- **Labels**: codex

## Connections
