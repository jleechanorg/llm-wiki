---
title: "OpenClaw Setup for WorldArchitect"
type: source
tags: [openclaw, worldarchitect, tunnel, networking, setup]
source_file: "raw/openclaw-setup-worldarchitect.html"
sources: []
last_updated: 2026-04-08
---

## Summary
HTML setup guide for exposing a local OpenClaw gateway to a remote WorldArchitect server. Provides quick start instructions, tunnel helper script download, and notes on public URL options including localhost.run, cloudflared, and ngrok.

## Key Claims
- **Local Gateway Requirement**: OpenClaw gateway must run locally on port 18789; Cloud Run cannot reach localhost directly
- **Tunnel Script**: openclaw_gateway_tunnel.sh provides public HTTPS URL for remote access
- **Provider Priority**: Script auto-selects available providers in order: localhost.run → cloudflared → ngrok
- **Settings Configuration**: Users must set Gateway URL and provider to OpenClaw in Settings after obtaining public URL
- **Health Verification**: Local gateway health check at http://127.0.0.1:18789/health

## Key Quotes
> "Use this page to expose a local OpenClaw gateway to a remote WorldArchitect server."

> "The public URL is needed for PR preview / remote environments."

## Connections
- [[OpenClaw]] — the gateway being exposed
- [[WorldArchitect]] — the remote server requiring public URL access
- [[OpenClaw Tailscale Tunnel Script]] — alternative tunnel solution using Tailscale Funnel
- [[OpenAI-Compatible Inference Proxy]] — Flask proxy that forwards to user gateways

## Contradictions
- []
