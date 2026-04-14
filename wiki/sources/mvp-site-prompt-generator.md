---
title: "mvp_site prompt_generator"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/prompt_generator.py
---

## summary
Utilities for generating LLM instructions and documentation from JSON Schemas (ADR-0003 Phase 4). Provides recursive property gathering and $ref resolution for schema-driven documentation generation.

## Key Claims
- _gather_properties() recursively gathers all properties from schema, resolving allOf/refs
- resolve_refs() follows $ref pointers to their source in definitions
- _infer_property_type() infers user-facing type labels when type is omitted
- generate_type_markdown() generates markdown documentation blocks for schema types

## Connections
- [[PromptEngineering]] — generates documentation for schema-defined prompts
- [[Serialization]] — works with JSON Schema definitions