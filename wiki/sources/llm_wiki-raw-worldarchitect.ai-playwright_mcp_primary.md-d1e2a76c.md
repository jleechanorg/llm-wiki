---
title: "Playwright MCP: Primary Browser Testing Method"
type: source
tags: [worldarchitect.ai, playwright, mcp, browser-automation, headless, testing, microsoft]
sources: [worldarchitect.ai-docs-testing_design.md]
source_file: "raw/llm_wiki-raw-worldarchitect.ai-playwright_mcp_primary.md"
last_updated: 2026-04-07
---

## Summary
This document establishes Playwright MCP as the mandatory primary browser automation method for WorldArchitect.AI, running exclusively in headless mode. It provides a tiered tool hierarchy: Playwright MCP as first choice, Puppeteer MCP for Chrome-specific needs, and local Playwright as fallback when MCP is unavailable.

## Key Claims
- **Playwright MCP is mandatory primary**: AI-optimized accessibility-tree approach, zero setup required, cross-browser support (Chrome/Firefox/Safari), session sharing for efficient test execution
- **2025 industry leadership**: Playwright MCP leads due to extensibility, multi-browser support, and tight AI/LLM ecosystem integration
- **Always headless**: All browser automation runs headless (no visible windows) — `headless=True` is mandatory
- **Fallback hierarchy**: Playwright MCP → Puppeteer MCP → local Playwright
- **MCP function reference**: browser_navigate, browser_click, browser_type, browser_take_screenshot, browser_snapshot, browser_wait_for

## Key Quotes
> "Playwright MCP Server currently leads due to its extensibility, multi-browser support, and tight integration with AI/LLM ecosystems"

> "Teams seeking AI-integrated browser automation are gravitating toward Playwright—especially when using the MCP standard"

## Testing Protocol
- **Authentication bypass**: URL parameters `test_mode=true` and `test_user_id=test-123`
- **Error handling**: Use browser_wait_for() for async operations, take screenshots on failures
- **Test commands**: `/testui` (Mock APIs), `/testuif` (Real APIs), `/testserver start`

## Connections
- [[Testing Design Document]] — 3-layer test architecture including UI layer with Playwright
- [[Browser Automation Comparison: Playwright vs Superpowers Chrome]] — Playwright vs alternative browser automation
- [[Browser Automation Workflows]] — Practical workflows combining Playwright and Superpowers Chrome

## Contradictions
- None identified. This document reinforces the existing Playwright-based UI testing architecture from the Testing Design Document.
