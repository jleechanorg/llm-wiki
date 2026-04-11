---
title: "OpenClaw E2E Remote Routing Fix"
type: source
tags: [openclaw, e2e, routing, dns, cloudflare, tunnel, testing, fix]
source_file: "raw/llm_wiki-raw-worldarchitect.ai-openclaw-e2e-remote-routing-fix.md-f09d3ec2.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Fix for OpenClaw E2E test failures in strict remote-only routing mode. DNS resolution was failing within the 12-second polling window, and the tunnel returned 502 Bad Gateway because the routing layer wasn't ready when HTTP requests arrived. Four fixes were applied: tap proxy timeout (30s→120s), DNS check window (12×1s→60×2s), Step 8 remote routing branch, and HTTP connectivity probe after DNS resolution.

## Key Claims
- **Tap proxy timeout fixed**: 30s → 120s to handle LLM streaming responses that routinely exceed 30 seconds
- **DNS check window fixed**: 12×1s → 60×2s (120s budget) because trycloudflare.com subdomains are NOT wildcards — each tunnel registers an individual DNS record taking 60–120 seconds to propagate
- **Step 8 remote routing fixed**: In remote_only mode, traffic goes directly to Cloudflare URL, so local tap proxy sees zero traffic by design — added is_remote_route branch
- **HTTP connectivity probe added**: DNS resolves before Cloudflare's routing layer is ready — 15-attempt × 2s probe loop waits for routing layer to accept traffic

## Test Results
- **Auto routing with local fallback**: PASSED — 7 tap proxy calls captured, all 8 steps green
- **Strict remote-only with DNS verification**: PASSED — streaming via Cloudflare tunnel confirmed, all 8 steps green

## Connections
- [[OpenClaw]] — the project being tested
- [[Cloudflare]] — provides Quick Tunnel for remote routing
- [[E2E Testing]] — end-to-end testing methodology