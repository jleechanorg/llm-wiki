---
title: "Prompt Injection"
type: concept
tags: [prompt-injection, templating, schema]
sources: []
last_updated: 2026-04-08
---

## Definition
Template-based system that injects schema documentation into prompt files at load time. Uses placeholder syntax {{SCHEMA:TypeName}} which gets replaced with cached schema docs.

## Key Properties
- **Placeholder format**: {{SCHEMA:TypeName}}
- **Injection mechanism**: _inject_dynamic_schema_docs() performs string replacement
- **Performance overhead**: <5ms vs baseline (non-injected) prompt loading
- **Supported types**: CombatState, CombatantState, EntityType, etc.

## Usage in System
Prompt files (e.g., combat_system_instruction.md) contain {{SCHEMA:...}} placeholders that get resolved at load time.
