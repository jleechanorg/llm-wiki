---
title: "D'Artagnan"
type: entity
tags: [player-character, validation-test]
sources: [entity-id-special-characters-validation]
last_updated: 2026-04-08
---

## Description
Test player character used to validate entity ID sanitization handles apostrophes in names. The name "D'Artagnan" (with apostrophe) should generate entity_id "pc_dartagnan_001".

## Connections
- [[EntityIDValidation]] — validation test case
