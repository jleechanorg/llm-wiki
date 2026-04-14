---
title: "mvp_site serialization"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/serialization.py
---

## Summary
Serialization utilities for Firestore and JSON operations. Handles datetime, TypedDict, and other non-standard types that standard JSON cannot handle.

## Key Claims
- _is_unittest_mock_object() detects unittest mock objects for exclusion
- _get_firestore() provides Firestore instance
- json_default_serializer() central serializer for complex types (datetime, TypedDict, etc.)
- json_serial() serializes objects to JSON-compatible strings

## Connections
- [[Serialization]] — central serialization module
- [[LLMIntegration]] — core_memories serialization uses json_default_serializer