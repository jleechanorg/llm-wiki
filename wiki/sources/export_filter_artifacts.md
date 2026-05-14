# Export Filter Artifacts - Double PROJECT_ROOT Bug

**Source**: Claude auto-memory, 2026-05-13

## Summary

Exportcommands sed filter creates doubled `$PROJECT_ROOT/$PROJECT_ROOT` bugs in exported files. Source `worldarchitect.ai` is clean — the bug is an artifact of export filtering.

## Technical Pattern

1. `exportcommands.sh` copies files then runs `sed -i 's|$PROJECT_ROOT/|$PROJECT_ROOT/|g'` content filters
2. This transforms paths, but somehow creates doubled `$PROJECT_ROOT/$PROJECT_ROOT/` in exported scripts
3. Same issue affects `$GITHUB_REPOSITORY` — literal shell variable strings appear in Python fallback code

## Example

**Source** (`scripts/start_mcp_server.sh` in worldarchitect.ai):
```bash
MCP_SERVER_PATH="$PROJECT_ROOT/mvp_site/mcp_api.py"  # correct
```

**Exported** (`claude_scripts/start_mcp_server.sh` in claude-commands):
```bash
MCP_SERVER_PATH="$PROJECT_ROOT/$PROJECT_ROOT/mcp_api.py"  # doubled - bug!
```

## See Also

- [[exportcommands]]
- [[evidence-standards]] — evidence requirements for exports