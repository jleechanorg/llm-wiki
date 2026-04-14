# PR #1: feat: Add functional integration tests for real Claude/Cursor agents

**Repo:** jleechanorg/bp-telemetry-core-fork
**Merged:** 2025-12-17
**Author:** jleechan2015
**Stats:** +1078/-0 in 10 files

## Summary
- Added real CLI integration tests that invoke actual Claude and Cursor CLIs
- Refactored test harness with Template Method pattern - child classes only define CLI config
- Tests verify full telemetry pipeline: CLI → Redis → SQLite

## Test Plan
- [x] Claude test passes with real CLI invocation
- [x] Cursor test correctly detects missing telemetry (expected behavior)
- [x] Template Method pattern prevents passive tests from passing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> Adds real CLI integration tests (Claude/Cursor), fixes an uninitialized iteration variable in the Claude consumer, and updates docs/deps.
> 
> - **Tests (integration)**:
>   - Add real CLI-based harness a

## Raw Body
## Summary

- Added real CLI integration tests that invoke actual Claude and Cursor CLIs
- Refactored test harness with Template Method pattern - child classes only define CLI config
- Tests verify full telemetry pipeline: CLI → Redis → SQLite

## Test Architecture

```
BaseTelemetryTest (parent)
├── All execution logic (run_all_tests, run_cli, check_cli, etc.)
├── Server lifecycle management
└── Event validation

ClaudeTelemetryTest (child - 36 lines)
├── CLI_COMMAND = ["claude"]
├── CLI_ARGS = ["-p", "--dangerously-skip-permissions"]
└── TABLE = "claude_raw_traces"

CursorTelemetryTest (child - 36 lines)
├── CLI_COMMAND = ["cursor-agent"]
├── CLI_ARGS = ["-p", "-f"]
└── TABLE = "cursor_raw_traces"
```

## Test Results

| Test | Status | Notes |
|------|--------|-------|
| Claude CLI | ✅ PASS | Full pipeline verified |
| Cursor CLI | ❌ EXPECTED FAIL | See limitation below |

## Known Limitation: Cursor CLI Test

**The Cursor test will intentionally fail** because:

- **Cursor IDE** writes to: `~/Library/Application Support/Cursor/User/.../state.vscdb` ✅ (monitored)
- **cursor-agent CLI** writes to: `~/.cursor/chats/{hash}/{uuid}/store.db` ❌ (not monitored)

To make Cursor CLI test pass, we would need to add a monitor for `~/.cursor/chats/*/store.db`.

**Cursor IDE telemetry works correctly** - only the CLI is not captured.

## Files Changed

- `testing_integration/test_harness_utils.py` - Base class with all logic
- `testing_integration/test_claude_telemetry.py` - Lightweight Claude test (36 lines)
- `testing_integration/test_cursor_telemetry.py` - Lightweight Cursor test (36 lines)

## Not in CI

These tests require real CLI tools installed and are meant for local validation only.

## Test Plan

- [x] Claude test passes with real CLI invocation
- [x] Cursor test correctly detects missing telemetry (expected behavior)
- [x] Template Method pattern prevents passive tests from passing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMAR
