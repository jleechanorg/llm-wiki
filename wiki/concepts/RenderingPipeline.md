---
title: "Rendering Pipeline"
type: concept
tags: [game-development, rendering, performance]
sources: ["animal-movement-web-game-technical-design-document"]
last_updated: 2026-04-07
---

Four-phase rendering pipeline:

1. **Clear canvas**: requestAnimationFrame callback
2. **Update logic**: Game state, physics, animations
3. **Render pass**: Background → sprites → UI → effects
4. **Frame limiting**: Target 60 FPS, fallback to 30 FPS

Performance optimizations: canvas sizing matching device pixel ratio, worker threads for physics calculations off main thread, aggressive browser cache headers, Gzip asset compression, JavaScript minification.
