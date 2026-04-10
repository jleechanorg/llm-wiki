---
title: "MvpSite"
type: entity
tags: [module, python, application]
sources: [world-content-loader]
last_updated: 2026-04-08
---

MvpSite is the Python package containing core functionality for WorldArchitect.AI, including file caching, logging utilities, and world content loading.

## Key Modules
- `file_cache`: Cached file reading utilities
- `logging_util`: Application logging
- `world`: Directory containing world content files (world_assiah_compressed.md, banned_names.md)

## Related Components
- [[WorldArchitect]] - the parent project
- [[WorldContentLoader]] - world loading module within mvp_site
- [[FileCache]] - file reading with caching
