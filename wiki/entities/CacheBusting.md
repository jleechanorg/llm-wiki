---
title: "CacheBusting"
type: entity
tags: [caching, scripts, deployment]
sources: []
last_updated: 2026-04-08
---

## Description
Cache busting script in scripts/cache_busting.py. Generates hashes for static asset cache busting to ensure browsers load fresh assets on deployment.

## In This Source
Imported via `from scripts.cache_busting import DEFAULT_HASH_LENGTH, apply_cache_busting`. Test verifies hash length constant.

## Connections
- [[FlaskAppImportEndpointTests]] — imports CACHE_BUST_HASH_LENGTH
- [[MVPSiteMain]] — integrates cache busting for static assets
