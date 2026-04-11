---
title: "PR #515: feat: implement refresh token authentication and local MCP Inspector"
type: source
tags: []
date: 2025-11-02
source_file: raw/prs-/pr-515.md
sources: []
last_updated: 2025-11-02
---

## Summary
This PR implements refresh token support for extended authentication sessions and creates a local MCP Inspector server with automatic token injection.

### Key Changes

**1. Refresh Token Authentication**
- ✅ Extended sessions (60+ days without re-authentication)
- ✅ Automatic token refresh using Firebase REST API
- ✅ New `refresh` command for manual token renewal
- ✅ Auto-refresh on `token` and `test` commands

**2. Local MCP Inspector Server**
- ✅ Automatic token injection from `~/.ai-universe

## Metadata
- **PR**: #515
- **Merged**: 2025-11-02
- **Author**: jleechan2015
- **Stats**: +507/-40 in 6 files
- **Labels**: none

## Connections
