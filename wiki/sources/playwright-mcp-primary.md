---
title: "Playwright MCP — Primary Browser Testing Method"
type: source
tags: [worldarchitect, playwright, mcp, browser-testing, automation]
date: 2026-01-12
source_file: raw/worldarchitect.ai/PLAYWRIGHT_MCP_PRIMARY.md
---

## Summary
Establishes Playwright MCP as the mandatory primary browser automation method for WorldArchitect.AI, always running in headless mode. Supersedes Puppeteer MCP (secondary, Chrome-only) and local Playwright (fallback). Key advantages: AI-optimized accessibility-tree approach, zero setup, cross-browser support, headless-only, and 2025 industry leadership.

## Key Claims
- **Playwright MCP is mandatory primary** for all browser automation in WorldArchitect.AI
- **Always headless** — no visible browser windows in testing
- **Cross-browser**: Chrome, Firefox, Safari (vs Puppeteer Chrome-only)
- **2025 industry leadership**: "Playwright MCP Server currently leads due to extensibility, multi-browser support, and tight integration with AI/LLM ecosystems"
- Tool hierarchy: (1) Playwright MCP, (2) Puppeteer MCP (Chrome-specific), (3) Local Playwright (MCP unavailable)
- Auth bypass: URL parameters `test_mode=true` and `test_user_id=test-123` enable headless authentication
- Existing tests use local Playwright and need migration to Playwright MCP

## Test URL Format
```
http://localhost:6006?test_mode=true&test_user_id=test-123
```

## Key Functions
| Function | Purpose |
|----------|---------|
| `browser_navigate` | Navigate to URL |
| `browser_click` | Click elements |
| `browser_type` | Fill forms |
| `browser_take_screenshot` | Capture screenshots |
| `browser_snapshot` | Get accessibility tree |
| `browser_wait_for` | Wait for conditions |

## Connections
- [[WorldArchitect.AI]] — primary project using Playwright MCP
- [[VisualRegressionTesting]] — browser testing methodology
- [[HeadlessAutomation]] — headless-only testing requirement
- [[MCPServerInstructions]] — MCP server configuration
