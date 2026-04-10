---
title: "WebSocket Protocol"
type: concept
tags: [protocol, networking, real-time]
sources: ["browser-automation-comparison-playwright-vs-superpowers-chrome"]
last_updated: 2026-04-07
---

WebSocket is a bidirectional communication protocol enabling real-time, persistent connections between client and server.

## WebSocket in Browser Automation

### Playwright
- Uses WebSocket for browser communication
- High-level abstraction hides protocol details
- Automatic reconnection handling
- Built-in wait strategies

### Superpowers Chrome
- Uses native WebSocket (Node.js built-in)
- Direct CDP access
- Minimal abstraction
- CLI-first commands (17 commands)

## Protocol Flow
```
Client → WebSocket Handshake (HTTP) → Persistent Connection → Bidirectional Messages → Client/Server
```

## Key Features
- **Bidirectional**: Both client and server can send messages
- **Persistent**: Single connection for multiple messages
- **Low overhead**: No HTTP headers per message
- **Real-time**: Immediate message delivery

## Related Concepts
- [[BrowserAutomation]]
- [[ChromeDevToolsProtocol]]
- [[Playwright]]
- [[SuperpowersChrome]]
