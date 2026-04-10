---
title: "REV-rrom"
type: entity
tags: [revision, schema-validation, non-blocking]
sources: []
last_updated: 2026-04-08
---

## Description
Revision identifier for making validation failures surface in corrections as non-blocking warnings. Part of PR #4534.

## Purpose
Ensures schema validation failures don't raise exceptions that block gameplay. Instead, they generate GCP log warnings and correction warnings that developers can review without impacting player experience.

## Related
- [[PR4534]] — Parent PR
- [[NonBlockingWarnings]] — The design pattern implemented
- [[SchemaValidation]] — The validation system being modified
