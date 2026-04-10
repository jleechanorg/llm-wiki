---
title: "Cazador's Spawn"
type: entity
tags: [npc, validation-test]
sources: [entity-id-special-characters-validation]
last_updated: 2026-04-08
---

## Description
Test NPC used to validate entity ID sanitization handles apostrophes in names. The apostrophe in "Cazador's Spawn" must be stripped when generating entity_id.

## Wiki Context
Used in test_sanitize_entity_name_for_id test case as validation input where "Cazador's Spawn" should sanitize to "cazadors_spawn".

## Connections
- [[EntityIDValidation]] — primary validation test case for this entity
