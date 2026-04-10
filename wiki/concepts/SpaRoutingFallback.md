---
title: "SPA Routing Fallback"
type: concept
tags: [frontend, routing, spa]
sources: ["fallback-behavior-review-mvp-site"]
last_updated: 2026-04-08
---

Single Page Application routing pattern where server serves index.html for any unmatched route, allowing client-side router to handle deep links.


## Implementation in mvp_site
- `main.py` `serve_frontend` route matches any path not in static assets
- Serves `index.html` for unmatched paths
- Adjacent `/handle_interaction` returns 410 for stale cached bundles

## Rationale
Standard SPA pattern. Stale cache handler protects users by forcing upgrade rather than failing silently.
