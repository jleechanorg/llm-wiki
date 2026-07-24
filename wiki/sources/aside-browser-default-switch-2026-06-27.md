---
title: "Aside browser default switch (2026-06-27)"
type: source
tags: [source-type:project-decision, aside-browser, browser-default, hermes, claude-code, codex, browser-automation]
date: 2026-06-27
source_file: raw/aside-browser-default-switch-2026-06-27.md
---

## Summary
Jeffrey Lee-Chan decided to make the Aside browser (a new Y Combinator–backed AI-native Chromium browser, GUI `/Applications/Aside.app`, CLI `~/.local/bin/aside` v1.26.626.1517) the default browser tool across `~/.hermes/`, `~/.claude/`, and `~/.codex/` skills. Implementation is a reversible-facade design: Aside is the primary tool; Playwright MCP and superpowers-chrome remain as named fallbacks for cases Aside can't handle. Also wired `aside-mcp` into `~/.claude.json`, set Aside as the macOS default browser, and extended browserclaw to support Aside Safe Storage keychain entry. A single rollback script (`~/.hermes/scripts/rollback-aside-default.sh`) reverts everything.

## Key Claims
- Aside CLI is verified working (`aside repl "listBrowserTabs().length"` → `[ok | 14ms]`; account `* u0 jleechan@gmail.com` signed in with Google provider).
- The `aside-mcp` HTTP server was already running on `http://127.0.0.1:8013/mcp` and registered in `~/.claude/mcp-strict.json`; only `~/.claude.json` needed the new entry for Claude Code/Codex MCP discovery.
- Chrome, Playwright MCP, and superpowers-chrome are kept as explicit fallbacks — never deleted — to make the switch reversible.
- All edits are line-targeted with `patch()` against stable, identifiable strings; no file overwrites for policy files.
- The new skill `~/.hermes/skills/aside-browser-default/SKILL.md` is the canonical reference; the SOUL/AGENTS/CLAUDE COMMIT blocks now reference it.

## Key Quotes
> "I wanna make the aside browser my default one for all the ~/.hermes and ~/.claude/ and ~/.codex skills, lets find what these skills are all using now and check the hermes soul MD and agents md and all thsoe files etc" — Jeffrey Lee-Chan, Slack C09GRLXF9GR, 2026-06-27

> "Ok lets do all 4 but make this easily reverisble and use /learn to save the decisions/info in various places" — Jeffrey Lee-Chan, 2026-06-27

## Connections
- [[AsideBrowser]] — the new primary browser tool
- [[Playwright]] — explicit fallback (Playwright MCP)
- [[PlaywrightMCP]] — explicit fallback MCP server
- [[SuperpowersChrome]] — explicit fallback (`chrome_use_browser`)
- [[Chrome]] — was the prior default; now fallback
- [[BrowserAutomation]] — concept this falls under
- [[ReversibleFacadePattern]] — design pattern for default-tool switches

## Reversal
`bash ~/.hermes/scripts/rollback-aside-default.sh` restores the prior state: removes `aside-browser-default` skill folder, removes `aside-mcp` from `~/.claude.json`, reverts SOUL/AGENTS/CLAUDE browser COMMIT blocks, resets macOS default browser to Chrome. Saves a `pre-aside-default-YYYY-MM-DD.json` snapshot of the original `mcpServers` block before mutating.