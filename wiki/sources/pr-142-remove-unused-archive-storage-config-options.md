---
title: "PR #142: Remove unused archive storage config options"
type: source
tags: []
date: 2025-12-25
source_file: raw/prs-/pr-142.md
sources: []
last_updated: 2025-12-25
---

## Summary
- Remove `project_key_storage_enabled` from StorageSettings
- Remove `local_archive_enabled` from StorageSettings
- Remove `project_key_prompt_enabled` from StorageSettings

These config options are no longer used since archive storage was removed. `is_archive_enabled()` now always returns `False`.

## Metadata
- **PR**: #142
- **Merged**: 2025-12-25
- **Author**: jleechan2015
- **Stats**: +2661/-784 in 51 files
- **Labels**: none

## Connections
