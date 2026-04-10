---
title: "Chrome DevTools Protocol (CDP)"
type: concept
tags: [protocol, debugging, chrome]
sources: ["browser-automation-comparison-playwright-vs-superpowers-chrome"]
last_updated: 2026-04-07
---

Chrome DevTools Protocol (CDP) is a debugging protocol that provides low-level access to Chrome browser functionality.

## CDP Capabilities
- Page navigation and manipulation
- DOM inspection and modification
- Network request interception
- Console logging access
- Performance profiling
- Screenshot capture
- JavaScript execution

## Implementation Approaches

### High-Level (Playwright)
```
Your Code → Playwright API → WebSocket → CDP
```
- Abstracts CDP complexity
- Adds retry logic, auto-healing
- Cross-browser support

### Direct (Superpowers Chrome)
```
Your Code/CLI → chrome-ws → Native WebSocket → CDP
```
- Minimal abstraction
- Zero dependencies
- CLI-first workflow

## Use Cases
- Automated testing
- Web scraping
- Performance monitoring
- Debugging
- Visual regression

## Related Concepts
- [[BrowserAutomation]]
- [[WebSocketProtocol]]
- [[Playwright]]
- [[SuperpowersChrome]]
