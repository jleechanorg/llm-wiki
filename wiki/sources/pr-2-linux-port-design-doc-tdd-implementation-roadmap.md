---
title: "PR #2: Linux port: design doc + TDD implementation roadmap"
type: source
tags: []
date: 2026-03-09
source_file: raw/prs-/pr-2.md
sources: []
last_updated: 2026-03-09
---

## Summary
- Design doc and TDD roadmap for the Linux port (Rust + GTK4 MVP)
- cmux-core crate: all 6 modules with 90 passing tests (split_tree, split_nav, tab, workspace, notification, session)
- Session persistence: atomic XDG write with tempfile swap
- Docker validation gates per phase (Ubuntu 24.04)
- Socket steering docs for agent coordination

## Metadata
- **PR**: #2
- **Merged**: 2026-03-09
- **Author**: jleechan2015
- **Stats**: +1266/-0 in 6 files
- **Labels**: none

## Connections
