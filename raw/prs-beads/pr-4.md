# PR #4: docs: add local MCP development skills and wrapper script

**Repo:** jleechanorg/beads
**Merged:** 2025-11-15
**Author:** jleechan2015
**Stats:** +378/-0 in 2 files

## Summary
Adds comprehensive documentation and tooling for developers who want to use the local development version of beads-mcp instead of the PyPI package.

## Raw Body
## Summary

Adds comprehensive documentation and tooling for developers who want to use the local development version of beads-mcp instead of the PyPI package.

## New Files

### `.claude/skills/use-local-beads-mcp.md`
Complete reference guide covering:
- **PyPI vs Local Development**: Comparison table and use case guidance
- **Configuration Commands**: Step-by-step for Claude Code and Codex CLI
- **Config Management**: Precedence rules, scope options, multi-config setups
- **Version Management**: Checking, switching, and updating versions
- **Troubleshooting**: Common issues and solutions
- **Workflows**: Development session, testing changes, switching versions

### `integrations/beads-mcp/run-local-mcp.sh`
Wrapper script that:
- Simplifies Codex CLI MCP server configuration
- Automatically changes to correct directory
- Runs `uv run python -m beads_mcp` with proper environment

## Benefits

✅ **Instant feedback** - Test MCP changes without rebuild/reinstall cycles  
✅ **Full debugging** - Edit source, add logs, step through code  
✅ **Latest features** - Access unreleased improvements immediately  
✅ **Easy switching** - Toggle between stable PyPI and local development  
✅ **System-wide** - Works in all projects with user config  

## Use Cases

Essential for:
- Contributing to beads-mcp development
- Testing unreleased features or bug fixes
- Debugging MCP server issues
- Developing beads itself

## Configuration Summary

After following the guide, both Claude Code and Codex CLI use:
- **Command**: `uv run python -m beads_mcp` (local source)
- **Location**: `/Users/jleechan/projects_other/beads/integrations/beads-mcp/`
- **Scope**: User-wide config (`~/.claude.json` and `~/.codex/config.toml`)

Changes to beads-mcp source code take effect on next CLI session - no reinstall needed!

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> Adds a concise guide for using 
