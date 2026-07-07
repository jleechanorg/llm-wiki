---
name: mcp-tool-search-default-and-config-dir-trap
description: "ENABLE_TOOL_SEARCH default is already full-deferral (not the auto% threshold mode); CLAUDE_CONFIG_DIR=~/.claude (vs unset) silently targets a different, orphaned .claude.json"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: ed376cb6-f347-4237-a510-b404c88d46f0
---

**Rule 1 — ENABLE_TOOL_SEARCH's real default is full deferral, not "auto".** Verified directly against `https://code.claude.com/docs/en/mcp` (WebFetch, primary source, not secondhand): when `ENABLE_TOOL_SEARCH` is **unset**, Claude Code already defers ALL MCP tool schemas (only names + short server instructions load at session start) for standard first-party API usage. `auto` is a DIFFERENT, LESS-deferred mode (threshold: load schemas upfront if they'd fit in <10% of context, defer only the overflow) — do not assume "auto" is the default just because it sounds like the safe/default-sounding option. Full value table: unset=defer-all (falls back to upfront-load only on GCP Agent Platform or non-first-party `ANTHROPIC_BASE_URL` proxies), `true`=force-defer-always, `auto`/`auto:N`=threshold mode, `false`=force-upfront-always.

**Why this matters:** initially assumed (wrongly) that a large `CLAUDE_CODE_MAX_CONTEXT_TOKENS` (950000, via the fable-5 1M-context model) was defeating a percentage-based auto-threshold, making 10-15 MCP servers' full schemas load every turn (~27-31K tokens raw byte estimate). That hypothesis was backwards — the real default already deferred almost everything; the actual "always-paid" floor is just tool names + brief server instructions, not full schemas.

**Real measured proof (jeff-ubuntu, live `claude --print --output-format json --model haiku` calls, same 15-MCP-server config, only `ENABLE_TOOL_SEARCH` value changed in settings.json between runs — NOT via shell env override, see Rule 3 below):**
- Deferral OFF (`false`): 80,012 `cache_creation_input_tokens`
- Deferral ON (`true`, the fix applied): 42,259 `cache_creation_input_tokens`
- Zero MCP servers (`--strict-mcp-config` empty file, floor): ~42,112 tokens
- → Marginal cost of 15 MCP servers WITH the fix: ~147 tokens (basically free). WITHOUT: ~37,900 tokens. Real saving: 37,753 tokens / 47% per fresh cache-miss.

**Fix applied:** added `"ENABLE_TOOL_SEARCH": "true"` to `~/.claude/settings.json`'s `env` block (shared via symlink to `~/.claude-wa/settings.json` on both this Mac and jeff-ubuntu) — pins the already-correct default explicitly so it can't silently fall back to full upfront-loading if `ANTHROPIC_BASE_URL` is ever pointed at a non-first-party proxy.

**Rule 2 — deferred loading is per-TOOL, not per-server.** Confirmed via the same doc: "Only the tools Claude actually uses enter context." Calling one tool from a 14-tool server (e.g. `filesystem-mcp`'s `read_file`) does NOT pull in the other 13 tools' schemas. But once a tool's schema loads, it stays resident for the rest of that session (no eviction) — so a session that touches many different tools across many servers still creeps back toward the full un-deferred total over its lifetime; a short focused session pays almost nothing beyond the ~150-token registration floor.

**Rule 3 — `CLAUDE_CONFIG_DIR=/Users/jleechan/.claude` (explicit) is NOT the same as unset, and silently creates/edits an orphaned duplicate `.claude.json`.** The real default profile (no `CLAUDE_CONFIG_DIR` at all) reads `~/.claude.json` at the home root directly. Setting `CLAUDE_CONFIG_DIR=/Users/jleechan/.claude` explicitly makes the CLI look for `.claude.json` **nested inside** that directory (`/Users/jleechan/.claude/.claude.json`) instead — a completely separate file with independently-drifting state (observed: `numStartups` differed by 45 between the two). Made this exact mistake mid-session: ran `claude mcp remove <server>` with `CLAUDE_CONFIG_DIR=/Users/jleechan/.claude` set, which silently edited the wrong/orphaned file while the real `~/.claude.json` (10 live MCP servers, actually used by the plain `claude` command) stayed untouched. Caught it by running `env -u CLAUDE_CONFIG_DIR claude mcp list` and noticing the server list differed from what the CLAUDE_CONFIG_DIR-scoped version showed.

**How to apply:** whenever inspecting or editing "the regular/default Claude Code profile" (not a named alt-profile like `claude-wa`), always invoke with `env -u CLAUDE_CONFIG_DIR claude ...` (or leave the ambient env var fully unset) — never assume `CLAUDE_CONFIG_DIR=~/.claude` is equivalent to the default. Check `type claude` / bashrc wrapper functions first to see if the session's ambient `CLAUDE_CONFIG_DIR` differs from what a plain terminal invocation would use (this session's ambient value was `~/.claude-wa`, not unset).

See also [[mcp-minimal-set-standardization-2026-07-07]] for the full MCP server cleanup done in the same session, and [[sidekick-same-name-respawn-race]] for a harness-durability gap found later the same day.
