---
name: context-mode-wired-all-runtimes
description: "context-mode MCP + hooks wired into Claude Code, claudew, and Codex; composable proxy modes with WaferFixPatcher deployed"
metadata: 
  node_type: memory
  type: project
  bead: none
  originSessionId: f6c08ed2-9a66-45b2-9ecb-2784de0ecba6
---

## Context

Session on 2026-05-14 wiring context-mode (FTS5 SQLite interceptor for PostToolUse/PreCompact/SessionStart hooks) into all three runtimes used in this project, and deploying the WaferFixPatcher to fix GLM-5.1 autocompact thrashing.

## What Was Done

### 1. context-mode wired into Claude Code (`~/.claude/settings.json`)

Added explicit MCP server entry:
```json
"context-mode": {
  "command": "node",
  "args": ["/Users/jleechan/.nvm/versions/node/v22.22.0/lib/node_modules/context-mode/start.mjs"]
}
```

Added SessionStart hook → `sessionstart.mjs` (injects `<context_window_protection>` XML block).
Added PostToolUse hook with broad matcher: `Bash|Read|Write|Edit|NotebookEdit|Glob|Grep|TodoWrite|TaskCreate|TaskUpdate|EnterPlanMode|ExitPlanMode|Skill|Agent|AskUserQuestion|EnterWorktree|mcp__`.
Added PreCompact hook → `precompact.mjs`.

Covers both `claude` CLI and `claudew` (which is `claude` with `ANTHROPIC_BASE_URL=http://localhost:9001`).

### 2. context-mode wired into Codex (`~/.codex/hooks.json` + `~/.codex/config.toml`)

Added 6 context-mode hook events via `context-mode hook codex <event>` pattern.
Preserved existing: mem0_recall (SessionStart), RTK PreToolUse/Bash, stop-hook-dispatch (Stop).

Appended to `~/.codex/config.toml`:
```toml
[mcp_servers.context-mode]
command = "context-mode"
```

### 3. WaferFixPatcher + composable proxy modes deployed

**Problem**: GLM-5.1 (wafer) always returns `"input_tokens":0` in SSE `message_start`, causing Claude Code autocompact to fire every ~3 turns (thinks context just cleared).

**Fix**: `WaferFixPatcher` in `src/filters.ts` buffers SSE chunks until first `\n\n`, patches `"input_tokens":0` → `Math.round(bodyBytes / 4)`.

**Composable modes**: `--tool-mode lean,on-demand,wafer-fix` — comma-separated flags via `parseModeFeatures()`.

Launchd plist updated: `lean,on-demand,wafer-fix`.

### 4. PR merged

PR [#1](https://github.com/jleechanorg/llm_inspector/pull/1) (`fix/anthropic-tool-schema`) squash-merged into main on `jleechanorg/llm_inspector`.

Commits: `4b39ce6` (Fix Anthropic tool stub schema), `859d912` (skip /claude prefix for direct upstreams), and others. Final rebase over `85b4ed7` (Cursor Agent lean re-issue fix).

## Verification

- `npm test`: 23/23 tests pass (14 new WaferFixPatcher + parseModeFeatures tests)
- Non-interactive: `claude -p` and `codex exec --yolo` both show context-mode SessionStart hook firing
- Interactive: tmux sessions for `claude` and `claudew` both working
- Evidence bundle: `/tmp/context-mode-evidence/` with `evidence.md`, JSON run files, SHA256 sidecars, `.cast` + `.gif`
- Proxy log confirms: `[lean: stripped 1 tools] [wafer-fix: est 38747 tokens]`

## Key Files

- `~/.claude/settings.json` — Claude Code MCP + hooks
- `~/.codex/hooks.json` — Codex hooks (6 context-mode events)
- `~/.codex/config.toml` — Codex MCP server entry
- `llm_inspector/src/filters.ts` — WaferFixPatcher, parseModeFeatures, estimateInputTokens
- `llm_inspector/src/proxy.ts` — mode feature dispatch wiring
- `llm_inspector/src/filters.test.ts` — 23 tests
- `~/Library/LaunchAgents/com.jleechan.llm-inspector-wafer.plist` — `lean,on-demand,wafer-fix`

## Reusable Pattern

- `enabledPlugins: {"context-mode@context-mode": true}` alone is NOT sufficient — must also add explicit `mcpServers.context-mode` entry
- Use absolute hook paths in settings.json; `${CLAUDE_PLUGIN_ROOT}` variable may not resolve for manually-wired hooks
- `claudew` is just `claude` with redirected `ANTHROPIC_BASE_URL`; settings.json hooks cover both automatically
- For Codex interactive: use `bash -i -c '...'` to load shell functions from `.bashrc`
- `WaferFixPatcher` pattern is reusable for any upstream returning `input_tokens:0`

## References

- PR: https://github.com/jleechanorg/llm_inspector/pull/1
- Evidence: `/tmp/context-mode-evidence/evidence.md`
- Wiki source: [[context-mode-wired-all-runtimes-2026-05-14]]
- Related: [[wafer-sse-input-tokens-zero-fix-2026-05-14]]
