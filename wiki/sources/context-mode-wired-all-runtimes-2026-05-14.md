---
title: "context-mode Wired into All 3 Runtimes (claude, claudew, codex)"
type: source
tags: [context-mode, llm-inspector, claude-code, codex, claudew, wafer, hooks, mcp]
raw: raw/project_2026-05-14_context-mode-wired-all-runtimes.md
date: 2026-05-14
---

## Summary

Session on 2026-05-14 wiring context-mode (FTS5 SQLite context interceptor) MCP server and hooks into all three runtimes (Claude Code, claudew, Codex), plus deploying composable proxy modes with WaferFixPatcher. PR [#1](https://github.com/jleechanorg/llm_inspector/pull/1) squash-merged.

## Key Changes

### `~/.claude/settings.json`
- Added `mcpServers.context-mode` with explicit node path (absolute, not `${CLAUDE_PLUGIN_ROOT}`)
- Added SessionStart hook → `sessionstart.mjs` (injects `<context_window_protection>` XML block)
- Added PostToolUse hook with broad matcher covering Read/Write/Edit/Bash/mcp__*
- Added PreCompact hook

### `~/.codex/hooks.json` + `~/.codex/config.toml`
- 6 context-mode hook events (SessionStart, PreToolUse, PostToolUse, PreCompact, UserPromptSubmit, Stop)
- Preserved: mem0_recall, RTK, stop-hook-dispatch
- `[mcp_servers.context-mode]` entry appended to config.toml

### `llm_inspector/src/filters.ts`
- `parseModeFeatures(modeStr)` — comma-separated flags: `lean`, `on-demand`, `wafer-fix`
- `WaferFixPatcher` — buffers SSE chunks until `\n\n`, patches `"input_tokens":0` → `Math.round(bodyBytes/4)`
- 23 tests pass (14 new)

## Key Lessons

1. **`enabledPlugins` ≠ MCP server running**: `enabledPlugins: {"context-mode@context-mode": true}` was already present but context-mode wasn't serving as MCP. Must add explicit `mcpServers.context-mode` entry.
2. **Absolute hook paths**: Use `/Users/jleechan/.nvm/.../context-mode/hooks/posttooluse.mjs` instead of `${CLAUDE_PLUGIN_ROOT}` in manually-wired settings.json hooks.
3. **claudew coverage**: `claudew` is just `claude` with `ANTHROPIC_BASE_URL=http://localhost:9001` — settings.json hooks apply automatically.
4. **Codex interactive needs `bash -i`**: `bash -c 'source ~/.bashrc'` doesn't load shell functions; use `bash -i -c '...'`.
5. **WaferFixPatcher pattern reusable**: Any upstream returning `input_tokens:0` causes autocompact thrashing. Regex fires only when value is literally `0`.

## Verification

- `npm test`: 23/23 pass
- Evidence bundle: `/tmp/context-mode-evidence/` — JSON runs, SHA256 sidecars, `.cast`/`.gif`
- Proxy log: `[lean: stripped 1 tools] [wafer-fix: est 38747 tokens]`

## Related Concepts

- [[ContextMode]] — FTS5 interceptor pattern
- [[Compaction]] — autocompact thrashing root cause
- [[WaferFixSSEPatcher]] — SSE patching pattern
- [[ProxyModes]] — composable feature flag system
