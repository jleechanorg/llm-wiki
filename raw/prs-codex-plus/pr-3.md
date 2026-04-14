# PR #3: feat: fix status line to show correct directory context

**Repo:** jleechanorg/codex_plus
**Merged:** 2025-09-22
**Author:** jleechan2015
**Stats:** +83/-28 in 5 files

## Summary
- Fix status line to display correct repository directory instead of proxy directory
- Remove ANSI color codes that weren't displaying properly in Codex CLI
- Improve status line injection mechanism for better visibility

## Raw Body
## Summary
- Fix status line to display correct repository directory instead of proxy directory
- Remove ANSI color codes that weren't displaying properly in Codex CLI
- Improve status line injection mechanism for better visibility

## Changes Made
- **Working Directory Detection**: Extract working directory from `<cwd>` tags in request body
- **Status Line Generation**: Use extracted working directory for git commands and status line generation  
- **Injection Mechanism**: Improve status line injection to appear directly in Claude responses
- **Color Removal**: Remove ANSI color codes that caused display issues

## Technical Details
- Modified `main_sync_cffi.py` to parse working directory from request body
- Updated `hooks.py` to accept working directory parameter for git operations
- Enhanced `status_line_middleware.py` to use provided working directory
- Improved `llm_execution_middleware.py` to inject status line as visible text
- Updated `.codexplus/settings.json` for dynamic repository name detection

## Before/After
**Before**: `[Dir: codex_plus | Local: gauth (synced) | Remote: origin/gauth | PR: none]`
**After**: `[Dir: worktree_worker1 | Local: codex/add-grok-as-default-supported-model (synced) | Remote: origin/codex/add-grok-as-default-supported-model | PR: #5 https://github.com/jleechanorg/ai_universe/pull/5]`

## Testing
- ✅ Status line shows correct repository context
- ✅ Working directory detection from request body
- ✅ Status line appears in Codex CLI responses
- ✅ No display issues with removed color codes
