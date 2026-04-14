# PR #4: fix: resolve proxy.sh lock acquisition failures and startup race conditions

**Repo:** jleechanorg/codex_plus
**Merged:** 2025-09-22
**Author:** jleechan2015
**Stats:** +31/-14 in 2 files

## Summary
Fixes critical proxy.sh startup issues that were causing lock acquisition failures and race conditions during proxy startup.

## Test Plan
- [x] Proxy starts successfully without lock timeouts
- [x] Proxy stays running after startup
- [x] Health endpoint responds correctly
- [x] Status command works without killing the proxy
- [x] No syntax warnings during startup

🤖 Generated with [Claude Code](https://claude.ai/code)

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Raw Body
## Summary
Fixes critical proxy.sh startup issues that were causing lock acquisition failures and race conditions during proxy startup.

## Issues Fixed
- **Lock acquisition timeouts**: Runtime directory wasn't created before trying to acquire lock file
- **Process termination race condition**: `cleanup_stale_resources` was killing newly started proxy processes
- **Trap handling issues**: Lock files were being removed on script exit instead of only on startup failure
- **Syntax warning**: Fixed regex escape sequence in hooks.py

## Changes Made
### proxy.sh
- Create runtime directory before lock file acquisition
- Modify trap to only remove lock file on startup failure, not script exit
- Prevent `cleanup_stale_resources` from running preemptively in status checks
- Show status inline after startup instead of calling `print_status` (which could kill the process)

### hooks.py
- Fix syntax warning by using raw string for regex pattern

## Test Plan
- [x] Proxy starts successfully without lock timeouts
- [x] Proxy stays running after startup
- [x] Health endpoint responds correctly
- [x] Status command works without killing the proxy
- [x] No syntax warnings during startup

🤖 Generated with [Claude Code](https://claude.ai/code)

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

* New Features
  * Added startup locking to prevent concurrent proxy launches.
  * Provides clearer, detailed status output after successful start.

* Bug Fixes
  * Smarter cleanup of stale PID/lock files improves reliability.
  * Ensures runtime directory is created with correct permissions.
  * Stop/restart now consistently removes locks and cleans remaining processes.
  * Health checks and status reporting are more accurate and consistent.
  * Fixed PR metadata parsing for GitHub CLI in the git status line, improving display of PR number and URL.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->
