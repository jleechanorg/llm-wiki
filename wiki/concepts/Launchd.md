---
title: "launchd"
type: concept
tags: [macos, daemon, service-manager]
sources: [openclaw-tailscale-tunnel-script]
last_updated: 2026-04-08
---

## Description
launchd is the service management framework on macOS that handles daemon and agent processes. Scripts note that launchd jobs start with a minimal PATH, requiring explicit PATH configuration.

## Connections
- [[OpenClawTailscaleTunnelScript]] — mentions launchd PATH limitations
- [[Tailscale]] — tailscaled daemon runs via launchd on macOS

## References
- Socket path on macOS: /var/run/tailscale/tailscaled.sock
