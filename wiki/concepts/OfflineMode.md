---
title: "Offline Mode"
type: concept
tags: [ml, deployment, hf]
sources: []
last_updated: 2026-04-08
---

Offline mode allows ML models to run without network access by loading from local cache. In FastEmbed, controlled by HF_HUB_OFFLINE=1 environment variable.

## Implementation
- Sets local_files_only=True when loading model
- Uses cached model from cache_dir
- Skips hub downloads
