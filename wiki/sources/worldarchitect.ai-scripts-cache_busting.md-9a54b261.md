---
title: "Cache-Busting Guide"
type: source
tags: [cache-busting, frontend, deployment, build-automation, performance]
sources: []
date: 2026-04-07
source_file: scripts/cache_busting.py
last_updated: 2026-04-07
---

## Summary

Cache-busting adds content-based hashes to frontend asset filenames (e.g., `app.c70a7330.js`) to enable aggressive browser caching with perfect cache invalidation. The system automatically runs during deployment via `deploy.sh`, hashes JS/CSS files using MD5 (8 chars), and updates HTML references accordingly.

## Key Claims

- **Cache-Busting During Deployment**: Automatically handled by `deploy.sh`; adds content-based hashes to filenames for aggressive caching with perfect invalidation
- **MD5 Hash Implementation**: Files hashed with 8-character MD5 suffix (e.g., `app.js` → `app.c70a7330.js`)
- **.gitignore Protection**: Prevents accidental commits of build artifacts via patterns matching `*.[0-9a-f]{8}.{js,css}`
- **Cache Headers**: Hashed files get `Cache-Control: public, max-age=31536000, immutable` (1 year); HTML gets `no-cache`
- **Dev Mode Fallback**: Server falls back to unhashed files in development mode

## Key Quotes

> "Script runs: `python3 scripts/cache_busting.py mvp_site/frontend_v1`" — process entry point

> "HTML files get `Cache-Control: no-cache, must-revalidate` (always fresh)" — cache header strategy

## Connections

- [[WorldArchitect.AI Deployment Log]] — cache-busting runs automatically during deployment
- [XSS Security Fix Report](sources/worldarchitect.ai-docs-xss-security-fix-report.md-e3391d92.md) — frontend security improvements alongside caching

## Contradictions

- None identified

## DO Run Cache-Busting
- During deployment (auto-handled by `deploy.sh`)
- In CI/CD pipelines as part of build process
- Before production releases

## DO NOT Run Cache-Busting
- During local development (adds unnecessary files)
- During testing (tests should work with or without)
- Before committing (build artifacts not source code)

## Architecture Components

1. **Script**: `scripts/cache_busting.py` — hashes all JS/CSS files, renames with hash suffix, updates HTML references
2. **Server**: `mvp_site/main.py` (`frontend_files_with_cache_busting()`) — serves hashed files with immutable cache headers, falls back to unhashed in dev mode
3. **Tests**: `testing_mcp/test_cache_busting_http.py` — HTTP integration tests validating cache headers