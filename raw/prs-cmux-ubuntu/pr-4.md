# PR #4: fix: resolve 21 bugs across all crates using TDD

**Repo:** jleechanorg/cmux_ubuntu
**Merged:** 2026-03-15
**Author:** jleechan2015
**Stats:** +1871/-162 in 17 files

## Summary
- Fixed 21 bugs across 4 crates (cmux-core, cmux-ascii, cmux-gtk, cmux-web)
- Added 18 new regression tests
- All 108 cmux-core tests pass, 9 cmux-web tests pass

### Priority 1 - Critical (5 bugs)
| Bug | Description |
|-----|-------------|
| cmux-dy4 | Implemented pane navigation (navigate_left/right/up/down) |
| cmux-7ay | Implemented split_pane() functionality |
| cmux-45g | Enabled GTK socket fetch at startup |
| cmux-mcu | Wired TerminalManager write/resize to VTE terminals |
| cmux-n50 | 

## Test Plan
- [x] cargo test -p cmux-core (108 passing)
- [x] cargo test -p cmux-web (9 passing)
- [x] cargo build -p cmux-ascii

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Touches core socket server behavior (permissions, SIGCHLD handling) and client I/O paths (timeouts, threaded PTY writes), which could impact connectivity and process/terminal lifecycle if incorrect, but changes are localized and covered by added regression te

## Raw Body
## Summary
- Fixed 21 bugs across 4 crates (cmux-core, cmux-ascii, cmux-gtk, cmux-web)
- Added 18 new regression tests
- All 108 cmux-core tests pass, 9 cmux-web tests pass

### Priority 1 - Critical (5 bugs)
| Bug | Description |
|-----|-------------|
| cmux-dy4 | Implemented pane navigation (navigate_left/right/up/down) |
| cmux-7ay | Implemented split_pane() functionality |
| cmux-45g | Enabled GTK socket fetch at startup |
| cmux-mcu | Wired TerminalManager write/resize to VTE terminals |
| cmux-n50 | Mapped VTE4 terminals to PaneIds |

### Priority 2 - High (10 bugs)
- cmux-dis: Added TTY detection to prevent crash
- cmux-cwd: Moved blocking I/O to background thread  
- cmux-94k: Added sidebar with live updates
- cmux-4th: Added notification badge to header
- cmux-wep: Wired tab close button handler
- cmux-a73: Created Entry widget for tab rename
- cmux-cuv: Added socket read timeout (5s)
- cmux-m1x: Fixed socket permissions (0o600)
- cmux-ajy: Added build/install instructions to README
- cmux-h8a: Documented Docker build option

### Priority 3 - Medium (6 bugs)
- cmux-vnj: Applied font config to VTE4 terminals
- cmux-bzh: Fixed CSS active class replacement
- cmux-sxq: Persisted split pane ratio
- cmux-nyf: Removed dead code in socket.rs
- cmux-bcy: Added tests for cmux-ascii and cmux-web
- cmux-gxo: Investigated - no child processes in cmux-core

## Test plan
- [x] cargo test -p cmux-core (108 passing)
- [x] cargo test -p cmux-web (9 passing)
- [x] cargo build -p cmux-ascii

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Touches core socket server behavior (permissions, SIGCHLD handling) and client I/O paths (timeouts, threaded PTY writes), which could impact connectivity and process/terminal lifecycle if incorrect, but changes are localized and covered by added regression tests.
> 
> **Overview**
> **Stabilizes client/server I/O and tightens security.** `cmux-core` now applies 5s sock
