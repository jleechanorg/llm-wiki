---
title: "Superpowers Chrome"
type: entity
tags: [project, testing, browser-automation]
sources: ["browser-automation-comparison-playwright-vs-superpowers-chrome"]
last_updated: 2026-04-07
---

Superpowers Chrome is a lightweight browser automation tool using direct Chrome DevTools Protocol (CDP) access with zero npm dependencies.

## Technical Specs
- **Dependencies**: 0 (zero dependencies)
- **Launch Time**: 1-2 seconds
- **Browsers**: Chrome only
- **Session**: Reuses existing Chrome
- **Features**: Direct CDP access, CLI-first workflow, MCP mode

## Best For
- Quick debugging and exploration
- Lightweight smoke tests
- Persistent browsing sessions
- CLI automation workflows
- MCP integration

## Architecture
```
Your Code/CLI → chrome-ws (17 commands) → Native WebSocket → CDP → Chrome (existing instance)
```

## Related Concepts
- [[ChromeDevToolsProtocol]]
- [[MCP]]
- [[WebSocketProtocol]]
