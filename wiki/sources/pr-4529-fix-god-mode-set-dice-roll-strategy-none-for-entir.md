---
title: "PR #4529: fix(god-mode): set dice_roll_strategy=None for entire god mode flow"
type: source
tags: []
date: 2026-02-02
source_file: raw/prs-worldarchitect-ai/pr-4529.md
sources: []
last_updated: 2026-02-02
---

## Summary
**BUG:** God mode still allowed code execution/dice rolls because `dice_roll_strategy` was set at line 4150 based on model, but we only passed `None` to `build_system_instructions`. The local variable still had `code_execution` value.

**FIX:** Set `dice_roll_strategy = None` when `is_god_mode_command` is True, BEFORE any code that uses it for API calls or validation.

**Key themes:**
- God mode dice strategy regression fix
- TDD-driven fix with failing test first

## Metadata
- **PR**: #4529
- **Merged**: 2026-02-02
- **Author**: jleechan2015
- **Stats**: +149/-6 in 5 files
- **Labels**: none

## Connections
