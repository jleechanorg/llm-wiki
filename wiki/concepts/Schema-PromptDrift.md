---
title: "Schema-Prompt Drift"
type: concept
tags: [schema, prompt-engineering, validation, technical-debt]
sources: [schema-prompt-drift-investigation]
last_updated: 2026-04-07
---

## Definition
The phenomenon where hardcoded JSON examples in prompt markdown files drift away from the JSON schema they should conform to over time, causing validation failures.

## Context
When schema fields are added or modified, manually written JSON examples in prompt files are often not updated, creating a mismatch between what the prompt tells the LLM to output and what the validation schema expects.

## Related Concepts
- [[JSON Schema Validation]] — fails when prompt examples don't match schema
- [[Runtime Injection]] — system meant to generate schema-derived content
- [[Prompt Engineering]] — best practice of keeping examples in sync

## Solutions
1. Add missing fields directly to schema
2. Replace hardcoded examples with runtime injection templates
3. Add to legacy allowlist in validation (workaround)
