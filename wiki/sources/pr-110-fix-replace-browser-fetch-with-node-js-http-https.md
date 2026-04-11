---
title: "PR #110: fix: replace browser fetch with Node.js http/https in IpfsBridge (WC-2ej)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-110.md
sources: []
last_updated: 2026-03-26
---

## Summary
IpfsBridge in `packages/backend/src/storage/ipfs_bridge.ts` used browser `fetch()` APIs for all IPFS HTTP calls. These do not work reliably in Node.js environments, causing health checks, pin operations, and content fetches to fail.

## Metadata
- **PR**: #110
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +593/-178 in 3 files
- **Labels**: none

## Connections
