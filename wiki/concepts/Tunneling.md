---
title: "Tunneling"
type: concept
tags: [networking, proxy, expose-local]
sources: []
last_updated: 2026-04-08
---

Tunneling is a networking technique that creates a public URL pointing to a local service, enabling remote access to localhost-only applications. Used when the remote server cannot reach the user's local machine directly.

In WorldArchitect context, tunnel solutions (localhost.run, cloudflared, ngrok, Tailscale Funnel) expose the local OpenClaw gateway to Cloud Run/remote environments.

## Related Pages
- [[OpenClaw Setup for WorldArchitect]] — Setup guide using tunnel scripts
- [[OpenClaw Tailscale Tunnel Script]] — Specific tunnel implementation
