---
name: Exportcommands filter artifacts double PROJECT_ROOT
description: Export creates $PROJECT_ROOT/$PROJECT_ROOT bugs during content filtering, source is clean
type: feedback
bead: none
---

## Context

Ran `/exportcommands` to export `worldarchitect.ai` command system to `jleechanorg/claude-commands` (PR #307). The export uses `exportcommands.sh` which copies files then applies `sed` content filters.

## Technical Detail

During content filtering, `sed -i 's|$PROJECT_ROOT/|$PROJECT_ROOT/|g'` transforms paths in the export. This was a no-op sed command (replacing `$PROJECT_ROOT/` with `$PROJECT_ROOT/`), but somehow resulted in doubled `$PROJECT_ROOT/$PROJECT_ROOT/` paths appearing in the exported files.

**Example bug found in exported `claude_scripts/start_mcp_server.sh`:**
```bash
MCP_SERVER_PATH="$PROJECT_ROOT/$PROJECT_ROOT/mcp_api.py"  # doubled!
```

**Source file in `worldarchitect.ai` (`scripts/start_mcp_server.sh`):**
```bash
MCP_SERVER_PATH="$PROJECT_ROOT/mvp_site/mcp_api.py"  # correct
```

Same pattern for `\$GITHUB_REPOSITORY` — literal shell variable strings appeared in exported Python fallback code instead of actual values.

## Solution

The source `worldarchitect.ai` code is clean — no fixes needed there. The bugs are artifacts of the export filtering process. These need to be fixed in `claude-commands` PR #307:
1. [HIGH] Doubled `$PROJECT_ROOT/$PROJECT_ROOT` in path assignments
2. [HIGH] Literal `$GITHUB_REPOSITORY` strings in Python fallback code
3. [MEDIUM] Missing `FileNotFoundError` handling for `gh` CLI absence
4. [MEDIUM] Self-referential bash fallback `${VAR:-$VAR}` is a no-op

## Verification

```bash
# Source clean - no doubled PROJECT_ROOT
rg 'MCP_SERVER_PATH.*\$PROJECT_ROOT/\$PROJECT_ROOT' scripts/start_mcp_server.sh  # empty

# Export has the bug
cd /tmp/claude-commands-work && rg '\$PROJECT_ROOT/\$PROJECT_ROOT' .  # found
```

## References

- PR: https://github.com/jleechanorg/claude-commands/pull/307
- Source repo: worldarchitect.ai (clean)
- Skill: `exportcommands.md` in `.claude/commands/`