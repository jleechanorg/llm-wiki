---
title: "PR #5879: feat(openclaw,mcp): personal API keys + Funnel migration + strict trace/evidence hardening"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldarchitect-ai/pr-5879.md
sources: []
last_updated: 2026-03-27
---

## Summary
WorldAI uses OpenClaw as a local AI gateway. To enable remote (GCP-hosted) WorldAI servers to reach a user's local OpenClaw instance, the gateway must be reachable at a stable public URL.

**This PR proves that a Tailscale URL works as the OpenClaw gateway URL with WorldAI.** Tailscale provides a stable, secure, always-on network hostname (`jeffreys-macbook-pro.tail5eb762.ts.net`) that GCP Cloud Run can reach via the tailnet — without a traditional tunnel script, without port forwarding, and wit

## Metadata
- **PR**: #5879
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +6486/-908 in 64 files
- **Labels**: none

## Connections
