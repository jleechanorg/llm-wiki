---
title: "Tailscale Funnel"
type: concept
tags: [networking, tunnel, public-url]
sources: [openclaw-tailscale-tunnel-script]
last_updated: 2026-04-08
---

## Description
Tailscale Funnel is a feature that exposes a local service to the public internet via a stable HTTPS URL. Part of Tailscale's zero-config networking capabilities.

## Key Details
- Generates URLs like https://<machine-name>.<tailnet>.ts.net
- Enables external access to locally running services
- Requires Tailscale daemon to be running and authenticated
- Command: `tailscale funnel status` to check status

## Connections
- [[OpenClawTailscaleTunnelScript]] — uses Funnel to expose OpenClaw gateway
- [[Tailscale]] — provides the Funnel feature

## Related Concepts
- [[TailscaleSocket]] — custom socket path for user-space Tailscale
- [[HealthEndpoint]] — /health endpoint verification for gateway
