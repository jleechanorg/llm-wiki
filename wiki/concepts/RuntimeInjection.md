---
title: "Runtime Injection"
type: concept
tags: [template, schema, injection, prompt-engineering]
sources: [schema-prompt-drift-investigation]
last_updated: 2026-04-07
---

## Definition
A templating system using `{{SCHEMA:TypeName}}` syntax that generates type documentation from JSON schema at runtime.

## How It Works
- Template placeholder `{{SCHEMA:TypeName}}` is replaced with generated schema documentation
- Currently generates type docs only, not example JSON
- Used in planning_protocol.md and other prompt files

## Limitation
Does not generate example JSON — only type documentation. This leaves a gap for prompts that need example output format.

## Related Concepts
- [[Schema-PromptDrift]] — the problem runtime injection could solve if extended
- [[JSON Schema Validation]] — what the generated docs feed into
