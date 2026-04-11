---
title: "PR #1837: Improve CLI detection and fallback for Codex support"
type: source
tags: [codex]
date: 2025-10-07
source_file: raw/prs-worldarchitect-ai/pr-1837.md
sources: []
last_updated: 2025-10-07
---

## Summary
- centralize CLI detection keywords and auto-select an installed CLI when tasks lack explicit preferences
- ensure agent creation falls back to an available CLI when the requested binary is missing and quote command templates safely
- extend Codex CLI tests to cover auto-selection and fallback execution scenarios

## Metadata
- **PR**: #1837
- **Merged**: 2025-10-07
- **Author**: jleechan2015
- **Stats**: +406/-52 in 4 files
- **Labels**: codex

## Connections
