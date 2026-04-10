---
title: "Embedded JSON Stripping"
type: concept
tags: [json-parsing, data-cleaning, narrative-processing]
sources: [test-embedded-planning-json-bug-reproduction]
last_updated: 2026-04-08
---

## Definition

The process of removing embedded JSON objects from narrative text when they appear as raw JSON strings that should instead be in structured fields.

## Purpose

The LLM may include planning data in both:
1. The structured `planning_block` field (correct)
2. The narrative text as raw JSON (incorrect)

The stripping function removes the raw JSON from narrative to prevent users from seeing:
- `"thinking":` key
- `"choices":` key
- `"magical_oaths_binding":` and other option keys
- `"analysis":` nested keys

## Implementation

`_strip_embedded_planning_json()` in `narrative_response_schema.py` handles:
- Full planning JSON blocks embedded in narrative
- Narrative that is entirely JSON
- Preserves non-JSON narrative content

## Related Concepts
- [[PlanningBlock]] — the data that should be isolated
- [[NarrativeResponseSchema]] — the module containing the stripping function
