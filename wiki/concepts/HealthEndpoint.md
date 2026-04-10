---
title: "Health Endpoint"
type: concept
tags: [api, monitoring, http]
sources: [openclaw-tailscale-tunnel-script]
last_updated: 2026-04-08
---

## Description
HTTP health endpoint used to verify that a service is running and responsive. The script checks http://127.0.0.1:PORT/health to confirm the OpenClaw gateway is accessible before configuring the tunnel.

## Key Details
- Default port: 18789
- Endpoint: /health
- Used for pre-flight validation before tunnel setup

## Connections
- [[OpenClawTailscaleTunnelScript]] — verifies gateway health before Funnel configuration
- [[OpenClaw]] — provides the /health endpoint
