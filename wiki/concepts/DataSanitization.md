---
title: "Data Sanitization"
type: concept
tags: [security, testing, capture, redaction]
sources: [capture-framework-tests]
last_updated: 2026-04-08
---

## Description
Automatic redaction of sensitive fields in captured data. Protects credentials, API keys, and passwords from being persisted in session logs.

## Redacted Fields
- `password` → `[REDACTED]`
- `api_key` → `[REDACTED]`
- Nested fields with key `secret` → `[REDACTED]`

## Behavior
Recursively traverses data structure, redacting matching keys while preserving non-sensitive data.

## Related
- [[CaptureInteraction]] — where sanitization applies
- [[SessionPersistence]] — export with sanitized data
