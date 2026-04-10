---
title: "Sentinel Pattern"
type: concept
tags: [python, sentinel, design-pattern]
sources: [mock-firestore-service-wrapper]
last_updated: 2026-04-08
---

Python pattern using a unique object (sentinel) to represent a special value that cannot be confused with legitimate data. Used here with `DELETE_FIELD = object()` to signal field deletion without using `None` (which might be a valid value).
