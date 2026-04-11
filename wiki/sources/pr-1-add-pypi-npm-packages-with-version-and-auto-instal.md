---
title: "PR #1: Add PyPI/npm packages with --version and auto-install"
type: source
tags: []
date: 2026-02-12
source_file: raw/prs-/pr-1.md
sources: []
last_updated: 2026-02-12
---

## Summary
- Published `ai-usage-tracker` to both **PyPI** (v0.1.2) and **npm** (v0.1.2)
- Added `--version` / `-V` flag support to both Python and Node.js CLIs
- Added dependency auto-detection: when `ccusage` or `ccusage-codex` are missing, prompts to install them interactively instead of crashing
- Fixed npm package throwing ugly stack traces on missing dependencies — now shows clean error with install instructions
- Correct npm package name used: `@ccusage/codex` (not `ccusage-codex`)
- Updated README

## Metadata
- **PR**: #1
- **Merged**: 2026-02-12
- **Author**: jleechan2015
- **Stats**: +945/-181 in 13 files
- **Labels**: none

## Connections
