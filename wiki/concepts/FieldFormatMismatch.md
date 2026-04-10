---
title: "Field Format Mismatch"
type: concept
tags: [testing, bug, api, firestore, data-validation]
sources: ["field-format-validation-red-green-test"]
last_updated: 2026-04-08
---

## Description
A bug where the translation layer expects {"text": content} but the source module outputs {"story": content}. This causes empty narratives in the API-to-Firestore flow when story entries are processed.

## Related Tests
- [[Field Format Validation Red-Green Test]] - tests for this mismatch

## Solution
Ensure consistent field naming (text vs story) across world_logic.py and main.py translation layer.
