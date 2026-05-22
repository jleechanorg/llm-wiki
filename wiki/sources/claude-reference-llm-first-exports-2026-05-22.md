# .claude_reference/commands/ + LLM-first Export Guards

**Date**: 2026-05-22
**Type**: Best Practice / Feedback
**Bead**: rev-j5rvr
**PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/6998

## Summary

204 duplicate `.claude/commands/` files moved to `.claude_reference/commands/` via `git mv` (not deletion). Both `/localexportcommands` and `/exportcommands` updated to be LLM-first: Phase 0 assessment → dry-run summary → mandatory confirmation gate before any writes.

## Key Rules

1. Never delete project commands that might have reference value — `git mv` to `.claude_reference/commands/` instead.
2. Export commands must have: Phase 0 LLM analysis + dry-run output + explicit `"Proceed? yes/no"` before executing any rsync/copy.
3. `/exportcommands` also stages `.claude_reference/commands/` → `repo/.claude_reference/commands/` via `reference_commands` key in `dirs_mapping`.
