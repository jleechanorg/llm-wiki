---
title: "State Migration"
type: concept
tags: [data-migration, backward-compatibility]
sources: ["mission-conversion-helpers-tests", "mission-auto-completion-e2e-tests"]
last_updated: 2026-04-08
---

## Description
Pattern for handling legacy campaign state that lacks newer fields. The mission conversion tests validate that older campaigns without completed_missions or with dict-style missions are migrated transparently.

## Related Pages
- [[Mission Conversion Helpers Tests]] — tests dict-to-list migration
- [[Mission Auto-Completion E2E Tests]] — tests completed_missions auto-initialization
