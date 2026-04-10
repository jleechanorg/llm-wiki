---
title: "Asset Pipeline"
type: concept
tags: [game-development, assets, pipeline]
sources: ["animal-movement-web-game-technical-design-document"]
last_updated: 2026-04-07
---

Asset organization structure for the game:

```
assets/
├── sprites/
│   ├── animals/
│   ├── environments/
│   └── ui/
├── audio/
    ├── sfx/
    ├── ambient/
```

Supports asset preloading during initialization and texture management for unloading unused sprite sheets. Browser optimization via compression and caching.
