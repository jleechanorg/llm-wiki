---
title: "PR #1: feat: GTK4 Linux port phases 1-7 complete — split panes, notifications, session restore"
type: source
tags: []
date: 2026-03-09
source_file: raw/prs-/pr-1.md
sources: []
last_updated: 2026-03-09
---

## Summary
Complete GTK4 Linux port of cmux through all 7 phases, with real UI evidence (Docker + Xvfb + scrot screenshots) reviewed by both supervisor and cmux_coder before each phase gate.

### Phase Evidence (all screenshots at 1280×800 RGB, Ubuntu 24.04 + Xvfb)

| Phase | Feature | Evidence | Tests |
|-------|---------|---------|-------|
| 1 | TDD setup + cmux-core data model | Baseline | 94 passing |
| 2 | Session persistence (XDG atomic save/load) | macOS PR screenshot | 94 passing |
| 3 | GTK4 sideb

## Metadata
- **PR**: #1
- **Merged**: 2026-03-09
- **Author**: jleechan2015
- **Stats**: +10284/-0 in 54 files
- **Labels**: none

## Connections
