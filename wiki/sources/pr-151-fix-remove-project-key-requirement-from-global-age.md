---
title: "PR #151: fix: Remove project_key requirement from global agent tools"
type: source
tags: []
date: 2025-12-29
source_file: raw/prs-/pr-151.md
sources: []
last_updated: 2025-12-29
---

## Summary
Fixes 5 critical violations where MCP tools claim `project_key` is "informational only" but actually require a valid project by calling `_get_project_by_identifier()`, which raises `NoResultFound` when the project doesn't exist.

This violates the documented global agent namespace design where agents are globally unique and should be accessible without project context.

## Metadata
- **PR**: #151
- **Merged**: 2025-12-29
- **Author**: jleechan2015
- **Stats**: +243/-105 in 10 files
- **Labels**: none

## Connections
