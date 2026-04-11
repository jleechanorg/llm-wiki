---
title: "PR #19: feat: Remote Mode + Auto-Scan Architecture"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-19.md
sources: []
last_updated: 2026-03-29
---

## Summary
Implements the full Remote Mode + Auto-Scan architecture per the [spec](docs/superpowers/specs/2026-03-26-remote-mode-auto-scan-design.md):

- **RepoRegistry** (`src/blog/repo-registry.ts`) — per-repo config persisted to `data/repos.json` with modes for autoScan, novelBranch, novelDaily
- **SHA-256 API key auth** (`src/blog/auth.ts`) — `crypto.createHash`, `timingSafeEqual`, `requireApiKey` middleware, `loadApiKeys`/`saveApiKeys` persistence to `data/api-keys.json`
- **GitHubClient** (`src/blog/

## Metadata
- **PR**: #19
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +1954/-50 in 16 files
- **Labels**: none

## Connections
