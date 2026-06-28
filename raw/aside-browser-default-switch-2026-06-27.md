---
name: Aside browser as default for Hermes/Claude/Codex skills
description: Switched the agent browser default from Playwright MCP / superpowers-chrome to Aside (AI-native Chromium browser, GUI /Applications/Aside.app, CLI ~/.local/bin/aside). Reversible via rollback script. Also added aside-mcp to ~/.claude.json and set Aside as the macOS default browser.
type: feedback
bead: none
---

# Aside browser as default for Hermes/Claude/Codex skills

**Date:** 2026-06-27
**Owner:** Jeffrey Lee-Chan (Slack C09GRLXF9GR)
**Trigger:** Jeffrey said *"I wanna make the aside browser my default one for all the ~/.hermes and ~/.claude/ and ~/.codex skills"* + *"Ok lets do all 4 but make this easily reversible and use /learn to save the decisions/info in various places"*

## What changed

### 1. Aside CLI added to all skill directories

Aside is now the **primary browser tool** in the agent ecosystem; Playwright MCP and superpowers-chrome are explicit fallbacks for cases Aside can't handle. The new skill `~/.hermes/skills/aside-browser-default/SKILL.md` is the canonical reference.

### 2. aside-mcp wired into `~/.claude.json`

The `aside-mcp` HTTP server (already running at `http://127.0.0.1:8013/mcp`, registered in `~/.claude/mcp-strict.json`) is now also in `~/.claude.json`, so Claude Code and Codex agents see it via their standard MCP discovery path.

### 3. SOUL.md / AGENTS.md / CLAUDE.md browser-default COMMIT blocks updated

All three user-scope policy files (`~/.hermes/SOUL.md`, `~/.hermes_prod/SOUL.md`, `~/.hermes/AGENTS.md`, `~/.hermes_prod/AGENTS.md`, `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`) now reference `aside-browser-default` first, with browser-headless-default as the explicit fallback for Playwright/superpowers-chrome paths.

### 4. macOS default browser

Aside is set as the macOS default browser via `~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist` overrides + `defaultbrowser aside`. Rollback via `defaultbrowser chrome` (or `arc` / `comet`).

### 5. browserclaw updated to support Aside Safe Storage

`browserclaw cookies decrypt` and `cookies inject` now accept `--keychain-service 'Aside Safe Storage'` and `--keychain-account 'Aside'` to decrypt/replay Aside's cookies. Aside DB path: `~/Library/Application Support/Aside/Default/Cookies`.

## Reversal

`~/.hermes/scripts/rollback-aside-default.sh` restores the prior state:
- Removes `aside-browser-default` skill folder
- Removes `aside-mcp` from `~/.claude.json`
- Reverts SOUL.md / AGENTS.md / CLAUDE.md browser COMMIT blocks
- Resets macOS default browser to Chrome
- Restores prior browserclaw default keychain params (Chrome Safe Storage / Chrome)

Run before merging any "switch back" PR. Keep the script — it's the single source of truth for the rollback recipe.

## Why this is reversible

- All edits are line-targeted with `patch()` — no file overwrites for policy files.
- The new skill lives in its own folder; delete it without touching existing skills.
- `~/.claude.json` is parsed and re-written with the original `mcpServers` keys preserved.
- macOS default browser change is a single `defaults write` + `lsregister` call; reversal is the inverse.
- Rollback script saves a `pre-aside-default-YYYY-MM-DD.json` snapshot of the original `mcpServers` block.

## References

- Skills touched: `~/.hermes/skills/aside-browser-default/SKILL.md` (new), `~/.hermes/skills/browser-headless-default/SKILL.md` (Aside added as preferred), `~/.hermes/skills/browserclaw/SKILL.md` (Aside keychain entry), mirror copies under `~/.hermes_prod/skills/`
- Policy files: `~/.hermes/SOUL.md`, `~/.hermes/AGENTS.md`, `~/.hermes_prod/SOUL.md`, `~/.hermes_prod/AGENTS.md`, `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`
- MCP config: `~/.claude.json` (added `aside-mcp` key pointing at `http://127.0.0.1:8013/mcp`)
- Rollback script: `~/.hermes/scripts/rollback-aside-default.sh`
- macOS: `defaultbrowser` shell wrapper or `defaults write com.apple.LaunchServices/com.apple.launchservices.secure.plist LSHandlers.<scheme> = <aside-bundle-id>`

## Reusable pattern

When introducing a new default tool across the skill ecosystem:
1. Write the decision to `/learn` BEFORE editing files (this file)
2. Build the change as a reversible facade — primary + named fallback(s)
3. Provide a single rollback script that snapshots state before mutating
4. Mirror the change in both `~/.hermes/` (staging) and `~/.hermes_prod/` (prod) via `scripts/deploy.sh`
5. Test both directions (forward + rollback) end-to-end before reporting done