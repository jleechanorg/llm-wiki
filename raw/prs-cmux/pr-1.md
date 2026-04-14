# PR #1: WORKING: Fix split CWD inheritance and bash job spam

**Repo:** jleechanorg/cmux
**Merged:** 2026-03-05
**Author:** jleechan2015
**Stats:** +215/-3 in 4 files

## Summary
- **Split CWD inheritance**: New split panes now inherit the working directory from the source panel (`panelDirectories[panelId]` → `currentDirectory` fallback chain)
- **Bash job spam fix**: Suppress `[N] Done ...` notifications from background shell integration probes via `& disown`
- **Integration test**: Added `tests/test_split_cwd_inheritance.py` to verify split and tab CWD inheritance via real sockets

## Test Plan
- [x] Automated integration test passes 5/5
- [x] Manual split in dev build inherits correct cwd
- [x] Debug log confirms `split.cwd resolved=<correct path>`
- [x] No more `[N] Done ...` spam in bash terminals
- [x] All 5 review comments addressed (test correctness, Ruff F841, shell race)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Raw Body
## Demo

![Split CWD Inheritance Demo](https://raw.githubusercontent.com/jleechanorg/cmux/fix-split-cwd-inheritance/docs/assets/split-cwd-inheritance-demo.gif)

1. Initial terminal state
2. After `cd /tmp/cmux-cwd-demo` + right split created
3. New split pane with `pwd` confirming inherited CWD

---

## Summary
- **Split CWD inheritance**: New split panes now inherit the working directory from the source panel (`panelDirectories[panelId]` → `currentDirectory` fallback chain)
- **Bash job spam fix**: Suppress `[N] Done ...` notifications from background shell integration probes via `& disown`
- **Integration test**: Added `tests/test_split_cwd_inheritance.py` to verify split and tab CWD inheritance via real sockets

## Test plan
- [x] Automated integration test passes 5/5
- [x] Manual split in dev build inherits correct cwd
- [x] Debug log confirms `split.cwd resolved=<correct path>`
- [x] No more `[N] Done ...` spam in bash terminals
- [x] All 5 review comments addressed (test correctness, Ruff F841, shell race)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
