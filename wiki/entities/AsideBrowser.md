---
title: "AsideBrowser"
type: entity
tags: [tool, browser, ai, chromium, mcp, cli]
sources: ["aside-browser-default-switch-2026-06-27"]
last_updated: 2026-06-27
---

## Description
Aside is a Y Combinator–backed AI-native Chromium browser launched June 2026. GUI app at `/Applications/Aside.app`, CLI binary at `/Users/jleechan/.local/bin/aside` (v1.26.626.1517). Three primary execution modes: natural-language agent (`aside "..."`), deterministic JavaScript REPL (`aside repl "..."` with Playwright-shaped snapshot/ref API), and MCP server (`aside mcp` over stdio / HTTP). Auth wired through `aside account list` — currently signed in as `u0 jleechan@gmail.com` via Google provider. Safe Storage keychain entry: `Aside Safe Storage` / `Aside` (separate from Chrome's `Chrome Safe Storage` / `Chrome`, so cookies cannot be cross-imported without re-encryption).

## Modes
- `aside "Open https://example.com and summarize"` — NL agent, supports `--effort ultrabrowse` for proactive high-thinking mode
- `aside repl "const p = await openTab('https://...'); const s = await snapshot(p); s.tree"` — Playwright-shaped deterministic JS API (`openTab`, `listBrowserTabs`, `attachActiveBrowserTab`, `snapshot`)
- `aside mcp` — MCP server, available over HTTP at `http://127.0.0.1:8013/mcp`
- `aside exec -m <model>` — model-pinned execution

## Used In
- [[Aside browser default switch (2026-06-27)]] — primary tool for browser work in Hermes/Claude/Codex skills
- Fallback when the user explicitly says "show browser" / "headed mode" — though Aside itself supports headed mode

## Related Concepts
- [[BrowserAutomation]] — falls under this concept
- [[ReversibleFacadePattern]] — design pattern used in the default switch
- [[BrowserBasedTesting]] — testing pattern that uses browser tools
- [[Playwright]] — sibling tool, named fallback
- [[PlaywrightMCP]] — sibling MCP server, named fallback
- [[SuperpowersChrome]] — sibling tool, named fallback
- [[Chrome]] — sibling tool, named fallback

## Gotchas
- **`snapshot()` without a page arg** throws `Cannot read properties of undefined (reading 'targetId')` — REPL has no implicit `page` global.
- `listTabs` does NOT exist — correct API is `listBrowserTabs()` / `attachActiveBrowserTab()`.
- Aside CLI only sees its own browser — cannot read Chrome/Comet/Arc history or cookies directly.
- Cross-browser cookie portability: there is NO shared key material between browsers; Chrome cookies cannot be "copied" into Aside without re-encryption under Aside's own Safe Storage password.
- Aside cookie DB path: `~/Library/Application Support/Aside/Default/Cookies` — note: same Chromium v24 schema as Chrome/Comet/Brave/Edge, but separate keychain entry.