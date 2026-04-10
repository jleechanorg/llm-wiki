---
title: "FirestoreService.py"
type: entity
tags: [python, file, firestore, database]
sources: ["fallback-behavior-review-mvp-site"]
last_updated: 2026-04-08
---

Firestore document write handling:
- Missing document reference `id` — raises `FirestoreWriteError`
- `document_id` is `None` after successful write — raises `FirestoreWriteError` with message "Document ID was not captured during write. This indicates an unexpected error in the Firestore write operation."

## Rationale
Fail-fast ensures write anomalies are surfaced rather than masked with fallback values.
