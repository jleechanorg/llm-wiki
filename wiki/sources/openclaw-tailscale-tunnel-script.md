---
title: "OpenClaw Tailscale Tunnel Script"
type: source
tags: [bash, tailscale, openclaw, tunnel, networking,Funnel]
source_file: "raw/openclaw_tailscale_tunnel.sh"
sources: []
last_updated: 2026-04-08
---

## Summary
Bash script that starts a public Tailscale Funnel to expose a local OpenClaw gateway. Creates a stable HTTPS URL like https://<machine-name>.<tailnet>.ts.net. Automatically installs Tailscale if needed, starts the daemon, logs in, and configures Funnel.

## Key Claims
- **Public URL Generation**: Creates stable HTTPS URL via Tailscale Funnel for local gateway exposure
- **Auto-Installation**: Detects missing Tailscale CLI and prompts installation via Homebrew (macOS) or install.sh (Linux)
- **Daemon Management**: Starts tailscaled daemon, verifies running state via JSON status parsing
- **Health Verification**: Checks both Tailscale backend state and local gateway /health endpoint
- **Port Validation**: Validates port is between 1-65535, defaults to 18789
- **Custom Socket Support**: Supports --socket flag for user-space Tailscale fallback
- **Doctor Checks**: Comprehensive pre-flight validation of CLI, daemon, authentication, and gateway reachability
- **URL Persistence**: Writes generated URL to ~/.openclaw/openclaw_gateway_tunnel_url.txt

## Key Funnel

## Connections
- [[OpenClaw]] — the local gateway being exposed via tunnel
- [[Tailscale]] — provides the Funnel feature for public URL generation
- [[Homebrew]] — package manager used for Tailscale installation on macOS

## Contradictions
- None identified
