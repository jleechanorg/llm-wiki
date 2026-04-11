---
title: "PR #2: feat: OpenClaw SSO Gateway — full TDD implementation (commits 1–9)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-/pr-2.md
sources: []
last_updated: 2026-03-31
---

## Summary
Complete implementation of the OpenClaw SSO Gateway — a BYOI (Bring Your Own Inference) relay system that lets users expose their local inference server (Ollama, LM Studio, etc.) to any browser or mobile client through a cloud relay, with Firebase as the single auth source.

**Architecture:**
```
Browser → Gateway (port 2003) → Relay (port 2004) → [WebSocket] → Agent binary → OpenClaw (localhost)
```
No VPN, no port forwarding — the agent connects **outbound** to the relay.

## Metadata
- **PR**: #2
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +475/-0 in 2 files
- **Labels**: none

## Connections
