---
title: "Choice ID Collision Resolution"
type: concept
tags: [worldarchitect, algorithm, idempotency]
sources: []
last_updated: 2026-04-08
---

Algorithm in planning block normalization that handles duplicate choice IDs:

1. Track seen IDs in a set
2. On collision, append numeric suffix (`_1`, `_2`, etc.)
3. Retry up to 1000 times before raising ValueError
4. Log warnings when collisions are resolved

Ensures each choice has a unique identifier for downstream processing.
