---
title: "NoSQL Injection Prevention"
type: concept
tags: [security, nosql, injection, prevention]
sources: ["security-validation-tests"]
last_updated: 2026-04-08
---

## Definition
Security measure to prevent NoSQL injection attacks where MongoDB-style operators ($ne, $gt, $where) are attempted in user inputs.

## Key Points
- Firestore does not support MongoDB-style operators
- Injection attempts like {$ne: null}, {$gt: ""} are rejected
- JS injection patterns are handled safely

## Related Concepts
- [[SQLInjectionPrevention]]
- [[InputValidation]]
