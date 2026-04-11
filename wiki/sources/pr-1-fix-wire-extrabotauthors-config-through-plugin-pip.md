---
title: "PR #1: fix: wire extraBotAuthors config through plugin pipeline"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-1.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Add plugins top-level field to OrchestratorConfig for plugin-specific settings
- Extend extractPluginConfig() in plugin-registry.ts to handle SCM slot
- Fix getSCM() in plugins.ts to pass config to plugin.create()
- Add unit tests covering extraBotAuthors config in scm-github plugin

## Metadata
- **PR**: #1
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +135/-2 in 5 files
- **Labels**: none

## Connections
