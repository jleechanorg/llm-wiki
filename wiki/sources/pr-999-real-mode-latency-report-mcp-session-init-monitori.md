---
title: "PR #999: real-mode latency report + MCP session init, monitoring flush resilience"
type: source
tags: []
date: 2026-02-17
source_file: raw/prs-/pr-999.md
sources: []
last_updated: 2026-02-17
---

## Summary
- Added MCP session initialization in the local smoke runner to satisfy newer JSON-RPC handshake expectations.
- Added auth deprecation warning suppression for repeated unauthenticated userId usage to reduce log noise.
- **Default OpenAI model is `gpt-5-mini`** — intentional choice for cost efficiency ($0.25/$2.00 per 1M input/output tokens vs $1.25/$10.00 for gpt-5). All documentation, display names, and cost mappings updated to reflect this.
- Hardened monitoring metric flushing to avoid concu

## Metadata
- **PR**: #999
- **Merged**: 2026-02-17
- **Author**: jleechan2015
- **Stats**: +2252/-812 in 39 files
- **Labels**: none

## Connections
