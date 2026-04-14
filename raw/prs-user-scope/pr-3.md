# PR #3: fix: sync mode for Dropbox sessions/projects + scaffold dev scripts

**Repo:** jleechanorg/user_scope
**Merged:** 2026-03-07
**Author:** jleechan2015
**Stats:** +6945/-5 in 29 files

## Summary
- **Bug fix**: `scripts/backup-home.sh` — conversation session/project directories (`sessions/`, `archived_sessions/`, `projects/`) were using additive rsync mode (`--ignore-existing`), so files rewritten in-place were silently skipped on subsequent backup runs. Changed all Dropbox-only session entries to `sync_mode=sync`.
- **TDD regression test**: `test_sessions_updated_in_place_are_recopied_on_second_run` — real rsync round-trip that writes a file, modifies it, runs backup again, and asserts 

## Test Plan
- [x] `pytest tests/` — 30 passed
- [x] New test `test_sessions_updated_in_place_are_recopied_on_second_run` fails before fix, passes after

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Moderate risk: changes affect automated backup behavior (rsync modes) and add several new developer/automation scripts that can impact local workflows, but do not modify core application runtime code.
> 
> **Overview**
> Fixes home-conv

## Raw Body
## Summary

- **Bug fix**: `scripts/backup-home.sh` — conversation session/project directories (`sessions/`, `archived_sessions/`, `projects/`) were using additive rsync mode (`--ignore-existing`), so files rewritten in-place were silently skipped on subsequent backup runs. Changed all Dropbox-only session entries to `sync_mode=sync`.
- **TDD regression test**: `test_sessions_updated_in_place_are_recopied_on_second_run` — real rsync round-trip that writes a file, modifies it, runs backup again, and asserts the updated content is present.
- **Scaffold**: Copied standard dev scripts from `claude-commands` into repo root (`create_worktree.sh`, `integrate.sh`, `schedule_branch_work.sh`) and `scripts/` (`push.sh`, `run_lint.sh`, `run_tests_with_coverage.sh`, `coverage.sh`, `claude_mcp.sh`, etc.).

## Test plan

- [x] `pytest tests/` — 30 passed
- [x] New test `test_sessions_updated_in_place_are_recopied_on_second_run` fails before fix, passes after

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Moderate risk: changes affect automated backup behavior (rsync modes) and add several new developer/automation scripts that can impact local workflows, but do not modify core application runtime code.
> 
> **Overview**
> Fixes home-conversation backups so Dropbox `sessions/`, `archived_sessions/`, and `projects/` are copied in `sync` mode (not additive `--ignore-existing`), ensuring files updated in-place get recopied on subsequent runs; also expands the set of backed-up AI tooling/config files in `scripts/backup-home.sh`.
> 
> Adds in-repo Beads issue-tracking scaffolding (`.beads/` config, hooks shims, metadata, and ignore rules) and introduces several workflow helper scripts (worktree creation, main-branch integration/branch refresh, scheduled Claude resume) plus a large `scripts/claude_mcp.sh` installer/orchestrator for MCP server setup.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboar
